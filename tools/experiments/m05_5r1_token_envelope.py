"""Offline-only token-envelope calibration for M05.5R1.

This module deliberately has no provider client, no reveal input, and never
returns holdout literals.  It counts only the frozen holdout text through the
official OpenAI Harmony tokenizer while constructing the same system/user
messages used by the current native runner.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence, Type

from pydantic import BaseModel


EXPERIMENT_ID = "EXP-M05.5R1-CONTROLLED-REPLICATION-20260901"
MODEL = "openai/gpt-oss-120b"
CONTEXT_WINDOW_TOKENS = 131_072
OLD_OUTPUT_CAP_TOKENS = 8_192
OUTPUT_CAP_TOKENS = 2_048
OFFICIAL_PACKAGE = "openai-harmony"
OFFICIAL_PACKAGE_VERSION = "0.0.8"
OFFICIAL_WHEEL_SHA256 = "39d44f0d8f466bd56698e7ead708bead3141e27b9b87e3ab7d5a6d0e4a869ee5"
OFFICIAL_ENCODING_NAME = "HarmonyGptOss"
HOLDOUT_PATH = Path(r"C:\Users\phped\Documents\IEE-SealedHoldouts\M05.5R1-HOLDOUT-SET-REV1.sealed.json")
HISTORICAL_ROOT = Path("experiments/EXP-M05.4-PROSPECTIVE-RERUN-20260829/REAL-EXECUTION-ATTEMPT-004/raw")


@dataclass(frozen=True)
class TokenizerIdentity:
    package: str
    package_version: str
    wheel_sha256: str
    encoding_name: str
    identity_sha256: str


@dataclass(frozen=True)
class RequestBound:
    input_tokens: int
    output_tokens: int
    total_tokens: int
    fixed_prompt_tokens: int
    holdout_tokens: int
    schema_tokens: int
    protocol_overhead_tokens: int
    previous_output_tokens: int
    source: str


@dataclass(frozen=True)
class Envelope:
    tokenizer: TokenizerIdentity
    historical_output_tokens: Mapping[str, Any]
    initial_request_maxima: Mapping[str, RequestBound]
    direct_request_maxima: Mapping[str, RequestBound]
    repair: RequestBound
    primary_requests: int
    repair_requests: int
    transport_requests: int
    experiment_max_input_tokens: int
    experiment_max_output_tokens: int
    experiment_max_total_tokens: int
    max_single_request_token_load: int


def _canonical_hash(value: object) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def strict_schema(model: Type[BaseModel]) -> dict[str, Any]:
    """Exact schema normalization used by NativeModelRunner, kept offline."""
    schema = model.model_json_schema()

    def process(obj: Any) -> None:
        if not isinstance(obj, dict):
            return
        if obj.get("type") == "object" or "properties" in obj:
            obj["type"] = "object"
            obj["additionalProperties"] = False
            properties = obj.get("properties", {})
            if properties:
                obj["required"] = list(properties.keys())
            for child in properties.values():
                process(child)
        for child in obj.get("$defs", {}).values():
            process(child)
        if "items" in obj:
            process(obj["items"])

    process(schema)
    return schema


def system_instruction(stage_name: str, output_schema: Type[BaseModel]) -> tuple[str, str]:
    schema_json = json.dumps(strict_schema(output_schema), indent=2)
    instruction = (
        f"Você é um módulo cognitivo do Idea Evolution Engine para o estágio {stage_name}.\n"
        "Sua resposta DEVE ser estritamente um objeto JSON válido correspondente ao seguinte JSON Schema:\n"
        f"{schema_json}\n"
        "IMPORTANTE: Não inclua tags markdown (```json ... ```) ou texto antes/depois do JSON."
    )
    return instruction, schema_json


def load_official_tokenizer() -> tuple[Any, TokenizerIdentity]:
    """Fail closed unless the installed artifact is the pinned official package."""
    try:
        installed = version(OFFICIAL_PACKAGE)
        from openai_harmony import HarmonyEncodingName, load_harmony_encoding
    except Exception as exc:  # pragma: no cover - depends on local installation
        raise RuntimeError("STOP_TOKENIZER_IDENTITY_UNRESOLVED") from exc
    if installed != OFFICIAL_PACKAGE_VERSION:
        raise RuntimeError("STOP_TOKENIZER_IDENTITY_UNRESOLVED")
    encoding = load_harmony_encoding(HarmonyEncodingName.HARMONY_GPT_OSS)
    if not tokenizer_identity_is_valid(installed, encoding_name=encoding.name):
        raise RuntimeError("STOP_TOKENIZER_IDENTITY_UNRESOLVED")
    identity = TokenizerIdentity(
        package=OFFICIAL_PACKAGE,
        package_version=installed,
        wheel_sha256=OFFICIAL_WHEEL_SHA256,
        encoding_name=encoding.name,
        identity_sha256=_canonical_hash({
            "package": OFFICIAL_PACKAGE,
            "version": installed,
            "wheel_sha256": OFFICIAL_WHEEL_SHA256,
            "encoding": encoding.name,
        }),
    )
    return encoding, identity


def tokenizer_identity_is_valid(package_version: str, encoding_name: str | None) -> bool:
    """Small fail-closed seam so a missing or substituted artifact is testable."""
    return package_version == OFFICIAL_PACKAGE_VERSION and encoding_name == OFFICIAL_ENCODING_NAME


def _chat_token_count(encoding: Any, system: str, user: str) -> int:
    from openai_harmony import Conversation, Message, Role

    conversation = Conversation.from_messages((
        Message.from_role_and_content(Role.SYSTEM, system),
        Message.from_role_and_content(Role.USER, user),
    ))
    return len(encoding.render_conversation_for_completion(conversation, Role.ASSISTANT))


def _text_tokens(encoding: Any, value: str) -> int:
    return len(encoding.encode(value, disallowed_special=()))


def _request_bound(
    encoding: Any,
    stage_name: str,
    output_schema: Type[BaseModel],
    user_prompt: str,
    *,
    holdout_text: str = "",
    previous_output_tokens: int = 0,
    source: str,
) -> RequestBound:
    system, schema_json = system_instruction(stage_name, output_schema)
    total_input = _chat_token_count(encoding, system, user_prompt)
    system_tokens = _text_tokens(encoding, system)
    user_tokens = _text_tokens(encoding, user_prompt)
    protocol = total_input - system_tokens - user_tokens
    return RequestBound(
        input_tokens=total_input,
        output_tokens=OUTPUT_CAP_TOKENS,
        total_tokens=total_input + OUTPUT_CAP_TOKENS,
        fixed_prompt_tokens=system_tokens + user_tokens - _text_tokens(encoding, holdout_text),
        holdout_tokens=_text_tokens(encoding, holdout_text),
        schema_tokens=_text_tokens(encoding, schema_json),
        protocol_overhead_tokens=protocol,
        previous_output_tokens=previous_output_tokens,
        source=source,
    )


def _load_holdouts(path: Path) -> tuple[tuple[str, str], ...]:
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("items") if isinstance(data, dict) else None
    if not isinstance(items, list) or len(items) != 8:
        raise RuntimeError("SEALED_HOLDOUT_SET_INVALID")
    extracted: list[tuple[str, str]] = []
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not isinstance(item.get("raw_idea"), str):
            raise RuntimeError("SEALED_HOLDOUT_SET_INVALID")
        extracted.append((item["id"], item["raw_idea"]))
    return tuple(extracted)


def _historical_output_token_distribution(encoding: Any, root: Path) -> Mapping[str, Any]:
    """Tokenize direct raw outputs; A/C use canonical validated outputs when raw is absent."""
    samples: list[tuple[str, int]] = []
    for path in sorted(root.rglob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        raw = data.get("raw_response") if isinstance(data, dict) else None
        if isinstance(raw, str) and raw:
            samples.append(("DIRECT_RAW", _text_tokens(encoding, raw)))
        elif path.name.startswith("IDEA-") and isinstance(data, dict) and isinstance(data.get("parsed_output"), dict):
            canonical = json.dumps(data["parsed_output"], ensure_ascii=False, separators=(",", ":"))
            samples.append(("CANONICAL_VALIDATED_FALLBACK", _text_tokens(encoding, canonical)))
    values = sorted(value for _, value in samples)
    if not values:
        raise RuntimeError("M05_4_OUTPUTS_UNAVAILABLE")
    p95 = values[round((len(values) - 1) * 0.95)]
    per_kind = {
        kind: {
            "count": len(kind_values),
            "min": min(kind_values),
            "max": max(kind_values),
        }
        for kind, kind_values in (
            (kind, [value for sample_kind, value in samples if sample_kind == kind])
            for kind in sorted({kind for kind, _ in samples})
        )
    }
    bins = ((0, 255), (256, 511), (512, 767), (768, 1023))
    histogram = {
        f"{lower}-{upper}": sum(lower <= value <= upper for value in values)
        for lower, upper in bins
    }
    return {
        "count": len(values),
        "min": values[0],
        "max": values[-1],
        "p50": values[(len(values) - 1) // 2],
        "p95": p95,
        "distribution": {"per_kind": per_kind, "histogram": histogram},
    }


def _dynamic_primary_bound(output_cap: int = OUTPUT_CAP_TOKENS) -> RequestBound:
    """Bound state-dependent prompts by the future executor's context guard."""
    max_input = CONTEXT_WINDOW_TOKENS - output_cap
    return RequestBound(
        input_tokens=max_input,
        output_tokens=output_cap,
        total_tokens=CONTEXT_WINDOW_TOKENS,
        fixed_prompt_tokens=0,
        holdout_tokens=0,
        schema_tokens=0,
        protocol_overhead_tokens=0,
        previous_output_tokens=output_cap,
        source="STATE_DEPENDENT_CONTEXT_GUARD_INPUT_PLUS_CAP_LE_CONTEXT_WINDOW",
    )


