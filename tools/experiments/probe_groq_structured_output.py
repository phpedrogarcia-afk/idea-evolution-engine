"""
tools/experiments/probe_groq_structured_output.py
Diagnostic micro-probe for Groq openai/gpt-oss-120b native structured output compatibility.

Executes at most 6 calls (3 initial + up to 1 diagnostic retry per failed schema) across:
  Schema A: BaselineRefineOutput
  Schema B: UnderstandOutput
  Schema C: LeanFirstPassOutput

Zero human review exposure.
"""

from typing import Dict, Any, List, Optional
import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

from src.idea_evolution.providers.native import NativeModelRunner
from src.idea_evolution.stages.contracts import BaselineRefineOutput
from src.idea_evolution.stages.understand import UnderstandOutput
from src.idea_evolution.domain.early_epistemic_gate import LeanFirstPassOutput

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROBE_DIR = REPO_ROOT / "experiments" / "EXP-M05.4-PROSPECTIVE-RERUN-20260829" / "micro-probe-001"


def run_micro_probe(runner: Optional[NativeModelRunner] = None, max_calls_total: int = 6, verbose: bool = True) -> Dict[str, Any]:
    PROBE_DIR.mkdir(parents=True, exist_ok=True)
    journal_path = PROBE_DIR / "MICRO-PROBE-RECEIPTS.jsonl"

    if runner is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY_MISSING: Cannot run probe without Groq API key.")
        runner = NativeModelRunner(provider="groq", api_key=api_key, default_model="openai/gpt-oss-120b")

    test_cases = [
        {
            "schema_code": "A",
            "schema_name": "BaselineRefineOutput",
            "schema_cls": BaselineRefineOutput,
            "stage_name": "BASELINE_REFINE",
            "prompt": "Analise e refine a seguinte ideia: Um sistema simples de notas rápidas em markdown com busca local.",
        },
        {
            "schema_code": "B",
            "schema_name": "UnderstandOutput",
            "schema_cls": UnderstandOutput,
            "stage_name": "UNDERSTAND",
            "prompt": "Compreenda e estruture a seguinte ideia: Um sistema simples de notas rápidas em markdown com busca local.",
        },
        {
            "schema_code": "C",
            "schema_name": "LeanFirstPassOutput",
            "schema_cls": LeanFirstPassOutput,
            "stage_name": "LEAN_FIRST_PASS",
            "prompt": "Você é o analista do Lean Idea Evolution Engine.\nAnalise a ideia original abaixo e produza uma estruturação mínima focada em intenção, mecanismo e riscos:\nIDEIA HUMANA:\nUm sistema simples de notas rápidas em markdown com busca local.",
        },
    ]

    receipts: List[Dict[str, Any]] = []
    results_by_schema: Dict[str, bool] = {}
    http_status_counts: Dict[str, int] = {}
    error_type_counts: Dict[str, int] = {}
    total_calls_spent = 0

    if verbose:
        print("=== INITIATING STRUCTURED-OUTPUT MICRO-PROBE (ROUND 1) ===")

    # Round 1: 1 call per schema
    for tc in test_cases:
        code = tc["schema_code"]
        name = tc["schema_name"]
        stage = tc["stage_name"]
        schema_cls = tc["schema_cls"]
        prompt = tc["prompt"]

        if verbose:
            print(f"Testing Schema {code} ({name})...", end="", flush=True)

        start_t = time.time()
        total_calls_spent += 1
        resp = runner.generate(prompt_text=prompt, output_schema=schema_cls, stage_name=stage, max_repairs=0)
        lat = time.time() - start_t

        success = (resp.parsed is not None) and (resp.error is None)
        results_by_schema[code] = success

        # Extract status if available in error
        err_str = resp.error or ""
        receipt = {
            "timestamp": datetime.now().isoformat(),
            "round": 1,
            "schema_code": code,
            "schema_name": name,
            "stage_name": stage,
            "success": success,
            "latency_seconds": round(lat, 3),
            "raw_response_present": bool(resp.raw_text.strip()),
            "structured_admission": success,
            "error": err_str,
            "retry_count": resp.retry_count,
        }
        receipts.append(receipt)

        with open(journal_path, "a", encoding="utf-8") as jf:
            jf.write(json.dumps(receipt, ensure_ascii=False) + "\n")

        if verbose:
            if success:
                print(f" PASS ({lat:.2f}s)")
            else:
                print(f" FAILED ({lat:.2f}s): {err_str[:60]}")

        # Bounded sleep to avoid burst rate limits
        time.sleep(1.0)

    # Check if Round 1 all passed
    round_1_all_pass = all(results_by_schema.values())

    # Round 2: retry only failed schemas if budget allows
    if not round_1_all_pass and total_calls_spent < max_calls_total:
        if verbose:
            print("=== INITIATING DIAGNOSTIC RETRY (ROUND 2) FOR FAILED SCHEMAS ===")
        for tc in test_cases:
            code = tc["schema_code"]
            if not results_by_schema[code] and total_calls_spent < max_calls_total:
                name = tc["schema_name"]
                stage = tc["stage_name"]
                schema_cls = tc["schema_cls"]
                prompt = tc["prompt"]

                if verbose:
                    print(f"Retrying Schema {code} ({name})...", end="", flush=True)

                start_t = time.time()
                total_calls_spent += 1
                resp = runner.generate(prompt_text=prompt, output_schema=schema_cls, stage_name=stage, max_repairs=0)
                lat = time.time() - start_t

                success = (resp.parsed is not None) and (resp.error is None)
                results_by_schema[code] = success

                receipt = {
                    "timestamp": datetime.now().isoformat(),
                    "round": 2,
                    "schema_code": code,
                    "schema_name": name,
                    "stage_name": stage,
                    "success": success,
                    "latency_seconds": round(lat, 3),
                    "raw_response_present": bool(resp.raw_text.strip()),
                    "structured_admission": success,
                    "error": resp.error or "",
                    "retry_count": resp.retry_count,
                }
                receipts.append(receipt)

                with open(journal_path, "a", encoding="utf-8") as jf:
                    jf.write(json.dumps(receipt, ensure_ascii=False) + "\n")

                if verbose:
                    if success:
                        print(f" PASS ({lat:.2f}s)")
                    else:
                        print(f" FAILED ({lat:.2f}s): {resp.error[:60]}")

                time.sleep(1.5)

    all_passed = all(results_by_schema.values())
    verdict = "PIPE_PROVEN_FOR_REPRESENTATIVE_SCHEMAS" if all_passed else "PIPE_NOT_YET_PROVEN"

    summary = {
        "probe_executed_at": datetime.now().isoformat(),
        "total_calls_spent": total_calls_spent,
        "schemas_tested": len(test_cases),
        "schema_a_admission": results_by_schema.get("A", False),
        "schema_b_admission": results_by_schema.get("B", False),
        "schema_c_admission": results_by_schema.get("C", False),
        "all_schemas_passed": all_passed,
        "verdict": verdict,
        "receipts": receipts,
    }

    summary_path = PROBE_DIR / "MICRO-PROBE-SUMMARY.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    return summary


if __name__ == "__main__":
    run_micro_probe(verbose=True)
