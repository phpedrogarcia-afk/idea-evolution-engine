"""Deterministic, offline-only capacity and order design for M05.5R1.

This module neither imports a provider nor loads sealed holdout/reveal content.
It freezes the preconditions a future, separately authorized executor must honor.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import secrets
from typing import Iterable, Mapping, Sequence


EXPERIMENT_ID = "EXP-M05.5R1-CONTROLLED-REPLICATION-20260901"
CONDITIONS = ("CONDITION_A", "CONDITION_B", "CONDITION_C")
HOLDOUT_COUNT = 8
MODEL_CONTEXT_WINDOW_TOKENS = 131_072
OUTPUT_CAP_TOKENS = 2_048
MAX_SEMANTIC_REPAIRS_PER_GENERATION = 1
MAX_TRANSPORT_RETRIES_PER_REQUEST = 0
TOKENIZER_METHOD = "PINNED_OPENAI_HARMONY_GPT_OSS_EXACT_INITIAL_AND_REPAIR_COUNTS_CONTEXT_GUARDED_STATE_DEPENDENT_COUNTS"
CALIBRATED_MAX_INPUT_TOKENS = 10_800_350
CALIBRATED_MAX_OUTPUT_TOKENS = 425_984
CALIBRATED_MAX_TOTAL_TOKENS = 11_226_334

PRIMARY_CALLS_PER_HOLDOUT = {
    "CONDITION_A": (1, 1),
    "CONDITION_B": (6, 10),
    "CONDITION_C": (1, 2),
}


def _canonical_hash(value: object) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class CapacityEnvelope:
    primary_minimum_generations: int
    primary_maximum_generations: int
    semantic_repair_maximum_generations: int
    maximum_generation_requests: int
    maximum_transport_attempts: int
    max_input_tokens_independent: int
    max_output_tokens_independent: int
    max_total_tokens: int
    per_request_token_reservation: int
    required_rpm: int
    required_tpm: int
    required_rpd: int
    required_tpd: int
    tokenizer_method: str
    token_count_status: str

    @property
    def sha256(self) -> str:
        return _canonical_hash(asdict(self))


def calculate_envelope() -> CapacityEnvelope:
    primary_minimum = HOLDOUT_COUNT * sum(item[0] for item in PRIMARY_CALLS_PER_HOLDOUT.values())
    primary_maximum = HOLDOUT_COUNT * sum(item[1] for item in PRIMARY_CALLS_PER_HOLDOUT.values())
    semantic_repairs = primary_maximum * MAX_SEMANTIC_REPAIRS_PER_GENERATION
    generation_requests = primary_maximum + semantic_repairs
    # These figures are frozen from PFI-M05_5R1-TOKEN-ENVELOPE-CALIBRATION-001.
    # Literal A/B/C first requests and structural repairs were counted with the
    # pinned OpenAI Harmony tokenizer. Only state-dependent B/C requests keep a
    # per-request context guard because current schemas permit unbounded strings.
    return CapacityEnvelope(
        primary_minimum_generations=primary_minimum,
        primary_maximum_generations=primary_maximum,
        semantic_repair_maximum_generations=semantic_repairs,
        maximum_generation_requests=generation_requests,
        maximum_transport_attempts=generation_requests * (1 + MAX_TRANSPORT_RETRIES_PER_REQUEST),
        max_input_tokens_independent=CALIBRATED_MAX_INPUT_TOKENS,
        max_output_tokens_independent=CALIBRATED_MAX_OUTPUT_TOKENS,
        max_total_tokens=CALIBRATED_MAX_TOTAL_TOKENS,
        per_request_token_reservation=MODEL_CONTEXT_WINDOW_TOKENS,
        required_rpm=1,
        required_tpm=MODEL_CONTEXT_WINDOW_TOKENS,
        required_rpd=generation_requests,
        required_tpd=CALIBRATED_MAX_TOTAL_TOKENS,
        tokenizer_method=TOKENIZER_METHOD,
        token_count_status="CALIBRATED_EXACT_AND_CONTEXT_GUARDED",
    )


def request_options() -> dict[str, int]:
    """The exact Groq API option a future authorized executor must pass."""
    return {"max_completion_tokens": OUTPUT_CAP_TOKENS}


def observe_output(completion_tokens: int | None) -> str:
    if completion_tokens is None:
        return "OUTPUT_USAGE_MISSING_INVALID_EXECUTION"
    if completion_tokens >= OUTPUT_CAP_TOKENS:
        return "OUTPUT_CAP_HIT_INVALID_EXECUTION"
    return "OUTPUT_WITHIN_CAP"


@dataclass(frozen=True)
class ScheduleEntry:
    block: int
    position: int
    holdout_id: str
    condition: str


def build_balanced_schedule(holdout_order: Sequence[str], base_permutation: Sequence[str]) -> tuple[ScheduleEntry, ...]:
    if len(holdout_order) != HOLDOUT_COUNT or len(set(holdout_order)) != HOLDOUT_COUNT:
        raise ValueError("SCHEDULE_HOLDOUT_SET_INVALID")
    if set(base_permutation) != set(CONDITIONS) or len(base_permutation) != len(CONDITIONS):
        raise ValueError("SCHEDULE_BASE_PERMUTATION_INVALID")
    base = tuple(base_permutation)
    rotations = (base, base[1:] + base[:1], base[2:] + base[:2])
    # Six cyclic blocks balance every condition in every position twice. The
    # final base/reverse pair keeps each treatment's mean position exactly 2.0.
    permutations = rotations + rotations + (base, tuple(reversed(base)))
    entries: list[ScheduleEntry] = []
    for block, (holdout_id, permutation) in enumerate(zip(holdout_order, permutations), start=1):
        entries.extend(ScheduleEntry(block, position, holdout_id, condition)
                       for position, condition in enumerate(permutation, start=1))
    schedule = tuple(entries)
    assert_neutral_schedule(schedule)
    return schedule


def make_csprng_schedule(holdout_ids: Sequence[str]) -> tuple[ScheduleEntry, ...]:
    rng = secrets.SystemRandom()
    return build_balanced_schedule(rng.sample(list(holdout_ids), HOLDOUT_COUNT), rng.sample(list(CONDITIONS), 3))


def schedule_commitment(entries: Iterable[ScheduleEntry]) -> str:
    return _canonical_hash([asdict(item) for item in entries])


def assert_neutral_schedule(entries: Sequence[ScheduleEntry]) -> None:
    if len(entries) != HOLDOUT_COUNT * len(CONDITIONS):
        raise ValueError("SCHEDULE_CELL_COUNT_INVALID")
    blocks: dict[int, list[ScheduleEntry]] = {}
    for entry in entries:
        blocks.setdefault(entry.block, []).append(entry)
    if len(blocks) != HOLDOUT_COUNT:
        raise ValueError("SCHEDULE_BLOCK_COUNT_INVALID")
    position_sum = {condition: 0 for condition in CONDITIONS}
    for block_entries in blocks.values():
        if {item.condition for item in block_entries} != set(CONDITIONS):
            raise ValueError("SCHEDULE_BLOCK_NOT_TREATMENT_COMPLETE")
        if {item.position for item in block_entries} != {1, 2, 3}:
            raise ValueError("SCHEDULE_BLOCK_POSITION_INVALID")
        for item in block_entries:
            position_sum[item.condition] += item.position
    expected_sum = HOLDOUT_COUNT * 2
    if any(total != expected_sum for total in position_sum.values()):
        raise ValueError("SCHEDULE_TREATMENT_POSITION_BIAS")


@dataclass(frozen=True)
class CapacityState:
    remaining_tpd: int | None
    remaining_tpm: int | None
    remaining_rpm: int | None
    schedule_commitment_sha256: str | None
    scheduler_state_present: bool = True


def pacing_decision(envelope: CapacityEnvelope, state: CapacityState, expected_schedule_commitment: str) -> str:
    if not state.scheduler_state_present:
        return "SCHEDULER_STATE_LOST_INVALID_EXECUTION"
    if state.schedule_commitment_sha256 != expected_schedule_commitment:
        return "ORDER_POLICY_VIOLATED_INVALID_EXECUTION"
    if state.remaining_tpd is None:
        return "TPD_UNKNOWN_BLOCKS_START"
    if state.remaining_tpd < envelope.required_tpd:
        return "TPD_INSUFFICIENT_BLOCKS_START"
    if state.remaining_tpm is None or state.remaining_tpm < envelope.required_tpm:
        return "WAIT_FOR_TPM_RESET"
    if state.remaining_rpm is None or state.remaining_rpm < envelope.required_rpm:
        return "WAIT_FOR_RPM_RESET"
    return "DISPATCH_ONE_REQUEST"


def classify_capacity_event(event: str) -> str:
    outcomes = {
        "OUTPUT_CAP_HIT": "INVALID_EXECUTION",
        "CAPACITY_RECEIPT_INVALID": "ABORTED_CAPACITY",
        "TPD_BECOMES_INSUFFICIENT": "ABORTED_CAPACITY",
        "ORDER_POLICY_VIOLATED": "INVALID_EXECUTION",
        "UNPLANNED_TRANSPORT_RETRY": "INVALID_EXECUTION",
        "SCHEDULER_STATE_LOST": "INVALID_EXECUTION",
        "HTTP_429": "ABORTED_CAPACITY",
        "PROVIDER_UNAVAILABLE": "INVALID_EXECUTION",
        "SEMANTIC_REPAIR_REQUEST": "EXPLICIT_REPAIR_REQUIRES_SCHEDULED_REQUEST",
    }
    return outcomes[event]
