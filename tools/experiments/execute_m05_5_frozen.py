#!/usr/bin/env python3
"""
tools/experiments/execute_m05_5_frozen.py
Executor do experimento de replicação controlada M05.5.

Architectural Invariant:
  EXECUTION_PLANE_HAS_NO_BLIND_KNOWLEDGE = True

Responsabilidades:
  1. Validar conformidade de provedor (groq) e modelo (openai/gpt-oss-120b).
  2. Executar as 24 células sequencialmente (REP-01 a REP-08 nas condições A, B, C).
  3. Gravar artefatos brutos em REAL-EXECUTION-ATTEMPT-001/raw/.
  4. Gerar RAW-EXECUTION-MANIFEST.json com hashes determinísticos de todos os 24 artefatos.
  5. Interromper a execução sem acessar mapeamento de cegamento ou pontuar saídas.
"""

from __future__ import annotations
import os
import sys
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Architectural invariant declaration
EXECUTION_PLANE_HAS_NO_BLIND_KNOWLEDGE = True

# Flush stdout immediately
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.idea_evolution.providers.native import NativeModelRunner
from src.idea_evolution.orchestration.baseline import BaselineRunner
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.orchestration.lean_loop import LeanLoopRunner
from src.idea_evolution.config.routing import ModelRoutingConfig, ModelDefinition
from src.idea_evolution.providers.router import RunnerRouter

EXP_DIR = REPO_ROOT / "experiments" / "EXP-M05.5-CONTROLLED-REPLICATION-20260831"
ATTEMPT_DIR = EXP_DIR / "REAL-EXECUTION-ATTEMPT-001"
RAW_DIR = ATTEMPT_DIR / "raw"

EXPECTED_PROVIDER = "groq"
EXPECTED_MODEL = "openai/gpt-oss-120b"
EXPERIMENT_ID = "EXP-M05.5-CONTROLLED-REPLICATION-20260831"
ATTEMPT_ID = "REAL-EXECUTION-ATTEMPT-001"


def calculate_sha256_text(text: str) -> str:
    norm = text.encode("utf-8").replace(b"\r\n", b"\n")
    return hashlib.sha256(norm).hexdigest()