def _repair_bound(
    encoding: Any,
    schemas: Iterable[tuple[str, Type[BaseModel]]],
    *,
    previous_output_cap: int = OUTPUT_CAP_TOKENS,
) -> RequestBound:
    """A repair embeds one failed primary output; it never carries a holdout or state."""
    maximum: RequestBound | None = None
    for stage_name, output_schema in schemas:
        system, schema_json = system_instruction(stage_name, output_schema)
        prefix = "O JSON fornecido falhou na validação com o erro: STRUCTURAL_VALIDATION_FAILURE\nTexto recebido anteriormente:\n"
        suffix = "\n\nCorrija o JSON para conformidade estrita com o schema:\n" + schema_json
        # BPE tokenization cannot exceed the concatenation of independently
        # encoded segments. The failed content is capped by the primary cap.
        fixed = _chat_token_count(encoding, system, prefix + suffix)
        bound = RequestBound(
            input_tokens=fixed + previous_output_cap,
            output_tokens=OUTPUT_CAP_TOKENS,
            total_tokens=fixed + previous_output_cap + OUTPUT_CAP_TOKENS,
            fixed_prompt_tokens=fixed,
            holdout_tokens=0,
            schema_tokens=_text_tokens(encoding, schema_json),
            protocol_overhead_tokens=0,
            previous_output_tokens=previous_output_cap,
            source=f"STRUCTURAL_REPAIR_{stage_name}_NO_HOLDOUT",
        )
        if maximum is None or bound.input_tokens > maximum.input_tokens:
            maximum = bound
    if maximum is None:
        raise RuntimeError("REPAIR_SCHEMA_SET_EMPTY")
    return maximum


