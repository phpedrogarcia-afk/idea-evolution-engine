"""
tools/experiments/execute_m05_5r2_cerebras_sacrificial_pilot.py
Executor do Piloto Sacrificial Delimitado M05.5R2 para Cerebras Cloud Free.

Invariantes estritas:
1. Fonte sacrificial única: IDEA-08 (M05.4 Attempt-004) com hash verificado.
2. Ordem de execução sacrificial: C -> B -> A.
3. Concorrência: 1.
4. Custo estrito: ZERO (bloqueia qualquer rota fora de https://api.cerebras.ai/v1).
5. Modelo: gpt-oss-120b (alias de transporte para openai/gpt-oss-120b).
6. Temperatura: 0.3, Max completion tokens: 2048.
7. Ledger append-only com encadeamento SHA-256.
8. Sem retries ocultos: max_retries = 0 (1 disparo lógico = 1 request).
9. Pacing conservador: 12.5s entre chamadas (respeita teto de 5 RPM da camada gratuita).
10. Sanitização completa de credenciais (CEREBRAS_API_KEY).
"""

from __future__ import annotations

import os
import sys
import json
import time
import hashlib
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple, Type, TypeVar

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pydantic import BaseModel, ValidationError
from src.idea_evolution.providers.base import ModelResponse, ModelRunner, ModelUsage
from src.idea_evolution.providers.cerebras import (
    CerebrasTransportBuilder,
    CEREBRAS_HOSTED_BASE_URL,
    CEREBRAS_TRANSPORT_MODEL_ID,
    SCIENTIFIC_MODEL_ID,
    EXPECTED_INFERENCE_PRICE,
    sanitize_cerebras_credential,
    is_cerebras_key_present,
)
from tools.experiments.m05_5r1_token_envelope import (
    OUTPUT_CAP_TOKENS,
    system_instruction,
)
from tools.experiments.execute_m05_5r1_confirmatory import (
    classify_cell_reviewability,
)

T = TypeVar("T", bound=BaseModel)

EXP_DIR = REPO_ROOT / "experiments" / "EXP-M05.5R2-FREE-PROVIDER-PORTABILITY-REPLICATION"
OUTPUT_CAP_TOKENS = 4096
SACRIFICIAL_ATTEMPT_ID = os.environ.get("SACRIFICIAL_ATTEMPT_ID", "CEREBRAS-FREE-SACRIFICIAL-PILOT-002")
PILOT_DIR = EXP_DIR / SACRIFICIAL_ATTEMPT_ID

SACRIFICIAL_SOURCE_ID = "M05.4-ATTEMPT-004-IDEA-08"
SACRIFICIAL_SOURCE_CONTENT_SHA256 = "90928bd682aae8f6193878091dfb3666edc7a3a2e30b302238642bae2fb131a6"
FROZEN_PILOT_ORDER = ("CONDITION_C", "CONDITION_B", "CONDITION_A")


