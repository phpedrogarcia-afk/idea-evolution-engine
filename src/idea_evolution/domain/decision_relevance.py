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


class RequirementType(str, Enum):
    """Ontologia tipada de requisitos e alegações."""
    PRODUCT_HYPOTHESIS = "PRODUCT_HYPOTHESIS"
    PRODUCT_REQUIREMENT = "PRODUCT_REQUIREMENT"
    ENGINEERING_REQUIREMENT = "ENGINEERING_REQUIREMENT"
    SECURITY_REQUIREMENT = "SECURITY_REQUIREMENT"
    COMPLIANCE_REQUIREMENT = "COMPLIANCE_REQUIREMENT"
    OPERATIONAL_REQUIREMENT = "OPERATIONAL_REQUIREMENT"


NON_PRODUCT_IMPLEMENTATION_TYPES = frozenset({
    RequirementType.ENGINEERING_REQUIREMENT,
    RequirementType.SECURITY_REQUIREMENT,
    RequirementType.COMPLIANCE_REQUIREMENT,
    RequirementType.OPERATIONAL_REQUIREMENT,
})


class StageProvenanceBasis(str, Enum):
    """Proveniência epistêmica da classificação do estágio da ideia."""
    USER_EXPLICIT_CURRENT_STAGE = "USER_EXPLICIT_CURRENT_STAGE"
    SOURCE_SUPPORTED_INFERENCE = "SOURCE_SUPPORTED_INFERENCE"
    MODEL_INFERENCE = "MODEL_INFERENCE"
    UNKNOWN = "UNKNOWN"


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


class IdeaStageAssessment(BaseModel):
    """
    Avaliação fundamentada do estágio atual de maturidade da ideia.
    Garante que MENTIONED_FUTURE_STAGE != CURRENT_IDEA_STAGE e
    MODEL_STAGE_INFERENCE != USER_EXPLICIT_STAGE.
    """
    current_stage: IdeaStage = IdeaStage.UNKNOWN
    basis: StageProvenanceBasis = StageProvenanceBasis.UNKNOWN
    justification: str = ""
    mentioned_future_stages: List[IdeaStage] = Field(default_factory=list)


class RiskCategory(str, Enum):
    """Ontological risk category."""
    MARKET = "MARKET"
    USER_BEHAVIOR = "USER_BEHAVIOR"
    BUSINESS_MODEL = "BUSINESS_MODEL"
    PRODUCT = "PRODUCT"
    TECHNICAL_FEASIBILITY = "TECHNICAL_FEASIBILITY"
    ENGINEERING = "ENGINEERING"
    SECURITY = "SECURITY"
    PRIVACY = "PRIVACY"
    COMPLIANCE = "COMPLIANCE"
    OPERATIONS = "OPERATIONS"
    UNKNOWN = "UNKNOWN"


NON_PRODUCT_RISK_CATEGORIES = frozenset({
    RiskCategory.ENGINEERING,
    RiskCategory.SECURITY,
    RiskCategory.PRIVACY,
    RiskCategory.COMPLIANCE,
    RiskCategory.OPERATIONS,
})


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
    req_type: RequirementType = RequirementType.ENGINEERING_REQUIREMENT
    category: RiskCategory = RiskCategory.ENGINEERING
    why_needed: str = ""
    stage_applicability: IdeaStage = IdeaStage.PRE_PRODUCTION
    is_non_functional: bool = True


