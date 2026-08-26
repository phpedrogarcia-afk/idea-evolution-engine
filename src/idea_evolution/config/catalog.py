"""
src/idea_evolution/config/catalog.py
Catálogo vivo de modelos, governança de custos e políticas de ciclo de vida (M06.1).
"""

from __future__ import annotations
import json
from pathlib import Path
from enum import Enum
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field


class CostClass(str, Enum):
    FREE_TIER = "FREE_TIER"
    FREE_ROUTER = "FREE_ROUTER"
    LOCAL_ZERO_MARGINAL_API_COST = "LOCAL_ZERO_MARGINAL_API_COST"
    PROMOTIONAL_CREDIT = "PROMOTIONAL_CREDIT"
    PAID = "PAID"
    UNKNOWN = "UNKNOWN"


class LifecycleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PREVIEW = "PREVIEW"
    DEPRECATED = "DEPRECATED"
    SHUT_DOWN = "SHUT_DOWN"
    UNKNOWN = "UNKNOWN"


class PrivacyClass(str, Enum):
    STANDARD_PRIVACY = "STANDARD_PRIVACY"
    PROVIDER_MAY_USE_FOR_PRODUCT_IMPROVEMENT = "PROVIDER_MAY_USE_FOR_PRODUCT_IMPROVEMENT"
    AIR_GAPPED_LOCAL = "AIR_GAPPED_LOCAL"
    UNKNOWN = "UNKNOWN"


class CostPolicy(str, Enum):
    FREE_ONLY = "FREE_ONLY"
    ALLOW_PROMOTIONAL = "ALLOW_PROMOTIONAL"
    ALLOW_PAID_WITH_BUDGET = "ALLOW_PAID_WITH_BUDGET"


class ExecutionMode(str, Enum):
    EXPERIMENTAL_PINNED = "EXPERIMENTAL_PINNED"  # Modo experimento M05: modelo fixo, sem auto-fallback
    FREE_POOL_OPERATIONAL = "FREE_POOL_OPERATIONAL"  # Modo operacional: tenta próximo free elegível apenas se cota esgotar


class ModelCapabilities(BaseModel):
    structured_output: bool = True
    reasoning: bool = True
    context_window: Optional[int] = None


class ModelCatalogEntry(BaseModel):
    provider: str
    model_id: str
    status: LifecycleStatus = LifecycleStatus.ACTIVE
    capabilities: ModelCapabilities = Field(default_factory=ModelCapabilities)
    cost_class: CostClass = CostClass.FREE_TIER
    free_capacity_type: str = "daily_quota"  # daily_quota, rate_limit_only, none, unlimited
    privacy_class: PrivacyClass = PrivacyClass.STANDARD_PRIVACY
    last_verified: str = "2026-08-26"
    verification_source: str = "official_provider_docs"
    replacement_if_deprecated: Optional[str] = None


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
CATALOG_PATH = REPO_ROOT / "config" / "model_catalog.json"


