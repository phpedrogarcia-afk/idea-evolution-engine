"""Guarded Free-tier multiday pilot for M05.5R1.

This is deliberately a separate execution seam.  It does not load R1 holdouts
or the reveal, and it cannot execute a confirmatory block.  It reuses the
frozen A/B/C orchestration and prompt/schema construction through a guarded
``ModelRunner``.  Every provider dispatch passes a local exact-token guard.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import time
from typing import Any, Callable, Mapping, Optional, Sequence, Type, TypeVar

from pydantic import BaseModel, ValidationError

from src.idea_evolution.providers.base import ModelResponse, ModelRunner, ModelUsage
from src.idea_evolution.providers.native import (
    parse_provider_exception,
    sanitize_error_message,
    to_strict_json_schema,
)
from tools.experiments.m05_5r1_token_envelope import (
    OUTPUT_CAP_TOKENS,
    _chat_token_count,
    load_official_tokenizer,
    system_instruction,
)

T = TypeVar("T", bound=BaseModel)

FREE_RPM = 30
FREE_RPD = 1_000
FREE_TPM = 8_000
FREE_TPD = 200_000
MODEL = "openai/gpt-oss-120b"
MAX_CAPACITY_WAIT_SECONDS = 75.0
CAPACITY_WAIT_SAFETY_MARGIN_SECONDS = 1.0
MAX_SANITIZED_ERROR_MESSAGE_CHARS = 512
SENSITIVE_OBSERVABILITY_KEYS = frozenset({"authorization", "api_key", "groq_api_key"})
CONFIRMATORY_IDS = frozenset({f"H0{index}" for index in range(1, 9)})
SACRIFICIAL_SOURCE_ID = "M05.4-ATTEMPT-004-IDEA-08"
SACRIFICIAL_CLASSIFICATION = "SACRIFICIAL_M05_4_HISTORICAL_NON_CONFIRMATORY"
SACRIFICIAL_SOURCE_CONTENT_SHA256 = "90928bd682aae8f6193878091dfb3666edc7a3a2e30b302238642bae2fb131a6"
# This is the frozen permutation for schedule block 1.  The pilot substitutes
# only its non-confirmatory source; it never selects or reads H08.
FROZEN_PILOT_TREATMENT_ORDER = ("CONDITION_C", "CONDITION_B", "CONDITION_A")


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _hash(value: object) -> str:
    return sha256(_canonical(value).encode("utf-8")).hexdigest()


def _bounded_sanitized_text(value: object) -> Optional[str]:
    if not isinstance(value, str) or not value:
        return None
    return sanitize_error_message(value)[:MAX_SANITIZED_ERROR_MESSAGE_CHARS]


def _sanitized_payload_observability(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return deterministic, non-secret request evidence without persisting prompt text."""
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
                "content_sha256": sha256(str(content or "").encode("utf-8")).hexdigest(),
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


def _now() -> datetime:
    return datetime.now(timezone.utc)


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
    """Hash-chained JSONL ledger: request identities cannot be reused."""

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
        payload["previous_event_sha256"] = (
            _hash(self._events[-1]) if self._events else ""
        )
        # Hash covers the previous-link and every non-secret field.
        record = {**payload, "integrity_sha256": _hash(payload)}
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(_canonical(record) + "\n")
        self._events.append(payload)
        return record

    def conservative_load_in_current_minute(self, now: datetime) -> int:
        cutoff = now - timedelta(minutes=1)
        total = 0
        for event in self._events:
            if event.get("event") != "pre_dispatch" or not event.get("allowed"):
                continue
            timestamp = datetime.fromisoformat(str(event["timestamp"]))
            if timestamp >= cutoff:
                total += int(event["conservative_request_load"])
        return total

    def requests_in_current_minute(self, now: datetime) -> int:
        cutoff = now - timedelta(minutes=1)
        return sum(
            1 for event in self._events
            if event.get("event") == "pre_dispatch" and event.get("allowed")
            and datetime.fromisoformat(str(event["timestamp"])) >= cutoff
        )

    def requests_in_current_day(self, now: datetime) -> int:
        cutoff = now - timedelta(hours=24)
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
    """Restart-safe 24-hour isolation state; never sleeps or auto-resumes."""

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


