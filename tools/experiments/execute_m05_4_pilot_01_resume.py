"""
tools/experiments/execute_m05_4_pilot_01_resume.py
Resume script for M05.4 Treatment-Delivery Pilot 01 after server restart.

STATE AT RESTART:
- CAL-01-CONDITION_A: COMPLETED (DELIVERED) - DO NOT RE-RUN
- CAL-01-CONDITION_B: INTERRUPTED after stage 4 SYNTHESIZE - must restart
- CAL-01-CONDITION_C through CAL-02-CONDITION_C: NOT YET RUN

APPROACH:
- Preserve CAL-01-A result.
- Re-run CAL-01-B with new run_id to avoid stage file collision; mark interrupted partial as INTERRUPTED evidence.
- Continue sequentially through remaining cells.
- Append to existing journal.
- Merge with completed cell from prior run.
"""

from typing import Dict, Any, List, Optional
import os
import sys
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime

from src.idea_evolution.providers.base import ModelRunner
from src.idea_evolution.providers.native import NativeModelRunner
from src.idea_evolution.orchestration.baseline import BaselineRunner
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.orchestration.lean_loop import LeanLoopRunner
from src.idea_evolution.providers.router import RunnerRouter
from src.idea_evolution.config.routing import ModelRoutingConfig, ModelDefinition

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PILOT_DIR = REPO_ROOT / "experiments" / "EXP-M05.4-PROSPECTIVE-RERUN-20260829" / "treatment-delivery-pilot-01"


