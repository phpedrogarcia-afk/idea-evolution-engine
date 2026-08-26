"""
src/idea_evolution/providers/router.py
Despachador determinístico de modelos por estágio (RunnerRouter) com Governança de Custos e Catálogo Vivo.
"""

from __future__ import annotations
from typing import Dict, Any, Optional, Tuple, List
from src.idea_evolution.config.routing import ModelRoutingConfig, ModelDefinition
from src.idea_evolution.config.catalog import ModelCatalog, CostPolicy, ExecutionMode, CostClass
from src.idea_evolution.providers.base import ModelRunner
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.providers.native import NativeModelRunner


class RunnerRouter:
    """
    Roteador responsável por instanciar e fornecer o ModelRunner correto para cada estágio do pipeline.
    Valida elegibilidade com base no ModelCatalog e na política de custo (FREE_ONLY).
    """

    def __init__(
        self,
        config: Optional[ModelRoutingConfig] = None,
        catalog: Optional[ModelCatalog] = None,
        custom_runners: Optional[Dict[str, ModelRunner]] = None,
    ):
        self.catalog = catalog or ModelCatalog()
        self.config = config or ModelRoutingConfig.default_single_model()
        self.custom_runners = custom_runners or {}
        self._runner_instances: Dict[str, ModelRunner] = {}

    def get_runner_for_stage(self, stage_name: str) -> Tuple[ModelRunner, str, str]:
        """
        Retorna (runner, model_name, logical_alias) para o estágio especificado.
        Valida elegibilidade sob a política de custos.
        Garante isolamento de falha e ausência de fallback silencioso entre provedores.
        """
        alias, model_def = self.config.resolve_stage(stage_name, catalog=self.catalog)

        # Se houver runner injetado diretamente para o alias
        if alias in self.custom_runners:
            return self.custom_runners[alias], model_def.model, alias

        # Se houver runner injetado pelo nome do provedor
        if model_def.provider in self.custom_runners:
            return self.custom_runners[model_def.provider], model_def.model, alias

        # Instanciação ou reutilização da instância
        cache_key = f"{model_def.provider}:{model_def.model}"
        if cache_key not in self._runner_instances:
            if model_def.provider.startswith("fake"):
                self._runner_instances[cache_key] = FakeModelRunner(
                    provider=model_def.provider,
                    default_model=model_def.model,
                )
            else:
                self._runner_instances[cache_key] = NativeModelRunner(
                    provider=model_def.provider,
                    default_model=model_def.model,
                )

        return self._runner_instances[cache_key], model_def.model, alias

    def handle_stage_failure(
        self,
        stage_name: str,
        current_alias: str,
        failure_type: str,
    ) -> Optional[Tuple[ModelRunner, str, str]]:
        """
        Governança de Fallback:
        - Se modo for EXPERIMENTAL_PINNED: NUNCA faz auto-fallback (retorna None).
        - Se erro for SCHEMA_INVALID, PROMPT_FAILURE, SEMANTIC_FAILURE, SAFETY_REJECTION: NUNCA faz fallback de provedor (retorna None).
        - Se modo for FREE_POOL_OPERATIONAL e erro for FREE_QUOTA_EXHAUSTED ou MODEL_UNAVAILABLE:
          tenta o próximo candidato FREE_TIER elegível dentro da política FREE_ONLY.
        """
        if self.config.execution_mode == ExecutionMode.EXPERIMENTAL_PINNED:
            return None

        # Falhas de schema ou semântica não devem trocar de provedor
        if failure_type in ["SCHEMA_INVALID", "PROMPT_FAILURE", "SEMANTIC_FAILURE", "SAFETY_REJECTION"]:
            return None

        if failure_type in ["FREE_QUOTA_EXHAUSTED", "MODEL_UNAVAILABLE", "RATE_LIMITED"]:
            _, current_model = self.config.resolve_stage(stage_name, catalog=self.catalog)
            fallbacks = self.catalog.get_eligible_free_fallbacks(
                provider=current_model.provider,
                exclude_model=current_model.model,
            )
            if not fallbacks:
                return None

            next_free = fallbacks[0]
            # Cria runner para o fallback gratuito elegível
            cache_key = f"{next_free.provider}:{next_free.model_id}"
            if cache_key not in self._runner_instances:
                if next_free.provider.startswith("fake"):
                    self._runner_instances[cache_key] = FakeModelRunner(
                        provider=next_free.provider,
                        default_model=next_free.model_id,
                    )
                else:
                    self._runner_instances[cache_key] = NativeModelRunner(
                        provider=next_free.provider,
                        default_model=next_free.model_id,
                    )
            return self._runner_instances[cache_key], next_free.model_id, f"{current_alias}_fallback"

        return None