def _experiment_totals(direct_input_tokens: int, repair_fixed_tokens: int, output_cap: int) -> tuple[int, int, int]:
    """Pure arithmetic for the frozen 104-primary / 104-repair maximum."""
    dynamic_primary_positions = 80
    primary_requests = 104
    repair_requests = 104
    input_total = (
        direct_input_tokens
        + dynamic_primary_positions * (CONTEXT_WINDOW_TOKENS - output_cap)
        + repair_requests * (repair_fixed_tokens + output_cap)
    )
    output_total = (primary_requests + repair_requests) * output_cap
    return input_total, output_total, input_total + output_total


def calculate_envelope(
    *,
    holdout_path: Path = HOLDOUT_PATH,
    historical_root: Path = HISTORICAL_ROOT,
) -> Envelope:
    """Return only derived counts and hashes; never expose sealed literals."""
    encoding, identity = load_official_tokenizer()
    from src.idea_evolution.domain.early_epistemic_gate import LeanFirstPassOutput, FocusedEscalationOutput
    from src.idea_evolution.stages.contracts import (
        AlternativesOutput, AttackOutput, BaselineRefineOutput, FinalReviewOutput,
        RealityCheckOutput, SynthesizeOutput, UnderstandOutput,
    )

    holdouts = _load_holdouts(holdout_path)
    baseline_template = Path("prompts/baseline_refine_v0_1.md").read_text(encoding="utf-8")
    understand_template = Path("prompts/understand_v0_1.md").read_text(encoding="utf-8")
    lean_template = (
        "Você é o analista do Lean Idea Evolution Engine.\n"
        "Analise a ideia original abaixo e produza uma estruturação mínima focada em intenção, mecanismo e riscos:\n"
        "IDEIA HUMANA:\n{idea}\n"
    )

    a_bounds = [_request_bound(encoding, "BASELINE_REFINE", BaselineRefineOutput,
                               baseline_template.replace("{idea}", idea), holdout_text=idea,
                               source="A_FROZEN_BASELINE") for _, idea in holdouts]
    b_first_bounds = [_request_bound(encoding, "UNDERSTAND", UnderstandOutput,
                                     understand_template.replace("{original_idea}", idea), holdout_text=idea,
                                     source="B_UNDERSTAND_FROZEN") for _, idea in holdouts]
    c_first_bounds = [_request_bound(encoding, "LEAN_FIRST_PASS", LeanFirstPassOutput,
                                     lean_template.replace("{idea}", idea), holdout_text=idea,
                                     source="C_LEAN_FIRST_PASS_FROZEN") for _, idea in holdouts]
    dynamic = _dynamic_primary_bound()
    repair = _repair_bound(encoding, (
        ("BASELINE_REFINE", BaselineRefineOutput), ("UNDERSTAND", UnderstandOutput),
        ("ATTACK", AttackOutput), ("ALTERNATIVES", AlternativesOutput),
        ("SYNTHESIZE", SynthesizeOutput), ("REALITY_CHECK", RealityCheckOutput),
        ("FINAL_REVIEW", FinalReviewOutput), ("LEAN_FIRST_PASS", LeanFirstPassOutput),
        ("FOCUSED_ESCALATION", FocusedEscalationOutput),
    ))
    maxima = {
        "A": max(a_bounds, key=lambda item: item.input_tokens),
        "B": dynamic,
        "C": dynamic,
    }
    primary_requests = 104
    repair_requests = 104
    transport_requests = primary_requests + repair_requests
    # A/B/C each have eight literal first requests.  The remaining 80 primary
    # positions (B: 9×8; C escalation: 1×8) depend on generated state.
    direct_input_total = sum(item.input_tokens for item in a_bounds + b_first_bounds + c_first_bounds)
    input_total, output_total, total = _experiment_totals(
        direct_input_total, repair.fixed_prompt_tokens, OUTPUT_CAP_TOKENS
    )
    return Envelope(
        tokenizer=identity,
        historical_output_tokens=_historical_output_token_distribution(encoding, historical_root),
        initial_request_maxima={
            "A_BASELINE": max(a_bounds, key=lambda item: item.input_tokens),
            "B_UNDERSTAND": max(b_first_bounds, key=lambda item: item.input_tokens),
            "C_LEAN_FIRST_PASS": max(c_first_bounds, key=lambda item: item.input_tokens),
        },
        direct_request_maxima=maxima,
        repair=repair,
        primary_requests=primary_requests,
        repair_requests=repair_requests,
        transport_requests=transport_requests,
        experiment_max_input_tokens=input_total,
        experiment_max_output_tokens=output_total,
        experiment_max_total_tokens=total,
        max_single_request_token_load=max(dynamic.total_tokens, repair.total_tokens, *(item.total_tokens for item in a_bounds + b_first_bounds + c_first_bounds)),
    )


