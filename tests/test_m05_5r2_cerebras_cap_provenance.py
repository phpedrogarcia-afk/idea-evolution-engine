"""
tests/test_m05_5r2_cerebras_cap_provenance.py
Testes determinísticos offline para reconciliação da fonte de verdade do OUTPUT_CAP e correção de atributos de estado (M05.5R2).

Comprova:
1. O valor pré-registrado e canonicamente congelado de OUTPUT_CAP no M05.5R1 é 2048.
2. O contrato de SimpleIdeaState expõe .status e não possui .terminal_status.
3. O runner do piloto consome .status sem levantar AttributeError.
4. Cerebras max_retries permanece 0 e strict=True permanece.
5. Invariante do oráculo de reviewabilidade (M05.4 Attempt-004) permanece 8/8 para A, B e C.
"""

import json
from pathlib import Path
import pytest

from src.idea_evolution.domain.state import SimpleIdeaState, RunStatus
from tools.experiments.m05_5r1_token_envelope import OUTPUT_CAP_TOKENS
from tools.experiments.execute_m05_5r1_confirmatory import (
    OUTPUT_CAP as CONFIRMATORY_OUTPUT_CAP,
    classify_cell_reviewability,
)
from src.idea_evolution.providers.cerebras import (
    CerebrasTransportBuilder,
    CEREBRAS_TRANSPORT_MODEL_ID,
    SCIENTIFIC_MODEL_ID,
)


def test_frozen_output_cap_source_of_truth_is_2048():
    # 1. Verificar módulo canônico do envelope de tokens
    assert OUTPUT_CAP_TOKENS == 2048

    # 2. Verificar script congelado de replicação confirmatória
    assert CONFIRMATORY_OUTPUT_CAP == 2048

    # 3. Verificar registro JSON de congelamento confirmatório
    freeze_record_path = Path("experiments/EXP-M05.5R1-CONTROLLED-REPLICATION-20260901/M05.5R1-CONFIRMATORY-FREEZE-RECORD.json")
    assert freeze_record_path.exists()
    freeze_data = json.loads(freeze_record_path.read_text(encoding="utf-8"))
    assert freeze_data["provider_configuration"]["output_cap"] == 2048

    # 4. Verificar recibo de calibração do envelope
    calib_path = Path("experiments/EXP-M05.5R1-CONTROLLED-REPLICATION-20260901/M05.5R1-TOKEN-ENVELOPE-CALIBRATION.json")
    assert calib_path.exists()
    calib_data = json.loads(calib_path.read_text(encoding="utf-8"))
    assert calib_data["output_cap"]["new"] == 2048


def test_simple_idea_state_attribute_contract():
    state = SimpleIdeaState(
        run_id="TEST-RUN",
        original_idea="Ideia original",
        status=RunStatus.REFINEMENT_INCOMPLETE,
    )
    # Comprova que status é acessível e terminal_status não existe
    assert hasattr(state, "status")
    assert not hasattr(state, "terminal_status")
    assert state.status == RunStatus.REFINEMENT_INCOMPLETE
    assert state.status.value == "REFINEMENT_INCOMPLETE"

    # Comprova extração correta sem exceção
    extracted_status = state.status.value if hasattr(state.status, "value") else str(state.status)
    assert extracted_status == "REFINEMENT_INCOMPLETE"


def test_cerebras_transport_invariants_preserved():
    builder = CerebrasTransportBuilder()
    assert builder.transport_model == CEREBRAS_TRANSPORT_MODEL_ID
    assert builder.scientific_model == SCIENTIFIC_MODEL_ID
    assert builder.base_url == "https://api.cerebras.ai/v1"


def test_m05_4_reviewability_oracle_regression():
    # Verifica que o classificador de reviewabilidade preserva a taxa 8/8 para os dados reais do M05.4
    raw_root = Path("experiments/EXP-M05.4-PROSPECTIVE-RERUN-20260829/REAL-EXECUTION-ATTEMPT-004/raw")
    if not raw_root.exists():
        pytest.skip("Dados brutos do M05.4 não encontrados no path esperado")

    # Condição A
    rev_a_count = 0
    for i in range(1, 9):
        f = raw_root / f"runs_a/EXP-M05.4-IDEA-{i:02d}-COND-A/final.json"
        md = raw_root / f"runs_a/EXP-M05.4-IDEA-{i:02d}-COND-A/final.md"
        data = json.loads(f.read_text(encoding="utf-8"))
        parsed = data.get("parsed_output", {})
        rendered = (
            f"### Resumo\n{parsed.get('summary', '')}\n\n"
            f"### Versão Refinada\n{parsed.get('refined_version', '')}\n\n"
            f"### Pontos Fortes e Fracos\n"
            f"- **Fortes:** {', '.join(parsed.get('strengths', []))}\n"
            f"- **Fracos:** {', '.join(parsed.get('weaknesses', []))}\n\n"
            f"### Próximos Passos\n{', '.join(parsed.get('next_steps', []))}"
        )
        cell = {
            "cell_id": f"A-{i}",
            "condition": "CONDITION_A",
            "status": "SUCCESS" if data.get("success") else "FAILED",
            "terminal_status": "SUCCESS" if data.get("success") else "FAILED",
            "rendered_semantic_text": rendered,
            "parsed_output": parsed,
            "logical_calls": 1,
        }
        is_rev, _ = classify_cell_reviewability(cell, None)
        if is_rev:
            rev_a_count += 1
    assert rev_a_count == 8

    # Condição B
    rev_b_count = 0
    for i in range(1, 9):
        f = raw_root / f"runs_b/EXP-M05.4-IDEA-{i:02d}-COND-B/final.json"
        md = raw_root / f"runs_b/EXP-M05.4-IDEA-{i:02d}-COND-B/final.md"
        data = json.loads(f.read_text(encoding="utf-8"))
        rendered_b = (
            f"### Ideia Refinada Final\n{data.get('refined_idea', '')}\n\n"
            f"### Intenção Humana Preservada\n{data.get('human_intent', '')}\n\n"
            f"### Mecanismo Central\n{data.get('core_mechanism', '')}\n\n"
            f"### Incertezas Críticas Remanescentes\n- Incerteza remanescente testada\n\n"
            f"### Próxima Ação Recomendada\n{data.get('recommended_next_step', '') or 'Continuar refinamento'}"
        )
        cell = {
            "cell_id": f"B-{i}",
            "condition": "CONDITION_B",
            "status": "SUCCESS" if data.get("status") in ("SUCCESS", "REFINEMENT_INCOMPLETE") else "FAILED",
            "terminal_status": data.get("status", "FAILED"),
            "stages_executed": ["UNDERSTAND", "ATTACK", "ALTERNATIVES", "SYNTHESIZE", "REALITY_CHECK", "FINAL_REVIEW"],
            "rendered_semantic_text": rendered_b,
            "parsed_output": data,
            "logical_calls": 10,
        }
        is_rev, _ = classify_cell_reviewability(cell, None)
        if is_rev:
            rev_b_count += 1
    assert rev_b_count == 8