class ModelCatalog:
    """Gerenciador central do catálogo de modelos do IEE."""

    def __init__(self, entries: Optional[Dict[str, ModelCatalogEntry]] = None):
        self.entries = entries or self._load_default_seed()

    def _load_default_seed(self) -> Dict[str, ModelCatalogEntry]:
        if CATALOG_PATH.exists():
            try:
                data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
                res = {}
                for item in data.get("models", []):
                    entry = ModelCatalogEntry.model_validate(item)
                    key = f"{entry.provider.lower()}:{entry.model_id}"
                    res[key] = entry
                return res
            except Exception:
                pass
        return self._get_fallback_seed()

    def _get_fallback_seed(self) -> Dict[str, ModelCatalogEntry]:
        seed_list = [
            # Groq
            ModelCatalogEntry(
                provider="groq",
                model_id="openai/gpt-oss-120b",
                status=LifecycleStatus.ACTIVE,
                cost_class=CostClass.FREE_TIER,
                free_capacity_type="1000_req_day_200k_tokens",
                last_verified="2026-08-26",
                verification_source="GroqCloud Models API & Free Plan Docs",
            ),
            ModelCatalogEntry(
                provider="groq",
                model_id="qwen/qwen3.6-27b",
                status=LifecycleStatus.ACTIVE,
                cost_class=CostClass.FREE_TIER,
                free_capacity_type="1000_req_day_200k_tokens",
                last_verified="2026-08-26",
                verification_source="GroqCloud Models API & Free Plan Docs",
            ),
            ModelCatalogEntry(
                provider="groq",
                model_id="llama-3.3-70b-versatile",
                status=LifecycleStatus.SHUT_DOWN,
                cost_class=CostClass.FREE_TIER,
                replacement_if_deprecated="openai/gpt-oss-120b",
                last_verified="2026-08-26",
                verification_source="GroqCloud Deprecations Notice (August 16, 2026)",
            ),
            # Gemini
            ModelCatalogEntry(
                provider="gemini",
                model_id="gemini-3.7-flash",
                status=LifecycleStatus.ACTIVE,
                cost_class=CostClass.FREE_TIER,
                privacy_class=PrivacyClass.PROVIDER_MAY_USE_FOR_PRODUCT_IMPROVEMENT,
                last_verified="2026-08-26",
                verification_source="Google AI Studio Pricing & Docs",
            ),
            ModelCatalogEntry(
                provider="gemini",
                model_id="gemini-3.6-flash",
                status=LifecycleStatus.ACTIVE,
                cost_class=CostClass.FREE_TIER,
                privacy_class=PrivacyClass.PROVIDER_MAY_USE_FOR_PRODUCT_IMPROVEMENT,
                last_verified="2026-08-26",
                verification_source="Google AI Studio Pricing & Docs",
            ),
            ModelCatalogEntry(
                provider="gemini",
                model_id="gemini-3.1-flash-lite",
                status=LifecycleStatus.ACTIVE,
                cost_class=CostClass.FREE_TIER,
                privacy_class=PrivacyClass.PROVIDER_MAY_USE_FOR_PRODUCT_IMPROVEMENT,
                last_verified="2026-08-26",
                verification_source="Google AI Studio Pricing & Docs",
            ),
            ModelCatalogEntry(
                provider="gemini",
                model_id="gemini-2.0-flash",
                status=LifecycleStatus.SHUT_DOWN,
                cost_class=CostClass.FREE_TIER,
                replacement_if_deprecated="gemini-3.7-flash",
                last_verified="2026-08-26",
                verification_source="Google AI Deprecations Notice (June 1, 2026)",
            ),
            # OpenAI
            ModelCatalogEntry(
                provider="openai",
                model_id="gpt-4o-mini",
                status=LifecycleStatus.ACTIVE,
                cost_class=CostClass.PAID,
                free_capacity_type="none",
                last_verified="2026-08-26",
                verification_source="OpenAI Platform Pricing",
            ),
            # Anthropic
            ModelCatalogEntry(
                provider="anthropic",
                model_id="claude-3-5-haiku-20241022",
                status=LifecycleStatus.ACTIVE,
                cost_class=CostClass.PROMOTIONAL_CREDIT,
                free_capacity_type="signup_credit_only",
                last_verified="2026-08-26",
                verification_source="Anthropic Platform Pricing",
            ),
            # OpenRouter Free
            ModelCatalogEntry(
                provider="openrouter",
                model_id="openrouter/free",
                status=LifecycleStatus.ACTIVE,
                cost_class=CostClass.FREE_ROUTER,
                free_capacity_type="50_req_day",
                last_verified="2026-08-26",
                verification_source="OpenRouter FAQ & Free Tier Docs",
            ),
            # Fake Local
            ModelCatalogEntry(
                provider="fake",
                model_id="default-model",
                status=LifecycleStatus.ACTIVE,
                cost_class=CostClass.LOCAL_ZERO_MARGINAL_API_COST,
                free_capacity_type="unlimited",
                last_verified="2026-08-26",
                verification_source="Internal Local Deterministic Mock",
            ),
        ]
        return {f"{e.provider.lower()}:{e.model_id}": e for e in seed_list}

    def get_entry(self, provider: str, model_id: str) -> Optional[ModelCatalogEntry]:
        key = f"{provider.lower()}:{model_id}"
        if key in self.entries:
            return self.entries[key]
        # Se for um provedor fake dinâmico (ex: fake_a, fake_b)
        if provider.lower().startswith("fake"):
            return ModelCatalogEntry(
                provider=provider.lower(),
                model_id=model_id,
                status=LifecycleStatus.ACTIVE,
                cost_class=CostClass.LOCAL_ZERO_MARGINAL_API_COST,
                free_capacity_type="unlimited",
            )
        return None

    def validate_eligibility(
        self,
        provider: str,
        model_id: str,
        cost_policy: CostPolicy = CostPolicy.FREE_ONLY,
        exclude_product_improvement_use: bool = False,
    ) -> Tuple[bool, str]:
        """
        Valida se o modelo é elegível sob a política de custos e ciclo de vida.
        Retorna (is_eligible, reason).
        """
        entry = self.get_entry(provider, model_id)
        if not entry:
            return False, f"MODEL_UNKNOWN_IN_CATALOG: Modelo '{provider}/{model_id}' não catalogado."

        if entry.status == LifecycleStatus.SHUT_DOWN:
            rep = f" Use '{entry.replacement_if_deprecated}'." if entry.replacement_if_deprecated else ""
            return False, f"MODEL_SHUT_DOWN: O modelo '{provider}/{model_id}' foi encerrado pelo provedor.{rep}"

        if entry.status == LifecycleStatus.DEPRECATED:
            return False, f"MODEL_DEPRECATED: O modelo '{provider}/{model_id}' está descontinuado."

        if exclude_product_improvement_use and entry.privacy_class == PrivacyClass.PROVIDER_MAY_USE_FOR_PRODUCT_IMPROVEMENT:
            return False, f"PRIVACY_POLICY_VIOLATION: O modelo '{provider}/{model_id}' permite uso de dados pelo provedor sob o free tier."

        if cost_policy == CostPolicy.FREE_ONLY:
            allowed_classes = {
                CostClass.FREE_TIER,
                CostClass.FREE_ROUTER,
                CostClass.LOCAL_ZERO_MARGINAL_API_COST,
            }
            if entry.cost_class not in allowed_classes:
                return False, f"COST_POLICY_VIOLATION: O modelo '{provider}/{model_id}' tem classe '{entry.cost_class.value}' e não é gratuito sob a política FREE_ONLY."

        if cost_policy == CostPolicy.ALLOW_PROMOTIONAL:
            allowed_classes = {
                CostClass.FREE_TIER,
                CostClass.FREE_ROUTER,
                CostClass.LOCAL_ZERO_MARGINAL_API_COST,
                CostClass.PROMOTIONAL_CREDIT,
            }
            if entry.cost_class not in allowed_classes:
                return False, f"COST_POLICY_VIOLATION: O modelo '{provider}/{model_id}' requer pagamento direto."

        return True, "ELIGIBLE"

    def get_eligible_free_fallbacks(self, provider: str, exclude_model: str) -> List[ModelCatalogEntry]:
        """Retorna candidatos gratuitos elegíveis ativos para um provedor específico."""
        res = []
        for entry in self.entries.values():
            if entry.provider.lower() == provider.lower() and entry.model_id != exclude_model:
                if entry.status == LifecycleStatus.ACTIVE and entry.cost_class in [CostClass.FREE_TIER, CostClass.FREE_ROUTER]:
                    res.append(entry)
        return res
