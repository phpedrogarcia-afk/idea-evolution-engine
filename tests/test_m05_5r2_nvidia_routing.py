"""
tests/test_m05_5r2_nvidia_routing.py
Testes determinísticos para o registro do provedor nvidia_nim no sistema de roteamento do IEE.
Comprova que:
1. nvidia_nim é aceito por ModelDefinition.
2. openai/gpt-oss-120b + nvidia_nim valida em ModelDefinition e ModelRoutingConfig.
3. Provedores existentes continuam validando normalmente.
4. Provedores desconhecidos continuam falhando fechado (fail-closed) com ValidationError.
5. ModelRoutingConfig.resolve_stage é aprovado sob a política FREE_ONLY.
6. RunnerRouter resolve custom_runner injetado para nvidia_nim.
"""

import pytest
from pydantic import ValidationError

from src.idea_evolution.config.routing import ModelDefinition, ModelRoutingConfig
from src.idea_evolution.config.catalog import ModelCatalog, CostPolicy, CostClass, LifecycleStatus
from src.idea_evolution.providers.router import RunnerRouter
from src.idea_evolution.providers.fake import FakeModelRunner


def test_nvidia_nim_provider_accepted_by_model_definition():
    m = ModelDefinition(provider="nvidia_nim", model="openai/gpt-oss-120b")
    assert m.provider == "nvidia_nim"
    assert m.model == "openai/gpt-oss-120b"


def test_nvidia_nim_case_insensitivity():
    m = ModelDefinition(provider="NVIDIA_NIM", model="openai/gpt-oss-120b")
    assert m.provider == "nvidia_nim"


def test_existing_providers_still_validate():
    for p in ["groq", "openai", "gemini", "anthropic", "openrouter", "fake", "fake_a", "fake_b", "fake_c"]:
        m = ModelDefinition(provider=p, model="any-model")
        assert m.provider == p.lower()


def test_unknown_providers_fail_closed():
    for bad_provider in ["unknown_provider", "unsupported_llm", "random_backend", "paid_partner"]:
        with pytest.raises(ValidationError) as exc_info:
            ModelDefinition(provider=bad_provider, model="openai/gpt-oss-120b")
        assert "não suportado" in str(exc_info.value)


def test_nvidia_nim_catalog_entry_properties():
    cat = ModelCatalog()
    entry = cat.get_entry("nvidia_nim", "openai/gpt-oss-120b")
    assert entry is not None
    assert entry.provider == "nvidia_nim"
    assert entry.model_id == "openai/gpt-oss-120b"
    assert entry.cost_class == CostClass.FREE_TIER
    assert entry.status == LifecycleStatus.ACTIVE
    assert entry.capabilities.structured_output is True


def test_nvidia_nim_resolves_stage_under_free_only_policy():
    m = ModelDefinition(provider="nvidia_nim", model="openai/gpt-oss-120b")
    cfg = ModelRoutingConfig(
        cost_policy=CostPolicy.FREE_ONLY,
        models={"default": m},
        routes={},
        default_model_alias="default",
    )
    alias, resolved_m = cfg.resolve_stage("understand")
    assert alias == "default"
    assert resolved_m.provider == "nvidia_nim"
    assert resolved_m.model == "openai/gpt-oss-120b"


def test_runner_router_resolves_custom_runner_for_nvidia_nim():
    m = ModelDefinition(provider="nvidia_nim", model="openai/gpt-oss-120b")
    cfg = ModelRoutingConfig(
        cost_policy=CostPolicy.FREE_ONLY,
        models={"default": m},
        routes={},
        default_model_alias="default",
    )
    fake_runner = FakeModelRunner(provider="nvidia_nim", default_model="openai/gpt-oss-120b")
    router = RunnerRouter(config=cfg, custom_runners={"default": fake_runner})

    runner, model_name, alias = router.get_runner_for_stage("understand")
    assert runner is fake_runner
    assert model_name == "openai/gpt-oss-120b"
    assert alias == "default"
