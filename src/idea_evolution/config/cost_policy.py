"""
src/idea_evolution/config/cost_policy.py
Governança de Custos, Fronteira de Provedor e Guarda Fail-Closed para FioIdeias V1 (M06 P4).

Implementa a política inegociável de custo de bolso zero (OUT_OF_POCKET_COST = ZERO),
separação estrita entre modelo científico e modelo de transporte,
e salvaguardas fail-closed contra rotas tarifadas ou desconhecidas.
"""

from __future__ import annotations

import re
from enum import Enum
from typing import Optional, Dict, Any, Tuple
from pydantic import BaseModel, Field

from src.idea_evolution.config.catalog import ModelCatalog, CostClass, CostPolicy


class CostEligibility(str, Enum):
    """Status formal de elegibilidade financeira da rota de inferência."""
    FREE = "FREE"
    FREE_TRIAL = "FREE_TRIAL"
    CREDIT_COVERED = "CREDIT_COVERED"
    PAID = "PAID"
    UNKNOWN = "UNKNOWN"


class ProviderConfig(BaseModel):
    """
    Configuração e metadados operacionais de provedor para execução de produto.
    Desacopla semântica de aplicação do transporte físico e da rota de custo.
    """
    provider: str
    transport_model: str
    scientific_model: str = ""
    cost_eligibility: CostEligibility = CostEligibility.FREE
    paid_inference_allowed: bool = False  # Em V1: SEMPRE False por padrão
    structured_output_required: bool = True
    max_retries: int = 0  # Sem retries ocultos na camada de transporte
    base_url: Optional[str] = None
    api_key_env_var: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def model_post_init(self, __context: Any) -> None:
        if not self.scientific_model:
            self.scientific_model = self.transport_model

    @classmethod
    def infer_from_runner(
        cls,
        runner: Any,
        model_name: Optional[str] = None,
        catalog: Optional[ModelCatalog] = None,
    ) -> ProviderConfig:
        """Infere deterministicamente a configuração de provedor a partir do runner e catálogo."""
        runner_cls_name = type(runner).__name__.lower()
        provider = getattr(runner, "provider", None)
        if not provider:
            if "cerebras" in runner_cls_name:
                provider = "cerebras"
            elif "fake" in runner_cls_name:
                provider = "fake"
            elif "native" in runner_cls_name:
                provider = getattr(runner, "provider_name", "unknown")
            else:
                provider = "unknown"

        transport_model = (
            model_name
            or getattr(runner, "model_name", None)
            or getattr(runner, "default_model", None)
            or "unknown"
        )

        scientific_model = transport_model
        if provider == "cerebras":
            if transport_model in ("gpt-oss-120b", "openai/gpt-oss-120b"):
                transport_model = "gpt-oss-120b"
                scientific_model = "openai/gpt-oss-120b"

        if provider.startswith("fake"):
            return cls(
                provider=provider,
                transport_model=transport_model,
                scientific_model=scientific_model,
                cost_eligibility=CostEligibility.FREE,
                paid_inference_allowed=False,
                structured_output_required=True,
                max_retries=0,
            )

        cat = catalog or ModelCatalog()
        entry = cat.get_entry(provider, transport_model)
        if not entry and scientific_model != transport_model:
            entry = cat.get_entry(provider, scientific_model)

        if entry:
            if entry.cost_class in (CostClass.FREE_TIER, CostClass.FREE_ROUTER, CostClass.LOCAL_ZERO_MARGINAL_API_COST):
                eligibility = CostEligibility.FREE
            elif entry.cost_class == CostClass.PROMOTIONAL_CREDIT:
                eligibility = CostEligibility.CREDIT_COVERED
            elif entry.cost_class == CostClass.PAID:
                eligibility = CostEligibility.PAID
            else:
                eligibility = CostEligibility.UNKNOWN

            return cls(
                provider=provider,
                transport_model=transport_model,
                scientific_model=scientific_model,
                cost_eligibility=eligibility,
                paid_inference_allowed=False,
                structured_output_required=entry.capabilities.structured_output,
                max_retries=0,
            )

        return cls(
            provider=provider,
            transport_model=transport_model,
            scientific_model=scientific_model,
            cost_eligibility=CostEligibility.UNKNOWN,
            paid_inference_allowed=False,
            structured_output_required=True,
            max_retries=0,
        )


class CostPolicyViolationError(RuntimeError):
    """Exceção levantada quando uma rota viola a política de custo zero."""
    pass


class StructuredOutputRequirementError(RuntimeError):
    """Exceção levantada quando um modelo não suporta structured outputs estritos."""
    pass