class FreePreRequestGuard:
    """Fail-closed gate evaluated before every provider dispatch."""

    def __init__(self, ledger: AppendOnlyUsageLedger, *, now: Callable[[], datetime] = _now,
                 allow_sacrificial_fingerprint_drift: bool = False,
                 sleep: Callable[[float], None] = time.sleep):
        self.ledger = ledger
        self.now = now
        self.allow_sacrificial_fingerprint_drift = allow_sacrificial_fingerprint_drift
        self.sleep = sleep
        self.encoding, self.tokenizer_identity = load_official_tokenizer()
        self._closed_outcome: Optional[str] = None
        self._fingerprint: Optional[str] = None
        self._fingerprints: list[str] = []
        self._fingerprint_drift_observed = False

    def ensure_pilot_source(self, source_id: str, classification: str) -> None:
        if source_id in CONFIRMATORY_IDS or classification != SACRIFICIAL_CLASSIFICATION:
            raise PermissionError("CONFIRMATORY_HOLDOUT_SELECTION_DENIED")

    def assert_frozen_order(self, order: Sequence[str]) -> None:
        if tuple(order) != FROZEN_PILOT_TREATMENT_ORDER:
            raise RuntimeError("SCHEDULE_MUTATION_INVALID_EXECUTION")

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
        """Re-evaluate a not-yet-dispatched request after each bounded, recorded wait."""
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
                if not self.allow_sacrificial_fingerprint_drift:
                    self._closed_outcome = "INVALID_EXECUTION:BACKEND_DRIFT_WITHIN_BLOCK"
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
                "sacrificial_relaxation_applied": self.allow_sacrificial_fingerprint_drift,
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
    def fingerprint(self) -> Optional[str]:
        return self._fingerprint

    @property
    def fingerprints(self) -> tuple[str, ...]:
        return tuple(self._fingerprints)

    @property
    def fingerprint_drift_observed(self) -> bool:
        return self._fingerprint_drift_observed


Transport = Callable[[Mapping[str, Any]], Mapping[str, Any]]


def _groq_transport(api_key: str) -> Transport:
    def send(payload: Mapping[str, Any]) -> Mapping[str, Any]:
        from groq import Groq
        client = Groq(api_key=api_key)
        # Raw response is required solely for non-secret rate-limit headers.
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