class IdeaStageGroundingPolicy:
    """
    Política determinística de ancoragem do estágio atual da ideia (Seções 9 a 13).
    Invariantes:
    1. MENTIONED_FUTURE_STAGE != CURRENT_IDEA_STAGE
    2. MODEL_STAGE_INFERENCE != USER_EXPLICIT_STAGE
    3. AMBIGUOUS_STAGE -> não fabrica maturidade de pré-produção/produção.
    """

    EXPLICIT_PREPROD_OR_PROD_MARKERS = [
        "produto implementado", "piloto validado", "preparando produção",
        "preparando deploy", "fase final de homologação", "em homologação",
        "rodando em produção", "pre-production", "preparing production deployment",
        "product is implemented", "pilot validated", "validação concluída",
        "já temos clientes ativos", "sistema já construído e testado",
        "preparing production", "fase de pré-produção", "pré-produção"
    ]

    FUTURE_ROADMAP_OR_PENDING_MARKERS = [
        "futuro mvp", "no futuro", "versão futura", "planejamos mvp",
        "pretendemos lançar", "roadmap", "future mvp", "future production",
        "future ai features", "validação pendente", "ainda não validamos",
        "experimento não executado", "ainda não testamos", "validação ainda pendente",
        "ideia inicial", "conceito inicial", "pesquisa exploratória", "precisamos validar",
        "client-zero experiment not yet executed", "client-zero", "cliente zero não executado",
        "validation still pending"
    ]

    @classmethod
    def ground_stage(
        cls,
        declared_stage: IdeaStage,
        declared_justification: str = "",
        source_text: str = "",
        explicit_user_stage: Optional[IdeaStage] = None,
    ) -> IdeaStageAssessment:
        source_lower = (source_text or "").lower()
        just_lower = (declared_justification or "").lower()

        # 1. Se o usuário forneceu estágio explícito via canal soberano
        if explicit_user_stage and explicit_user_stage != IdeaStage.UNKNOWN:
            return IdeaStageAssessment(
                current_stage=explicit_user_stage,
                basis=StageProvenanceBasis.USER_EXPLICIT_CURRENT_STAGE,
                justification="Estágio atual declarado explicitamente pelo usuário humano.",
                mentioned_future_stages=[],
            )

        # 2. Verificar se o texto fonte traz evidência explícita de estágio operacional atual
        is_explicit_preprod = any(m in source_lower for m in cls.EXPLICIT_PREPROD_OR_PROD_MARKERS)
        if is_explicit_preprod:
            target_stage = IdeaStage.PRE_PRODUCTION
            if "rodando em produção" in source_lower or "já em produção" in source_lower:
                target_stage = IdeaStage.PRODUCTION
            return IdeaStageAssessment(
                current_stage=target_stage,
                basis=StageProvenanceBasis.USER_EXPLICIT_CURRENT_STAGE,
                justification="Fonte humana explicita produto implementado e em fase de pré-produção/produção.",
                mentioned_future_stages=[],
            )

        # 3. Detectar menções a estágios futuros em roadmap vs validação pendente
        future_detected: List[IdeaStage] = []
        if any(m in source_lower or m in just_lower for m in ["mvp", "futuro mvp", "future mvp"]):
            future_detected.append(IdeaStage.MVP)
        if any(m in source_lower or m in just_lower for m in ["produção", "future production", "escala", "future ai"]):
            future_detected.append(IdeaStage.PRE_PRODUCTION)

        has_pending_validation = any(m in source_lower or m in just_lower for m in cls.FUTURE_ROADMAP_OR_PENDING_MARKERS)

        # Invariante Central: MENTIONED_FUTURE_STAGE != CURRENT_IDEA_STAGE
        # Se a fonte ou o modelo menciona MVP/produção como aspiração futura ou tem validação pendente,
        # o estágio atual JAMAIS pode ser promovido para MVP, PRE_PRODUCTION ou PRODUCTION!
        if declared_stage in (IdeaStage.MVP, IdeaStage.PRE_PRODUCTION, IdeaStage.PRODUCTION, IdeaStage.SCALE):
            # O modelo propôs estágio avançado, mas a fonte é conceitual ou tem validação pendente
            if not is_explicit_preprod:
                return IdeaStageAssessment(
                    current_stage=IdeaStage.DISCOVERY,
                    basis=StageProvenanceBasis.SOURCE_SUPPORTED_INFERENCE,
                    justification="Menção a estágio futuro em roadmap não promove estágio atual; validação pendente mantém estágio em DISCOVERY.",
                    mentioned_future_stages=future_detected or [declared_stage],
                )

        # 4. Caso comum: DISCOVERY ou VALIDATION fundamentados
        if declared_stage in (IdeaStage.DISCOVERY, IdeaStage.VALIDATION, IdeaStage.PROTOTYPE):
            return IdeaStageAssessment(
                current_stage=declared_stage,
                basis=StageProvenanceBasis.SOURCE_SUPPORTED_INFERENCE if source_text else StageProvenanceBasis.MODEL_INFERENCE,
                justification=declared_justification or "Estágio inicial de descoberta/validação suportado pela fonte.",
                mentioned_future_stages=future_detected,
            )

        # 5. Ambíguo / UNKNOWN
        return IdeaStageAssessment(
            current_stage=IdeaStage.DISCOVERY,  # Conservador para governança (não adquire autoridade de estágio tardio)
            basis=StageProvenanceBasis.UNKNOWN,
            justification="Evidência insuficiente de maturidade operacional; governança preserva restrições de DISCOVERY.",
            mentioned_future_stages=future_detected,
        )