def sanitize_secret_text(text: str) -> str:
    """
    Sanitiza strings, mensagens de erro e payloads, mascarando quaisquer
    chaves de API, tokens Bearer, senhas ou segredos detectados.
    """
    if not text:
        return ""
    sanitized = text
    # Cerebras: csk-...
    sanitized = re.sub(r"csk-[A-Za-z0-9_\-]+", "csk-***", sanitized)
    # Groq: gsk_...
    sanitized = re.sub(r"gsk_[A-Za-z0-9_\-]+", "gsk-***", sanitized)
    # NVIDIA NIM: nvapi-...
    sanitized = re.sub(r"nvapi-[A-Za-z0-9_\-]+", "nvapi-***", sanitized)
    # OpenAI/Gerais: sk-...
    sanitized = re.sub(r"sk-[A-Za-z0-9_\-]+", "sk-***", sanitized)
    # Bearer tokens
    sanitized = re.sub(r"Bearer\s+[A-Za-z0-9_\.\-]+", "Bearer ***", sanitized, flags=re.IGNORECASE)
    # Parâmetros com api_key ou token
    sanitized = re.sub(
        r"(api[_\-]?key|token|password|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\.\-]+['\"]?",
        r"\1=***",
        sanitized,
        flags=re.IGNORECASE,
    )
    return sanitized


class ZeroCostGuard:
    """
    Guarda determinístico de Custo Zero para FioIdeias V1.
    Bloqueia categoricamente (fail-closed) inferência paga ou rotas de custo desconhecido.
    """

    @classmethod
    def validate_provider_config(
        cls,
        config: ProviderConfig,
        catalog: Optional[ModelCatalog] = None,
    ) -> Tuple[bool, Optional[str]]:
        """
        Valida a configuração do provedor sob a política de custo zero e requisitos de capacidade.
        Retorna (True, None) se aprovado, ou (False, motivo) se bloqueado.
        """
        # 1. Trava contra permissão explícita de inferência paga em FioIdeias V1
        if config.paid_inference_allowed:
            return (
                False,
                "PAID_INFERENCE_BLOCKED: Chamadas a modelos pagos violam a política Zero-Cost do FioIdeias V1."
            )

        # 2. Custo desconhecido DEVE falhar fechado (fail-closed)
        if config.cost_eligibility == CostEligibility.UNKNOWN:
            return (
                False,
                "UNKNOWN_COST_FAIL_CLOSED: Provedor ou modelo com custo desconhecido. Operação bloqueada em modo fail-closed."
            )

        # 3. Modelos declarados como PAID são estritamente proibidos
        if config.cost_eligibility == CostEligibility.PAID:
            return (
                False,
                "COST_POLICY_BLOCKED: Modelo de classe tarifada/paga não permitido sob a política Zero-Cost."
            )

        # 4. Classes aceitas: FREE, FREE_TRIAL, CREDIT_COVERED
        allowed_eligibilities = {
            CostEligibility.FREE,
            CostEligibility.FREE_TRIAL,
            CostEligibility.CREDIT_COVERED,
        }
        if config.cost_eligibility not in allowed_eligibilities:
            return (
                False,
                f"COST_POLICY_BLOCKED: Elegibilidade de custo inválida ou não autorizada: {config.cost_eligibility.value}"
            )

        # 5. Validação contra o Catálogo Vivo (se disponível)
        if catalog is not None:
            # Provedores de teste determinístico local sempre passam
            if not config.provider.lower().startswith("fake"):
                entry = catalog.get_entry(config.provider, config.transport_model)
                if not entry and config.scientific_model:
                    entry = catalog.get_entry(config.provider, config.scientific_model)

                if entry is not None:
                    if entry.cost_class in (CostClass.PAID, CostClass.UNKNOWN):
                        return (
                            False,
                            f"COST_POLICY_BLOCKED: O modelo '{config.provider}/{config.transport_model}' "
                            f"está catalogado como '{entry.cost_class.value}' e requer pagamento direto."
                        )
                    if config.structured_output_required and not entry.capabilities.structured_output:
                        return (
                            False,
                            f"STRUCTURED_OUTPUT_NOT_SUPPORTED: O modelo '{config.provider}/{config.transport_model}' "
                            f"não oferece suporte garantido a Structured Outputs estritos."
                        )
                else:
                    # Modelo não encontrado no catálogo vivo e não é fake
                    return (
                        False,
                        f"UNKNOWN_COST_FAIL_CLOSED: O modelo '{config.provider}/{config.transport_model}' "
                        f"não consta no catálogo vivo de modelos autorizados. Fail-closed obrigatório."
                    )

        return True, None

    @classmethod
    def ensure_zero_cost(
        cls,
        config: ProviderConfig,
        catalog: Optional[ModelCatalog] = None,
    ) -> None:
        """Versão assertiva que levanta exceção específica se violar a política."""
        is_valid, reason = cls.validate_provider_config(config, catalog)
        if not is_valid:
            if "STRUCTURED_OUTPUT" in (reason or ""):
                raise StructuredOutputRequirementError(reason or "Requisito de Structured Output não satisfeito.")
            raise CostPolicyViolationError(reason or "Violação da política de governança de custo.")