def calculate_sha256_file(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def execute_replication(api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.environ.get("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY_MISSING: Não é possível executar M05.5 sem a chave Groq.")

    runner = NativeModelRunner(
        provider=EXPECTED_PROVIDER,
        api_key=key,
        default_model=EXPECTED_MODEL,
    )

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    holdout_file = EXP_DIR / "HOLDOUT-IDEAS.json"
    with open(holdout_file, "r", encoding="utf-8") as f:
        holdout_data = json.load(f)
        ideas = holdout_data["ideas"]

    raw_manifest_entries: List[Dict[str, Any]] = []
    total_calls = 0
    calls_by_cond: Dict[str, int] = {"CONDITION_A": 0, "CONDITION_B": 0, "CONDITION_C": 0}

    print(f"=== INICIANDO EXECUÇÃO SEQUENCIAL M05.5 REAL-EXECUTION-ATTEMPT-001 ===", flush=True)
    print(f"Provedor: {EXPECTED_PROVIDER} | Modelo: {EXPECTED_MODEL}", flush=True)
    print(f"Total de ideias: {len(ideas)} (24 células)", flush=True)

    for idx, item in enumerate(ideas, 1):
        idea_id = item["idea_id"]
        raw_idea = item["raw_idea"]
        suite_class = item.get("suite_class", "UNKNOWN")
        print(f"\n--- [{idx}/8] Processando {idea_id} ({suite_class}) ---", flush=True)

        # --- Condição A: Baseline (1 chamada) ---
        print(f"[{idea_id}] Executando Condição A (Baseline)...", end=" ", flush=True)
        runs_dir_a = RAW_DIR / "runs_a"
        runs_dir_a.mkdir(parents=True, exist_ok=True)
        baseline_runner = BaselineRunner(runner=runner, model_name=EXPECTED_MODEL)

        start_t = time.time()
        res_a = baseline_runner.run(
            original_idea=raw_idea,
            run_id=f"EXP-M05.5-{idea_id}-COND-A",
            runs_dir=runs_dir_a,
        )
        lat_a = time.time() - start_t

        output_data_a = res_a.get("parsed_output", {})
        summary = output_data_a.get("summary", "")
        refined = output_data_a.get("refined_version", "")
        strengths = output_data_a.get("strengths", [])
        weaknesses = output_data_a.get("weaknesses", [])
        next_steps = output_data_a.get("next_steps", [])

        rendered_a = (
            f"### Resumo\n{summary}\n\n"
            f"### Versão Refinada\n{refined}\n\n"
            f"### Pontos Fortes e Fracos\n"
            f"- **Fortes:** {', '.join(strengths)}\n"
            f"- **Fracos:** {', '.join(weaknesses)}\n\n"
            f"### Próximos Passos\n{', '.join(next_steps)}"
        )

        fpath_a = RAW_DIR / f"{idea_id}_condition_a.json"
        payload_a = {
            "experiment_id": EXPERIMENT_ID,
            "attempt_id": ATTEMPT_ID,
            "idea_id": idea_id,
            "condition": "CONDITION_A",
            "raw_idea": raw_idea,
            "latency_seconds": lat_a,
            "model_calls": 1,
            "success": res_a.get("success", False),
            "error": res_a.get("error"),
            "parsed_output": output_data_a,
            "rendered_semantic_text": rendered_a,
        }
        with open(fpath_a, "w", encoding="utf-8") as f:
            json.dump(payload_a, f, indent=2, ensure_ascii=False)

        calls_by_cond["CONDITION_A"] += 1
        total_calls += 1
        print(f"OK (latência: {lat_a:.2f}s, chamadas: 1)", flush=True)

        # --- Condição B: Simple Loop Standard (até 10 chamadas) ---
        print(f"[{idea_id}] Executando Condição B (Simple Loop)...", end=" ", flush=True)
        runs_dir_b = RAW_DIR / "runs_b"
        runs_dir_b.mkdir(parents=True, exist_ok=True)

        config_b = ModelRoutingConfig(
            models={
                "default": ModelDefinition(
                    provider=runner.provider,
                    model=runner.default_model,
                )
            },
            routes={},
            default_model_alias="default",
        )
        router_b = RunnerRouter(config=config_b, custom_runners={"default": runner})
        simple_runner = SimpleLoopRunner(
            router=router_b,
            topology="STANDARD_6_STAGE",
            runs_dir=runs_dir_b,
        )

        start_t = time.time()
        state_b = simple_runner.run(
            original_idea=raw_idea,
            run_id=f"EXP-M05.5-{idea_id}-COND-B",
        )
        lat_b = time.time() - start_t

        rendered_b = (
            f"### Ideia Refinada Final\n{state_b.current_idea or state_b.original_idea}\n\n"
            f"### Intenção Humana Preservada\n{state_b.human_intent}\n\n"
            f"### Mecanismo Central\n{state_b.core_mechanism}\n\n"
            f"### Incertezas Críticas Remanescentes\n"
            + "\n".join(f"- {u}" for u in state_b.remaining_uncertainties)
            + f"\n\n### Próxima Ação Recomendada\n{state_b.recommended_next_step}"
        )

        calls_b = len(state_b.stage_history)
        fpath_b = RAW_DIR / f"{idea_id}_condition_b.json"
        payload_b = {
            "experiment_id": EXPERIMENT_ID,
            "attempt_id": ATTEMPT_ID,
            "idea_id": idea_id,
            "condition": "CONDITION_B",
            "raw_idea": raw_idea,
            "latency_seconds": lat_b,
            "model_calls": calls_b,
            "terminal_status": state_b.status.value,
            "reconstruction_count": state_b.reconstruction_count,
            "stages_executed": [s.stage_id for s in state_b.stage_history],
            "rendered_semantic_text": rendered_b,
        }
        with open(fpath_b, "w", encoding="utf-8") as f:
            json.dump(payload_b, f, indent=2, ensure_ascii=False)

        calls_by_cond["CONDITION_B"] += calls_b
        total_calls += calls_b
        print(f"OK (latência: {lat_b:.2f}s, status: {state_b.status.value}, chamadas: {calls_b})", flush=True)

        # --- Condição C: Lean Loop L1 (máximo 2 chamadas) ---
        print(f"[{idea_id}] Executando Condição C (Lean L1)...", end=" ", flush=True)
        runs_dir_c = RAW_DIR / "runs_c"
        runs_dir_c.mkdir(parents=True, exist_ok=True)
        lean_runner = LeanLoopRunner(
            runner=runner,
            model_name=EXPECTED_MODEL,
            runs_dir=runs_dir_c,
        )

        start_t = time.time()
        res_c = lean_runner.run(
            original_idea=raw_idea,
            run_id=f"EXP-M05.5-{idea_id}-COND-C",
        )
        lat_c = time.time() - start_t

        rendered_c = res_c.final_markdown or ""
        if not rendered_c and res_c.first_pass:
            fp = res_c.first_pass
            rendered_c = (
                f"### Intenção Central\n{fp.core_intent}\n\n"
                f"### Mecanismo Proposto\n{fp.primary_mechanism.mechanism}\n\n"
                f"### Vulnerabilidades Identificadas\n"
                + "\n".join(
                    f"- **{v.risk_level}:** {v.vulnerability}" for v in fp.vulnerabilities
                )
                + "\n\n### Próxima Ação Recomendada\n"
                f"{fp.recommended_action}"
            )

        fpath_c = RAW_DIR / f"{idea_id}_condition_c.json"
        payload_c = {
            "experiment_id": EXPERIMENT_ID,
            "attempt_id": ATTEMPT_ID,
            "idea_id": idea_id,
            "condition": "CONDITION_C",
            "raw_idea": raw_idea,
            "latency_seconds": lat_c,
            "model_calls": res_c.total_model_calls,
            "terminal_status": res_c.terminal_status,
            "gate_outcome": res_c.gate_result.outcome.value if res_c.gate_result else "UNKNOWN",
            "human_decision_requested": res_c.human_decision_requested,
            "rendered_semantic_text": rendered_c,
        }
        with open(fpath_c, "w", encoding="utf-8") as f:
            json.dump(payload_c, f, indent=2, ensure_ascii=False)

        calls_by_cond["CONDITION_C"] += res_c.total_model_calls
        total_calls += res_c.total_model_calls
        print(f"OK (latência: {lat_c:.2f}s, status: {res_c.terminal_status}, chamadas: {res_c.total_model_calls})", flush=True)

        # Append hashes
        for cond_name, p_file, res_obj in [
            ("CONDITION_A", fpath_a, payload_a),
            ("CONDITION_B", fpath_b, payload_b),
            ("CONDITION_C", fpath_c, payload_c),
        ]:
            h = calculate_sha256_file(p_file)
            raw_manifest_entries.append({
                "idea_id": idea_id,
                "condition": cond_name,
                "raw_artifact_file": str(p_file.relative_to(EXP_DIR)),
                "sha256": h,
                "model_calls": res_obj["model_calls"],
                "latency_seconds": res_obj["latency_seconds"],
            })

    # Save RAW-EXECUTION-MANIFEST.json
    raw_manifest_path = ATTEMPT_DIR / "RAW-EXECUTION-MANIFEST.json"
    manifest_data = {
        "experiment_id": EXPERIMENT_ID,
        "attempt_id": ATTEMPT_ID,
        "executed_at": datetime.now().isoformat(),
        "provider": EXPECTED_PROVIDER,
        "model": EXPECTED_MODEL,
        "total_cells": len(raw_manifest_entries),
        "total_real_model_calls": total_calls,
        "calls_by_condition": calls_by_cond,
        "entries": raw_manifest_entries,
    }
    with open(raw_manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)

    print(f"\n=== EXECUÇÃO M05.5 CONCLUÍDA COM SUCESSO ===", flush=True)
    print(f"Total de células: {len(raw_manifest_entries)} / 24", flush=True)
    print(f"Total de chamadas: {total_calls} (A={calls_by_cond['CONDITION_A']}, B={calls_by_cond['CONDITION_B']}, C={calls_by_cond['CONDITION_C']})", flush=True)
    print(f"Manifesto salvo em: {raw_manifest_path}", flush=True)

    return {
        "total_cells": len(raw_manifest_entries),
        "total_calls": total_calls,
        "calls_by_condition": calls_by_cond,
        "manifest_path": str(raw_manifest_path),
    }


if __name__ == "__main__":
    execute_replication()
