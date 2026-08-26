"""
src/idea_evolution/providers/router.py
Despachador determinístico de modelos por estágio (RunnerRouter).
"""

from __future__ import annotations
from typing import Dict, Any, Optional, Tuple
from src.idea_evolution.config.routing import ModelRoutingConfig, ModelDefinition
from src.idea_evolution.providers.base import ModelRunner
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.providers.native import NativeModelRunner


class RunnerRouter:
    """
    Roteador responsável por instanciar e fornecer o ModelRunner correto para cada estágio do pipeline.
    """

    def __init__(
        self,
        config: Optional[ModelRoutingConfig] = None,
        custom_runners: Optional[Dict[str, ModelRunner]] = None,
    ):
        self.config = config or ModelRoutingConfig.default_single_model()
        self.custom_runners = custom_runners or {}
        self._runner_instances: Dict[str, ModelRunner] = {}

    def get_runner_for_stage(self, stage_name: str) -> Tuple[ModelRunner, str, str]:
        """
        Retorna (runner, model_name, logical_alias) para o estágio especificado.
        Garante isolamento de falha e ausência de fallback silencioso entre provedores.
        """
        alias, model_def = self.config.resolve_stage(stage_name)

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
