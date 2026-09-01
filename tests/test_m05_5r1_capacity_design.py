"""Synthetic-only tests for the M05.5R1 capacity design freeze."""

from dataclasses import replace

import pytest

from tools.experiments.m05_5r1_capacity_design import (
    CONDITIONS, HOLDOUT_COUNT, MODEL_CONTEXT_WINDOW_TOKENS, OUTPUT_CAP_TOKENS,
    CapacityState, ScheduleEntry, assert_neutral_schedule, build_balanced_schedule,
    calculate_envelope, classify_capacity_event, observe_output, pacing_decision,
    request_options, schedule_commitment,
)


HOLDOUTS = ("H01", "H02", "H03", "H04", "H05", "H06", "H07", "H08")
BASE = ("CONDITION_A", "CONDITION_B", "CONDITION_C")


def schedule():
    return build_balanced_schedule(HOLDOUTS, BASE)


def ready_state():
    envelope = calculate_envelope()
    frozen = schedule_commitment(schedule())
    return CapacityState(envelope.required_tpd + 1, envelope.required_tpm, 1, frozen), frozen


def test_envelope_is_source_bound_and_repair_inclusive():
    item = calculate_envelope()
    assert item.primary_minimum_generations == 64
    assert item.primary_maximum_generations == 104
    assert item.semantic_repair_maximum_generations == 104
    assert item.maximum_generation_requests == 208
    assert item.maximum_transport_attempts == 208
    assert item.max_total_tokens == 208 * MODEL_CONTEXT_WINDOW_TOKENS
    assert item.max_output_tokens_independent == 208 * OUTPUT_CAP_TOKENS
    assert item.token_count_status == "CONSERVATIVE_BOUND"


def test_condition_call_ceilings_are_preserved_in_primary_and_repair_bounds():
    item = calculate_envelope()
    assert item.primary_maximum_generations == HOLDOUT_COUNT * (1 + 10 + 2)
    assert item.maximum_generation_requests == item.primary_maximum_generations * 2


def test_output_cap_is_sent_as_the_official_option_and_hits_are_observable():
    assert request_options() == {"max_completion_tokens": OUTPUT_CAP_TOKENS}
    assert observe_output(OUTPUT_CAP_TOKENS - 1) == "OUTPUT_WITHIN_CAP"
    assert observe_output(OUTPUT_CAP_TOKENS) == "OUTPUT_CAP_HIT_INVALID_EXECUTION"
    assert observe_output(None) == "OUTPUT_USAGE_MISSING_INVALID_EXECUTION"


def test_schedule_is_reproducible_auditable_and_complete():
    first, second = schedule(), schedule()
    assert first == second
    assert schedule_commitment(first) == schedule_commitment(second)
    assert len(first) == 24
    assert {item.condition for item in first} == set(CONDITIONS)


def test_schedule_neutralizes_treatment_position():
    entries = schedule()
    assert_neutral_schedule(entries)
    positions = {condition: sum(item.position for item in entries if item.condition == condition) for condition in CONDITIONS}
    assert positions == {condition: 16 for condition in CONDITIONS}


def test_legacy_fixed_order_is_detected_as_biased():
    legacy = tuple(ScheduleEntry(block, position, holdout, condition)
                   for block, holdout in enumerate(HOLDOUTS, 1)
                   for position, condition in enumerate(BASE, 1))
    with pytest.raises(ValueError, match="SCHEDULE_TREATMENT_POSITION_BIAS"):
        assert_neutral_schedule(legacy)


def test_pacing_waits_without_mutating_schedule_or_treatment():
    envelope = calculate_envelope()
    state, frozen = ready_state()
    wait = replace(state, remaining_tpm=envelope.required_tpm - 1)
    assert pacing_decision(envelope, wait, frozen) == "WAIT_FOR_TPM_RESET"
    assert schedule_commitment(schedule()) == frozen


def test_insufficient_rpm_waits_and_insufficient_tpm_waits():
    envelope = calculate_envelope()
    state, frozen = ready_state()
    assert pacing_decision(envelope, replace(state, remaining_rpm=0), frozen) == "WAIT_FOR_RPM_RESET"
    assert pacing_decision(envelope, replace(state, remaining_tpm=0), frozen) == "WAIT_FOR_TPM_RESET"


def test_daily_capacity_insufficient_or_unknown_blocks_start():
    envelope = calculate_envelope()
    state, frozen = ready_state()
    assert pacing_decision(envelope, replace(state, remaining_tpd=envelope.required_tpd - 1), frozen) == "TPD_INSUFFICIENT_BLOCKS_START"
    assert pacing_decision(envelope, replace(state, remaining_tpd=None), frozen) == "TPD_UNKNOWN_BLOCKS_START"


def test_transport_retry_is_invalid_and_semantic_repair_is_explicit():
    assert classify_capacity_event("UNPLANNED_TRANSPORT_RETRY") == "INVALID_EXECUTION"
    assert classify_capacity_event("SEMANTIC_REPAIR_REQUEST") == "EXPLICIT_REPAIR_REQUIRES_SCHEDULED_REQUEST"


@pytest.mark.parametrize("event, outcome", [
    ("OUTPUT_CAP_HIT", "INVALID_EXECUTION"),
    ("CAPACITY_RECEIPT_INVALID", "ABORTED_CAPACITY"),
    ("TPD_BECOMES_INSUFFICIENT", "ABORTED_CAPACITY"),
    ("ORDER_POLICY_VIOLATED", "INVALID_EXECUTION"),
    ("SCHEDULER_STATE_LOST", "INVALID_EXECUTION"),
    ("HTTP_429", "ABORTED_CAPACITY"),
    ("PROVIDER_UNAVAILABLE", "INVALID_EXECUTION"),
])
def test_capacity_failures_never_become_product_results(event, outcome):
    assert classify_capacity_event(event) == outcome


def test_schedule_mutation_and_scheduler_state_loss_fail_closed():
    envelope = calculate_envelope()
    state, frozen = ready_state()
    assert pacing_decision(envelope, replace(state, schedule_commitment_sha256="0" * 64), frozen) == "ORDER_POLICY_VIOLATED_INVALID_EXECUTION"
    assert pacing_decision(envelope, replace(state, scheduler_state_present=False), frozen) == "SCHEDULER_STATE_LOST_INVALID_EXECUTION"
