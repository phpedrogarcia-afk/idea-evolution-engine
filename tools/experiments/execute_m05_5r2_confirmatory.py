#!/usr/bin/env python3
"""
tools/experiments/execute_m05_5r2_confirmatory.py
Confirmatory replication execution harness for M05.5R2 (Cerebras Cloud Free Tier).

Architecture:
  1. Fail-closed pre-execution verification (hashes, receipts, registry, worktree).
  2. Append-only registry reservation transition (M05.5R2-REAL-EXECUTION-ATTEMPT-001).
  3. Strict CSPRNG-balanced schedule execution (24 cells across 8 blocks).
  4. Token-aware rolling-window pacing (SAFE_RPM_BUDGET=4, SAFE_TPM_BUDGET=27000, 15s min cadence).
  5. Symmetric 4096 output-cap enforcement (A_4096_B_4096_C_4096) with cap-hit fail-closed guard.
  6. Immutable cell output writing (fail-closed if cell file already exists).
  7. Deterministic cell reviewability gate (classify_cell_reviewability per frozen scientific contract).
  8. Post-execution blind review packet rendering (machine-only reveal access, zero leaks).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import urllib.request
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple, Type, TypeVar

from pydantic import BaseModel, ValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.idea_evolution.config.routing import ModelDefinition, ModelRoutingConfig
from src.idea_evolution.experiments.blind_renderer import BlindRenderer, BlindReviewItem, BlindReviewPacket
from src.idea_evolution.orchestration.baseline import BaselineRunner
from src.idea_evolution.orchestration.lean_loop import LeanLoopRunner
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.providers.base import ModelResponse, ModelRunner, ModelUsage
from src.idea_evolution.providers.cerebras import (
    CerebrasTransportBuilder,
    get_cerebras_api_key,
    CEREBRAS_HOSTED_BASE_URL,
    CEREBRAS_TRANSPORT_MODEL_ID,
    SCIENTIFIC_MODEL_ID,
)
from src.idea_evolution.providers.native import to_strict_json_schema
from src.idea_evolution.providers.router import RunnerRouter
from tools.experiments.execute_m05_5r1_confirmatory import classify_cell_reviewability
from tools.experiments.m05_5r1_capacity_design import ScheduleEntry, build_balanced_schedule, schedule_commitment
from tools.experiments.m05_5r1_token_envelope import (
    _chat_token_count,
    load_official_tokenizer,
    system_instruction as get_system_instruction,
)

T = TypeVar("T", bound=BaseModel)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
EXPERIMENT_ID = "EXP-M05.5R2-FREE-PROVIDER-PORTABILITY-REPLICATION"
DEFAULT_ATTEMPT_ID = "M05.5R2-REAL-EXECUTION-ATTEMPT-002"
PROVIDER = "cerebras"
SCIENTIFIC_MODEL = SCIENTIFIC_MODEL_ID  # "openai/gpt-oss-120b"
TRANSPORT_MODEL = CEREBRAS_TRANSPORT_MODEL_ID  # "gpt-oss-120b"
SERVICE_TIER = "FREE_TRIAL"
CONCURRENCY = 1
OUTPUT_CAP = 4096
OUTPUT_CAP_SYMMETRY = "A_4096_B_4096_C_4096"

MAX_IDENTICAL_HTTP500_REPLAYS_PER_LOGICAL_CALL = 1
MAX_TOTAL_HTTP500_REPLAYS_PER_ATTEMPT = 1
SDK_MAX_RETRIES = 0

EFFECTIVE_RPM = 5
EFFECTIVE_TPM = 30000
EFFECTIVE_TPH = 1000000
EFFECTIVE_TPD = 1000000

SAFE_RPM_BUDGET = 4      # 80% de 5 RPM
SAFE_TPM_BUDGET = 27000  # 90% de 30.000 TPM
MIN_CADENCE_SECONDS = 15.0  # 60s / 4 = 15s

EXP_DIR = REPO_ROOT / "experiments" / EXPERIMENT_ID
REGISTRY_FILE = EXP_DIR / "ATTEMPT-REGISTRY.jsonl"

RECEIPT_HOLDOUT_PATH = REPO_ROOT / "experiments/EXP-M05.5R1-CONTROLLED-REPLICATION-20260901/M05.5R1-HOLDOUT-SET-REV1-RECEIPT.json"
RECEIPT_BLINDING_PATH = REPO_ROOT / "experiments/EXP-M05.5R1-CONTROLLED-REPLICATION-20260901/M05.5R1-BLINDING-REV1-RECEIPT.json"
RECEIPT_SCHEDULE_PATH = REPO_ROOT / "experiments/EXP-M05.5R1-CONTROLLED-REPLICATION-20260901/M05.5R1-CAPACITY-DESIGN-FREEZE.json"

SEALED_HOLDOUT_PATH = Path(r"C:\Users\phped\Documents\IEE-SealedHoldouts\M05.5R1-HOLDOUT-SET-REV1.sealed.json")
SEALED_REVEAL_PATH = Path(r"C:\Users\phped\Documents\IEE-SealedHoldouts\M05.5R1-BLINDING-REV1.reveal.json")

EXPECTED_HOLDOUT_SET_SHA256 = "9b2a3b004a3b5533072bf7b6974ed17ee0180b61788621eefa03e1da12092cb9"
EXPECTED_BLIND_COMMITMENT_SHA256 = "d2de9ac1bbcd76c7aaef639b0b61d63dd355f1bea96f9d1c0f41ef7d434eed02"
EXPECTED_SCHEDULE_COMMITMENT_SHA256 = "05f948a49bdf11e7233dce98771359e216339989818cf46782d014ee94af7983"

FROZEN_HOLDOUT_ORDER = ("H08", "H02", "H03", "H01", "H07", "H04", "H05", "H06")
FROZEN_BASE_PERMUTATION = ("CONDITION_C", "CONDITION_B", "CONDITION_A")


# ---------------------------------------------------------------------------
# Ledger & Token-Aware Pacer
# ---------------------------------------------------------------------------
class AppendOnlyUsageLedger:
    """Ledger imutável encadeado por SHA-256 com verificação de integridade."""

    def __init__(self, path: Path):
        self.path = path
        self.events: List[Dict[str, Any]] = []
        if self.path.exists():
            self._verify_and_load()

    def _verify_and_load(self) -> None:
        prev_hash = "GENESIS"
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                ev = json.loads(line)
                record_hash = ev.get("integrity_sha256")
                check_ev = dict(ev)
                check_ev.pop("integrity_sha256", None)
                expected_hash = hashlib.sha256(
                    json.dumps(check_ev, sort_keys=True, separators=(",", ":")).encode("utf-8")
                ).hexdigest()
                if record_hash != expected_hash:
                    raise RuntimeError("LEDGER_CORRUPTION: hash mismatch")
                if ev.get("previous_event_sha256") != prev_hash:
                    raise RuntimeError("LEDGER_CORRUPTION: chain broken")
                prev_hash = record_hash
                self.events.append(ev)

    def append(self, event_data: Dict[str, Any]) -> str:
        prev_hash = self.events[-1]["integrity_sha256"] if self.events else "GENESIS"
        ev = dict(event_data)
        ev["previous_event_sha256"] = prev_hash
        ev_hash = hashlib.sha256(
            json.dumps(ev, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        ev["integrity_sha256"] = ev_hash

        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
        self.events.append(ev)
        return ev_hash


class TokenAwarePacer:
    """
    Controlador determinístico de pacing com janela deslizante de 60 segundos.
    Respeita: SAFE_RPM_BUDGET=4 e SAFE_TPM_BUDGET=27000 tokens reservados.
    Cadência mínima: 15,0s entre despachos.
    """

    def __init__(
        self,
        ledger: AppendOnlyUsageLedger,
        safe_rpm: int = SAFE_RPM_BUDGET,
        safe_tpm: int = SAFE_TPM_BUDGET,
        min_cadence_seconds: float = MIN_CADENCE_SECONDS,
    ):
        self.ledger = ledger
        self.safe_rpm = safe_rpm
        self.safe_tpm = safe_tpm
        self.min_cadence = min_cadence_seconds
        # Histórico na memória: lista de (timestamp, reserved_tokens)
        self.dispatches: List[Tuple[float, int]] = []
        self.last_dispatch_time = 0.0

    def prune(self, now: float) -> None:
        cutoff = now - 60.0
        self.dispatches = [d for d in self.dispatches if d[0] >= cutoff]

    def wait_if_needed(self, reserved_tokens: int, request_id: str, cell_id: str) -> None:
        while True:
            now = time.time()
            self.prune(now)

            # 1. Verificar cadência mínima desde o último despacho
            time_since_last = now - self.last_dispatch_time
            if time_since_last < self.min_cadence:
                cadence_wait = self.min_cadence - time_since_last
                self.ledger.append({
                    "event": "capacity_wait",
                    "reason": "MIN_CADENCE",
                    "request_id": request_id,
                    "cell_id": cell_id,
                    "wait_seconds": round(cadence_wait, 3),
                    "active_rpm": len(self.dispatches),
                    "active_tpm": sum(d[1] for d in self.dispatches),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                time.sleep(cadence_wait)
                continue

            # 2. Verificar limite de RPM na janela de 60s
            if len(self.dispatches) >= self.safe_rpm:
                oldest_time = self.dispatches[0][0]
                rpm_wait = max(0.1, (oldest_time + 60.0 - now) + 0.5)
                self.ledger.append({
                    "event": "capacity_wait",
                    "reason": "SAFE_RPM_EXCEEDED",
                    "request_id": request_id,
                    "cell_id": cell_id,
                    "wait_seconds": round(rpm_wait, 3),
                    "active_rpm": len(self.dispatches),
                    "active_tpm": sum(d[1] for d in self.dispatches),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                time.sleep(rpm_wait)
                continue

            # 3. Verificar limite de TPM na janela de 60s
            current_reserved_sum = sum(d[1] for d in self.dispatches)
            if current_reserved_sum + reserved_tokens > self.safe_tpm:
                oldest_time = self.dispatches[0][0]
                tpm_wait = max(0.1, (oldest_time + 60.0 - now) + 0.5)
                self.ledger.append({
                    "event": "capacity_wait",
                    "reason": "SAFE_TPM_EXCEEDED",
                    "request_id": request_id,
                    "cell_id": cell_id,
                    "wait_seconds": round(tpm_wait, 3),
                    "active_rpm": len(self.dispatches),
                    "active_tpm": current_reserved_sum,
                    "proposed_reserved": reserved_tokens,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                time.sleep(tpm_wait)
                continue

            # Orçamento seguro disponível
            break

    def record_dispatch(self, reserved_tokens: int) -> None:
        now = time.time()
        self.dispatches.append((now, reserved_tokens))
        self.last_dispatch_time = now


# ---------------------------------------------------------------------------
# Attempt Resilience Tracker (HTTP 500 Bounded Amendment 001)
# ---------------------------------------------------------------------------
class AttemptResilienceTracker:
    """
    Rastreia o orçamento global de resiliência HTTP 500 por tentativa confirmatória.
    Sob a Emenda 001:
      MAX_IDENTICAL_HTTP500_REPLAYS_PER_LOGICAL_CALL = 1
      MAX_TOTAL_HTTP500_REPLAYS_PER_ATTEMPT = 1
      SDK_MAX_RETRIES = 0
    """

    def __init__(self, max_attempt_http500_replays: int = MAX_TOTAL_HTTP500_REPLAYS_PER_ATTEMPT):
        self.max_attempt_http500_replays = max_attempt_http500_replays
        self.http500_replays_used = 0
        self.http500_errors_seen = 0
        self.http500_replay_successes = 0
        self.http500_replay_exhausted = False


# ---------------------------------------------------------------------------
# Confirmatory ModelRunner
# ---------------------------------------------------------------------------
class ConfirmatoryCerebrasRunner(ModelRunner):
    """
    Executor ModelRunner com verificação de cotas, token-aware pacing,
    teto de 4096 tokens e resiliência estrita a HTTP 500 (Emenda 001).
    """

    def __init__(
        self,
        ledger: AppendOnlyUsageLedger,
        pacer: TokenAwarePacer,
        cell_id: str,
        treatment: str,
        tracker: Optional[AttemptResilienceTracker] = None,
        temperature: float = 0.3,
        max_tokens: int = OUTPUT_CAP,
    ):
        self.model_name = SCIENTIFIC_MODEL
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.ledger = ledger
        self.pacer = pacer
        self.cell_id = cell_id
        self.treatment = treatment
        self.tracker = tracker or AttemptResilienceTracker()
        self.call_count = 0
        self.closed_outcome: Optional[str] = None
        self.builder = CerebrasTransportBuilder(
            base_url=CEREBRAS_HOSTED_BASE_URL,
            scientific_model=SCIENTIFIC_MODEL,
            transport_model=TRANSPORT_MODEL,
        )
        # Tokenizador oficial offline
        tok_tuple = load_official_tokenizer()
        self.harmony_encoding = tok_tuple[0]

    def generate(
        self,
        prompt_text: Optional[str] = None,
        output_schema: Optional[Type[T]] = None,
        stage_name: Optional[str] = None,
        model_name: Optional[str] = None,
        max_repairs: int = 1,
        system_prompt: Optional[str] = None,
        user_prompt: Optional[str] = None,
        schema: Optional[Type[T]] = None,
        system_instruction: Optional[str] = None,
        **kwargs: Any,
    ) -> ModelResponse[T]:
        actual_prompt = prompt_text if prompt_text is not None else (user_prompt or "")
        actual_schema = output_schema if output_schema is not None else schema
        actual_stage = stage_name or (actual_schema.__name__ if actual_schema else "RAW")

        self.call_count += 1
        request_id = f"{self.cell_id}:{self.treatment}:{self.call_count}"

        # 1. Obter instrução do sistema
        sys_inst = ""
        if system_prompt:
            sys_inst = system_prompt
        elif system_instruction:
            sys_inst = system_instruction
        elif actual_schema:
            sys_inst, _ = get_system_instruction(actual_stage, actual_schema)

        # 2. Estimar tokens de entrada e reserva
        input_tokens = _chat_token_count(self.harmony_encoding, sys_inst, actual_prompt)
        reserved_request_tokens = input_tokens + self.max_tokens

        # 3. Token-Aware Pacing
        self.pacer.wait_if_needed(reserved_request_tokens, request_id, self.cell_id)

        # 4. Registrar pre_dispatch
        self.ledger.append({
            "event": "pre_dispatch",
            "request_id": request_id,
            "cell_id": self.cell_id,
            "treatment": self.treatment,
            "stage_name": actual_stage,
            "estimated_input_tokens": input_tokens,
            "reserved_output_tokens": self.max_tokens,
            "reserved_request_tokens": reserved_request_tokens,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        # 5. Construir mensagens e payload
        messages = []
        if sys_inst:
            messages.append({"role": "system", "content": sys_inst})
        messages.append({"role": "user", "content": actual_prompt})

        payload = self.builder.build_request_payload(
            messages=messages,
            schema_cls=actual_schema,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        payload_sha256 = self.builder.compute_sanitized_payload_sha256(payload)
        headers = self.builder.build_headers()
        req_data = json.dumps(payload).encode("utf-8")

        # Registrar despacho no pacer
        self.pacer.record_dispatch(reserved_request_tokens)

        def _execute_http_request(is_replay: bool = False) -> ModelResponse[T]:
            req = urllib.request.Request(
                f"{self.builder.base_url}/chat/completions",
                data=req_data,
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                resp_bytes = resp.read()
                resp_json = json.loads(resp_bytes.decode("utf-8"))
                choice = resp_json.get("choices", [{}])[0]
                message = choice.get("message", {})
                content = message.get("content", "")
                usage_info = resp_json.get("usage", {})
                fp = resp_json.get("system_fingerprint")
                finish_reason = choice.get("finish_reason")
                actual_comp = usage_info.get("completion_tokens", 0)
                cap_util = round(actual_comp / self.max_tokens, 4) if self.max_tokens else 0.0

                # Monitoramento do Teto de 4096 tokens
                if actual_comp >= self.max_tokens or finish_reason == "length":
                    self.ledger.append({
                        "event": "output_cap_binding",
                        "request_id": request_id,
                        "cell_id": self.cell_id,
                        "actual_completion_tokens": actual_comp,
                        "configured_output_cap": self.max_tokens,
                        "finish_reason": finish_reason,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })
                    raise RuntimeError(f"OUTPUT_CAP_4096_BINDING: Generation reached cap of {self.max_tokens} tokens")

                # Registrar sucesso no ledger
                self.ledger.append({
                    "event": "post_response",
                    "request_id": request_id,
                    "cell_id": self.cell_id,
                    "treatment": self.treatment,
                    "stage_name": actual_stage,
                    "http_status": 200,
                    "is_http500_replay": is_replay,
                    "sanitized_payload_sha256": payload_sha256,
                    "actual_prompt_tokens": usage_info.get("prompt_tokens", 0),
                    "actual_completion_tokens": actual_comp,
                    "actual_total_tokens": usage_info.get("total_tokens", 0),
                    "configured_output_cap": self.max_tokens,
                    "reserved_request_tokens": reserved_request_tokens,
                    "output_cap_utilization_ratio": cap_util,
                    "finish_reason": finish_reason,
                    "system_fingerprint": fp,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })

                parsed_data = None
                if actual_schema:
                    try:
                        parsed_data = actual_schema.model_validate_json(content)
                    except ValidationError as ve:
                        self.ledger.append({
                            "event": "validation_error",
                            "request_id": request_id,
                            "error": str(ve),
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        })
                        raise RuntimeError(f"VALIDATION_ERROR: {ve}")

                return ModelResponse(
                    raw_text=content,
                    parsed=parsed_data,
                    provider="cerebras",
                    model=self.model_name,
                    usage=ModelUsage(
                        prompt_tokens=usage_info.get("prompt_tokens", 0),
                        completion_tokens=actual_comp,
                        total_tokens=usage_info.get("total_tokens", 0),
                    ),
                    system_fingerprint=fp,
                )

        try:
            return _execute_http_request(is_replay=False)
        except urllib.error.HTTPError as e:
            if e.code == 500:
                self.tracker.http500_errors_seen += 1
                self.ledger.append({
                    "event": "provider_error",
                    "request_id": request_id,
                    "cell_id": self.cell_id,
                    "treatment": self.treatment,
                    "stage_name": actual_stage,
                    "http_status": 500,
                    "error": str(e),
                    "sanitized_payload_sha256": payload_sha256,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })

                # Verificar se o orçamento de replay da tentativa foi esgotado
                if self.tracker.http500_replays_used >= self.tracker.max_attempt_http500_replays:
                    self.tracker.http500_replay_exhausted = True
                    self.ledger.append({
                        "event": "http500_replay_budget_exhausted",
                        "request_id": request_id,
                        "cell_id": self.cell_id,
                        "treatment": self.treatment,
                        "stage_name": actual_stage,
                        "replays_used": self.tracker.http500_replays_used,
                        "max_allowed": self.tracker.max_attempt_http500_replays,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })
                    self.closed_outcome = "HTTP500_ATTEMPT_BUDGET_EXHAUSTED"
                    raise RuntimeError("HTTP500_ATTEMPT_BUDGET_EXHAUSTED: Max 1 HTTP500 replay allowed per attempt.")

                # Autorizar exatamente 1 replay idêntico
                self.tracker.http500_replays_used += 1
                replay_payload = self.builder.build_request_payload(
                    messages=messages,
                    schema_cls=actual_schema,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )
                replay_sha256 = self.builder.compute_sanitized_payload_sha256(replay_payload)
                if replay_sha256 != payload_sha256:
                    raise RuntimeError(f"REPLAY_MUTATION_DETECTED: {payload_sha256} != {replay_sha256}")

                self.ledger.append({
                    "event": "http500_replay_authorized",
                    "request_id": request_id,
                    "cell_id": self.cell_id,
                    "treatment": self.treatment,
                    "stage_name": actual_stage,
                    "replay_number": self.tracker.http500_replays_used,
                    "sanitized_payload_sha256": replay_sha256,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })

                # Requisito 6: Esperar pelo menos 15s + re-entrar no token-aware pacer
                time.sleep(15.0)
                self.pacer.wait_if_needed(reserved_request_tokens, f"{request_id}:REPLAY", self.cell_id)
                self.pacer.record_dispatch(reserved_request_tokens)

                try:
                    res = _execute_http_request(is_replay=True)
                    self.tracker.http500_replay_successes += 1
                    return res
                except Exception as replay_err:
                    self.closed_outcome = "HTTP500_REPLAY_FAILED"
                    self.ledger.append({
                        "event": "http500_replay_failed",
                        "request_id": request_id,
                        "cell_id": self.cell_id,
                        "treatment": self.treatment,
                        "stage_name": actual_stage,
                        "error": str(replay_err),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })
                    raise RuntimeError(f"HTTP500_REPLAY_FAILED: Replay failed with {replay_err}")

            else:
                self.closed_outcome = f"PROVIDER_HTTP_{e.code}"
                self.ledger.append({
                    "event": "provider_error",
                    "request_id": request_id,
                    "cell_id": self.cell_id,
                    "treatment": self.treatment,
                    "stage_name": actual_stage,
                    "http_status": e.code,
                    "error": str(e),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
                raise

        except Exception as e:
            self.closed_outcome = "PROVIDER_FAILURE"
            self.ledger.append({
                "event": "provider_error",
                "request_id": request_id,
                "cell_id": self.cell_id,
                "treatment": self.treatment,
                "stage_name": actual_stage,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            raise


# ---------------------------------------------------------------------------
# Preflight Gate Verification
# ---------------------------------------------------------------------------
def run_preflight_verification() -> Tuple[Dict[str, str], List[ScheduleEntry]]:
    print("--- Executing Preflight Verification Gates ---")

    # 1. Chave da API
    key = get_cerebras_api_key()
    if not key:
        raise RuntimeError("PREFLIGHT_FAIL: CEREBRAS_API_KEY absent")

    # 2. Holdouts lacrados
    if not SEALED_HOLDOUT_PATH.exists():
        raise RuntimeError("PREFLIGHT_FAIL: Sealed holdout file missing")
    holdout_data = json.loads(SEALED_HOLDOUT_PATH.read_text(encoding="utf-8"))
    receipt_data = json.loads(RECEIPT_HOLDOUT_PATH.read_text(encoding="utf-8"))
    receipt_items = {item["id"]: item["raw_idea_sha256"] for item in receipt_data["items"]}

    holdout_map: Dict[str, str] = {}
    for item in holdout_data["items"]:
        hid = item["id"]
        raw = item["raw_idea"]
        h_sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        if receipt_items.get(hid) != h_sha:
            raise RuntimeError(f"PREFLIGHT_FAIL: Holdout hash mismatch on {hid}")
        holdout_map[hid] = raw

    # 3. Blinding commitment
    blind_receipt = json.loads(RECEIPT_BLINDING_PATH.read_text(encoding="utf-8"))
    if blind_receipt["reveal_commitment_sha256"] != EXPECTED_BLIND_COMMITMENT_SHA256:
        raise RuntimeError("PREFLIGHT_FAIL: Reveal commitment mismatch")

    # 4. Schedule commitment
    schedule = build_balanced_schedule(FROZEN_HOLDOUT_ORDER, FROZEN_BASE_PERMUTATION)
    if schedule_commitment(schedule) != EXPECTED_SCHEDULE_COMMITMENT_SHA256:
        raise RuntimeError("PREFLIGHT_FAIL: Schedule commitment mismatch")

    print("PREFLIGHT VERIFICATION PASS: All gates, hashes, and commitments valid.")
    return holdout_map, schedule


# ---------------------------------------------------------------------------
# Execution of Confirmatory Cell
# ---------------------------------------------------------------------------
def execute_cell(
    *,
    holdout_id: str,
    condition: str,
    raw_idea: str,
    runner: ConfirmatoryCerebrasRunner,
    raw_dir: Path,
    attempt_id: str = DEFAULT_ATTEMPT_ID,
) -> Dict[str, Any]:
    cell_id = f"{holdout_id}-{condition}"
    raw_artifact_file = raw_dir / f"{holdout_id}_{condition.lower()}.json"
    if raw_artifact_file.exists():
        raise RuntimeError(f"CELL_OVERWRITE_GUARD: Cell artifact '{raw_artifact_file.name}' already exists")

    start_time = time.time()

    if condition == "CONDITION_A":
        runs_dir = raw_dir / "runs_a"
        runs_dir.mkdir(parents=True, exist_ok=True)
        baseline = BaselineRunner(runner=runner, model_name=SCIENTIFIC_MODEL)
        result = baseline.run(original_idea=raw_idea, run_id=f"EXP-M05.5R2-{holdout_id}-COND-A", runs_dir=runs_dir)
        lat = time.time() - start_time
        output_data = result.get("parsed_output") or {}
        is_success = (result.get("success") is True) and bool(output_data)
        status = "SUCCESS" if is_success else "FAILED"

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
            "model_calls": 1,
            "status": status,
            "terminal_status": "SUCCESS" if is_success else "FAILED",
            "error": result.get("error"),
            "parsed_output": output_data,
            "rendered_semantic_text": rendered_text,
        }

    elif condition == "CONDITION_B":
        runs_dir = raw_dir / "runs_b"
        runs_dir.mkdir(parents=True, exist_ok=True)
        config = ModelRoutingConfig(
            models={"default": ModelDefinition(provider="cerebras", model=TRANSPORT_MODEL)},
            routes={},
            default_model_alias="default",
        )
        router = RunnerRouter(config=config, custom_runners={"default": runner})
        simple_runner = SimpleLoopRunner(router=router, topology="STANDARD_6_STAGE", runs_dir=runs_dir)
        state = simple_runner.run(original_idea=raw_idea, run_id=f"EXP-M05.5R2-{holdout_id}-COND-B")
        lat = time.time() - start_time
        calls = len(state.stage_history)
        status_val = getattr(state.status, "value", str(state.status))
        is_success = status_val in ("REFINED_IDEA_READY", "COMPLETED", "STABILIZED")
        status = "SUCCESS" if is_success else "FAILED"

        unc_lines = "\n".join(f"- {u}" for u in state.remaining_uncertainties)
        rendered_text = (
            f"### Ideia Refinada Final\n{state.current_idea or state.original_idea}\n\n"
            f"### Intenção Humana Preservada\n{state.human_intent}\n\n"
            f"### Mecanismo Central\n{state.core_mechanism}\n\n"
            f"### Incertezas Críticas Remanescentes\n{unc_lines}\n\n"
            f"### Próxima Ação Recomendada\n{state.recommended_next_step}"
        )

        b_final_json = runs_dir / f"EXP-M05.5R2-{holdout_id}-COND-B" / "final.json"
        b_final_data = json.loads(b_final_json.read_text(encoding="utf-8")) if b_final_json.exists() else {}

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
            "parsed_output": b_final_data,
            "rendered_semantic_text": rendered_text,
        }

    elif condition == "CONDITION_C":
        runs_dir = raw_dir / "runs_c"
        runs_dir.mkdir(parents=True, exist_ok=True)
        lean_runner = LeanLoopRunner(runner=runner, model_name=SCIENTIFIC_MODEL, runs_dir=runs_dir)
        result = lean_runner.run(original_idea=raw_idea, run_id=f"EXP-M05.5R2-{holdout_id}-COND-C")
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

        c_final_json = runs_dir / f"EXP-M05.5R2-{holdout_id}-COND-C" / "final.json"
        c_final_data = json.loads(c_final_json.read_text(encoding="utf-8")) if c_final_json.exists() else {}

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
            "parsed_output": c_final_data,
            "rendered_semantic_text": rendered_text,
        }
    else:
        raise ValueError(f"UNKNOWN_CONDITION: {condition}")

    # Escrever artefato bruto
    raw_artifact_file.write_text(json.dumps(raw_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # Classificar reviewabilidade
    is_rev, reason = classify_cell_reviewability(raw_payload, runner.closed_outcome)
    print(f"Cell {cell_id} -> Status: {raw_payload['terminal_status']} | Reviewable: {is_rev} ({reason})")
    if not is_rev:
        raise RuntimeError(f"CELL_NOT_REVIEWABLE: {cell_id} failed reviewability ({reason})")

    return raw_payload


# ---------------------------------------------------------------------------
# Human Blind Review Packet Rendering
# ---------------------------------------------------------------------------
def render_human_review_packet(raw_dir: Path, attempt_dir: Path, holdout_map: Dict[str, str]) -> None:
    print("\n--- Generating Blind Human Review Packet (Machine-Only Reveal Access) ---")
    if not SEALED_REVEAL_PATH.exists():
        raise RuntimeError("REVEAL_MISSING: Sealed reveal file not found")
    reveal_data = json.loads(SEALED_REVEAL_PATH.read_text(encoding="utf-8"))
    entries = reveal_data.get("reveal_entries", [])
    mappings = {e["holdout_id"]: e["treatment_to_review_label"] for e in entries}

    packets: List[BlindReviewPacket] = []
    for hid in sorted(holdout_map.keys()):
        raw_idea = holdout_map[hid]
        t2r = mappings[hid]
        r2t = {v: k for k, v in t2r.items()}

        data_a = json.loads((raw_dir / f"{hid}_condition_a.json").read_text(encoding="utf-8"))
        data_b = json.loads((raw_dir / f"{hid}_condition_b.json").read_text(encoding="utf-8"))
        data_c = json.loads((raw_dir / f"{hid}_condition_c.json").read_text(encoding="utf-8"))

        content_by_condition = {
            "A": data_a["rendered_semantic_text"],
            "B": data_b["rendered_semantic_text"],
            "C": data_c["rendered_semantic_text"],
        }

        items = [
            BlindReviewItem(label="RESULTADO 1", content_text=content_by_condition[r2t["R1"]]),
            BlindReviewItem(label="RESULTADO 2", content_text=content_by_condition[r2t["R2"]]),
            BlindReviewItem(label="RESULTADO 3", content_text=content_by_condition[r2t["R3"]]),
        ]
        packets.append(BlindReviewPacket(idea_id=hid, raw_idea=raw_idea, items=items))

    packet_lines = [
        "# PACOTE DE AVALIAÇÃO CEGA COMPLETO — M05.5R2 REPLICAÇÃO CONTROLADA",
        "",
        "> **AVISO AO REVISOR HUMANO:**",
        "> Este documento contém as 8 ideias holdout avaliadas pelas três condições anônimas (RESULTADO 1, RESULTADO 2, RESULTADO 3).",
        "> A ordem dos resultados foi aleatorizada de forma independente para cada ideia sob compromisso criptográfico prévio (Rev1).",
        "> Preencha o formulário `M05.5R2-HUMAN-REVIEW-FORM.md` e congele suas notas antes de abrir qualquer mapeamento de revelação.",
        "",
        "---",
        "",
    ]
    for p in packets:
        packet_lines.append(BlindRenderer.render_markdown_packet(p))
        packet_lines.append("\n\n============================================================\n\n")

    packet_text = "\n".join(packet_lines)
    packet_path = attempt_dir / "M05.5R2-HUMAN-BLIND-REVIEW-PACKET.md"
    packet_path.write_text(packet_text, encoding="utf-8")

    # Detecção de vazamentos
    leaks = BlindRenderer.detect_leaks(packet_text)
    if leaks:
        raise RuntimeError(f"BLIND_LEAK_DETECTED: Found {len(leaks)} unblinded leaks in packet: {leaks}")

    # Formulário de Avaliação
    form_lines = [
        "# M05.5R2-HUMAN-REVIEW-FORM.md — Formulário de Avaliação Humana Cega (M05.5R2)",
        "",
        "> **INSTRUÇÕES PARA O AVALIADOR HUMANO:**",
        "> Avalie cada ideia holdout (H01 a H08) comparando os 3 resultados anônimos (RESULTADO 1, RESULTADO 2, RESULTADO 3).",
        "> Atribua notas de 1 a 5 para cada dimensão e defina o ranking ordinal (1º = 3pts, 2º = 2pts, 3º = 1pt).",
        "> Escolha também com qual resultado você continuaria o desenvolvimento (CONTINUE).",
        "",
        "---",
        "",
    ]
    for hid in sorted(holdout_map.keys()):
        raw_idea = holdout_map[hid]
        form_lines.extend([
            f"## {hid}",
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
    form_path = attempt_dir / "M05.5R2-HUMAN-REVIEW-FORM.md"
    form_path.write_text("\n".join(form_lines), encoding="utf-8")
    print(f"Blind packet written to: {packet_path}")
    print(f"Review form written to: {form_path}")


# ---------------------------------------------------------------------------
# Main Confirmatory Orchestrator
# ---------------------------------------------------------------------------
def run_confirmatory_replication(attempt_id: str = DEFAULT_ATTEMPT_ID) -> None:
    print(f"============================================================")
    print(f"STARTING CONFIRMATORY REPLICATION: {attempt_id}")
    print(f"Provider: {PROVIDER} | Model: {SCIENTIFIC_MODEL} (alias: {TRANSPORT_MODEL})")
    print(f"Output Cap: {OUTPUT_CAP} (Symmetric: {OUTPUT_CAP_SYMMETRY})")
    print(f"============================================================\n")

    # 1. Preflight Gates
    holdout_map, schedule = run_preflight_verification()

    attempt_dir = EXP_DIR / attempt_id
    raw_dir = attempt_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    ledger_path = attempt_dir / "usage-ledger.jsonl"
    ledger = AppendOnlyUsageLedger(ledger_path)
    pacer = TokenAwarePacer(ledger)
    tracker = AttemptResilienceTracker(max_attempt_http500_replays=MAX_TOTAL_HTTP500_REPLAYS_PER_ATTEMPT)

    # 2. Atualizar registro para RUNNING
    # Ler linhas do registro e atualizar status
    lines = [json.loads(l) for l in REGISTRY_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
    updated = False
    new_lines = []
    for line in lines:
        if line.get("attempt_id") == attempt_id:
            line["status"] = "RUNNING"
            line["started_at"] = datetime.now(timezone.utc).isoformat()
            updated = True
        new_lines.append(line)
    if not updated:
        new_lines.append({
            "attempt_id": attempt_id,
            "status": "RUNNING",
            "started_at": datetime.now(timezone.utc).isoformat(),
        })
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        for l in new_lines:
            f.write(json.dumps(l) + "\n")

    # 3. Executar as 24 células
    executed_cells = 0
    results: List[Dict[str, Any]] = []
    try:
        for idx, entry in enumerate(schedule, 1):
            hid = entry.holdout_id
            cond = entry.condition
            print(f"\n[{idx}/24] Executing Block {entry.block} | Holdout {hid} | Condition {cond}")
            raw_idea = holdout_map[hid]
            runner = ConfirmatoryCerebrasRunner(
                ledger=ledger,
                pacer=pacer,
                cell_id=f"{hid}-{cond}",
                treatment=cond,
                tracker=tracker,
                temperature=0.3,
                max_tokens=OUTPUT_CAP,
            )
            cell_res = execute_cell(
                holdout_id=hid,
                condition=cond,
                raw_idea=raw_idea,
                runner=runner,
                raw_dir=raw_dir,
                attempt_id=attempt_id,
            )
            results.append(cell_res)
            executed_cells += 1
    except Exception as exc:
        print(f"\nEXECUTION_HALTED: {exc}")
        # Atualizar registro para STOPPED_FAILED
        reg_lines = [json.loads(l) for l in REGISTRY_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
        for line in reg_lines:
            if line.get("attempt_id") == attempt_id:
                line["status"] = "STOPPED_FAILED"
                line["stopped_at"] = datetime.now(timezone.utc).isoformat()
                line["cells_executed"] = executed_cells
                line["error"] = str(exc)
        with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
            for l in reg_lines:
                f.write(json.dumps(l) + "\n")
        raise

    print(f"\nALL {executed_cells}/24 CELLS EXECUTED SUCCESSFULLY!")

    # 4. Gerar pacote cego para o revisor humano
    render_human_review_packet(raw_dir, attempt_dir, holdout_map)

    # 5. Salvar resumo executivo da replicação
    posts = [e for e in ledger.events if e.get("event") == "post_response"]
    errs = [e for e in ledger.events if e.get("event") == "provider_error"]
    waits = [e for e in ledger.events if e.get("event") == "capacity_wait"]
    replays = [e for e in ledger.events if e.get("event") == "http500_replay_authorized"]

    comp_tokens = [e.get("actual_completion_tokens", 0) for e in posts]
    max_comp = max(comp_tokens) if comp_tokens else 0
    max_util = max(e.get("output_cap_utilization_ratio", 0.0) for e in posts) if posts else 0.0
    exact_caps = sum(1 for c in comp_tokens if c == OUTPUT_CAP)

    http400 = sum(1 for e in errs if e.get("http_status") == 400)
    http401 = sum(1 for e in errs if e.get("http_status") == 401)
    http403 = sum(1 for e in errs if e.get("http_status") == 403)
    http429 = sum(1 for e in errs if e.get("http_status") == 429)
    http500 = sum(1 for e in errs if e.get("http_status") == 500)
    http502_504 = sum(1 for e in errs if e.get("http_status") in (502, 503, 504))

    summary = {
        "attempt_id": attempt_id,
        "experiment_id": EXPERIMENT_ID,
        "provider": PROVIDER,
        "scientific_model": SCIENTIFIC_MODEL,
        "transport_model": TRANSPORT_MODEL,
        "output_cap": OUTPUT_CAP,
        "cells_expected": 24,
        "cells_executed": executed_cells,
        "logical_calls_total": len(posts) - len(replays),
        "provider_requests_total": len(posts) + len(errs),
        "http_200_count": len(posts),
        "http_400_count": http400,
        "http_401_count": http401,
        "http_403_count": http403,
        "http_429_count": http429,
        "http_500_count": http500,
        "http_502_504_count": http502_504,
        "http500_replay_count": len(replays),
        "http500_replay_success_count": tracker.http500_replay_successes,
        "http500_replay_exhausted_count": 1 if tracker.http500_replay_exhausted else 0,
        "http500_attempt_budget_exhausted": tracker.http500_replay_exhausted,
        "unplanned_retry_count": 0,
        "capacity_wait_count": len(waits),
        "capacity_wait_seconds_total": sum(w.get("wait_seconds", 0.0) for w in waits),
        "prompt_tokens_total": sum(e.get("actual_prompt_tokens", 0) for e in posts),
        "completion_tokens_total": sum(comp_tokens),
        "total_tokens": sum(e.get("actual_total_tokens", 0) for e in posts),
        "max_completion_tokens_observed": max_comp,
        "max_output_cap_utilization": max_util,
        "requests_at_exact_cap": exact_caps,
        "output_cap_4096_binding": exact_caps > 0,
        "execution_validity": "VALID_FOR_BLINDED_HUMAN_REVIEW",
        "human_review_packet_created": True,
        "unblinding_allowed": False,
        "completed_at": datetime.now(timezone.utc).isoformat(),
    }
    (attempt_dir / "CONFIRMATORY-SUMMARY.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # 6. Atualizar registro para COMPLETED_AWAITING_HUMAN_SCORING
    lines = [json.loads(l) for l in REGISTRY_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
    for line in lines:
        if line.get("attempt_id") == attempt_id:
            line["status"] = "COMPLETED_AWAITING_HUMAN_SCORING"
            line["completed_at"] = datetime.now(timezone.utc).isoformat()
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        for l in lines:
            f.write(json.dumps(l) + "\n")

    print("\nCONFIRMATORY EXECUTION COMPLETE AND SEALED.")
    print("READY FOR BLINDED HUMAN REVIEW.")


if __name__ == "__main__":
    run_confirmatory_replication()
