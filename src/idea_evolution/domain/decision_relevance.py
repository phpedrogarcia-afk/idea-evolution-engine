"""
src/idea_evolution/domain/decision_relevance.py
Tipos, Enums e Políticas Determinísticas de Relevância Decisória, Estágio de Ideia,
Guarda de Falsa Precisão e Arbitragem de Próximo Passo (FIOIDEIAS-V1.1-RQ-01).

Invariantes Centrais:
1. SEVERITY != PRIORITY (Uma vulnerabilidade HIGH em estágio inicial permanece HIGH em severidade,
   mas sua relevância para a decisão imediata pode ser LATER).
2. FOCUSED_ESCALATION_CAN_UNILATERALLY_OVERRIDE_NEXT_ACTION = FALSE.
3. PRODUCT_REFINEMENT != ENGINEERING_REQUIREMENT (Segurança/criptografia não mutam hipótese de produto).
4. FALSE_PRECISION_GUARD: Afirmações numéricas sem evidência são rebaixadas a MEASUREMENT_REQUIRED ou UNKNOWN.
5. Custo de chamadas de IA = 0 (Toda a política é estritamente determinística).
"""

from __future__ import annotations
import re
from enum import Enum
from typing import List, Optional, Tuple, Any
from pydantic import BaseModel, Field

from src.idea_evolution.domain.state import PromotionAuthorityBasis


class IdeaStage(str, Enum):
    """Idea evolution stage."""
    DISCOVERY = "DISCOVERY"
    VALIDATION = "VALIDATION"
    PROTOTYPE = "PROTOTYPE"
    MVP = "MVP"
    PRE_PRODUCTION = "PRE_PRODUCTION"
    PRODUCTION = "PRODUCTION"
    SCALE = "SCALE"
    UNKNOWN = "UNKNOWN"


class RiskCategory(str, Enum):
    """Ontological risk category."""
    MARKET = "MARKET"
    USER_BEHAVIOR = "USER_BEHAVIOR"
    BUSINESS_MODEL = "BUSINESS_MODEL"
    PRODUCT = "PRODUCT"
    TECHNICAL_FEASIBILITY = "TECHNICAL_FEASIBILITY"
    SECURITY = "SECURITY"
    PRIVACY = "PRIVACY"
    COMPLIANCE = "COMPLIANCE"
    OPERATIONS = "OPERATIONS"
    UNKNOWN = "UNKNOWN"


class DecisionRelevance(str, Enum):
    """Ordinal decision relevance for immediate next step."""
    CRITICAL_NOW = "CRITICAL_NOW"
    HIGH_NOW = "HIGH_NOW"
    LATER = "LATER"
    NOT_DECISION_RELEVANT_NOW = "NOT_DECISION_RELEVANT_NOW"
    UNKNOWN = "UNKNOWN"


class AlternativeCategory(str, Enum):
    """Alternative classification."""
    DIRECT_COMPETITOR = "DIRECT_COMPETITOR"
    SUBSTITUTE = "SUBSTITUTE"
    STATUS_QUO = "STATUS_QUO"
    DO_NOTHING = "DO_NOTHING"
    OTHER = "OTHER"


class NumericBasis(str, Enum):
    """Declared authority basis for quantitative metrics."""
    USER_SUPPLIED = "USER_SUPPLIED"
    DETERMINISTIC_CALCULATION = "DETERMINISTIC_CALCULATION"
    MEASURED = "MEASURED"
    EXTERNAL_EVIDENCE = "EXTERNAL_EVIDENCE"
    EXPLICIT_HYPOTHESIS = "EXPLICIT_HYPOTHESIS"
    UNSUPPORTED = "UNSUPPORTED"
    UNKNOWN = "UNKNOWN"


class FalsificationCriterion(BaseModel):
    """Structured empirical falsification criterion."""
    hypothesis: str
    what_would_kill_it: str
    lowest_cost_discriminating_test: str


class EngineeringRequirement(BaseModel):
    """
    Requisito técnico, de segurança ou de conformidade.
    Não muta o refinamento da proposta de produto no estágio de descoberta.
    """
    requirement: str
    category: RiskCategory = RiskCategory.UNKNOWN
    why_needed: str = ""
    stage_applicability: IdeaStage = IdeaStage.PRE_PRODUCTION
    is_non_functional: bool = True


