#!/usr/bin/env python3
"""
tools/experiments/execute_m05_5r1_confirmatory.py
Confirmatory replication execution harness for M05.5R1.

Architecture:
  1. Fail-closed pre-execution verification (hashes, receipts, registry, worktree).
  2. Append-only registry reservation (configurable attempt_id, e.g. REAL-EXECUTION-ATTEMPT-003).
  3. Strict CSPRNG-balanced schedule execution (24 cells across 8 blocks).
  4. Paced Groq execution (concurrency=1, TPM wait, zero retry, fingerprint drift tracking).
  5. Immutable cell output writing (fail-closed if cell file already exists).
  6. Deterministic cell reviewability gate (classify_cell_reviewability per frozen scientific contract).
  7. Post-execution blind review packet rendering (machine-only reveal access, zero leaks).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Type, TypeVar

from pydantic import BaseModel

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.idea_evolution.config.routing import ModelDefinition, ModelRoutingConfig
from src.idea_evolution.experiments.blind_renderer import BlindRenderer, BlindReviewItem, BlindReviewPacket
from src.idea_evolution.orchestration.baseline import BaselineRunner
from src.idea_evolution.orchestration.lean_loop import LeanLoopRunner
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.providers.base import ModelResponse, ModelRunner, ModelUsage
from src.idea_evolution.providers.native import (
    parse_provider_exception,
    sanitize_error_message,
    to_strict_json_schema,
)
from src.idea_evolution.providers.router import RunnerRouter
from tools.experiments.m05_5r1_capacity_design import ScheduleEntry, build_balanced_schedule, schedule_commitment
from tools.experiments.m05_5r1_token_envelope import (
    OUTPUT_CAP_TOKENS,
    _chat_token_count,
    load_official_tokenizer,
    system_instruction,
)

T = TypeVar("T", bound=BaseModel)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
EXPERIMENT_ID = "EXP-M05.5R1-CONTROLLED-REPLICATION-20260901"
DEFAULT_ATTEMPT_ID = "REAL-EXECUTION-ATTEMPT-003"
PROVIDER = "groq_direct"
MODEL = "openai/gpt-oss-120b"
SERVICE_TIER = "FREE"
CONCURRENCY = 1
OUTPUT_CAP = 2048
FREE_RPM = 30
FREE_RPD = 1_000
FREE_TPM = 8_000
FREE_TPD = 200_000
MAX_CAPACITY_WAIT_SECONDS = 75.0
CAPACITY_WAIT_SAFETY_MARGIN_SECONDS = 1.0
MAX_SANITIZED_ERROR_MESSAGE_CHARS = 512
SENSITIVE_OBSERVABILITY_KEYS = frozenset({"authorization", "api_key", "groq_api_key"})
CONFIRMATORY_CLASSIFICATION = "CONFIRMATORY_M05_5R1_REPLICATION"
CONFIRMATORY_IDS = frozenset({f"H0{index}" for index in range(1, 9)})

EXP_DIR = REPO_ROOT / "experiments" / EXPERIMENT_ID
REGISTRY_FILE = EXP_DIR / "ATTEMPT-REGISTRY.jsonl"

SEALED_HOLDOUT_PATH = Path(r"C:\Users\phped\Documents\IEE-SealedHoldouts\M05.5R1-HOLDOUT-SET-REV1.sealed.json")
SEALED_REVEAL_PATH = Path(r"C:\Users\phped\Documents\IEE-SealedHoldouts\M05.5R1-BLINDING-REV1.reveal.json")

EXPECTED_HOLDOUT_SET_SHA256 = "9b2a3b004a3b5533072bf7b6974ed17ee0180b61788621eefa03e1da12092cb9"
EXPECTED_BLIND_COMMITMENT_SHA256 = "d2de9ac1bbcd76c7aaef639b0b61d63dd355f1bea96f9d1c0f41ef7d434eed02"
EXPECTED_SCHEDULE_COMMITMENT_SHA256 = "05f948a49bdf11e7233dce98771359e216339989818cf46782d014ee94af7983"

FROZEN_HOLDOUT_ORDER = ("H08", "H02", "H03", "H01", "H07", "H04", "H05", "H06")
FROZEN_BASE_PERMUTATION = ("CONDITION_C", "CONDITION_B", "CONDITION_A")

M054_FREEZE_MANIFEST = (
    REPO_ROOT
    / "experiments"
    / "EXP-M05.4-PROSPECTIVE-RERUN-20260829"
    / "RERUN-FREEZE-MANIFEST.json"
)

TREATMENT_CRITICAL_FILES: Dict[str, Path] = {
    "baseline.py": REPO_ROOT / "src/idea_evolution/orchestration/baseline.py",
    "simple_loop.py": REPO_ROOT / "src/idea_evolution/orchestration/simple_loop.py",
    "lean_loop.py": REPO_ROOT / "src/idea_evolution/orchestration/lean_loop.py",
    "early_epistemic_gate.py": REPO_ROOT / "src/idea_evolution/domain/early_epistemic_gate.py",
    "routing.py": REPO_ROOT / "src/idea_evolution/config/routing.py",
    "native.py": REPO_ROOT / "src/idea_evolution/providers/native.py",
    "router.py": REPO_ROOT / "src/idea_evolution/providers/router.py",
}


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _hash(value: object) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _bounded_sanitized_text(value: object) -> Optional[str]:
    if not isinstance(value, str) or not value:
        return None
    return sanitize_error_message(value)[:MAX_SANITIZED_ERROR_MESSAGE_CHARS]


def _sanitized_payload_observability(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    payload_keys = [str(key) for key in payload if str(key).lower() not in SENSITIVE_OBSERVABILITY_KEYS]
    messages = payload.get("messages")
    sanitized_messages = []
    if isinstance(messages, list):
        for message in messages:
            if not isinstance(message, Mapping):
                continue
            content = message.get("content")
            sanitized_messages.append({
                "role": str(message.get("role") or ""),
                "content_sha256": hashlib.sha256(str(content or "").encode("utf-8")).hexdigest(),
            })
    response_format = payload.get("response_format")
    sanitized_response_format: Mapping[str, Any] = {}
    if isinstance(response_format, Mapping):
        json_schema = response_format.get("json_schema")
        schema_details: Mapping[str, Any] = {}
        if isinstance(json_schema, Mapping):
            schema_details = {
                "name": str(json_schema.get("name") or ""),
                "strict": bool(json_schema.get("strict")),
                "schema_sha256": _hash(json_schema.get("schema") or {}),
            }
        sanitized_response_format = {
            "type": str(response_format.get("type") or ""),
            "json_schema": schema_details,
        }
    sanitized = {
        "payload_keys": payload_keys,
        "model": str(payload.get("model") or ""),
        "messages": sanitized_messages,
        "response_format": sanitized_response_format,
        "temperature": payload.get("temperature"),
        "max_completion_tokens": payload.get("max_completion_tokens"),
    }
    return {"payload_keys": payload_keys, "sanitized_payload_sha256": _hash(sanitized)}


def _provider_request_id(exc: Exception) -> Optional[str]:
    response = getattr(exc, "response", None)
    headers = getattr(response, "headers", None)
    if not headers:
        return None
    for key in ("x-request-id", "request-id", "x-groq-request-id"):
        value = headers.get(key) or headers.get(key.title())
        sanitized = _bounded_sanitized_text(value)
        if sanitized:
            return sanitized
    return None


def _provider_error_message(exc: Exception, fallback: object) -> Optional[str]:
    body = getattr(exc, "body", None)
    if isinstance(body, Mapping):
        error = body.get("error")
        if isinstance(error, Mapping):
            message = _bounded_sanitized_text(error.get("message"))
            if message:
                return message
    return _bounded_sanitized_text(fallback)


# ---------------------------------------------------------------------------
# Ledger and Windows
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PreDispatchDecision:
    request_id: str
    block_id: str
    classification: str
    treatment: str
    call_index: int
    serialized_input_tokens: int
    reserved_output_tokens: int
    conservative_request_load: int
    cache_assumed_tokens: int
    allowed: bool
    outcome: str
    timestamp: str


class AppendOnlyUsageLedger:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._events = self._load_verify()

    def _load_verify(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        previous = ""
        events: list[dict[str, Any]] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            event = json.loads(line)
            integrity = event.pop("integrity_sha256", None)
            if event.get("previous_event_sha256") != previous or integrity != _hash(event):
                raise RuntimeError("USAGE_LEDGER_INTEGRITY_INVALID")
            previous = integrity
            events.append(event)
        return events

    @property
    def events(self) -> tuple[Mapping[str, Any], ...]:
        return tuple(self._events)

    def append(self, event: Mapping[str, Any]) -> Mapping[str, Any]:
        payload = dict(event)
        if payload.get("event") == "pre_dispatch":
            request_id = payload.get("request_id")
            if not isinstance(request_id, str) or any(
                old.get("event") == "pre_dispatch" and old.get("request_id") == request_id
                for old in self._events
            ):
                raise RuntimeError("DUPLICATE_REQUEST_ID_DENIED")
        payload["previous_event_sha256"] = _hash(self._events[-1]) if self._events else ""
        record = {**payload, "integrity_sha256": _hash(payload)}
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(_canonical(record) + "\n")
        self._events.append(payload)
        return record

    def requests_in_current_day(self, now: datetime) -> int:
        cutoff = now - timedelta(hours=24)
        return sum(
            1 for event in self._events
            if event.get("event") == "pre_dispatch" and event.get("allowed")
            and datetime.fromisoformat(str(event["timestamp"])) >= cutoff
        )

    def requests_in_current_minute(self, now: datetime) -> int:
        cutoff = now - timedelta(minutes=1)
        return sum(
            1 for event in self._events
            if event.get("event") == "pre_dispatch" and event.get("allowed")
            and datetime.fromisoformat(str(event["timestamp"])) >= cutoff
        )

    def reserved_block_load(self, block_id: str) -> int:
        return sum(
            int(event["conservative_request_load"])
            for event in self._events
            if event.get("event") == "pre_dispatch" and event.get("allowed")
            and event.get("block_id") == block_id
        )


class QuotaIsolatedBlockWindow:
    def __init__(self, path: Path, *, safety_margin: timedelta = timedelta(minutes=5)):
        self.path, self.safety_margin = path, safety_margin
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._read()

    def _read(self) -> dict[str, str]:
        if not self.path.exists():
            return {}
        value = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise RuntimeError("BLOCK_WINDOW_STATE_INVALID")
        return {str(key): str(item) for key, item in value.items()}

    def assert_may_start(self, now: datetime) -> None:
        not_before = self.state.get("next_block_not_before")
        if not_before and now < datetime.fromisoformat(not_before):
            raise RuntimeError("NEXT_BLOCK_NOT_BEFORE_DENIED")

    def close(self, last_request_at: datetime) -> dict[str, str]:
        next_at = last_request_at + timedelta(hours=24) + self.safety_margin
        self.state = {
            "previous_block_last_request_at": last_request_at.isoformat(),
            "next_block_not_before": next_at.isoformat(),
        }
        self.path.write_text(_canonical(self.state), encoding="utf-8")
        return dict(self.state)


# ---------------------------------------------------------------------------
# Pre-request Guard & Pacing
# ---------------------------------------------------------------------------

class ConfirmatoryPreRequestGuard:
    def __init__(self, ledger: AppendOnlyUsageLedger, *, now: Callable[[], datetime] = _now,
                 sleep: Callable[[float], None] = time.sleep):
        self.ledger = ledger
        self.now = now
        self.sleep = sleep
        self.encoding, self.tokenizer_identity = load_official_tokenizer()
        self._closed_outcome: Optional[str] = None
        self._fingerprint: Optional[str] = None
        self._fingerprints: list[str] = []
        self._fingerprint_drift_observed = False

    def ensure_confirmatory_source(self, source_id: str, classification: str) -> None:
        if source_id not in CONFIRMATORY_IDS or classification != CONFIRMATORY_CLASSIFICATION:
            raise PermissionError("INVALID_CONFIRMATORY_SOURCE_SELECTION")

    def _tpm_wait_plan(self, now: datetime, load: int) -> tuple[Optional[float], str]:
        for event in reversed(self.ledger.events):
            if event.get("event") != "post_response":
                continue
            remaining = event.get("rate_limit_remaining_tokens")
            reset = event.get("rate_limit_reset_tokens")
            if remaining is None or reset is None:
                continue
            try:
                remaining_tokens = int(str(remaining))
            except ValueError:
                break
            match = re.fullmatch(r"(?:(\d+)m)?(?:(\d+(?:\.\d+)?)s)?", str(reset).strip())
            if not match:
                break
            reset_seconds = int(match.group(1) or 0) * 60 + float(match.group(2) or 0)
            age = max(0.0, (now - datetime.fromisoformat(str(event["timestamp"]))).total_seconds())
            if age < reset_seconds:
                if remaining_tokens >= load:
                    return 0.0, "PROVIDER_TOKEN_HEADERS"
                return reset_seconds - age + CAPACITY_WAIT_SAFETY_MARGIN_SECONDS, "PROVIDER_TOKEN_HEADERS"
            break
        recent = []
        cutoff = now - timedelta(minutes=1)
        for event in self.ledger.events:
            if event.get("event") == "pre_dispatch" and event.get("allowed"):
                timestamp = datetime.fromisoformat(str(event["timestamp"]))
                if timestamp >= cutoff:
                    recent.append((timestamp, int(event["conservative_request_load"])))
        used = sum(item[1] for item in recent)
        if used + load <= FREE_TPM:
            return 0.0, "ROLLING_WINDOW"
        for timestamp, reserved in sorted(recent):
            used -= reserved
            if used + load <= FREE_TPM:
                return max(0.0, (timestamp + timedelta(minutes=1) - now).total_seconds()) + CAPACITY_WAIT_SAFETY_MARGIN_SECONDS, "ROLLING_WINDOW"
        return None, "ROLLING_WINDOW_UNSAFE"

    def wait_for_tpm_capacity(self, *, request_id: str, block_id: str, system: str, user: str) -> None:
        load = _chat_token_count(self.encoding, system, user) + OUTPUT_CAP_TOKENS
        if self._closed_outcome or load > FREE_TPM or self.ledger.reserved_block_load(block_id) + load > FREE_TPD:
            return
        total_wait_seconds = 0.0
        while True:
            now = self.now()
            wait_seconds, reason = self._tpm_wait_plan(now, load)
            if wait_seconds == 0.0:
                return
            if wait_seconds is None or total_wait_seconds + wait_seconds > MAX_CAPACITY_WAIT_SECONDS:
                self.ledger.append({"event": "capacity_wait", "state": "UNSAFE", "request_id": request_id,
                                    "block_id": block_id, "started_at": now.isoformat(), "reason": reason,
                                    "planned_duration_seconds": wait_seconds, "total_wait_seconds": total_wait_seconds,
                                    "timestamp": now.isoformat()})
                return
            self.ledger.append({"event": "capacity_wait", "state": "STARTED", "request_id": request_id,
                                    "block_id": block_id, "started_at": now.isoformat(), "reason": reason,
                                    "planned_duration_seconds": wait_seconds, "total_wait_seconds": total_wait_seconds,
                                    "timestamp": now.isoformat()})
            self.sleep(wait_seconds)
            finished = self.now()
            elapsed = max(0.0, (finished - now).total_seconds())
            total_wait_seconds += elapsed
            self.ledger.append({"event": "capacity_wait", "state": "COMPLETED", "request_id": request_id,
                                    "block_id": block_id, "started_at": now.isoformat(), "reason": reason,
                                    "duration_seconds": elapsed, "total_wait_seconds": total_wait_seconds,
                                    "timestamp": finished.isoformat()})

    def pre_dispatch(
        self, *, request_id: str, block_id: str, classification: str,
        treatment: str, call_index: int, system: str, user: str,
    ) -> PreDispatchDecision:
        now = self.now()
        input_tokens = _chat_token_count(self.encoding, system, user)
        load = input_tokens + OUTPUT_CAP_TOKENS
        outcome = "ALLOW"
        allowed = True
        if self._closed_outcome:
            allowed, outcome = False, self._closed_outcome
        elif load > FREE_TPM:
            allowed, outcome = False, "ABORTED_CAPACITY"
            self._closed_outcome = outcome
        elif self.ledger.reserved_block_load(block_id) + load > FREE_TPD:
            allowed, outcome = False, "ABORTED_CAPACITY"
            self._closed_outcome = outcome
        elif self.ledger.requests_in_current_day(now) >= FREE_RPD:
            allowed, outcome = False, "ABORTED_CAPACITY"
            self._closed_outcome = outcome
        elif self.ledger.requests_in_current_minute(now) >= FREE_RPM:
            allowed, outcome = False, "ABORTED_CAPACITY"
            self._closed_outcome = outcome
        elif self._tpm_wait_plan(now, load)[0] not in (0.0,):
            allowed, outcome = False, "ABORTED_CAPACITY"
            self._closed_outcome = outcome
        decision = PreDispatchDecision(
            request_id=request_id, block_id=block_id, classification=classification,
            treatment=treatment, call_index=call_index,
            serialized_input_tokens=input_tokens,
            reserved_output_tokens=OUTPUT_CAP_TOKENS,
            conservative_request_load=load, cache_assumed_tokens=0,
            allowed=allowed, outcome=outcome, timestamp=now.isoformat(),
        )
        self.ledger.append({"event": "pre_dispatch", **asdict(decision)})
        return decision

    def post_response(self, decision: PreDispatchDecision, response: Mapping[str, Any]) -> None:
        usage = response.get("usage") or {}
        details = usage.get("prompt_tokens_details") or {}
        cached = int(details.get("cached_tokens") or 0)
        prompt = int(usage.get("prompt_tokens") or 0)
        completion = int(usage.get("completion_tokens") or 0)
        total = int(usage.get("total_tokens") or 0)
        fingerprint = response.get("system_fingerprint")
        drift_observed = False
        if fingerprint:
            fingerprint = str(fingerprint)
            if self._fingerprint is None:
                self._fingerprint = fingerprint
            elif self._fingerprint != fingerprint:
                drift_observed = True
                self._fingerprint_drift_observed = True
            self._fingerprints.append(fingerprint)
        rate_headers = response.get("rate_limit_headers") or {}
        if not isinstance(rate_headers, Mapping):
            rate_headers = {}
        normalized_headers = {str(key).lower(): str(value)[:128] for key, value in rate_headers.items()}
        self.ledger.append({
            "event": "post_response", "request_id": decision.request_id,
            "block_id": decision.block_id, "http_status": 200,
            "actual_prompt_tokens": prompt, "actual_cached_tokens": cached,
            "actual_completion_tokens": completion, "actual_total_tokens": total,
            "rate_limit_relevant_token_count": total if total else None,
            "system_fingerprint": fingerprint, "retry_attempt": 0,
            "rate_limit_remaining_tokens": normalized_headers.get("x-ratelimit-remaining-tokens"),
            "rate_limit_reset_tokens": normalized_headers.get("x-ratelimit-reset-tokens"),
            "timestamp": self.now().isoformat(),
        })
        if drift_observed:
            self.ledger.append({
                "event": "fingerprint_drift_observed",
                "request_id": decision.request_id,
                "block_id": decision.block_id,
                "fingerprints_in_order": list(self._fingerprints),
                "confirmatory_policy": "RECORD_CONTINUE_NO_RERUN_NO_REWEIGHT",
                "timestamp": self.now().isoformat(),
            })

    def post_error(
        self,
        decision: PreDispatchDecision,
        *,
        http_status: Optional[int],
        error: str,
        provider_error_code: Optional[str] = None,
        provider_error_message: Optional[str] = None,
        provider_request_id: Optional[str] = None,
        failed_generation_present: bool = False,
        payload: Optional[Mapping[str, Any]] = None,
        model: str = MODEL,
        stage_name: Optional[str] = None,
    ) -> None:
        outcome = "ABORTED_CAPACITY" if http_status == 429 else "INVALID_EXECUTION"
        self._closed_outcome = outcome
        payload_evidence = _sanitized_payload_observability(payload) if payload else {}
        self.ledger.append({
            "event": "post_error", "request_id": decision.request_id,
            "block_id": decision.block_id, "http_status": http_status,
            "is_429": http_status == 429, "retry_attempt": 0,
            "outcome": outcome, "error": error,
            "provider_error_type": error,
            "provider_error_code": _bounded_sanitized_text(provider_error_code),
            "provider_error_message": _bounded_sanitized_text(provider_error_message),
            "provider_request_id": _bounded_sanitized_text(provider_request_id),
            "failed_generation_present": failed_generation_present,
            "model": model, "stage_name": stage_name,
            "condition": decision.treatment,
            **payload_evidence,
            "timestamp": self.now().isoformat(),
        })

    @property
    def closed_outcome(self) -> Optional[str]:
        return self._closed_outcome

    @property
    def fingerprints(self) -> tuple[str, ...]:
        return tuple(self._fingerprints)

    @property
    def fingerprint_drift_observed(self) -> bool:
        return self._fingerprint_drift_observed


# ---------------------------------------------------------------------------
# Confirmatory Model Runner
# ---------------------------------------------------------------------------

Transport = Callable[[Mapping[str, Any]], Mapping[str, Any]]


def _groq_transport(api_key: str) -> Transport:
    def send(payload: Mapping[str, Any]) -> Mapping[str, Any]:
        from groq import Groq
        client = Groq(api_key=api_key)
        raw = client.chat.completions.with_raw_response.create(**dict(payload))
        parsed = raw.parse()
        return {
            "content": parsed.choices[0].message.content or "",
            "usage": parsed.usage.model_dump() if parsed.usage else {},
            "system_fingerprint": getattr(parsed, "system_fingerprint", None),
            "rate_limit_headers": {
                key: value for key, value in raw.headers.items()
                if key.lower().startswith("x-ratelimit-")
            },
        }
    return send


class GuardedGroqConfirmatoryRunner(ModelRunner):
    def __init__(self, guard: ConfirmatoryPreRequestGuard, *, block_id: str, treatment: str,
                 api_key: Optional[str] = None, transport: Optional[Transport] = None):
        self.guard, self.block_id, self.treatment = guard, block_id, treatment
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        self.transport = transport or (_groq_transport(self.api_key) if self.api_key else None)
        self.provider, self.default_model, self._call_number = "groq", MODEL, 0

    def _dispatch(self, prompt_text: str, output_schema: Type[T], stage_name: str,
                  request_kind: str) -> ModelResponse:
        self._call_number += 1
        system, _ = system_instruction(stage_name, output_schema)
        request_id = f"{self.block_id}:{self.treatment}:{self._call_number}:{request_kind}"
        self.guard.wait_for_tpm_capacity(request_id=request_id, block_id=self.block_id, system=system, user=prompt_text)
        decision = self.guard.pre_dispatch(
            request_id=request_id, block_id=self.block_id,
            classification=CONFIRMATORY_CLASSIFICATION, treatment=self.treatment,
            call_index=self._call_number, system=system, user=prompt_text,
        )
        if not decision.allowed:
            return ModelResponse(raw_text="", provider="groq", model=MODEL,
                                 error=decision.outcome, retry_count=0)
        if self.transport is None:
            self.guard.post_error(decision, http_status=None, error="GROQ_API_KEY_MISSING")
            return ModelResponse(raw_text="", provider="groq", model=MODEL,
                                 error="GROQ_API_KEY_MISSING", retry_count=0)
        payload = {
            "model": MODEL,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt_text}],
            "response_format": {"type": "json_schema", "json_schema": {
                "name": f"{stage_name.lower()}_output", "strict": True,
                "schema": to_strict_json_schema(output_schema),
            }},
            "temperature": 0.3, "max_completion_tokens": OUTPUT_CAP_TOKENS,
        }
        try:
            response = self.transport(payload)
        except Exception as exc:
            details = parse_provider_exception(exc, provider="groq", attempts=1, retries=0)
            self.guard.post_error(
                decision,
                http_status=details.http_status,
                error=details.error_type,
                provider_error_code=_bounded_sanitized_text(details.error_code),
                provider_error_message=_provider_error_message(exc, details.message_sanitized),
                provider_request_id=_provider_request_id(exc),
                failed_generation_present=bool(details.failed_generation),
                payload=payload,
                model=MODEL,
                stage_name=stage_name,
            )
            return ModelResponse(raw_text="", provider="groq", model=MODEL,
                                 error=f"PROVIDER_EXECUTION_ERROR:{details.error_type}", retry_count=0)
        self.guard.post_response(decision, response)
        usage = response.get("usage") or {}
        return ModelResponse(
            raw_text=str(response.get("content") or ""), provider="groq", model=MODEL,
            usage=ModelUsage(prompt_tokens=usage.get("prompt_tokens"),
                             completion_tokens=usage.get("completion_tokens"),
                             total_tokens=usage.get("total_tokens")), retry_count=0,
        )

    def generate(self, prompt_text: str, output_schema: Type[T], stage_name: str,
                  model_name: Optional[str] = None, max_repairs: int = 1) -> ModelResponse:
        if model_name and model_name != MODEL:
            return ModelResponse(raw_text="", provider="groq", model=MODEL, error="MODEL_SPEC_VIOLATION")
        primary = self._dispatch(prompt_text, output_schema, stage_name, "PRIMARY")
        if primary.error:
            return primary
        try:
            parsed = output_schema.model_validate(json.loads(primary.raw_text))
            primary.parsed = parsed
            return primary
        except Exception as exc:
            if max_repairs < 1:
                primary.error = "SCHEMA_VALIDATION_FAILED"
                return primary
            system, schema_json = system_instruction(stage_name, output_schema)
            repair = (
                f"O JSON fornecido falhou na validação com o erro: {exc}\n"
                f"Texto recebido anteriormente:\n{primary.raw_text}\n\n"
                f"Corrija o JSON para conformidade estrita com o schema:\n{schema_json}"
            )
            repaired = self._dispatch(repair, output_schema, stage_name, "SEMANTIC_REPAIR")
            if repaired.error:
                return repaired
            try:
                repaired.parsed = output_schema.model_validate(json.loads(repaired.raw_text))
                repaired.retry_count = 1
                return repaired
            except Exception:
                repaired.error = "SCHEMA_VALIDATION_FAILED"
                return repaired


# ---------------------------------------------------------------------------
# Reviewability Classifier (Frozen Scientific Contract)
# ---------------------------------------------------------------------------

def classify_cell_reviewability(
    cell_result: Mapping[str, Any],
    guard_closed_outcome: Optional[str] = None,
) -> tuple[bool, str]:
    """
    Deterministic classification of cell reviewability per frozen scientific contract.
    Distinguishes domain outcome from infrastructure/harness failure.
    Enforces that non-empty text alone is NOT sufficient.
    """
    if guard_closed_outcome:
        return False, f"INFRASTRUCTURE_GUARD_CLOSED:{guard_closed_outcome}"

    cond = cell_result.get("condition")
    error = cell_result.get("error")
    rendered = str(cell_result.get("rendered_semantic_text") or "").strip()

    if cond == "CONDITION_A":
        status = cell_result.get("status")
        parsed = cell_result.get("parsed_output") or {}
        refined = parsed.get("refined_version", "").strip() if isinstance(parsed, dict) else ""
        if error:
            return False, f"A_EXECUTION_ERROR:{error}"
        if status != "SUCCESS":
            return False, f"A_STATUS_NOT_SUCCESS:{status}"
        if not refined:
            return False, "A_MISSING_REFINED_VERSION"
        if "### Versão Refinada" not in rendered:
            return False, "A_MISSING_RENDERED_REFINED_SECTION"
        return True, "A_VALID_BASELINE_CANDIDATE"

    elif cond == "CONDITION_B":
        if error:
            return False, f"B_EXECUTION_ERROR:{error}"
        term_status = cell_result.get("terminal_status")
        valid_terms = {"REFINED_IDEA_READY", "COMPLETED", "STABILIZED", "REFINEMENT_INCOMPLETE"}
        if term_status not in valid_terms:
            return False, f"B_INVALID_TERMINAL_STATUS:{term_status}"
        stages = cell_result.get("stages_executed") or []
        if not isinstance(stages, list) or "FINAL_REVIEW" not in stages:
            return False, f"B_FINAL_REVIEW_NOT_REACHED:stages={stages}"
        required_sections = [
            "### Ideia Refinada Final",
            "### Intenção Humana Preservada",
            "### Mecanismo Central",
            "### Incertezas Críticas Remanescentes",
            "### Próxima Ação Recomendada",
        ]
        for sec in required_sections:
            if sec not in rendered:
                return False, f"B_MISSING_SECTION:{sec}"
        parts = rendered.split("### ")
        for part in parts[1:]:
            lines = part.strip().splitlines()
            if len(lines) <= 1 or not any(line.strip() for line in lines[1:]):
                header = lines[0] if lines else "unknown"
                return False, f"B_EMPTY_SECTION_BODY:{header}"
        return True, f"B_SUBSTANTIVE_CANDIDATE_{term_status}"

    elif cond == "CONDITION_C":
        if error:
            return False, f"C_EXECUTION_ERROR:{error}"
        term_status = cell_result.get("terminal_status")
        valid_terms = {
            "COMPLETED", "COMPLETED_DIRECT_ONE_PASS", "COMPLETED_WITH_FOCUSED_ESCALATION",
            "HUMAN_DECISION_REQUIRED", "DECISION_REQUIRED", "DECISION_SATISFIED", "EARLY_EXIT",
        }
        if term_status == "FIRST_PASS_FAILED":
            return False, "C_FIRST_PASS_FAILED"
        if term_status not in valid_terms:
            return False, f"C_INVALID_TERMINAL_STATUS:{term_status}"
        if not rendered or "### Falha na Execução" in rendered:
            return False, "C_EXECUTION_FAILURE_TEXT_PRESENT"
        return True, f"C_SUBSTANTIVE_CANDIDATE_{term_status}"

    return False, f"UNKNOWN_CONDITION:{cond}"


# ---------------------------------------------------------------------------
# Pre-execution Gate & Registry
# ---------------------------------------------------------------------------

def _registry_entries() -> List[Dict[str, Any]]:
    if not REGISTRY_FILE.exists():
        return []
    entries: List[Dict[str, Any]] = []
    for line in REGISTRY_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            entries.append(json.loads(line))
    return entries


def preflight_verification(attempt_id: str = DEFAULT_ATTEMPT_ID) -> tuple[Dict[str, str], tuple[ScheduleEntry, ...]]:
    """Strict offline preflight checks."""
    if not M054_FREEZE_MANIFEST.exists():
        raise RuntimeError(f"PREFLIGHT_FAIL: M05.4 manifest missing at {M054_FREEZE_MANIFEST}")
    manifest = json.loads(M054_FREEZE_MANIFEST.read_text(encoding="utf-8"))
    ref_hashes = manifest.get("execution_critical_hashes", {})
    for name, path in TREATMENT_CRITICAL_FILES.items():
        ref = ref_hashes.get(name)
        if not ref:
            raise RuntimeError(f"PREFLIGHT_FAIL: {name} not in M05.4 manifest")
        cur = sha256_file(path)
        if cur != ref:
            raise RuntimeError(f"PREFLIGHT_FAIL: Treatment hash mismatch on {name}")

    if not SEALED_HOLDOUT_PATH.exists():
        raise RuntimeError("PREFLIGHT_FAIL: Sealed holdouts missing")
    holdout_data = json.loads(SEALED_HOLDOUT_PATH.read_text(encoding="utf-8"))
    receipt_data = json.loads((EXP_DIR / "M05.5R1-HOLDOUT-SET-REV1-RECEIPT.json").read_text(encoding="utf-8"))
    receipt_items = {item["id"]: item["raw_idea_sha256"] for item in receipt_data["items"]}
    holdout_map: Dict[str, str] = {}
    for item in holdout_data["items"]:
        hid = item["id"]
        raw = item["raw_idea"]
        h_sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        if receipt_items.get(hid) != h_sha:
            raise RuntimeError(f"PREFLIGHT_FAIL: Holdout hash mismatch on {hid}")
        holdout_map[hid] = raw

    schedule = build_balanced_schedule(FROZEN_HOLDOUT_ORDER, FROZEN_BASE_PERMUTATION)
    if schedule_commitment(schedule) != EXPECTED_SCHEDULE_COMMITMENT_SHA256:
        raise RuntimeError("PREFLIGHT_FAIL: Schedule commitment mismatch")

    for entry in _registry_entries():
        if entry.get("attempt_id") == attempt_id:
            raise RuntimeError(f"ATTEMPT_REGISTRY_GUARD: Attempt '{attempt_id}' already registered")

    attempt_path = EXP_DIR / attempt_id
    if attempt_path.exists() and list(attempt_path.glob("**/*.json")):
        raise RuntimeError(f"ATTEMPT_ALREADY_EXISTS: {attempt_path} contains existing evidence")

    return holdout_map, schedule


def reserve_attempt(start_head: str, attempt_id: str = DEFAULT_ATTEMPT_ID) -> None:
    EXP_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "experiment_id": EXPERIMENT_ID,
        "attempt_id": attempt_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "start_head": start_head,
        "status": "RUNNING",
    }
    with open(REGISTRY_FILE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


def create_lock(start_head: str, attempt_id: str = DEFAULT_ATTEMPT_ID) -> None:
    attempt_path = EXP_DIR / attempt_id
    raw_path = attempt_path / "raw"
    attempt_path.mkdir(parents=True, exist_ok=True)
    raw_path.mkdir(parents=True, exist_ok=True)
    (raw_path / "runs_a").mkdir(parents=True, exist_ok=True)
    (raw_path / "runs_b").mkdir(parents=True, exist_ok=True)
    (raw_path / "runs_c").mkdir(parents=True, exist_ok=True)
    lock_data = {
        "experiment_id": EXPERIMENT_ID,
        "attempt_id": attempt_id,
        "start_timestamp": datetime.now(timezone.utc).isoformat(),
        "start_head": start_head,
    }
    (attempt_path / ".attempt_immutability_lock").write_text(json.dumps(lock_data, indent=2), encoding="utf-8")


def update_attempt_status(status: str, attempt_id: str = DEFAULT_ATTEMPT_ID) -> None:
    if not REGISTRY_FILE.exists():
        return
    lines = REGISTRY_FILE.read_text(encoding="utf-8").splitlines()
    updated: List[str] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        entry = json.loads(line)
        if entry.get("attempt_id") == attempt_id:
            entry["status"] = status
            entry["completed_at"] = datetime.now(timezone.utc).isoformat()
        updated.append(json.dumps(entry))
    REGISTRY_FILE.write_text("\n".join(updated) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Cell Execution
# ---------------------------------------------------------------------------

def execute_confirmatory_cell(
    *,
    holdout_id: str,
    condition: str,
    raw_idea: str,
    runner: ModelRunner,
    raw_dir: Path,
    attempt_id: str = DEFAULT_ATTEMPT_ID,
) -> Dict[str, Any]:
    cell_id = f"{holdout_id}-{condition}"
    raw_artifact_file = raw_dir / f"{holdout_id}_{condition.lower()}.json"
    if raw_artifact_file.exists():
        raise RuntimeError(f"CELL_OVERWRITE_GUARD: Cell '{raw_artifact_file.name}' already exists")

    start_time = time.time()

    if condition == "CONDITION_A":
        runs_dir = raw_dir / "runs_a"
        baseline = BaselineRunner(runner=runner, model_name=MODEL)
        result = baseline.run(original_idea=raw_idea, run_id=f"EXP-M05.5R1-{holdout_id}-COND-A", runs_dir=runs_dir)
        lat = time.time() - start_time
        output_data = result.get("parsed_output") or {}
        is_success = (result.get("success") is True) and bool(output_data)
        status = "SUCCESS" if is_success else "FAILED"
        calls = 1

        summary = output_data.get("summary", "")
        refined = output_data.get("refined_version", "")
        strengths = output_data.get("strengths", [])
        weaknesses = output_data.get("weaknesses", [])
        next_steps = output_data.get("next_steps", [])

        rendered_text = (
            f"### Resumo\n{summary}\n\n"
            f"### Versão Refinada\n{refined}\n\n"
            f"### Pontos Fortes e Fracos\n"
            f"- **Fortes:** {', '.join(strengths)}\n"
            f"- **Fracos:** {', '.join(weaknesses)}\n\n"
            f"### Próximos Passos\n{', '.join(next_steps)}"
        )

        raw_payload = {
            "cell_id": cell_id,
            "experiment_id": EXPERIMENT_ID,
            "attempt_id": attempt_id,
            "idea_id": holdout_id,
            "condition": "CONDITION_A",
            "raw_idea": raw_idea,
            "latency_seconds": round(lat, 3),
            "model_calls": calls,
            "status": status,
            "error": result.get("error"),
            "parsed_output": output_data,
            "rendered_semantic_text": rendered_text,
        }

    elif condition == "CONDITION_B":
        runs_dir = raw_dir / "runs_b"
        config = ModelRoutingConfig(
            models={"default": ModelDefinition(provider="groq", model=MODEL)},
            routes={}, default_model_alias="default",
        )
        router = RunnerRouter(config=config, custom_runners={"default": runner})
        simple_runner = SimpleLoopRunner(router=router, topology="STANDARD_6_STAGE", runs_dir=runs_dir)
        state = simple_runner.run(original_idea=raw_idea, run_id=f"EXP-M05.5R1-{holdout_id}-COND-B")
        lat = time.time() - start_time
        calls = len(state.stage_history)
        status_val = getattr(state.status, "value", str(state.status))
        is_success = status_val in ("REFINED_IDEA_READY", "COMPLETED", "STABILIZED")
        status = "SUCCESS" if is_success else "FAILED"

        rendered_text = (
            f"### Ideia Refinada Final\n{state.current_idea or state.original_idea}\n\n"
            f"### Intenção Humana Preservada\n{state.human_intent}\n\n"
            f"### Mecanismo Central\n{state.core_mechanism}\n\n"
            f"### Incertezas Críticas Remanescentes\n"
            + "\n".join(f"- {u}" for u in state.remaining_uncertainties)
            + f"\n\n### Próxima Ação Recomendada\n{state.recommended_next_step}"
        )

        raw_payload = {
            "cell_id": cell_id,
            "experiment_id": EXPERIMENT_ID,
            "attempt_id": attempt_id,
            "idea_id": holdout_id,
            "condition": "CONDITION_B",
            "raw_idea": raw_idea,
            "latency_seconds": round(lat, 3),
            "model_calls": calls,
            "status": status,
            "terminal_status": status_val,
            "reconstruction_count": state.reconstruction_count,
            "stages_executed": [s.stage_id for s in state.stage_history],
            "rendered_semantic_text": rendered_text,
        }

    elif condition == "CONDITION_C":
        runs_dir = raw_dir / "runs_c"
        lean_runner = LeanLoopRunner(runner=runner, model_name=MODEL, runs_dir=runs_dir)
        result = lean_runner.run(original_idea=raw_idea, run_id=f"EXP-M05.5R1-{holdout_id}-COND-C")
        lat = time.time() - start_time
        calls = result.total_model_calls
        term_status = result.terminal_status or "UNKNOWN"
        is_success = term_status in (
            "COMPLETED",
            "COMPLETED_DIRECT_ONE_PASS",
            "COMPLETED_WITH_FOCUSED_ESCALATION",
            "HUMAN_DECISION_REQUIRED",
            "DECISION_REQUIRED",
            "DECISION_SATISFIED",
            "EARLY_EXIT",
        )
        status = "SUCCESS" if is_success else "FAILED"
        rendered_text = result.final_markdown or ""
        gate_outcome_val = result.gate_result.outcome.value if result.gate_result else "UNKNOWN"

        raw_payload = {
            "cell_id": cell_id,
            "experiment_id": EXPERIMENT_ID,
            "attempt_id": attempt_id,
            "idea_id": holdout_id,
            "condition": "CONDITION_C",
            "raw_idea": raw_idea,
            "latency_seconds": round(lat, 3),
            "model_calls": calls,
            "status": status,
            "terminal_status": term_status,
            "gate_outcome": gate_outcome_val,
            "human_decision_requested": result.human_decision_requested,
            "rendered_semantic_text": rendered_text,
        }

    else:
        raise ValueError(f"UNKNOWN_CONDITION: {condition}")

    raw_artifact_file.write_text(json.dumps(raw_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return raw_payload


# ---------------------------------------------------------------------------
# Main Confirmatory Execution Orchestrator
# ---------------------------------------------------------------------------

def run_confirmatory_replication(start_head: str, attempt_id: str = DEFAULT_ATTEMPT_ID) -> Dict[str, Any]:
    holdout_map, schedule = preflight_verification(attempt_id=attempt_id)
    reserve_attempt(start_head, attempt_id=attempt_id)
    create_lock(start_head, attempt_id=attempt_id)

    attempt_path = EXP_DIR / attempt_id
    raw_path = attempt_path / "raw"

    ledger = AppendOnlyUsageLedger(attempt_path / "usage-ledger.jsonl")
    window = QuotaIsolatedBlockWindow(attempt_path / "block-window.json")
    window.assert_may_start(_now())
    guard = ConfirmatoryPreRequestGuard(ledger)

    executed_cells: List[Dict[str, Any]] = []
    calls_by_cond = {"CONDITION_A": 0, "CONDITION_B": 0, "CONDITION_C": 0}

    print(f"CONFIRMATORY_EXECUTION_START: Attempt '{attempt_id}', {len(schedule)} scheduled cells.")

    for entry in schedule:
        holdout_id = entry.holdout_id
        condition = entry.condition
        guard.ensure_confirmatory_source(holdout_id, CONFIRMATORY_CLASSIFICATION)
        raw_idea = holdout_map[holdout_id]

        print(f"\n--- Block {entry.block} Pos {entry.position}: {holdout_id} {condition} ---")
        runner = GuardedGroqConfirmatoryRunner(guard, block_id=f"{attempt_id}-{holdout_id}", treatment=condition)

        cell_result = execute_confirmatory_cell(
            holdout_id=holdout_id,
            condition=condition,
            raw_idea=raw_idea,
            runner=runner,
            raw_dir=raw_path,
            attempt_id=attempt_id,
        )
        executed_cells.append(cell_result)
        calls_by_cond[condition] += cell_result["model_calls"]

        # Deterministic Reviewability Gate per frozen scientific contract
        is_reviewable, review_reason = classify_cell_reviewability(cell_result, guard.closed_outcome)

        if guard.closed_outcome:
            update_attempt_status("FAILED", attempt_id=attempt_id)
            raise RuntimeError(f"INFRASTRUCTURE_ABORT: {cell_result['cell_id']} guard={guard.closed_outcome}")

        if not is_reviewable:
            update_attempt_status("FAILED", attempt_id=attempt_id)
            raise RuntimeError(f"CELL_NOT_REVIEWABLE: {cell_result['cell_id']} reason={review_reason}")

        print(f"  -> Reviewability: PASS ({review_reason})")

    # All 24 cells completed and reviewable
    update_attempt_status("COMPLETED", attempt_id=attempt_id)

    posts = [event for event in ledger.events if event.get("event") in {"post_response", "post_error"}]
    if posts:
        last = datetime.fromisoformat(str(posts[-1]["timestamp"]))
        window.close(last)

    # Write REAL-EXECUTION-MANIFEST.json
    manifest_data = {
        "experiment_id": EXPERIMENT_ID,
        "attempt_id": attempt_id,
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "total_cells": len(executed_cells),
        "total_semantic_model_calls": sum(calls_by_cond.values()),
        "calls_by_condition": calls_by_cond,
        "cells": [
            {
                "cell_id": c["cell_id"],
                "idea_id": c["idea_id"],
                "condition": c["condition"],
                "model_calls": c["model_calls"],
                "status": c["status"],
                "terminal_status": c.get("terminal_status"),
                "sha256": sha256_file(raw_path / f"{c['idea_id']}_{c['condition'].lower()}.json"),
            }
            for c in executed_cells
        ],
    }
    (attempt_path / "REAL-EXECUTION-MANIFEST.json").write_text(
        json.dumps(manifest_data, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    return manifest_data


# ---------------------------------------------------------------------------
# Blind Review Packet Renderer
# ---------------------------------------------------------------------------

def render_confirmatory_blind_packet(
    attempt_dir: Path,
    reveal_file: Path,
    holdout_file: Path,
    output_packet_path: Path,
    output_form_path: Path,
) -> Dict[str, Any]:
    raw_dir = attempt_dir / "raw"
    if not raw_dir.is_dir():
        raise FileNotFoundError(f"Raw directory not found: {raw_dir}")
    if not reveal_file.is_file():
        raise FileNotFoundError(f"Sealed reveal file not found: {reveal_file}")

    reveal_data = json.loads(reveal_file.read_text(encoding="utf-8"))
    mappings = reveal_data["mappings"]

    holdout_data = json.loads(holdout_file.read_text(encoding="utf-8"))
    ideas = holdout_data["items"]

    blind_packets: List[BlindReviewPacket] = []

    for item in ideas:
        idea_id = item["id"]
        raw_idea = item["raw_idea"]

        file_a = raw_dir / f"{idea_id}_condition_a.json"
        file_b = raw_dir / f"{idea_id}_condition_b.json"
        file_c = raw_dir / f"{idea_id}_condition_c.json"

        data_a = json.loads(file_a.read_text(encoding="utf-8"))
        data_b = json.loads(file_b.read_text(encoding="utf-8"))
        data_c = json.loads(file_c.read_text(encoding="utf-8"))

        idea_mapping = mappings[idea_id]
        cond_map = {
            "CONDITION_A": data_a["rendered_semantic_text"],
            "CONDITION_B": data_b["rendered_semantic_text"],
            "CONDITION_C": data_c["rendered_semantic_text"],
        }

        items = [
            BlindReviewItem(label="RESULTADO 1", content_text=cond_map[idea_mapping["R1"]]),
            BlindReviewItem(label="RESULTADO 2", content_text=cond_map[idea_mapping["R2"]]),
            BlindReviewItem(label="RESULTADO 3", content_text=cond_map[idea_mapping["R3"]]),
        ]
        blind_packets.append(BlindReviewPacket(idea_id=idea_id, raw_idea=raw_idea, items=items))

    packet_lines = [
        "# PACOTE DE AVALIAÇÃO CEGA COMPLETO — M05.5R1 REPLICAÇÃO CONTROLADA",
        "",
        "> **AVISO AO REVISOR HUMANO:**",
        "> Este documento contém as 8 ideias holdout avaliadas pelas três condições anônimas (RESULTADO 1, RESULTADO 2, RESULTADO 3).",
        "> A ordem dos resultados foi aleatorizada de forma independente para cada ideia sob compromisso criptográfico prévio (Rev1).",
        "> Preencha o formulário `M05.5R1-HUMAN-REVIEW-FORM.md` e congele suas notas antes de abrir qualquer mapeamento de revelação.",
        "",
    ]

    for p in blind_packets:
        packet_lines.append(BlindRenderer.render_markdown_packet(p))
        packet_lines.append("\n\n============================================================\n\n")

    packet_text = "\n".join(packet_lines)
    output_packet_path.write_text(packet_text, encoding="utf-8")

    leaks = BlindRenderer.detect_leaks(packet_text)

    form_lines = [
        "# M05.5R1-HUMAN-REVIEW-FORM.md — Formulário de Avaliação Humana Cega (M05.5R1)",
        "",
        "> **INSTRUÇÕES PARA O AVALIADOR HUMANO:**",
        "> Avalie cada ideia holdout (H01 a H08) comparando os 3 resultados anônimos (RESULTADO 1, RESULTADO 2, RESULTADO 3).",
        "> Atribua notas de 1 a 5 para cada dimensão e defina o ranking ordinal (1º = 3pts, 2º = 2pts, 3º = 1pt).",
        "> Escolha também com qual resultado você continuaria o desenvolvimento (CONTINUE).",
        "",
        "---",
        "",
    ]

    for item in ideas:
        idea_id = item["id"]
        raw_idea = item["raw_idea"]
        form_lines.extend([
            f"## {idea_id}",
            f"**Ideia Original:** {raw_idea}",
            "",
            "### Pontuação Dimensional (1 a 5)",
            "| Dimensão | RESULTADO 1 | RESULTADO 2 | RESULTADO 3 |",
            "|---|---|---|---|",
            "| 1. Preservação de Intenção | | | |",
            "| 2. Ganho de Clareza | | | |",
            "| 3. Crítica Útil | | | |",
            "| 4. Novidade Útil | | | |",
            "| 5. Controle de Premissas | | | |",
            "| 6. Utilidade Decisória | | | |",
            "| 7. Honestidade Epistêmica | | | |",
            "| 8. Preservação Criativa | | | |",
            "| 9. Moderação Apropriada | | | |",
            "| 10. Acionabilidade Pertinente | | | |",
            "| **TOTAL SECUNDÁRIO** | | | |",
            "",
            "### Ranking Ordinal e Decisão",
            "- **1º Lugar (Melhor - 3 pts):** RESULTADO_",
            "- **2º Lugar (Intermediário - 2 pts):** RESULTADO_",
            "- **3º Lugar (Pior - 1 pt):** RESULTADO_",
            "- **PROCESS_WITH_WHICH_I_WOULD_CONTINUE:** RESULTADO_",
            "",
            "---",
            "",
        ])

    form_text = "\n".join(form_lines)
    output_form_path.write_text(form_text, encoding="utf-8")

    return {
        "blind_packet_path": str(output_packet_path),
        "human_review_form_path": str(output_form_path),
        "total_packets": len(blind_packets),
        "leak_count": len(leaks),
        "leaks": leaks,
    }