class GuardedGroqRunner(ModelRunner):
    """Same structured prompt/schema semantics; no transport retry or hidden cache credit."""

    def __init__(self, guard: FreePreRequestGuard, *, block_id: str, treatment: str,
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
            classification=SACRIFICIAL_CLASSIFICATION, treatment=self.treatment,
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
        except (json.JSONDecodeError, ValidationError) as exc:
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
            except (json.JSONDecodeError, ValidationError):
                repaired.error = "SCHEMA_VALIDATION_FAILED"
                return repaired


def sacrificial_source_path(repo_root: Path) -> Path:
    path = (repo_root / "experiments" / "EXP-M05.4-PROSPECTIVE-RERUN-20260829"
            / "REAL-EXECUTION-ATTEMPT-004" / "raw" / "runs_b"
            / "EXP-M05.4-IDEA-08-COND-B" / "input.json")
    if not path.exists():
        raise RuntimeError("SACRIFICIAL_SOURCE_UNAVAILABLE")
    return path


def load_sacrificial_source(repo_root: Path) -> Mapping[str, str]:
    """Load the canonical Attempt-004 input through a representation-only adapter."""
    source_data = json.loads(sacrificial_source_path(repo_root).read_text(encoding="utf-8"))
    original_idea = source_data.get("original_idea")
    if not isinstance(original_idea, str) or not original_idea:
        raise RuntimeError("SACRIFICIAL_SOURCE_INVALID")
    if sha256(original_idea.encode("utf-8")).hexdigest() != SACRIFICIAL_SOURCE_CONTENT_SHA256:
        raise RuntimeError("SACRIFICIAL_SOURCE_HASH_MISMATCH")
    # `original_idea` -> `source_idea` changes only the in-memory representation;
    # the verified UTF-8 content is passed through byte-for-byte unchanged.
    return {"source_idea": original_idea}


def run_sacrificial_pilot(repo_root: Path, runtime_dir: Path) -> Mapping[str, Any]:
    """Run exactly one non-confirmatory C/B/A block after local auth exists.

    This function is intentionally not a CLI default.  It has no parameter for
    an R1 holdout or reveal path, and raises before any work if local auth is
    absent.  The caller must invoke it under a separate live-pilot authority.
    """
    if not api_credential_available():
        raise RuntimeError("HUMAN_API_KEY_LOCAL_SETUP_REQUIRED")
    source_data = load_sacrificial_source(repo_root)
    raw_idea = source_data.get("source_idea")
    if not isinstance(raw_idea, str) or not raw_idea:
        raise RuntimeError("SACRIFICIAL_SOURCE_INVALID")
    block_id = runtime_dir.name
    ledger = AppendOnlyUsageLedger(runtime_dir / "usage-ledger.jsonl")
    if ledger.events:
        raise RuntimeError("SACRIFICIAL_PILOT_RESUME_UNSUPPORTED")
    window = QuotaIsolatedBlockWindow(runtime_dir / "block-window.json")
    window.assert_may_start(_now())
    guard = FreePreRequestGuard(ledger, allow_sacrificial_fingerprint_drift=True)
    guard.ensure_pilot_source(SACRIFICIAL_SOURCE_ID, SACRIFICIAL_CLASSIFICATION)
    guard.assert_frozen_order(FROZEN_PILOT_TREATMENT_ORDER)

    from src.idea_evolution.config.routing import ModelDefinition, ModelRoutingConfig
    from src.idea_evolution.orchestration.baseline import BaselineRunner
    from src.idea_evolution.orchestration.lean_loop import LeanLoopRunner
    from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
    from src.idea_evolution.providers.router import RunnerRouter

    logical_calls: dict[str, int] = {}
    for treatment in FROZEN_PILOT_TREATMENT_ORDER:
        runner = GuardedGroqRunner(guard, block_id=block_id, treatment=treatment)
        run_root = runtime_dir / "raw" / treatment.lower()
        if treatment == "CONDITION_A":
            result = BaselineRunner(runner=runner, model_name=MODEL).run(
                raw_idea, run_id=f"{block_id}-A", runs_dir=run_root
            )
            logical_calls[treatment] = 1
            failed = not bool(result.get("success"))
        elif treatment == "CONDITION_B":
            config = ModelRoutingConfig(
                models={"default": ModelDefinition(provider="groq", model=MODEL)},
                routes={}, default_model_alias="default",
            )
            state = SimpleLoopRunner(
                router=RunnerRouter(config=config, custom_runners={"default": runner}),
                topology="STANDARD_6_STAGE", runs_dir=run_root,
            ).run(raw_idea, run_id=f"{block_id}-B")
            logical_calls[treatment] = len(state.stage_history)
            failed = state.status.value == "FAILED"
        else:
            result = LeanLoopRunner(runner=runner, model_name=MODEL, runs_dir=run_root).run(
                raw_idea, run_id=f"{block_id}-C"
            )
            logical_calls[treatment] = result.total_model_calls
            failed = result.terminal_status.endswith("FAILED")
        if guard.closed_outcome or failed:
            raise RuntimeError(guard.closed_outcome or "PILOT_INVALID")

    posts = [event for event in ledger.events if event.get("event") in {"post_response", "post_error"}]
    if not posts:
        raise RuntimeError("PILOT_NO_PROVIDER_REQUESTS")
    last = datetime.fromisoformat(str(posts[-1]["timestamp"]))
    window_state = window.close(last)
    actual = [event for event in posts if event.get("event") == "post_response"]
    summary = {
        "pilot_attempt_id": block_id,
        "sacrificial_source": SACRIFICIAL_SOURCE_ID,
        "confirmatory_value": "NO",
        "treatment_order": list(FROZEN_PILOT_TREATMENT_ORDER),
        "logical_calls": logical_calls,
        "provider_requests": len(posts),
        "total_prompt_tokens": sum(int(event.get("actual_prompt_tokens") or 0) for event in actual),
        "total_cached_tokens": sum(int(event.get("actual_cached_tokens") or 0) for event in actual),
        "total_completion_tokens": sum(int(event.get("actual_completion_tokens") or 0) for event in actual),
        "total_tokens": sum(int(event.get("actual_total_tokens") or 0) for event in actual),
        "max_request_input_tokens": max(int(event["serialized_input_tokens"]) for event in ledger.events if event.get("event") == "pre_dispatch"),
        "max_conservative_request_load": max(int(event["conservative_request_load"]) for event in ledger.events if event.get("event") == "pre_dispatch"),
        "max_actual_request_total": max((int(event.get("actual_total_tokens") or 0) for event in actual), default=0),
        "system_fingerprints": list(guard.fingerprints),
        "fingerprint_drift_observed": guard.fingerprint_drift_observed,
        "next_block_window": window_state,
    }
    (runtime_dir / "PILOT-SUMMARY.json").write_text(_canonical(summary), encoding="utf-8")
    return summary


def api_credential_available() -> bool:
    return bool(os.environ.get("GROQ_API_KEY"))