def calculate_sha256_file(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def _build_condition_b_router(runner: ModelRunner) -> RunnerRouter:
    config = ModelRoutingConfig(
        models={
            "default": ModelDefinition(
                provider=getattr(runner, "provider", "groq"),
                model=getattr(runner, "default_model", "openai/gpt-oss-120b")
            )
        },
        routes={},
        default_model_alias="default"
    )
    return RunnerRouter(config=config, custom_runners={"default": runner})


def _append_journal(journal_path: Path, entry: Dict[str, Any]) -> None:
    with open(journal_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def execute_pilot_resume(runner: Optional[ModelRunner] = None, verbose: bool = True) -> Dict[str, Any]:
    PILOT_DIR.mkdir(parents=True, exist_ok=True)
    raw_dir = PILOT_DIR / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    journal_path = PILOT_DIR / "PILOT-JOURNAL.jsonl"

    cal_ideas_path = PILOT_DIR / "CALIBRATION-IDEAS.json"
    cal_ideas = {i["idea_id"]: i for i in json.loads(cal_ideas_path.read_text(encoding="utf-8"))}

    if runner is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY_MISSING")
        runner = NativeModelRunner(provider="groq", api_key=api_key, default_model="openai/gpt-oss-120b")

    # --- LOAD COMPLETED RESULTS FROM PRIOR PARTIAL RUN ---
    prior_cal01_a_path = raw_dir / "CAL-01_condition_a.json"
    prior_cal01_a = json.loads(prior_cal01_a_path.read_text(encoding="utf-8"))

    # Mark interrupted B partial evidence in journal
    _append_journal(journal_path, {
        "event": "SERVER_RESTART_RECOVERY",
        "note": "CAL-01-CONDITION_B interrupted after stage 4 SYNTHESIZE. Re-running with run_id_v2. Partial stages in runs_b/PILOT-CAL-01-COND-B/stages preserved as evidence.",
        "timestamp": datetime.now().isoformat(),
    })

    # Cells remaining: CAL-01-B (restart), CAL-01-C, CAL-02-A, CAL-02-B, CAL-02-C
    cells_to_run = [
        {"cell_id": "CAL-01-CONDITION_B", "idea_id": "CAL-01", "condition": "CONDITION_B", "run_suffix": "_v2"},
        {"cell_id": "CAL-01-CONDITION_C", "idea_id": "CAL-01", "condition": "CONDITION_C", "run_suffix": ""},
        {"cell_id": "CAL-02-CONDITION_A", "idea_id": "CAL-02", "condition": "CONDITION_A", "run_suffix": ""},
        {"cell_id": "CAL-02-CONDITION_B", "idea_id": "CAL-02", "condition": "CONDITION_B", "run_suffix": ""},
        {"cell_id": "CAL-02-CONDITION_C", "idea_id": "CAL-02", "condition": "CONDITION_C", "run_suffix": ""},
    ]

    executed_new_cells: List[Dict[str, Any]] = []
    total_semantic_calls = prior_cal01_a["model_calls"]  # start with 1 from prior CAL-01-A
    calls_by_cond = {"CONDITION_A": prior_cal01_a["model_calls"], "CONDITION_B": 0, "CONDITION_C": 0}

    if verbose:
        print("=== RESUMING M05.4 TREATMENT-DELIVERY PILOT 01 ===")
        print("Prior CAL-01-A: DELIVERED (preserved)")

    start_pilot_time = time.time()

    for idx, cell in enumerate(cells_to_run, 1):
        cell_id = cell["cell_id"]
        idea_id = cell["idea_id"]
        cond = cell["condition"]
        suffix = cell.get("run_suffix", "")
        raw_idea = cal_ideas[idea_id]["raw_idea"]

        if verbose:
            print("[%d/5] Executing %s..." % (idx, cell_id), end="", flush=True)

        _append_journal(journal_path, {
            "event": "CELL_STARTED",
            "cell_id": cell_id,
            "idea_id": idea_id,
            "condition": cond,
            "run_note": "v2_restart" if suffix else "fresh",
            "timestamp": datetime.now().isoformat(),
        })

        cell_start = time.time()

        if cond == "CONDITION_A":
            runs_dir = raw_dir / "runs_a"
            runs_dir.mkdir(parents=True, exist_ok=True)
            baseline = BaselineRunner(runner=runner, model_name="openai/gpt-oss-120b")
            res = baseline.run(original_idea=raw_idea, run_id=("PILOT-%s-COND-A" % idea_id), runs_dir=runs_dir)
            lat = time.time() - cell_start

            output_data = res.get("parsed_output") or {}
            success = (res.get("success") is True) and bool(output_data)
            calls = 1
            refined_text = output_data.get("refined_version", "")
            delivery_class = "DELIVERED" if (success and len(refined_text.strip()) > 50) else "NOT_DELIVERED"

            cell_payload = {
                "cell_id": cell_id, "idea_id": idea_id, "condition": cond,
                "latency_seconds": round(lat, 3), "model_calls": calls,
                "status": "SUCCESS" if success else "FAILED",
                "terminal_status": "SUCCESS" if success else "FAILED",
                "delivery_class": delivery_class,
                "error": res.get("error"),
                "candidate_present": bool(refined_text.strip()),
                "parsed_output": output_data,
            }
            artifact_name = "CAL-02_condition_a.json"

        elif cond == "CONDITION_B":
            runs_dir = raw_dir / "runs_b"
            runs_dir.mkdir(parents=True, exist_ok=True)
            router = _build_condition_b_router(runner)
            simple_runner = SimpleLoopRunner(router=router, topology="STANDARD_6_STAGE", runs_dir=runs_dir)
            run_id = "PILOT-%s-COND-B%s" % (idea_id, suffix)
            state = simple_runner.run(original_idea=raw_idea, run_id=run_id)
            lat = time.time() - cell_start

            calls = len(state.stage_history)
            status_val = getattr(state.status, "value", str(state.status))
            stages_executed = [s.stage_id for s in state.stage_history]
            candidate_text = state.current_idea or ""
            has_candidate = bool(candidate_text.strip()) and len(candidate_text.strip()) > 50

            if status_val in ("REFINED_IDEA_READY", "COMPLETED", "STABILIZED") and has_candidate:
                delivery_class = "DELIVERED"
            elif status_val == "REFINEMENT_INCOMPLETE" and has_candidate:
                delivery_class = "PARTIALLY_DELIVERED"
            else:
                delivery_class = "NOT_DELIVERED"

            cell_payload = {
                "cell_id": cell_id, "idea_id": idea_id, "condition": cond,
                "run_id_used": run_id,
                "latency_seconds": round(lat, 3), "model_calls": calls,
                "status": "SUCCESS" if delivery_class in ("DELIVERED", "PARTIALLY_DELIVERED") else "FAILED",
                "terminal_status": status_val,
                "delivery_class": delivery_class,
                "reconstruction_count": state.reconstruction_count,
                "stages_executed": stages_executed,
                "candidate_present": has_candidate,
            }
            artifact_name = ("%s_condition_b%s.json" % (idea_id.lower(), suffix)).replace("-", "_")

        elif cond == "CONDITION_C":
            runs_dir = raw_dir / "runs_c"
            runs_dir.mkdir(parents=True, exist_ok=True)
            lean_runner = LeanLoopRunner(runner=runner, model_name="openai/gpt-oss-120b", runs_dir=runs_dir)
            run_id = "PILOT-%s-COND-C%s" % (idea_id, suffix)
            lean_res = lean_runner.run(original_idea=raw_idea, run_id=run_id)
            lat = time.time() - cell_start

            calls = lean_res.total_model_calls
            term_status = lean_res.terminal_status or "UNKNOWN"
            has_first_pass = lean_res.first_pass is not None

            if term_status in (
                "COMPLETED", "COMPLETED_DIRECT_ONE_PASS", "COMPLETED_WITH_FOCUSED_ESCALATION",
                "HUMAN_DECISION_REQUIRED", "DECISION_REQUIRED", "DECISION_SATISFIED", "EARLY_EXIT"
            ) and has_first_pass:
                delivery_class = "DELIVERED"
            else:
                delivery_class = "NOT_DELIVERED"

            cell_payload = {
                "cell_id": cell_id, "idea_id": idea_id, "condition": cond,
                "run_id_used": run_id,
                "latency_seconds": round(lat, 3), "model_calls": calls,
                "status": "SUCCESS" if delivery_class == "DELIVERED" else "FAILED",
                "terminal_status": term_status,
                "delivery_class": delivery_class,
                "gate_outcome": lean_res.gate_result.outcome.value if lean_res.gate_result else "UNKNOWN",
                "human_decision_requested": lean_res.human_decision_requested,
                "candidate_present": has_first_pass,
            }
            artifact_name = ("%s_condition_c%s.json" % (idea_id.lower(), suffix)).replace("-", "_")

        else:
            raise ValueError("Unknown condition: %s" % cond)

        raw_artifact_file = raw_dir / artifact_name
        raw_artifact_file.write_text(json.dumps(cell_payload, indent=2, ensure_ascii=False), encoding="utf-8")

        total_semantic_calls += calls
        calls_by_cond[cond] += calls
        executed_new_cells.append(cell_payload)

        _append_journal(journal_path, {
            "event": "CELL_COMPLETED",
            "cell_id": cell_id,
            "delivery_class": delivery_class,
            "terminal_status": cell_payload.get("terminal_status"),
            "model_calls": calls,
            "latency_seconds": round(lat, 3),
            "timestamp": datetime.now().isoformat(),
        })

        if verbose:
            print(" -> %s (%s, %d calls, %.1fs)" % (delivery_class, cell_payload.get("terminal_status"), calls, lat))

        time.sleep(1.5)

    # Build complete picture including prior CAL-01-A
    all_cells = [prior_cal01_a] + executed_new_cells

    a_delivered = sum(1 for c in all_cells if c["condition"] == "CONDITION_A" and c["delivery_class"] == "DELIVERED")
    b_delivered_or_partial = sum(1 for c in all_cells if c["condition"] == "CONDITION_B" and c["delivery_class"] in ("DELIVERED", "PARTIALLY_DELIVERED"))
    c_delivered = sum(1 for c in all_cells if c["condition"] == "CONDITION_C" and c["delivery_class"] == "DELIVERED")

    all_delivered_cleanly = (a_delivered == 2) and (b_delivered_or_partial == 2) and (c_delivered == 2)
    verdict = "END_TO_END_TREATMENT_DELIVERY_PROVEN_ON_CALIBRATION" if all_delivered_cleanly else "END_TO_END_TREATMENT_DELIVERY_NOT_YET_PROVEN"

    delivery_counts: Dict[str, int] = {}
    for c in all_cells:
        dc = c["delivery_class"]
        delivery_counts[dc] = delivery_counts.get(dc, 0) + 1

    manifest_payload = {
        "pilot_id": "M05.4-TREATMENT-DELIVERY-PILOT-01",
        "timestamp": datetime.now().isoformat(),
        "resume_note": "Resumed after server restart; CAL-01-CONDITION_B partial evidence preserved, restarted as v2.",
        "total_duration_seconds": round(time.time() - start_pilot_time, 2),
        "total_cells_planned": 6,
        "total_cells_completed": len(all_cells),
        "total_semantic_model_calls": total_semantic_calls,
        "calls_by_condition": calls_by_cond,
        "delivery_counts": delivery_counts,
        "a_delivered_count": a_delivered,
        "b_delivered_or_partial_count": b_delivered_or_partial,
        "c_delivered_count": c_delivered,
        "verdict": verdict,
        "cells": all_cells,
    }

    (PILOT_DIR / "PILOT-MANIFEST.json").write_text(json.dumps(manifest_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    evidence_items: Dict[str, Any] = {}
    for p in sorted(PILOT_DIR.rglob("*")):
        if p.is_file() and p.name != "PILOT-EVIDENCE-MANIFEST.json":
            rel_path = str(p.relative_to(PILOT_DIR)).replace("\\", "/")
            evidence_items[rel_path] = {"sha256": calculate_sha256_file(p), "size_bytes": p.stat().st_size}

    evidence_manifest = {
        "pilot_id": "M05.4-TREATMENT-DELIVERY-PILOT-01",
        "generated_at": datetime.now().isoformat(),
        "total_files": len(evidence_items),
        "files": evidence_items,
    }
    (PILOT_DIR / "PILOT-EVIDENCE-MANIFEST.json").write_text(json.dumps(evidence_manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    summary_lines = [
        "# PILOT-SUMMARY.md - M05.4 Treatment-Delivery Pilot 01 Summary\n",
        "- **Pilot ID:** `M05.4-TREATMENT-DELIVERY-PILOT-01`",
        "- **Verdict:** `%s`" % verdict,
        "- **Cells Completed:** `%d / 6`" % len(all_cells),
        "- **Total Semantic Calls:** `%d / 26 max`" % total_semantic_calls,
        "- **Calls by Condition:** A=%d, B=%d, C=%d" % (calls_by_cond["CONDITION_A"], calls_by_cond["CONDITION_B"], calls_by_cond["CONDITION_C"]),
        "- **Delivery:** A: %d/2 DELIVERED, B: %d/2 DELIVERED/PARTIAL, C: %d/2 DELIVERED\n" % (a_delivered, b_delivered_or_partial, c_delivered),
        "## Cell Breakdown\n",
        "| Cell | Condition | Delivery | Terminal Status | Calls | Latency |",
        "|---|---|---|---|---|---|",
    ]
    for c in all_cells:
        summary_lines.append("| `%s` | `%s` | `%s` | `%s` | %d | %ss |" % (
            c["cell_id"], c["condition"], c["delivery_class"], c.get("terminal_status"), c["model_calls"], c["latency_seconds"]))

    (PILOT_DIR / "PILOT-SUMMARY.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    return manifest_payload


if __name__ == "__main__":
    execute_pilot_resume(verbose=True)
