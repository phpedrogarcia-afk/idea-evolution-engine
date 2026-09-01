"""Controls for the offline M05.5R1 token-envelope calibration."""

from tools.experiments.m05_5r1_token_envelope import (
    OFFICIAL_ENCODING_NAME,
    OFFICIAL_PACKAGE_VERSION,
    OUTPUT_CAP_TOKENS,
    _experiment_totals,
    _repair_bound,
    load_official_tokenizer,
    run_offline_controls,
    tokenizer_identity_is_valid,
)


def test_known_text_fixture_and_pinned_identity_are_exact():
    encoding, identity = load_official_tokenizer()
    assert len(encoding.encode("Hello world")) == 2
    assert identity.package_version == OFFICIAL_PACKAGE_VERSION
    assert identity.encoding_name == OFFICIAL_ENCODING_NAME


def test_mutating_output_cap_changes_experiment_bound():
    baseline = _experiment_totals(100, 200, OUTPUT_CAP_TOKENS)
    mutated = _experiment_totals(100, 200, OUTPUT_CAP_TOKENS - 1)
    assert baseline != mutated


def test_larger_previous_output_increases_repair_request_bound():
    from src.idea_evolution.stages.contracts import BaselineRefineOutput

    encoding, _ = load_official_tokenizer()
    schemas = (("BASELINE_REFINE", BaselineRefineOutput),)
    baseline = _repair_bound(encoding, schemas, previous_output_cap=100)
    enlarged = _repair_bound(encoding, schemas, previous_output_cap=101)
    assert enlarged.input_tokens == baseline.input_tokens + 1


def test_missing_or_substituted_identity_fails_closed():
    assert tokenizer_identity_is_valid(OFFICIAL_PACKAGE_VERSION, OFFICIAL_ENCODING_NAME)
    assert not tokenizer_identity_is_valid("missing", OFFICIAL_ENCODING_NAME)
    assert not tokenizer_identity_is_valid(OFFICIAL_PACKAGE_VERSION, "other")


def test_offline_controls_all_pass_without_provider_activity():
    assert all(run_offline_controls().values())
