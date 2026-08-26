"""
src/idea_evolution/stages/stage_base.py
Classe base abstrata para os estágios do pipeline cognitivo do IEE.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type, TypeVar, Optional, Dict, Any
from pydantic import BaseModel
from src.idea_evolution.domain.state import SimpleIdeaState
from src.idea_evolution.providers.base import ModelRunner, ModelResponse

T = TypeVar("T", bound=BaseModel)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
PROMPTS_DIR = REPO_ROOT / "prompts"


class StageExecutionResult(BaseModel):
    stage_id: str
    stage_version: str
    success: bool
    output: Optional[Any] = None
    raw_response: str = ""
    error: Optional[str] = None
    delta_summary: str = ""
    retry_count: int = 0
    latency_seconds: float = 0.0


class BaseStage(ABC):
    """Contrato base para execução de um estágio do pipeline."""

    def __init__(self, stage_id: str, stage_version: str = "0.1.0", prompt_filename: Optional[str] = None):
        self.stage_id = stage_id
        self.stage_version = stage_version
        self.prompt_filename = prompt_filename

    def load_prompt_template(self) -> str:
        if not self.prompt_filename:
            return ""
        prompt_path = PROMPTS_DIR / self.prompt_filename
        if not prompt_path.exists():
            raise FileNotFoundError(f"Arquivo de prompt não encontrado: {prompt_path}")
        return prompt_path.read_text(encoding="utf-8")

    @abstractmethod
    def build_prompt_context(self, state: SimpleIdeaState) -> str:
        """Monta o texto de entrada do prompt a partir do estado atual."""
        pass

    @abstractmethod
    def get_output_schema(self) -> Type[T]:
        """Retorna o schema Pydantic esperado para a saída deste estágio."""
        pass

    @abstractmethod
    def apply_output_to_state(self, state: SimpleIdeaState, output: T) -> str:
        """Aplica o output estruturado sobre o estado e retorna um resumo do delta."""
        pass

    def execute(self, state: SimpleIdeaState, runner: ModelRunner, model_name: Optional[str] = None) -> StageExecutionResult:
        prompt_text = self.build_prompt_context(state)
        output_schema = self.get_output_schema()

        response: ModelResponse = runner.generate(
            prompt_text=prompt_text,
            output_schema=output_schema,
            stage_name=self.stage_id,
            model_name=model_name,
            max_repairs=1,
        )

        if response.error or response.parsed is None:
            state.record_stage_execution(
                stage_id=self.stage_id,
                stage_version=self.stage_version,
                provider=response.provider,
                model=response.model,
                success=False,
                retry_count=response.retry_count,
                delta_summary=f"FALHA: {response.error}",
            )
            return StageExecutionResult(
                stage_id=self.stage_id,
                stage_version=self.stage_version,
                success=False,
                raw_response=response.raw_text,
                error=response.error,
                retry_count=response.retry_count,
                latency_seconds=response.latency_seconds,
            )

        delta_summary = self.apply_output_to_state(state, response.parsed)
        state.record_stage_execution(
            stage_id=self.stage_id,
            stage_version=self.stage_version,
            provider=response.provider,
            model=response.model,
            success=True,
            retry_count=response.retry_count,
            delta_summary=delta_summary,
        )

        return StageExecutionResult(
            stage_id=self.stage_id,
            stage_version=self.stage_version,
            success=True,
            output=response.parsed,
            raw_response=response.raw_text,
            delta_summary=delta_summary,
            retry_count=response.retry_count,
            latency_seconds=response.latency_seconds,
        )
