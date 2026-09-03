"""
tools/experiments/reconcile_pilot_002_reviewability.py
Script determinístico offline para reconciliação de reviewabilidade dos artefatos armazenados do Piloto-002 (M05.5R2).
Zero chamadas ao modelo.
Zero chamadas de rede.
"""

import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.experiments.execute_m05_5r1_confirmatory import classify_cell_reviewability

def reconcile_pilot_002():
    p = REPO_ROOT / "experiments" / "EXP-M05.5R2-FREE-PROVIDER-PORTABILITY-REPLICATION" / "CEREBRAS-FREE-SACRIFICIAL-PILOT-002"
    assert p.exists(), f"Path not found: {p}"

    # 1. Condition C
    fc = p / "raw" / "runs_c" / "CEREBRAS-FREE-SACRIFICIAL-PILOT-002-C" / "final.json"
    mdc = p / "raw" / "runs_c" / "CEREBRAS-FREE-SACRIFICIAL-PILOT-002-C" / "final.md"
    dc = json.loads(fc.read_text(encoding="utf-8"))
    cell_c = {
        "cell_id": "PILOT-002-C",
        "condition": "CONDITION_C",
        "status": "SUCCESS",
        "terminal_status": dc.get("status", "HUMAN_DECISION_REQUIRED"),
        "rendered_semantic_text": mdc.read_text(encoding="utf-8"),
        "parsed_output": dc,
        "logical_calls": 1,
    }
    rev_c, reason_c = classify_cell_reviewability(cell_c, None)
    print(f"Condition C: reviewable={rev_c}, reason={reason_c}")

    # 2. Condition B
    fb = p / "raw" / "runs_b" / "CEREBRAS-FREE-SACRIFICIAL-PILOT-002-B" / "final.json"
    sb = p / "raw" / "runs_b" / "CEREBRAS-FREE-SACRIFICIAL-PILOT-002-B" / "state.json"
    db = json.loads(fb.read_text(encoding="utf-8"))
    state_data = json.loads(sb.read_text(encoding="utf-8"))
    stages_b = [s["stage_id"] for s in state_data.get("stage_history", [])]
    
    unc_lines = "\n".join(f"- {u}" for u in state_data.get("remaining_uncertainties", []))
    rendered_b = (
        f"### Ideia Refinada Final\n{state_data.get('current_idea') or state_data.get('original_idea')}\n\n"
        f"### Intenção Humana Preservada\n{state_data.get('human_intent')}\n\n"
        f"### Mecanismo Central\n{state_data.get('core_mechanism')}\n\n"
        f"### Incertezas Críticas Remanescentes\n{unc_lines}\n\n"
        f"### Próxima Ação Recomendada\n{state_data.get('recommended_next_step')}"
    )
    cell_b = {
        "cell_id": "PILOT-002-B",
        "condition": "CONDITION_B",
        "status": "SUCCESS" if state_data.get("status") in ("SUCCESS", "REFINEMENT_INCOMPLETE") else "FAILED",
        "terminal_status": state_data.get("status", "REFINEMENT_INCOMPLETE"),
        "stages_executed": stages_b,
        "rendered_semantic_text": rendered_b,
        "parsed_output": db,
        "logical_calls": len(stages_b),
    }
    rev_b, reason_b = classify_cell_reviewability(cell_b, None)
    print(f"Condition B: reviewable={rev_b}, reason={reason_b}")

    # 3. Condition A
    fa = p / "raw" / "runs_a" / "CEREBRAS-FREE-SACRIFICIAL-PILOT-002-A" / "final.json"
    da = json.loads(fa.read_text(encoding="utf-8"))
    parsed_a = da.get("parsed_output", {})
    strengths_a = parsed_a.get("strengths", [])
    weaknesses_a = parsed_a.get("weaknesses", [])
    next_steps_a = parsed_a.get("next_steps", [])
    rendered_a = (
        f"### Resumo\n{parsed_a.get('summary', '')}\n\n"
        f"### Versão Refinada\n{parsed_a.get('refined_version', '')}\n\n"
        f"### Pontos Fortes e Fracos\n"
        f"- **Fortes:** {', '.join(strengths_a)}\n"
        f"- **Fracos:** {', '.join(weaknesses_a)}\n\n"
        f"### Próximos Passos\n{', '.join(next_steps_a)}"
    )
    cell_a = {
        "cell_id": "PILOT-002-A",
        "condition": "CONDITION_A",
        "status": "SUCCESS" if da.get("success") else "FAILED",
        "terminal_status": "SUCCESS" if da.get("success") else "FAILED",
        "rendered_semantic_text": rendered_a,
        "parsed_output": parsed_a,
        "logical_calls": 1,
    }
    rev_a, reason_a = classify_cell_reviewability(cell_a, None)
    print(f"Condition A: reviewable={rev_a}, reason={reason_a}")

    all_three = rev_c and rev_b and rev_a
    print(f"\nThree-way Reviewability Reconciliation: {'PASS' if all_three else 'FAIL'}")
    assert rev_c is True, f"Condition C failed: {reason_c}"
    assert rev_b is True, f"Condition B failed: {reason_b}"
    assert rev_a is True, f"Condition A failed: {reason_a}"
    assert all_three is True

    # Output reconciliation summary JSON
    reconciliation_summary = {
        "attempt_id": "CEREBRAS-FREE-SACRIFICIAL-PILOT-002",
        "execution_plane": "OFFLINE_EVIDENCE_RECONCILIATION_NO_NETWORK",
        "condition_c_reviewable": rev_c,
        "condition_c_reason": reason_c,
        "condition_b_reviewable": rev_b,
        "condition_b_reason": reason_b,
        "condition_a_reviewable": rev_a,
        "condition_a_reason": reason_a,
        "all_three_reviewable": all_three,
        "reconciliation_verdict": "PASS",
    }
    out_path = p / "RECONCILED-REVIEWABILITY-SUMMARY.json"
    out_path.write_text(json.dumps(reconciliation_summary, indent=2), encoding="utf-8")
    print(f"Reconciliation summary written to: {out_path}")
    return reconciliation_summary

if __name__ == "__main__":
    reconcile_pilot_002()