class MetricEvidenceBasis(str, Enum):
    """Bases legítimas de evidência para métricas e números."""
    UNSUPPORTED = "UNSUPPORTED"
    USER_SUPPLIED = "USER_SUPPLIED"
    DETERMINISTIC_CALCULATION = "DETERMINISTIC_CALCULATION"
    MEASURED = "MEASURED"
    EXTERNAL_EVIDENCE = "EXTERNAL_EVIDENCE"
    EXPLICIT_HYPOTHESIS = "EXPLICIT_HYPOTHESIS"


class FalsePrecisionGuard:
    """
    Guarda determinístico contra falsa precisão numérica sem evidência declarada.
    Detecta métricas quantitativas (ex: '<200 ms', '99.9%', 'R$ 12.37', '3.4x', '85% conversion', '50 ms latency')
    sem base de evidência declarada (USER_SUPPLIED, DETERMINISTIC_CALCULATION, MEASURED, EXTERNAL_EVIDENCE, EXPLICIT_HYPOTHESIS).
    """

    METRIC_PATTERNS = [
        r"(?:[<>≤≥~]\s*\d+(?:[\.,]\d+)?\s*(?:ms|s|min|h|%|bps|kbps|mbps|gbps|rps|req/s))",
        r"(?:\b\d+(?:[\.,]\d+)?\s*(?:ms|s|min|h)\b(?:\s+(?:latency|latência))?)",
        r"(?:\b\d+(?:[\.,]\d+)?\s*%(?:\s*(?:conversion|conversão|disponibilidade|uptime|precisão|accuracy|retenção|churn))?)",
        r"(?:(?:R\$|\$|USD|EUR)\s*\d+(?:[\.,]\d{1,2})?|\b\d+(?:[\.,]\d{1,2})\s*(?:reais|dólares|euros|usd|brl|eur)\b)",
        r"(?:\b\d+(?:[\.,]\d+)?x\b)",
    ]
    METRIC_PATTERN = re.compile("|".join(METRIC_PATTERNS), re.IGNORECASE)

    SUPPORTED_CONTEXT_TAGS = {
        MetricEvidenceBasis.DETERMINISTIC_CALCULATION: ["calculado", "determinístico", "calculation", "calculada"],
        MetricEvidenceBasis.MEASURED: ["medido", "medida", "measured", "benchmark", "telemetria"],
        MetricEvidenceBasis.EXTERNAL_EVIDENCE: ["evidência", "external_evidence", "citação", "estudo", "fonte"],
        MetricEvidenceBasis.EXPLICIT_HYPOTHESIS: ["hipótese", "explicit_hypothesis", "meta", "alvo", "estimativa"],
    }

    SECURITY_TECH_TERMS = [
        "e2ee", "end-to-end encryption", "criptografia ponta a ponta",
        "aes-256", "aes256", "tls 1.3", "tls1.3", "certificate pinning",
        "zero-knowledge", "hsm", "sha-256"
    ]

    @classmethod
    def detect_unsupported_metrics(
        cls,
        text: str,
        source_text: str = "",
        evidence_basis: Optional[Union[str, MetricEvidenceBasis]] = None,
    ) -> List[str]:
        """Detecta números ou métricas de precisão que não constam de base de evidência declarada."""
        if evidence_basis:
            basis_str = str(evidence_basis.value if hasattr(evidence_basis, "value") else evidence_basis).upper()
            if basis_str in {
                "USER_SUPPLIED",
                "DETERMINISTIC_CALCULATION",
                "MEASURED",
                "EXTERNAL_EVIDENCE",
                "EXPLICIT_HYPOTHESIS",
            }:
                return []

        text_lower = text.lower()
        for basis_enum, tags in cls.SUPPORTED_CONTEXT_TAGS.items():
            if any(f"[{tag}" in text_lower or f"({tag}" in text_lower for tag in tags):
                return []

        matches = cls.METRIC_PATTERN.findall(text)
        unsupported = []
        for m in matches:
            clean_m = m.strip()
            # Se consta da fonte fornecida pelo usuário, é USER_SUPPLIED
            if source_text and clean_m.lower() in source_text.lower():
                continue
            unsupported.append(clean_m)
        return unsupported

    @classmethod
    def sanitize_unsupported_precision(
        cls,
        text: str,
        source_text: str = "",
        evidence_basis: Optional[Union[str, MetricEvidenceBasis]] = None,
    ) -> Tuple[str, bool]:
        """
        Rebaixa asserções numéricas de precisão não suportadas para anotações de medição requerida.
        Retorna (texto_sanitizado, houve_rebaixamento).
        """
        unsupported = cls.detect_unsupported_metrics(text, source_text=source_text, evidence_basis=evidence_basis)
        if not unsupported:
            return text, False

        sanitized = text
        for m in unsupported:
            sanitized = sanitized.replace(m, "[MÉTRICA NÃO MEDIDA: medição necessária]")
        return sanitized, True


