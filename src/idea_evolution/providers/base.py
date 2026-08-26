"""
src/idea_evolution/providers/base.py
Interface e Tipos Base para Abstração de Executores de Modelos (ModelRunner).
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type, TypeVar, Optional, Dict, Any
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class ModelUsage(BaseModel):
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    cost_usd: Optional[float] = None


class ModelResponse(BaseModel):
    parsed: Optional[Any] = None
    raw_text: str
    provider: str
    model: str
    usage: ModelUsage = ModelUsage()
    latency_seconds: float = 0.0
    retry_count: int = 0
    error: Optional[str] = None
    failed_generation: Optional[str] = None


class ModelRunner(ABC):
    """Interface abstrata para execução de estágios sobre LLMs ou Fakes."""

    @abstractmethod
    def generate(
        self,
        prompt_text: str,
        output_schema: Type[T],
        stage_name: str,
        model_name: Optional[str] = None,
        max_repairs: int = 1,
    ) -> ModelResponse:
        """Executa a inferência e valida contra o schema Pydantic fornecido."""
        pass