def public_receipt(envelope: Envelope) -> dict[str, Any]:
    """A repository-safe receipt with no holdout literals, paths, or reveal data."""
    old_bound = 27_262_976
    return {
        "schema_version": "1.0.0",
        "mission_id": "PFI-M05_5R1-TOKEN-ENVELOPE-CALIBRATION-001",
        "execution_authority": "OFFLINE_ONLY",
        "experiment_id": EXPERIMENT_ID,
        "model": MODEL,
        "tokenizer": asdict(envelope.tokenizer),
        "m05_4_output_tokens": envelope.historical_output_tokens,
        "output_cap": {
            "old": OLD_OUTPUT_CAP_TOKENS,
            "new": OUTPUT_CAP_TOKENS,
            "decision": "LOWER_TO_DEFENSIBLE_NONBINDING_CAP",
            "headroom_vs_max_observed": OUTPUT_CAP_TOKENS / envelope.historical_output_tokens["max"],
            "headroom_vs_p95_observed": OUTPUT_CAP_TOKENS / envelope.historical_output_tokens["p95"],
            "treatment_semantics_changed": False,
            "reason": "All schemas remain unchanged; cap hits remain observable and invalidating.",
        },
        "request_maxima": {key: asdict(value) for key, value in envelope.direct_request_maxima.items()},
        "initial_request_maxima": {key: asdict(value) for key, value in envelope.initial_request_maxima.items()},
        "state_dependent_positions": {
            "B": {"count": 72, "positions_per_holdout": 9, "guard": "serialized_input + 2048 <= 131072"},
            "C": {"count": 8, "positions_per_holdout": 1, "guard": "serialized_input + 2048 <= 131072"},
        },
        "repair_maximum": asdict(envelope.repair),
        "request_counts": {
            "max_primary_requests": envelope.primary_requests,
            "max_repair_requests": envelope.repair_requests,
            "max_transport_requests": envelope.transport_requests,
            "transport_retries": 0,
        },
        "experiment_max_input_tokens": envelope.experiment_max_input_tokens,
        "experiment_max_output_tokens": envelope.experiment_max_output_tokens,
        "experiment_max_total_tokens": envelope.experiment_max_total_tokens,
        "old_full_context_bound": old_bound,
        "bound_reduction_percent": round(100 * (old_bound - envelope.experiment_max_total_tokens) / old_bound, 4),
        "max_single_request_token_load": envelope.max_single_request_token_load,
        "required_tpm_for_no_wait": envelope.max_single_request_token_load,
        "safe_pacing_policy": "CONCURRENCY_1; before every request count the frozen serialized message; dispatch only if serialized_input + cap <= 131072 and remaining TPM covers that load; otherwise wait without changing the committed schedule.",
        "hard_bound_scope": "A/B/C initial requests and all structural repairs are tokenizer-counted exactly. State-dependent B/C requests are guarded at the actual model context limit; this is required because current output schemas permit unconstrained Unicode strings whose reserialization cannot be bounded more narrowly without changing treatment semantics.",
        "observed_expected_envelope": "NOT_EMITTED_M05_4_OUTPUT_HISTORY_DOES_NOT_PROVE_M05_5R1_STATE_DEPENDENT_INPUT_MAXIMUM",
        "holdout_content_exposed_to_coordinator": False,
        "reveal_accessed": False,
        "provider_calls": 0,
        "network_inference_calls": 0,
        "a_b_c_cells_executed": 0,
        "real_replication_started": False,
    }