class DecisionRelevancePolicy:
    """
    Política determinística de Relevância Decisória (Severity != Priority).
    Determina se uma vulnerabilidade severa ou requisito não-funcional tem relevância para o estágio atual da decisão.
    """

    SECURITY_PRIVACY_CATEGORIES = {
        RiskCategory.SECURITY,
        RiskCategory.PRIVACY,
        RiskCategory.COMPLIANCE,
    }

    NON_PRODUCT_RISK_CATEGORIES = {
        RiskCategory.SECURITY,
        RiskCategory.PRIVACY,
        RiskCategory.COMPLIANCE,
        RiskCategory.ENGINEERING,
    }

    FATAL_EARLY_CATEGORIES = {
        RiskCategory.USER_BEHAVIOR,
        RiskCategory.MARKET,
        RiskCategory.BUSINESS_MODEL,
        RiskCategory.PRODUCT,
        RiskCategory.TECHNICAL_FEASIBILITY,
    }

    SECURITY_KEYWORDS = [
        "segurança", "security", "privacidade", "privacy",
        "criptografia", "encryption", "vazamento", "e2ee", "aes", "tls",
        "compliance", "conformidade", "dados sensíveis", "regulatório"
    ]

    ENGINEERING_KEYWORDS = [
        "kubernetes", "k8s", "kafka", "rabbitmq", "reescrever em rust", "rewrite in rust",
        "microserviço", "microserviços", "microservices", "infraestrutura", "cluster",
        "migrar banco", "banco de dados", "postgres", "redis", "deploy", "ci/cd",
        "escalabilidade técnica", "gpu infrastructure"
    ]

    USER_SECURITY_REQUEST_KEYWORDS = [
        "segurança", "privacidade", "criptografia", "security",
        "vazamento", "auditoria de segurança", "proteger dados", "sigilo"
    ]

    USER_TECHNICAL_REQUEST_KEYWORDS = [
        "segurança", "privacidade", "criptografia", "security", "privacy", "encryption",
        "vazamento", "auditoria de segurança", "proteger dados", "sigilo",
        "arquitetura técnica", "infraestrutura", "kubernetes", "k8s", "kafka", "reescrever em rust",
        "migrar banco", "microserviços", "microservices", "infra", "devops", "cloud",
        "migração técnica", "performance técnica", "stack de engenharia", "technical architecture",
        "engineering requirement", "infrastructure requirement", "rust"
    ]

    @classmethod
    def is_user_explicit_security_request(cls, original_idea: str) -> bool:
        """Verifica se o usuário humano explicitamente solicitou análise ou foco em segurança."""
        lower_idea = original_idea.lower()
        return any(kw in lower_idea for kw in cls.USER_SECURITY_REQUEST_KEYWORDS)

    @classmethod
    def is_user_explicit_technical_request(cls, original_idea: str) -> bool:
        """Verifica se o usuário humano explicitamente solicitou análise ou foco técnico/engenharia/segurança."""
        lower_idea = original_idea.lower()
        return any(kw in lower_idea for kw in cls.USER_TECHNICAL_REQUEST_KEYWORDS)

    @classmethod
    def infer_category(cls, vulnerability_text: str, declared_category: RiskCategory) -> RiskCategory:
        """Inferência determinística de categoria se UNKNOWN."""
        if declared_category != RiskCategory.UNKNOWN:
            return declared_category
        text_lower = vulnerability_text.lower()
        if any(kw in text_lower for kw in cls.SECURITY_KEYWORDS):
            return RiskCategory.SECURITY
        if any(kw in text_lower for kw in cls.ENGINEERING_KEYWORDS):
            return RiskCategory.ENGINEERING
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
    def infer_requirement_type(
        cls,
        text: str,
        category: RiskCategory = RiskCategory.UNKNOWN,
        declared_type: Optional[RequirementType] = None,
    ) -> RequirementType:
        """Inferência estruturada de tipo de requisito a partir de categoria e texto."""
        if declared_type and declared_type != RequirementType.PRODUCT_HYPOTHESIS:
            return declared_type
        if category in (RiskCategory.SECURITY, RiskCategory.PRIVACY):
            return RequirementType.SECURITY_REQUIREMENT
        if category == RiskCategory.COMPLIANCE:
            return RequirementType.COMPLIANCE_REQUIREMENT
        if category == RiskCategory.ENGINEERING:
            return RequirementType.ENGINEERING_REQUIREMENT

        text_lower = (text or "").lower()
        if any(kw in text_lower for kw in cls.SECURITY_KEYWORDS):
            return RequirementType.SECURITY_REQUIREMENT
        if any(kw in text_lower for kw in ["lgpd", "gdpr", "compliance", "conformidade", "regulatório"]):
            return RequirementType.COMPLIANCE_REQUIREMENT
        if any(kw in text_lower for kw in cls.ENGINEERING_KEYWORDS):
            return RequirementType.ENGINEERING_REQUIREMENT
        return RequirementType.PRODUCT_HYPOTHESIS

    @classmethod
    def evaluate_vulnerability_relevance(
        cls,
        vulnerability_text: str,
        severity: str,
        category: RiskCategory,
        stage: IdeaStage,
        original_idea: str,
        explicit_relevance: DecisionRelevance = DecisionRelevance.UNKNOWN,
        requirement_type: Optional[RequirementType] = None,
    ) -> DecisionRelevance:
        """
        Avalia deterministicamente a relevância decisória AGORA de uma vulnerabilidade.
        Regra fundamental:
        - Em DISCOVERY/VALIDATION: Engenharia/Segurança/Privacidade HIGH -> LATER (salvo pedido do usuário).
        - Em DISCOVERY/VALIDATION: Usabilidade fatal / Desistência / Rejeição de modelo -> CRITICAL_NOW.
        - Em PRE_PRODUCTION/PRODUCTION: Engenharia/Segurança/Privacidade HIGH -> CRITICAL_NOW.
        """
        sev_upper = severity.upper()
        if sev_upper not in ("HIGH", "CRITICAL"):
            return DecisionRelevance.LATER

        # Se o usuário pediu explicitamente técnico/engenharia/segurança
        if cls.is_user_explicit_technical_request(original_idea):
            effective_cat = cls.infer_category(vulnerability_text, category)
            if effective_cat in cls.NON_PRODUCT_RISK_CATEGORIES:
                return DecisionRelevance.CRITICAL_NOW

        effective_category = cls.infer_category(vulnerability_text, category)

        # Se o chamador já definiu explicitamente uma relevância válida
        if explicit_relevance not in (DecisionRelevance.UNKNOWN, None):
            return explicit_relevance

        # Avaliação por estágio
        if stage in (IdeaStage.DISCOVERY, IdeaStage.VALIDATION, IdeaStage.UNKNOWN):
            if effective_category in cls.NON_PRODUCT_RISK_CATEGORIES or requirement_type in NON_PRODUCT_IMPLEMENTATION_TYPES:
                # Invariante: Em discovery, engenharia/segurança é severa, mas seu aluguel decisório imediato é LATER
                return DecisionRelevance.LATER
            if effective_category in cls.FATAL_EARLY_CATEGORIES:
                return DecisionRelevance.CRITICAL_NOW
            return DecisionRelevance.HIGH_NOW

        elif stage in (IdeaStage.PROTOTYPE, IdeaStage.MVP):
            if effective_category in cls.NON_PRODUCT_RISK_CATEGORIES or requirement_type in NON_PRODUCT_IMPLEMENTATION_TYPES:
                return DecisionRelevance.HIGH_NOW
            return DecisionRelevance.CRITICAL_NOW

        elif stage in (IdeaStage.PRE_PRODUCTION, IdeaStage.PRODUCTION, IdeaStage.SCALE):
            # No estágio pré-produção, falhas graves de engenharia/segurança são CRITICAL_NOW
            if effective_category in cls.NON_PRODUCT_RISK_CATEGORIES or requirement_type in NON_PRODUCT_IMPLEMENTATION_TYPES:
                return DecisionRelevance.CRITICAL_NOW
            return DecisionRelevance.HIGH_NOW

        return DecisionRelevance.LATER

    @classmethod
    def is_non_product_implementation_override(
        cls,
        candidate_text: str,
        original_mechanism: str = "",
        candidate_type: Optional[RequirementType] = None,
        candidate_category: Optional[RiskCategory] = None,
        is_implementation_only: Optional[bool] = None,
    ) -> bool:
        """
        Verifica se uma hipótese mutada ou proposta substitui a função de produto
        por uma implementação puramente técnica de infraestrutura, arquitetura ou segurança.
        Invariante: KEYWORD_BLACKLIST_IS_PRIMARY_POLICY = NO (classificação estruturada é primária).
        """
        # 1. Classificação estruturada primária
        if candidate_type in NON_PRODUCT_IMPLEMENTATION_TYPES:
            return True
        if candidate_category in cls.NON_PRODUCT_RISK_CATEGORIES:
            return True
        if is_implementation_only is True:
            return True

        # 2. Análise semântica / vocabulário técnico de fallback
        cand_lower = candidate_text.lower()
        orig_lower = original_mechanism.lower()

        all_tech_terms = FalsePrecisionGuard.SECURITY_TECH_TERMS + [
            "kubernetes", "k8s", "kafka", "rabbitmq", "reescrever em rust", "rewrite in rust",
            "microserviços", "microservices", "migrar banco", "database migration",
            "cluster", "infraestrutura gpu", "gpu infrastructure"
        ]

        tech_hits = sum(1 for term in all_tech_terms if term in cand_lower)
        if tech_hits >= 1:
            if not any(term in orig_lower for term in all_tech_terms):
                return True
        return False

    @classmethod
    def is_engineering_security_override(cls, candidate_text: str, original_mechanism: str) -> bool:
        """Alias retrocompatível para is_non_product_implementation_override."""
        return cls.is_non_product_implementation_override(candidate_text, original_mechanism)