class FalsePrecisionGuard:
    """
    Guarda determinístico contra falsa precisão numérica sem evidência declarada.
    Detecta métricas quantitativas (ex: '<200 ms', '99.99%', '50ms') não fundamentadas.
    """

    METRIC_PATTERN = re.compile(
        r"(?:<\s*\d+(?:\.\d+)?\s*(?:ms|s|%|min|h)|"
        r"\b\d+(?:\.\d+)?\s*(?:ms|s|%|bps|kbps|mbps)\b|"
        r"\b99\.\d+%\b)",
        re.IGNORECASE
    )

    SECURITY_TECH_TERMS = [
        "e2ee", "end-to-end encryption", "criptografia ponta a ponta",
        "aes-256", "aes256", "tls 1.3", "tls1.3", "certificate pinning",
        "zero-knowledge", "hsm", "sha-256"
    ]

    @classmethod
    def detect_unsupported_metrics(cls, text: str, source_text: str = "") -> List[str]:
        """Detecta números ou métricas de precisão que não constam da fonte humana original."""
        matches = cls.METRIC_PATTERN.findall(text)
        unsupported = []
        for m in matches:
            clean_m = m.strip()
            # Se não consta literalmente da ideia humana original, é não suportado
            if source_text and clean_m.lower() in source_text.lower():
                continue
            unsupported.append(clean_m)
        return unsupported

    @classmethod
    def sanitize_unsupported_precision(cls, text: str, source_text: str = "") -> Tuple[str, bool]:
        """
        Rebaixa asserções numéricas de precisão não suportadas para anotações de medição requerida.
        Retorna (texto_sanitizado, houve_rebaixamento).
        """
        unsupported = cls.detect_unsupported_metrics(text, source_text)
        if not unsupported:
            return text, False

        sanitized = text
        for m in unsupported:
            sanitized = sanitized.replace(m, f"[MÉTRICA NÃO MEDIDA: medição necessária]")
        return sanitized, True


class DecisionRelevancePolicy:
    """
    Política determinística de Relevância Decisória (Severity != Priority).
    Determina se uma vulnerabilidade severa tem relevância para o estágio atual da decisão.
    """

    SECURITY_PRIVACY_CATEGORIES = {
        RiskCategory.SECURITY,
        RiskCategory.PRIVACY,
        RiskCategory.COMPLIANCE,
    }

    FATAL_EARLY_CATEGORIES = {
        RiskCategory.USER_BEHAVIOR,
        RiskCategory.MARKET,
        RiskCategory.BUSINESS_MODEL,
        RiskCategory.PRODUCT,
        RiskCategory.TECHNICAL_FEASIBILITY,
    }

    SECURITY_KEYWORDS = [
        "segurança", "security", "privacidade", "privacy", "lgpd",
        "criptografia", "encryption", "vazamento", "e2ee", "aes", "tls",
        "compliance", "conformidade", "dados sensíveis"
    ]

    USER_SECURITY_REQUEST_KEYWORDS = [
        "segurança", "privacidade", "lgpd", "criptografia", "security",
        "vazamento", "auditoria de segurança", "proteger dados"
    ]

    @classmethod
    def is_user_explicit_security_request(cls, original_idea: str) -> bool:
        """Verifica se o usuário humano explicitamente solicitou análise ou foco em segurança."""
        lower_idea = original_idea.lower()
        return any(kw in lower_idea for kw in cls.USER_SECURITY_REQUEST_KEYWORDS)

    @classmethod
    def infer_category(cls, vulnerability_text: str, declared_category: RiskCategory) -> RiskCategory:
        """Inferência determinística de categoria se UNKNOWN."""
        if declared_category != RiskCategory.UNKNOWN:
            return declared_category
        text_lower = vulnerability_text.lower()
        if any(kw in text_lower for kw in cls.SECURITY_KEYWORDS):
            return RiskCategory.SECURITY
        if any(kw in text_lower for kw in ["abandono", "adesão", "retenção", "fadiga", "hábito", "disciplina"]):
            return RiskCategory.USER_BEHAVIOR
        if any(kw in text_lower for kw in ["pagar", "preço", "disposição a pagar", "monetização", "custo", "margem"]):
            return RiskCategory.BUSINESS_MODEL
        if any(kw in text_lower for kw in ["mercado", "concorrente", "substituto", "nicho", "tamanho"]):
            return RiskCategory.MARKET
        if any(kw in text_lower for kw in ["viabilidade", "impossível", "api", "hardware", "bloqueio técnico"]):
            return RiskCategory.TECHNICAL_FEASIBILITY
        return RiskCategory.PRODUCT

    @classmethod
    def evaluate_vulnerability_relevance(
        cls,
        vulnerability_text: str,
        severity: str,
        category: RiskCategory,
        stage: IdeaStage,
        original_idea: str,
        explicit_relevance: DecisionRelevance = DecisionRelevance.UNKNOWN,
    ) -> DecisionRelevance:
        """
        Avalia deterministicamente a relevância decisória AGORA de uma vulnerabilidade.
        Regra fundamental:
        - Em DISCOVERY/VALIDATION: Segurança/Privacidade HIGH -> LATER (salvo pedido do usuário).
        - Em DISCOVERY/VALIDATION: Usabilidade fatal / Desistência / Rejeição de modelo -> CRITICAL_NOW.
        - Em PRE_PRODUCTION/PRODUCTION: Segurança/Privacidade HIGH -> CRITICAL_NOW.
        """
        sev_upper = severity.upper()
        if sev_upper not in ("HIGH", "CRITICAL"):
            return DecisionRelevance.LATER

        # Se o usuário pediu explicitamente segurança, torna-se prioridade agora
        if cls.is_user_explicit_security_request(original_idea):
            effective_cat = cls.infer_category(vulnerability_text, category)
            if effective_cat in cls.SECURITY_PRIVACY_CATEGORIES:
                return DecisionRelevance.CRITICAL_NOW

        effective_category = cls.infer_category(vulnerability_text, category)

        # Se o chamador já definiu explicitamente uma relevância válida
        if explicit_relevance not in (DecisionRelevance.UNKNOWN, None):
            return explicit_relevance

        # Avaliação por estágio
        if stage in (IdeaStage.DISCOVERY, IdeaStage.VALIDATION, IdeaStage.UNKNOWN):
            if effective_category in cls.SECURITY_PRIVACY_CATEGORIES:
                # Invariante: Em discovery, segurança é severa, mas seu aluguel decisório imediato é LATER
                return DecisionRelevance.LATER
            if effective_category in cls.FATAL_EARLY_CATEGORIES:
                return DecisionRelevance.CRITICAL_NOW
            return DecisionRelevance.HIGH_NOW

        elif stage in (IdeaStage.PROTOTYPE, IdeaStage.MVP):
            if effective_category in cls.SECURITY_PRIVACY_CATEGORIES:
                return DecisionRelevance.HIGH_NOW
            return DecisionRelevance.CRITICAL_NOW

        elif stage in (IdeaStage.PRE_PRODUCTION, IdeaStage.PRODUCTION, IdeaStage.SCALE):
            # No estágio pré-produção, falhas graves de segurança são CRITICAL_NOW
            if effective_category in cls.SECURITY_PRIVACY_CATEGORIES:
                return DecisionRelevance.CRITICAL_NOW
            return DecisionRelevance.HIGH_NOW

        return DecisionRelevance.LATER

    @classmethod
    def is_engineering_security_override(cls, candidate_text: str, original_mechanism: str) -> bool:
        """
        Verifica se uma hipótese mutada ou proposta substitui a função de produto
        por uma arquitetura puramente técnica de criptografia/segurança (E2EE, AES, TLS).
        """
        cand_lower = candidate_text.lower()
        orig_lower = original_mechanism.lower()

        # Se menciona múltiplos termos de segurança/criptografia
        tech_hits = sum(1 for term in FalsePrecisionGuard.SECURITY_TECH_TERMS if term in cand_lower)
        if tech_hits >= 1:
            # Se a ideia original não era sobre segurança (ex: era sobre cotações esquecidas no WhatsApp)
            # e a nova descrição transformou o mecanismo em 'arquitetura de criptografia'
            if not any(term in orig_lower for term in FalsePrecisionGuard.SECURITY_TECH_TERMS):
                return True
        return False