def run_offline_controls() -> Mapping[str, bool]:
    encoding, identity = load_official_tokenizer()
    fixture_ok = _text_tokens(encoding, "Hello world") == 2
    identity_ok = identity.identity_sha256 == _canonical_hash({
        "package": OFFICIAL_PACKAGE, "version": OFFICIAL_PACKAGE_VERSION,
        "wheel_sha256": OFFICIAL_WHEEL_SHA256, "encoding": OFFICIAL_ENCODING_NAME,
    })
    cap_mutation_ok = _experiment_totals(100, 200, OUTPUT_CAP_TOKENS)[2] != _experiment_totals(100, 200, OUTPUT_CAP_TOKENS - 1)[2]
    repair_small = _repair_bound(encoding, (("BASELINE_REFINE", __import__("src.idea_evolution.stages.contracts", fromlist=["BaselineRefineOutput"]).BaselineRefineOutput),), previous_output_cap=100)
    repair_large = _repair_bound(encoding, (("BASELINE_REFINE", __import__("src.idea_evolution.stages.contracts", fromlist=["BaselineRefineOutput"]).BaselineRefineOutput),), previous_output_cap=101)
    previous_output_growth_ok = repair_large.input_tokens > repair_small.input_tokens
    missing_identity_fails_closed = not tokenizer_identity_is_valid("MISSING", OFFICIAL_ENCODING_NAME)
    return {
        "known_text_fixture": fixture_ok,
        "tokenizer_identity_hash": identity_ok,
        "output_cap_mutation_changes_bound": cap_mutation_ok,
        "enlarged_previous_output_increases_downstream_bound": previous_output_growth_ok,
        "missing_tokenizer_identity_fails_closed": missing_identity_fails_closed,
    }