class NextActionArbitrationPolicy:
    """
    Política determinística de arbitragem de próximo passo recomendado.
    Invariante: FOCUSED_ESCALATION_CAN_UNILATERALLY_OVERRIDE_NEXT_ACTION = FALSE.
    """

    TECHNICAL_IMPLEMENTATION_KEYWORDS = [
        "implementar criptografia", "desenvolver e2ee", "configurar tls",
        "implementar aes", "arquitetura de segurança", "certificate pinning",
        "desenvolver backend seguro", "implementar autenticação mfa", "auditoria de segurança",
        "migrar para kubernetes", "deploy em kubernetes", "reescrever em rust", "rewrite in rust",
        "introduzir kafka", "migrar banco de dados", "adotar microserviços",
        "migrar para microserviços", "infraestrutura gpu", "configurar cluster"
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
        candidate_risk_category: RiskCategory = RiskCategory.UNKNOWN,
        candidate_requirement_type: Optional[RequirementType] = None,
        is_implementation_only: Optional[bool] = None,
    ) -> Tuple[str, bool]:
        """
        Arbitra deterministicamente o próximo passo final.
        Retorna (next_action_final, next_action_foi_alterada).
        Invariante: CANDIDATE_RISK_CATEGORY_DROPPED = NO.
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

        # 3. Determinar se o candidato é implementação não-produto
        cand_lower = candidate.lower()
        is_non_product = (
            candidate_risk_category in DecisionRelevancePolicy.NON_PRODUCT_RISK_CATEGORIES
            or candidate_requirement_type in NON_PRODUCT_IMPLEMENTATION_TYPES
            or is_implementation_only is True
            or DecisionRelevancePolicy.is_non_product_implementation_override(
                candidate_text=candidate,
                original_mechanism=first_pass,
                candidate_type=candidate_requirement_type,
                candidate_category=candidate_risk_category,
                is_implementation_only=is_implementation_only,
            )
            or any(kw in cand_lower for kw in cls.TECHNICAL_IMPLEMENTATION_KEYWORDS)
        )

        # 4. Em DISCOVERY ou VALIDATION:
        if stage in (IdeaStage.DISCOVERY, IdeaStage.VALIDATION, IdeaStage.UNKNOWN):
            if is_non_product:
                # Se o usuário pediu explicitamente análise técnica/segurança, permite
                if DecisionRelevancePolicy.is_user_explicit_technical_request(original_idea):
                    return candidate, True
                # Rejeita o override unilateral da escalação!
                # Mantém o próximo passo de falseamento da hipótese de produto da primeira passada
                return first_pass, False

        # 5. Em PRE_PRODUCTION / PRODUCTION / SCALE:
        # Bloqueadores de infraestrutura e segurança SÃO passos legítimos em pré-produção
        if stage in (IdeaStage.PRE_PRODUCTION, IdeaStage.PRODUCTION, IdeaStage.SCALE):
            return candidate, True

        # 6. Se o candidato for um teste discriminativo válido ou resolver blocker atual do estágio
        return candidate, True