class NextActionArbitrationPolicy:
    """
    Política determinística de arbitragem de próximo passo recomendado.
    Invariante: FOCUSED_ESCALATION_CAN_UNILATERALLY_OVERRIDE_NEXT_ACTION = FALSE.
    """

    TECHNICAL_IMPLEMENTATION_KEYWORDS = [
        "implementar criptografia", "desenvolver e2ee", "configurar tls",
        "implementar aes", "arquitetura de segurança", "certificate pinning",
        "desenvolver backend seguro", "implementar autenticação mfa"
    ]

    @classmethod
    def arbitrate(
        cls,
        first_pass_next_action: str,
        escalation_candidate_next_action: Optional[str],
        stage: IdeaStage,
        original_idea: str,
        requires_human_decision: bool = False,
        human_decision_description: Optional[str] = None,
    ) -> Tuple[str, bool]:
        """
        Arbitra deterministicamente o próximo passo final.
        Retorna (next_action_final, next_action_foi_alterada).
        """
        # 1. Se requer decisão humana normativa soberana
        if requires_human_decision:
            desc = human_decision_description or "Decisão normativa de valor humano necessária antes de avançar."
            return f"Decisão humana requerida: {desc}", False

        # 2. Se não houve escalação ou candidato está vazio
        if not escalation_candidate_next_action or not escalation_candidate_next_action.strip():
            fallback = first_pass_next_action or "Validar proposta inicial com o usuário."
            return fallback, False

        candidate = escalation_candidate_next_action.strip()
        first_pass = first_pass_next_action.strip()

        # Se forem idênticos, sem mudança
        if candidate.lower() == first_pass.lower():
            return first_pass, False

        # 3. Em DISCOVERY ou VALIDATION:
        if stage in (IdeaStage.DISCOVERY, IdeaStage.VALIDATION, IdeaStage.UNKNOWN):
            cand_lower = candidate.lower()

            # Se a escalação tentar propor implementação técnica/segurança precoce
            # sem que o usuário tenha pedido segurança explicitamente
            if not DecisionRelevancePolicy.is_user_explicit_security_request(original_idea):
                if any(kw in cand_lower for kw in cls.TECHNICAL_IMPLEMENTATION_KEYWORDS):
                    # Rejeita o override unilateral da escalação!
                    # Mantém o próximo passo de falseamento de descoberta da primeira passada
                    return first_pass, False

        # 4. Se o candidato for um teste discriminativo válido ou resolver blocker atual do estágio
        return candidate, True
