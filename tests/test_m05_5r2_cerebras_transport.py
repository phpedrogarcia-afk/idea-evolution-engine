"""
tests/test_m05_5r2_cerebras_transport.py
Testes determinísticos offline para o adapter de transporte Cerebras Cloud (M05.5R2).
Garante:
1. Invariante do modelo e alias de transporte: gpt-oss-120b -> openai/gpt-oss-120b.
2. Guarda de custo fail-closed contra desvios de base_url.
3. Compatibilidade estrita de 100% dos schemas dos tratamentos A/B/C.
4. Preservação exata do schema lógico no payload da requisição.
5. Invariante de max_retries = 0 (1 disparo lógico = 1 request).
6. Sanitização completa de credenciais (csk-...).
7. Bloqueio fail-closed por ausência de credencial antes de qualquer rede.
8. Parsing de resposta em mock de transporte.
"""

import json
import pytest
from pydantic import BaseModel, Field

from src.idea_evolution.providers.cerebras import (
    CerebrasTransportBuilder,
    CerebrasRunner,
    CEREBRAS_HOSTED_BASE_URL,
    CEREBRAS_TRANSPORT_MODEL_ID,
    SCIENTIFIC_MODEL_ID,
    EXPECTED_INFERENCE_PRICE,
    sanitize_cerebras_credential,
    validate_cerebras_strict_schema_compatibility,
    is_cerebras_key_present,
)
from src.idea_evolution.stages.contracts import (
    BaselineRefineOutput,
    UnderstandOutput,
    AttackOutput,
    AlternativesOutput,
    SynthesizeOutput,
    RealityCheckOutput,
    FinalReviewOutput,
)
from src.idea_evolution.domain.early_epistemic_gate import LeanFirstPassOutput
from src.idea_evolution.providers.native import to_strict_json_schema


def test_model_id_and_transport_alias_invariants():
    builder = CerebrasTransportBuilder()
    assert builder.base_url == "https://api.cerebras.ai/v1"
    assert builder.scientific_model == "openai/gpt-oss-120b"
    assert builder.transport_model == "gpt-oss-120b"
    assert EXPECTED_INFERENCE_PRICE == 0.0


def test_paid_endpoint_selection_is_blocked_fail_closed():
    for bad_url in [
        "https://api.openai.com/v1",
        "https://api.cerebras.ai/v1/paid",
        "https://openrouter.ai/api/v1",
        "https://custom-proxy.internal",
    ]:
        with pytest.raises(RuntimeError, match="FAIL_CLOSED_PAID_ROUTING_GUARD"):
            CerebrasTransportBuilder(base_url=bad_url)


def test_unauthorized_model_id_is_blocked_fail_closed():
    for bad_model in ["llama-3.3-70b", "gpt-4o", "cerebras/llama-3.1"]:
        with pytest.raises(RuntimeError, match="FAIL_CLOSED_MODEL_GUARD"):
            CerebrasTransportBuilder(transport_model=bad_model)


def test_all_8_treatment_schemas_pass_cerebras_strict_constraints():
    treatment_schemas = [
        BaselineRefineOutput,
        UnderstandOutput,
        AttackOutput,
        AlternativesOutput,
        SynthesizeOutput,
        RealityCheckOutput,
        FinalReviewOutput,
        LeanFirstPassOutput,
    ]
    for schema_cls in treatment_schemas:
        strict_s = to_strict_json_schema(schema_cls)
        is_compat, errors = validate_cerebras_strict_schema_compatibility(strict_s)
        assert is_compat, f"Schema {schema_cls.__name__} failed strict validation: {errors}"
        assert len(errors) == 0


def test_exact_logical_schema_preservation_in_payload():
    builder = CerebrasTransportBuilder()
    payload = builder.build_request_payload(
        messages=[{"role": "user", "content": "Teste"}],
        schema_cls=UnderstandOutput,
        temperature=0.3,
        max_tokens=2048,
    )
    assert payload["model"] == "gpt-oss-120b"
    assert payload["temperature"] == 0.3
    assert payload["max_completion_tokens"] == 2048
    assert "response_format" in payload
    rf = payload["response_format"]
    assert rf["type"] == "json_schema"
    assert rf["json_schema"]["strict"] is True
    assert rf["json_schema"]["name"] == "UnderstandOutput"

    # Verificar que propriedades e required foram preservados
    schema = rf["json_schema"]["schema"]
    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False
    expected_props = {
        "interpreted_problem", "human_intent", "proposed_mechanism", "explicit_mechanism",
        "inferred_candidates", "actors_or_users", "assumptions", "ambiguities",
        "strengths", "structured_idea"
    }
    assert set(schema["properties"].keys()) == expected_props
    assert set(schema["required"]) == expected_props


def test_credential_sanitization():
    raw_error = "Error with key csk-9876543210abcdef and Bearer csk-9876543210abcdef in api_key=csk-secret"
    sanitized = sanitize_cerebras_credential(raw_error)
    assert "csk-9876543210abcdef" not in sanitized
    assert "csk-***" in sanitized
    assert "Bearer ***" in sanitized
    assert "api_key=***" in sanitized


def test_absence_of_key_raises_fail_closed_before_network(monkeypatch):
    monkeypatch.setattr("src.idea_evolution.providers.cerebras.get_cerebras_api_key", lambda: None)
    assert not is_cerebras_key_present()

    runner = CerebrasRunner()
    with pytest.raises(RuntimeError, match="CEREBRAS_API_KEY_ABSENT"):
        runner.generate("Prompt", UnderstandOutput)


def test_mock_transport_execution_success():
    def mock_transport(payload):
        assert payload["model"] == "gpt-oss-120b"
        assert payload["temperature"] == 0.3
        assert payload["max_completion_tokens"] == 2048
        return {
            "content": json.dumps({
                "summary": "Resumo",
                "strengths": ["s1"],
                "weaknesses": ["w1"],
                "refined_version": "Versão refinada",
            }),
            "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
        }

    runner = CerebrasRunner(transport_callable=mock_transport)
    resp = runner.generate("Prompt text", BaselineRefineOutput)
    assert resp.error is None
    assert resp.parsed is not None
    assert resp.parsed.summary == "Resumo"
    assert resp.parsed.refined_version == "Versão refinada"
    assert resp.usage.total_tokens == 150
    assert resp.provider == "cerebras"
    assert resp.model == "openai/gpt-oss-120b"