def load_sacrificial_idea_08() -> str:
    path = (
        REPO_ROOT
        / "experiments"
        / "EXP-M05.4-PROSPECTIVE-RERUN-20260829"
        / "REAL-EXECUTION-ATTEMPT-004"
        / "raw"
        / "runs_b"
        / "EXP-M05.4-IDEA-08-COND-B"
        / "input.json"
    )
    if not path.exists():
        raise RuntimeError(f"SACRIFICIAL_SOURCE_NOT_FOUND: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    idea_text = data.get("original_idea", "")
    h = hashlib.sha256(idea_text.encode("utf-8")).hexdigest()
    if h != SACRIFICIAL_SOURCE_CONTENT_SHA256:
        raise RuntimeError(f"SACRIFICIAL_SOURCE_HASH_MISMATCH: got {h}, expected {SACRIFICIAL_SOURCE_CONTENT_SHA256}")
    return idea_text


class AppendOnlyUsageLedger:
    """Ledger append-only com integridade encadeada por SHA-256."""

    def __init__(self, path: Path):
        self.path = path
        self.events: List[Dict[str, Any]] = []
        if path.exists():
            self._load_and_verify()

    def _load_and_verify(self):
        prev_hash = "GENESIS"
        for line in self.path.read_text(encoding="utf-8").splitlines():
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


class GuardedCerebrasRunner(ModelRunner):
    """
    Executor ModelRunner com guardas estritas de custo, integridade e pacing para Cerebras Cloud.
    """

    def __init__(
        self,
        ledger: AppendOnlyUsageLedger,
        block_id: str,
        treatment: str,
        temperature: float = 0.3,
        max_tokens: int = OUTPUT_CAP_TOKENS,
        min_call_interval_seconds: float = 12.5,  # 5 RPM baseline -> 12.5s entre chamadas
    ):
        self.model_name = SCIENTIFIC_MODEL_ID
        self.temperature = temperature
        self.ledger = ledger
        self.block_id = block_id
        self.treatment = treatment
        self.max_tokens = max_tokens
        self.min_interval = min_call_interval_seconds
        self.last_call_time = 0.0
        self.builder = CerebrasTransportBuilder(
            base_url=CEREBRAS_HOSTED_BASE_URL,
            scientific_model=SCIENTIFIC_MODEL_ID,
            transport_model=CEREBRAS_TRANSPORT_MODEL_ID,
        )
        self.call_number = 0
        self.closed_outcome: Optional[str] = None

    def _dispatch(
        self,
        prompt_text: str,
        output_schema: Optional[Type[BaseModel]],
        stage_name: str,
    ) -> ModelResponse:
        self.call_number += 1
        request_id = f"{self.block_id}:{self.treatment}:{self.call_number}"

        # 1. Validação prévia de custo e destino fail-closed
        if self.builder.base_url != CEREBRAS_HOSTED_BASE_URL:
            self.closed_outcome = "FAIL_CLOSED_PAID_ROUTING_GUARD"
            raise RuntimeError(f"PAID_ROUTING_ATTEMPT_BLOCKED: {self.builder.base_url}")
        if self.builder.transport_model != CEREBRAS_TRANSPORT_MODEL_ID:
            self.closed_outcome = "FAIL_CLOSED_MODEL_GUARD"
            raise RuntimeError(f"MODEL_VIOLATION_BLOCKED: {self.builder.transport_model}")
        if EXPECTED_INFERENCE_PRICE != 0.0:
            self.closed_outcome = "NON_ZERO_PRICE_BLOCKED"
            raise RuntimeError("PRICE_GUARD_BLOCKED: Expected price is non-zero")
        if not is_cerebras_key_present():
            self.closed_outcome = "CEREBRAS_API_KEY_ABSENT"
            raise RuntimeError("CEREBRAS_API_KEY_ABSENT")

        # 2. Pacing de tráfego para manter < 5 RPM
        now = time.time()
        elapsed = now - self.last_call_time
        if elapsed < self.min_interval:
            wait_s = self.min_interval - elapsed
            time.sleep(wait_s)

        # 3. Montar mensagens e payload
        system, _ = system_instruction(stage_name, output_schema) if output_schema else ("", "")
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt_text})

        payload = self.builder.build_request_payload(
            messages=messages,
            schema_cls=output_schema,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        payload_sha = self.builder.compute_sanitized_payload_sha256(payload)

        # 4. Registrar evento pre_dispatch
        self.ledger.append({
            "event": "pre_dispatch",
            "request_id": request_id,
            "block_id": self.block_id,
            "treatment": self.treatment,
            "stage_name": stage_name,
            "scientific_model": SCIENTIFIC_MODEL_ID,
            "transport_model": CEREBRAS_TRANSPORT_MODEL_ID,
            "base_url": CEREBRAS_HOSTED_BASE_URL,
            "sanitized_payload_sha256": payload_sha,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        # 5. Despacho HTTP
        headers = self.builder.build_headers()
        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.builder.base_url}/chat/completions",
            data=req_data,
            headers=headers,
            method="POST",
        )

        start_time = time.time()
        self.last_call_time = start_time

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                self.last_call_time = time.time()
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

                # Registrar sucesso no ledger
                self.ledger.append({
                    "event": "post_response",
                    "request_id": request_id,
                    "block_id": self.block_id,
                    "treatment": self.treatment,
                    "stage_name": stage_name,
                    "http_status": 200,
                    "actual_prompt_tokens": usage_info.get("prompt_tokens", 0),
                    "actual_completion_tokens": actual_comp,
                    "actual_total_tokens": usage_info.get("total_tokens", 0),
                    "configured_output_cap": self.max_tokens,
                    "output_cap_utilization_ratio": cap_util,
                    "finish_reason": finish_reason,
                    "system_fingerprint": fp,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })

                parsed_data = None
                if output_schema:
                    try:
                        parsed_data = output_schema.model_validate_json(content)
                    except ValidationError as ve:
                        self.ledger.append({
                            "event": "validation_error",
                            "request_id": request_id,
                            "error": str(ve),
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        })
                        return ModelResponse(
                            raw_text=content,
                            parsed=None,
                            provider="cerebras",
                            model=self.model_name,
                            usage=ModelUsage(
                                prompt_tokens=usage_info.get("prompt_tokens", 0),
                                completion_tokens=usage_info.get("completion_tokens", 0),
                                total_tokens=usage_info.get("total_tokens", 0),
                            ),
                            error=f"VALIDATION_ERROR: {str(ve)}",
                        )

                return ModelResponse(
                    raw_text=content,
                    parsed=parsed_data,
                    provider="cerebras",
                    model=self.model_name,
                    usage=ModelUsage(
                        prompt_tokens=usage_info.get("prompt_tokens", 0),
                        completion_tokens=usage_info.get("completion_tokens", 0),
                        total_tokens=usage_info.get("total_tokens", 0),
                    ),
                )

        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
            sanitized_body = sanitize_cerebras_credential(err_body)
            self.ledger.append({
                "event": "post_error",
                "request_id": request_id,
                "block_id": self.block_id,
                "treatment": self.treatment,
                "stage_name": stage_name,
                "http_status": e.code,
                "error_reason": sanitize_cerebras_credential(e.reason),
                "error_body": sanitized_body[:512],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            self.closed_outcome = f"HTTP_{e.code}_{sanitize_cerebras_credential(e.reason)}"
            return ModelResponse(
                raw_text="",
                parsed=None,
                provider="cerebras",
                model=self.model_name,
                error=f"HTTP_{e.code}: {sanitized_body[:200]}",
            )
        except Exception as e:
            sanitized_err = sanitize_cerebras_credential(str(e))
            self.ledger.append({
                "event": "post_error",
                "request_id": request_id,
                "block_id": self.block_id,
                "treatment": self.treatment,
                "stage_name": stage_name,
                "http_status": None,
                "error": sanitized_err[:512],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            self.closed_outcome = f"EXCEPTION_{sanitized_err[:50]}"
            return ModelResponse(
                raw_text="",
                parsed=None,
                provider="cerebras",
                model=self.model_name,
                error=f"CEREBRAS_TRANSPORT_ERROR: {sanitized_err}",
            )

    def generate(
        self,
        prompt_text: str,
        output_schema: Optional[Type[T]] = None,
        stage_name: Optional[str] = None,
        model_name: Optional[str] = None,
        max_repairs: int = 1,
        system_prompt: Optional[str] = None,
    ) -> ModelResponse:
        if model_name and model_name not in {SCIENTIFIC_MODEL_ID, CEREBRAS_TRANSPORT_MODEL_ID}:
            return ModelResponse(raw_text="", provider="cerebras", model=SCIENTIFIC_MODEL_ID, error="MODEL_SPEC_VIOLATION")
        return self._dispatch(prompt_text, output_schema, stage_name or "GENERATE")


def run_bounded_sacrificial_pilot() -> Dict[str, Any]:
    """Executa o piloto sacrificial C -> B -> A com IDEA-08 na Cerebras Cloud."""
    if not is_cerebras_key_present():
        raise RuntimeError("CEREBRAS_API_KEY_ABSENT: Chave ausente no ambiente.")

    idea_text = load_sacrificial_idea_08()
    PILOT_DIR.mkdir(parents=True, exist_ok=True)
    raw_dir = PILOT_DIR / "raw"
    raw_dir.mkdir(exist_ok=True)

    ledger_path = PILOT_DIR / "usage-ledger.jsonl"
    ledger = AppendOnlyUsageLedger(ledger_path)

    from src.idea_evolution.config.routing import ModelDefinition, ModelRoutingConfig
    from src.idea_evolution.orchestration.baseline import BaselineRunner
    from src.idea_evolution.orchestration.lean_loop import LeanLoopRunner
    from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
    from src.idea_evolution.providers.router import RunnerRouter

    cell_results: Dict[str, Any] = {}
    reviewability: Dict[str, bool] = {}
    review_reasons: Dict[str, str] = {}

    print(f"STARTING SACRIFICIAL PILOT on Cerebras Cloud Free ({CEREBRAS_TRANSPORT_MODEL_ID} -> {SCIENTIFIC_MODEL_ID})")
    print(f"Sacrificial Idea SHA-256: {SACRIFICIAL_SOURCE_CONTENT_SHA256}")
    print(f"Order: {' -> '.join(FROZEN_PILOT_ORDER)}\n")

    def _save_summary() -> Dict[str, Any]:
        posts = [e for e in ledger.events if e.get("event") == "post_response"]
        errors = [e for e in ledger.events if e.get("event") == "post_error"]
        fps = set(e.get("system_fingerprint") for e in posts if e.get("system_fingerprint"))
        comp_tokens_list = [e.get("actual_completion_tokens", 0) for e in posts]
        max_comp = max(comp_tokens_list) if comp_tokens_list else 0
        cap_utils = [e.get("output_cap_utilization_ratio", 0.0) for e in posts]
        max_util = max(cap_utils) if cap_utils else 0.0
        exact_cap_count = sum(1 for c in comp_tokens_list if c == OUTPUT_CAP_TOKENS)
        binding_cap = exact_cap_count > 0

        s = {
            "attempt_id": SACRIFICIAL_ATTEMPT_ID,
            "sacrificial_source": SACRIFICIAL_SOURCE_ID,
            "sacrificial_source_sha256": SACRIFICIAL_SOURCE_CONTENT_SHA256,
            "provider": "cerebras",
            "scientific_model": SCIENTIFIC_MODEL_ID,
            "transport_model": CEREBRAS_TRANSPORT_MODEL_ID,
            "base_url": CEREBRAS_HOSTED_BASE_URL,
            "expected_inference_price": EXPECTED_INFERENCE_PRICE,
            "output_cap_tokens": OUTPUT_CAP_TOKENS,
            "logical_calls_total": sum(c.get("logical_calls", 0) for c in cell_results.values()),
            "provider_requests_total": len(posts) + len(errors),
            "http_200_count": len(posts),
            "http_400_count": sum(1 for e in errors if e.get("http_status") == 400),
            "http_403_count": sum(1 for e in errors if e.get("http_status") == 403),
            "http_429_count": sum(1 for e in errors if e.get("http_status") == 429),
            "other_error_count": sum(1 for e in errors if e.get("http_status") not in (400, 403, 429)),
            "prompt_tokens_total": sum(e.get("actual_prompt_tokens", 0) for e in posts),
            "completion_tokens_total": sum(e.get("actual_completion_tokens", 0) for e in posts),
            "tokens_total": sum(e.get("actual_total_tokens", 0) for e in posts),
            "max_completion_tokens_observed": max_comp,
            "max_output_cap_utilization": max_util,
            "requests_at_exact_cap": exact_cap_count,
            "output_cap_4096_binding": binding_cap,
            "unique_fingerprints_count": len(fps),
            "condition_c_reviewable": reviewability.get("CONDITION_C", False),
            "condition_b_reviewable": reviewability.get("CONDITION_B", False),
            "condition_a_reviewable": reviewability.get("CONDITION_A", False),
            "all_three_reviewable": all(reviewability.get(k, False) for k in FROZEN_PILOT_ORDER),
        }
        (PILOT_DIR / "PILOT-SUMMARY.json").write_text(json.dumps(s, indent=2), encoding="utf-8")
        return s

    # 1. Executar CONDITION_C (Lean Loop L1)
    print("--- 1. Executing CONDITION_C (Lean Loop L1) ---")
    c_run_dir = raw_dir / "runs_c"
    c_run_dir.mkdir(exist_ok=True)
    runner_c = GuardedCerebrasRunner(ledger, block_id=SACRIFICIAL_ATTEMPT_ID, treatment="CONDITION_C")
    res_c = LeanLoopRunner(runner=runner_c, model_name=SCIENTIFIC_MODEL_ID, runs_dir=c_run_dir).run(
        idea_text, run_id=f"{SACRIFICIAL_ATTEMPT_ID}-C"
    )

    c_final_dir = c_run_dir / f"{SACRIFICIAL_ATTEMPT_ID}-C"
    c_final_md = (c_final_dir / "final.md").read_text(encoding="utf-8") if (c_final_dir / "final.md").exists() else ""
    c_final_data = json.loads((c_final_dir / "final.json").read_text(encoding="utf-8")) if (c_final_dir / "final.json").exists() else {}

    c_cell = {
        "cell_id": f"{SACRIFICIAL_ATTEMPT_ID}-C",
        "condition": "CONDITION_C",
        "status": "FAILED" if res_c.terminal_status.endswith("FAILED") else "SUCCESS",
        "terminal_status": res_c.terminal_status,
        "rendered_semantic_text": c_final_md,
        "parsed_output": c_final_data,
        "logical_calls": res_c.total_model_calls,
    }
    is_rev_c, reason_c = classify_cell_reviewability(c_cell, runner_c.closed_outcome)
    reviewability["CONDITION_C"] = is_rev_c
    review_reasons["CONDITION_C"] = reason_c
    cell_results["CONDITION_C"] = c_cell
    print(f"Condition C -> Terminal: {res_c.terminal_status} | Reviewable: {is_rev_c} ({reason_c})")
    if not is_rev_c:
        _save_summary()
        raise RuntimeError(f"CONDITION_C_NOT_REVIEWABLE: {reason_c}")

    # 2. Executar CONDITION_B (Simple Loop)
    print("\n--- 2. Executing CONDITION_B (Simple Loop) ---")
    b_run_dir = raw_dir / "runs_b"
    b_run_dir.mkdir(exist_ok=True)
    runner_b = GuardedCerebrasRunner(ledger, block_id=SACRIFICIAL_ATTEMPT_ID, treatment="CONDITION_B")
    config_b = ModelRoutingConfig(
        models={"default": ModelDefinition(provider="cerebras", model=CEREBRAS_TRANSPORT_MODEL_ID)},
        routes={},
        default_model_alias="default",
    )
    state_b = SimpleLoopRunner(
        router=RunnerRouter(config=config_b, custom_runners={"default": runner_b}),
        topology="STANDARD_6_STAGE",
        runs_dir=b_run_dir,
    ).run(idea_text, run_id=f"{SACRIFICIAL_ATTEMPT_ID}-B")

    b_final_dir = b_run_dir / f"{SACRIFICIAL_ATTEMPT_ID}-B"
    b_final_md = (b_final_dir / "final.md").read_text(encoding="utf-8") if (b_final_dir / "final.md").exists() else ""
    b_final_data = json.loads((b_final_dir / "final.json").read_text(encoding="utf-8")) if (b_final_dir / "final.json").exists() else {}

    b_term_status = state_b.status.value if hasattr(state_b.status, "value") else str(state_b.status)
    rendered_b = (
        f"### Ideia Refinada Final\n{state_b.current_idea or state_b.original_idea}\n\n"
        f"### Intenção Humana Preservada\n{state_b.human_intent}\n\n"
        f"### Mecanismo Central\n{state_b.core_mechanism}\n\n"
        f"### Incertezas Críticas Remanescentes\n"
        + "\n".join(f"- {u}" for u in state_b.remaining_uncertainties)
        + f"\n\n### Próxima Ação Recomendada\n{state_b.recommended_next_step}"
    )
    b_cell = {
        "cell_id": f"{SACRIFICIAL_ATTEMPT_ID}-B",
        "condition": "CONDITION_B",
        "status": "SUCCESS" if state_b.status.value == "SUCCESS" else "FAILED",
        "terminal_status": b_term_status,
        "stages_executed": [s.stage_id for s in state_b.stage_history],
        "rendered_semantic_text": rendered_b,
        "parsed_output": b_final_data,
        "logical_calls": len(state_b.stage_history),
    }
    is_rev_b, reason_b = classify_cell_reviewability(b_cell, runner_b.closed_outcome)
    reviewability["CONDITION_B"] = is_rev_b
    review_reasons["CONDITION_B"] = reason_b
    cell_results["CONDITION_B"] = b_cell
    print(f"Condition B -> Terminal: {b_term_status} | Reviewable: {is_rev_b} ({reason_b})")
    if not is_rev_b:
        _save_summary()
        raise RuntimeError(f"CONDITION_B_NOT_REVIEWABLE: {reason_b}")

    # 3. Executar CONDITION_A (Baseline)
    print("\n--- 3. Executing CONDITION_A (Baseline) ---")
    a_run_dir = raw_dir / "runs_a"
    a_run_dir.mkdir(exist_ok=True)
    runner_a = GuardedCerebrasRunner(ledger, block_id=SACRIFICIAL_ATTEMPT_ID, treatment="CONDITION_A")
    res_a = BaselineRunner(runner=runner_a, model_name=SCIENTIFIC_MODEL_ID).run(
        idea_text, run_id=f"{SACRIFICIAL_ATTEMPT_ID}-A", runs_dir=a_run_dir
    )

    a_final_dir = a_run_dir / f"{SACRIFICIAL_ATTEMPT_ID}-A"
    a_final_md = (a_final_dir / "final.md").read_text(encoding="utf-8") if (a_final_dir / "final.md").exists() else ""
    a_final_data = json.loads((a_final_dir / "final.json").read_text(encoding="utf-8")) if (a_final_dir / "final.json").exists() else {}

    parsed_a = a_final_data.get("parsed_output", {}) if isinstance(a_final_data, dict) else {}
    strengths_a = parsed_a.get("strengths", []) if isinstance(parsed_a.get("strengths"), list) else []
    weaknesses_a = parsed_a.get("weaknesses", []) if isinstance(parsed_a.get("weaknesses"), list) else []
    next_steps_a = parsed_a.get("next_steps", []) if isinstance(parsed_a.get("next_steps"), list) else []
    rendered_a = (
        f"### Resumo\n{parsed_a.get('summary', '')}\n\n"
        f"### Versão Refinada\n{parsed_a.get('refined_version', '')}\n\n"
        f"### Pontos Fortes e Fracos\n"
        f"- **Fortes:** {', '.join(strengths_a)}\n"
        f"- **Fracos:** {', '.join(weaknesses_a)}\n\n"
        f"### Próximos Passos\n{', '.join(next_steps_a)}"
    )
    a_cell = {
        "cell_id": f"{SACRIFICIAL_ATTEMPT_ID}-A",
        "condition": "CONDITION_A",
        "status": "SUCCESS" if bool(res_a.get("success")) else "FAILED",
        "terminal_status": "SUCCESS" if bool(res_a.get("success")) else "FAILED",
        "rendered_semantic_text": rendered_a,
        "parsed_output": a_final_data,
        "logical_calls": 1,
    }
    is_rev_a, reason_a = classify_cell_reviewability(a_cell, runner_a.closed_outcome)
    reviewability["CONDITION_A"] = is_rev_a
    review_reasons["CONDITION_A"] = reason_a
    cell_results["CONDITION_A"] = a_cell
    print(f"Condition A -> Terminal: SUCCESS | Reviewable: {is_rev_a} ({reason_a})")
    if not is_rev_a:
        _save_summary()
        raise RuntimeError(f"CONDITION_A_NOT_REVIEWABLE: {reason_a}")

    summary = _save_summary()
    print("\nALL 3 CONDITIONS REVIEWABLE: SUCCESS!")
    return summary


if __name__ == "__main__":
    try:
        run_bounded_sacrificial_pilot()
    except Exception as e:
        print(f"\nPILOT EXECUTION STOPPED: {e}")
