"""
tests/test_m05_5r2_cerebras_routing.py
Testes determinísticos para o registro do provedor cerebras no sistema de roteamento do IEE.
Comprova que:
1. cerebras é aceito por ModelDefinition.
2. gpt-oss-120b + cerebras valida em ModelDefinition e ModelRoutingConfig.
3. Provedores existentes continuam validando normalmente.
4. Provedores desconhecidos continuam falhando fechado (fail-closed) com ValidationError.
5. ModelRoutingConfig.resolve_stage é aprovado sob a política FREE_ONLY.
6. RunnerRouter resolve custom_runner injetado para cerebras.
"""

import pytest
from pydantic import ValidationError

from src.idea_evolution.config.routing import ModelDefinition, ModelRoutingConfig
from src.idea_evolution.config.catalog import ModelCatalog, CostPolicy, CostClass, LifecycleStatus
from src.idea_evolution.providers.router import RunnerRouter
from src.idea_evolution.providers.fake import FakeModelRunner


def test_cerebras_provider_accepted_by_model_definition():
    m = ModelDefinition(provider="cerebras", model="gpt-oss-120b")
    assert m.provider == "cerebras"
    assert m.model == "gpt-oss-120b"


def test_cerebras_case_insensitivity():
    m = ModelDefinition(provider="CEREBRAS", model="gpt-oss-120b")
    assert m.provider == "cerebras"


def test_existing_providers_still_validate():
    for p in ["groq", "openai", "gemini", "anthropic", "openrouter", "nvidia_nim", "cerebras", "fake", "fake_a"]:
        m = ModelDefinition(provider=p, model="any-model")
        assert m.provider == p.lower()


def test_unknown_providers_fail_closed():
    for bad_provider in ["unknown_provider", "cerebras_partner", "random_backend"]:
        with pytest.raises(ValidationError) as exc_info:
            ModelDefinition(provider=bad_provider, model="gpt-oss-120b")
        assert "não suportado" in str(exc_info.value)


def test_cerebras_catalog_entry_properties():
    cat = ModelCatalog()
    entry = cat.get_entry("cerebras", "gpt-oss-120b")
    assert entry is not None
    assert entry.provider == "cerebras"
    assert entry.model_id == "gpt-oss-120b"
    assert entry.cost_class == CostClass.FREE_TIER
    assert entry.status == LifecycleStatus.ACTIVE
    assert entry.capabilities.structured_output is True


def test_cerebras_resolves_stage_under_free_only_policy():
    m = ModelDefinition(provider="cerebras", model="gpt-oss-120b")
    cfg = ModelRoutingConfig(
        cost_policy=CostPolicy.FREE_ONLY,
        models={"default": m},
        routes={},
        default_model_alias="default",
    )
    alias, resolved_m = cfg.resolve_stage("understand")
    assert alias == "default"
    assert resolved_m.provider == "cerebras"
    assert resolved_m.model == "gpt-oss-120b"


def test_runner_router_resolves_custom_runner_for_cerebras():
    m = ModelDefinition(provider="cerebras", model="gpt-oss-120b")
    cfg = ModelRoutingConfig(
        cost_policy=CostPolicy.FREE_ONLY,
        models={"default": m},
        routes={},
        default_model_alias="default",
    )
    fake_runner = FakeModelRunner(provider="cerebras", default_model="gpt-oss-120b")
    router = RunnerRouter(config=cfg, custom_runners={"default": fake_runner})

    runner, model_name, alias = router.get_runner_for_stage("understand")
    assert runner is fake_runner
    assert model_name == "gpt-oss-120b"
    assert alias == "default"
