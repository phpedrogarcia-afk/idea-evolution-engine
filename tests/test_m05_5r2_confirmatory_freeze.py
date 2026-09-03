"""
tests/test_m05_5r2_confirmatory_freeze.py
Testes determinísticos offline para validação do congelamento confirmatório e reconciliação do Piloto-002 (M05.5R2).

Zero chamadas ao modelo.
Zero chamadas de rede.
"""

import json
from pathlib import Path
import pytest

from tools.experiments.reconcile_pilot_002_reviewability import reconcile_pilot_002
from tools.experiments.execute_m05_5r1_confirmatory import classify_cell_reviewability


def test_pilot_002_three_way_reviewability_reconciled():
    res = reconcile_pilot_002()
    assert res["condition_c_reviewable"] is True
    assert res["condition_c_reason"] == "C_SUBSTANTIVE_CANDIDATE_HUMAN_DECISION_REQUIRED"
    assert res["condition_b_reviewable"] is True
    assert res["condition_b_reason"] == "B_SUBSTANTIVE_CANDIDATE_REFINEMENT_INCOMPLETE"
    assert res["condition_a_reviewable"] is True
    assert res["condition_a_reason"] == "A_VALID_BASELINE_CANDIDATE"
    assert res["all_three_reviewable"] is True
    assert res["reconciliation_verdict"] == "PASS"


def test_m05_5r2_confirmatory_freeze_record_integrity():
    freeze_path = Path("experiments/EXP-M05.5R2-FREE-PROVIDER-PORTABILITY-REPLICATION/M05.5R2-CONFIRMATORY-FREEZE-RECORD.json")
    assert freeze_path.exists()
    data = json.loads(freeze_path.read_text(encoding="utf-8"))

    # Configuração de provedor
    cfg = data["provider_configuration"]
    assert cfg["provider"] == "cerebras"
    assert cfg["scientific_model"] == "openai/gpt-oss-120b"
    assert cfg["transport_model"] == "gpt-oss-120b"
    assert cfg["output_cap"] == 4096
    assert cfg["output_cap_symmetry"] == "A_4096_B_4096_C_4096"
    assert cfg["temperature"] == 0.3
    assert cfg["max_retries"] == 0
    assert cfg["concurrency"] == 1

    # Compromissos e Holdouts
    assert data["holdout_manifest"]["holdout_set_sha256"] == "9b2a3b004a3b5533072bf7b6974ed17ee0180b61788621eefa03e1da12092cb9"
    assert data["blind_commitment"]["reveal_commitment_sha256"] == "d2de9ac1bbcd76c7aaef639b0b61d63dd355f1bea96f9d1c0f41ef7d434eed02"
    assert data["execution_order_reference"]["schedule_commitment_sha256"] == "05f948a49bdf11e7233dce98771359e216339989818cf46782d014ee94af7983"

    # Status de autorização
    meta = data["methodological_classification"]
    assert meta["sacrificial_phase"] == "CLOSED_SUCCESSFULLY"
    assert meta["cerebras_free_portability_status"] == "PROVEN_ENOUGH_FREEZE_AND_USE"
    assert meta["confirmatory_execution_authorized"] is False
    assert meta["h01_h08_executed"] is False

    # Registro de tentativa reservada
    reg_path = Path("experiments/EXP-M05.5R2-FREE-PROVIDER-PORTABILITY-REPLICATION/ATTEMPT-REGISTRY.jsonl")
    assert reg_path.exists()
    lines = [json.loads(line) for line in reg_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(lines) >= 1
    assert lines[0]["attempt_id"] == "M05.5R2-REAL-EXECUTION-ATTEMPT-001"
    assert lines[0]["status"] in ("RESERVED", "RUNNING", "COMPLETED_AWAITING_HUMAN_SCORING")
    assert lines[0]["execution_authorized"] is False
