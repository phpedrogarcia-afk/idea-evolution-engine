"""
tests/test_m05_5r2_nvidia_nim_transport.py
Testes determinísticos offline para o adapter de transporte NVIDIA NIM.

Comprova:
1. Identidade do schema lógico Pydantic (properties, required, additionalProperties).
2. Preservação de prompt, temperatura (0.3), output cap (2048) e modelo exato (openai/gpt-oss-120b).
3. Fail-closed contra roteamento pago ou alteração de base_url.
4. Sanitização estrita de credenciais.
5. Comportamento fail-closed na ausência de NVIDIA_API_KEY (zero chamadas de rede).
"""

import pytest
import json
from typing import List
from pydantic import BaseModel, ConfigDict
from src.idea_evolution.providers.nvidia_nim import (
    NvidiaNimTransportBuilder,
    NvidiaNimRunner,
    NVIDIA_HOSTED_BASE_URL,
    NVIDIA_MODEL_ID,
    sanitize_nvidia_credential,
    is_nvidia_key_present,
)


class DummyUnderstandSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    summary: str
    proposed_mechanism: str
    critical_assumptions: List[str]
    falsification_conditions: List[str]


class DummyAttackSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    attack_vectors: List[str]
    severity_assessment: str
    irreversible_contradiction_found: bool


def test_model_id_and_base_url_invariants():
    builder = NvidiaNimTransportBuilder()
    assert builder.model == "openai/gpt-oss-120b"
    assert builder.base_url == "https://integrate.api.nvidia.com/v1"


def test_paid_endpoint_selection_is_blocked_fail_closed():
    with pytest.raises(ValueError, match="FAIL_CLOSED_PAID_ROUTING_GUARD"):
        NvidiaNimTransportBuilder(base_url="https://api.openai.com/v1")

    with pytest.raises(ValueError, match="FAIL_CLOSED_PAID_ROUTING_GUARD"):
        NvidiaNimTransportBuilder(base_url="https://openrouter.ai/api/v1")

    with pytest.raises(ValueError, match="FAIL_CLOSED_MODEL_GUARD"):
        NvidiaNimTransportBuilder(model="openai/gpt-4o")


def test_exact_logical_schema_preservation_understand():
    builder = NvidiaNimTransportBuilder()
    messages = [{"role": "user", "content": "Analyze idea H08"}]
    payload = builder.build_request_payload(
        messages=messages,
        schema_cls=DummyUnderstandSchema,
        temperature=0.3,
        max_tokens=2048,
    )

    # 1. Parâmetros de execução congelados
    assert payload["model"] == "openai/gpt-oss-120b"
    assert payload["temperature"] == 0.3
    assert payload["max_tokens"] == 2048
    assert payload["messages"] == messages

    # 2. Schema original
    orig_schema = DummyUnderstandSchema.model_json_schema()

    # 3. guided_json direto
    assert "guided_json" in payload
    assert payload["guided_json"] == orig_schema

    # 4. extra_body.nvext.guided_json
    assert "extra_body" in payload
    assert payload["extra_body"]["nvext"]["guided_json"] == orig_schema

    # 5. response_format json_schema
    assert "response_format" in payload
    rf = payload["response_format"]
    assert rf["type"] == "json_schema"
    assert rf["json_schema"]["name"] == "DummyUnderstandSchema"
    assert rf["json_schema"]["strict"] is True
    assert rf["json_schema"]["schema"] == orig_schema

    # 6. Preservação exata de propriedades e campos obrigatórios
    target_props = orig_schema["properties"]
    assert set(target_props.keys()) == {
        "summary",
        "proposed_mechanism",
        "critical_assumptions",
        "falsification_conditions",
    }
    assert set(orig_schema["required"]) == {
        "summary",
        "proposed_mechanism",
        "critical_assumptions",
        "falsification_conditions",
    }
    assert orig_schema.get("additionalProperties") is False


def test_exact_logical_schema_preservation_attack():
    builder = NvidiaNimTransportBuilder()
    messages = [{"role": "user", "content": "Attack idea H08"}]
    payload = builder.build_request_payload(
        messages=messages,
        schema_cls=DummyAttackSchema,
        temperature=0.3,
        max_tokens=2048,
    )

    orig_schema = DummyAttackSchema.model_json_schema()
    assert payload["guided_json"] == orig_schema
    assert set(orig_schema["properties"].keys()) == {
        "attack_vectors",
        "severity_assessment",
        "irreversible_contradiction_found",
    }
    assert set(orig_schema["required"]) == {
        "attack_vectors",
        "severity_assessment",
        "irreversible_contradiction_found",
    }


def test_payload_hash_determinism():
    builder = NvidiaNimTransportBuilder()
    messages = [{"role": "user", "content": "Test prompt text"}]
    p1 = builder.build_request_payload(messages, DummyUnderstandSchema, 0.3, 2048)
    p2 = builder.build_request_payload(messages, DummyUnderstandSchema, 0.3, 2048)
    assert builder.compute_sanitized_payload_sha256(p1) == builder.compute_sanitized_payload_sha256(p2)


def test_credential_sanitization():
    raw_error = "Error: 401 Unauthorized for nvapi-abc123secretkey with Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 and api_key='nvapi-xyz987'"
    sanitized = sanitize_nvidia_credential(raw_error)
    assert "nvapi-abc123secretkey" not in sanitized
    assert "nvapi-xyz987" not in sanitized
    assert "eyJhbGciOi" not in sanitized
    assert "nvapi-***" in sanitized
    assert "Bearer ***" in sanitized
    assert "api_key=***" in sanitized


def test_absence_of_key_raises_fail_closed_before_network(monkeypatch):
    monkeypatch.delenv("NVIDIA_API_KEY", raising=False)
    monkeypatch.delenv("NGC_API_KEY", raising=False)

    assert not is_nvidia_key_present()

    runner = NvidiaNimRunner()
    with pytest.raises(RuntimeError, match="NVIDIA_API_KEY_ABSENT"):
        runner.generate("Test prompt", DummyUnderstandSchema)


def test_mock_transport_execution_success():
    def mock_transport(payload):
        assert payload["model"] == "openai/gpt-oss-120b"
        assert payload["temperature"] == 0.3
        assert payload["max_tokens"] == 2048
        return {
            "content": json.dumps({
                "summary": "Idea summary",
                "proposed_mechanism": "Logical mechanism",
                "critical_assumptions": ["assumption 1"],
                "falsification_conditions": ["condition 1"],
            }),
            "usage": {"prompt_tokens": 150, "completion_tokens": 75, "total_tokens": 225},
            "system_fingerprint": "fp_nvidia_test",
        }

    runner = NvidiaNimRunner(transport_callable=mock_transport)
    resp = runner.generate("Prompt text", DummyUnderstandSchema)
    assert resp.error is None
    assert resp.parsed is not None
    assert resp.parsed.summary == "Idea summary"
    assert resp.parsed.proposed_mechanism == "Logical mechanism"
    assert resp.usage.total_tokens == 225
    assert resp.provider == "nvidia_nim"
