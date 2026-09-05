"""
tests/unit/test_explicit_focus_and_sensitive_data.py
Testes determinísticos para FIOIDEIAS-V1.1-RQ-04:
1. Detecção de foco explícito vs. menção incidental (UserRequestedFocus).
2. Classificação robusta de dados sensíveis e privacidade (infer_category).
3. Proteção contra falsos positivos em dados de negócio (sales data, market data, etc.).
4. Prioridade da categoria estruturada (STRUCTURED_CATEGORY_PRIMARY = YES).
5. Relevância decisória em estágio de Descoberta (Severity != Priority).
6. Arbitragem determinística de próximo passo e proteção da hipótese de produto.
"""

import pytest
from src.idea_evolution.domain.decision_relevance import (
    DecisionRelevancePolicy,
    NextActionArbitrationPolicy,
    RiskCategory,
    IdeaStage,
    DecisionRelevance,
    FocusType,
    FocusBasis,
    UserRequestedFocus,
)


class TestExplicitTechnicalIntentDetection:
    """Testes para Seção 4, 5, 10, 11 e 12 (MENTION != REQUEST)."""

    POSITIVE_EXAMPLES = [
        ("Quero focar agora na segurança.", FocusType.SECURITY),
        ("Analise especificamente a arquitetura técnica.", FocusType.TECHNICAL),
        ("Priorize a infraestrutura antes do produto.", FocusType.TECHNICAL),
        ("Faça uma auditoria de segurança.", FocusType.SECURITY),
        ("Meu objetivo nesta análise é escolher a arquitetura do backend.", FocusType.TECHNICAL),
        ("Help me evaluate the security architecture.", FocusType.SECURITY),
        (
            "Antes de validar mercado, quero especificamente que esta análise priorize a arquitetura técnica e os riscos de segurança.",
            FocusType.SECURITY,
        ),
    ]

    NEGATIVE_EXAMPLES = [
        "O sistema usa infraestrutura simples.",
        "No futuro haverá infraestrutura em nuvem.",
        "Custos de infraestrutura devem ser baixos.",
        "O roadmap menciona segurança.",
        "Precisamos considerar LGPD antes da produção.",
        "O MVP poderá usar cloud.",
        "Há riscos de privacidade.",
        "Será necessário banco de dados.",
    ]

    @pytest.mark.parametrize("text,expected_focus", POSITIVE_EXAMPLES)
    def test_explicit_technical_requests_return_true(self, text, expected_focus):
        focus = DecisionRelevancePolicy.detect_user_requested_focus(text)
        assert focus.basis == FocusBasis.USER_EXPLICIT
        assert focus.is_technical is True
        assert focus.focus_type in (FocusType.TECHNICAL, FocusType.SECURITY)
        assert DecisionRelevancePolicy.is_user_explicit_technical_request(text) is True

    @pytest.mark.parametrize("text", NEGATIVE_EXAMPLES)
    def test_incidental_technical_mentions_return_false(self, text):
        focus = DecisionRelevancePolicy.detect_user_requested_focus(text)
        assert focus.basis != FocusBasis.USER_EXPLICIT or focus.is_technical is False
        assert DecisionRelevancePolicy.is_user_explicit_technical_request(text) is False

    def test_incidental_technical_content_in_long_document(self):
        long_doc = """
        # PROPOSTA DO PRODUTO
        SaaS simples conectado ao WhatsApp para recuperação de orçamentos perdidos.
        
        ## 5. Custos e Viabilidade
        A infraestrutura inicial será muito simples e barata.
        Custos de infraestrutura devem ser baixos nos primeiros meses.
        
        ## 12. Segurança e LGPD
        O roadmap menciona segurança e precisamos considerar LGPD antes da produção.
        No futuro haverá infraestrutura em nuvem (cloud) com banco de dados redundante.
        O MVP poderá usar cloud básica.
        """
        focus = DecisionRelevancePolicy.detect_user_requested_focus(long_doc)
        assert focus.basis != FocusBasis.USER_EXPLICIT or focus.is_technical is False
        assert DecisionRelevancePolicy.is_user_explicit_technical_request(long_doc) is False
        assert DecisionRelevancePolicy.is_user_explicit_security_request(long_doc) is False

    def test_explicit_security_countercase_in_document(self):
        doc = """
        Ideia de SaaS para WhatsApp.
        Antes de validar mercado, quero especificamente que esta análise priorize a arquitetura técnica e os riscos de segurança.
        """
        assert DecisionRelevancePolicy.is_user_explicit_technical_request(doc) is True
        assert DecisionRelevancePolicy.is_user_explicit_security_request(doc) is True


class TestSensitiveDataAndPrivacyClassification:
    """Testes para Seção 6, 7, 8, 15 e 16 (Classificação de dados sensíveis e privacidade)."""

    EXACT_RQ03_VULN = "Armazenamento de mensagens de clientes pode conter dados pessoais sensíveis"

    ADVERSARIAL_SENSITIVE_VARIATIONS = [
        "dados pessoais altamente sensíveis",
        "dados de clientes potencialmente sensíveis",
        "personal customer information",
        "customer PII",
        "personal and sensitive data",
        "vazamento de credenciais de acesso",
        "unauthorized access to customer messages",
        "exposição de dados pessoais na UI",
        "risco de conformidade com LGPD para mensagens armazenadas",
    ]

    NON_PERSONAL_DATA_COUNTEREXAMPLES = [
        ("sales data is missing", RiskCategory.PRODUCT),
        ("market data is incomplete", RiskCategory.MARKET),
        ("database performance is slow", RiskCategory.ENGINEERING),
        ("analytics dataset needs aggregation", RiskCategory.PRODUCT),
        ("sales data", RiskCategory.PRODUCT),
        ("market data", RiskCategory.MARKET),
        ("database", RiskCategory.ENGINEERING),
        ("analytics data", RiskCategory.PRODUCT),
    ]

    def test_rq03_vulnerability_classified_as_privacy_or_security(self):
        cat = DecisionRelevancePolicy.infer_category(self.EXACT_RQ03_VULN, RiskCategory.UNKNOWN)
        assert cat in (RiskCategory.PRIVACY, RiskCategory.SECURITY)
        assert cat in DecisionRelevancePolicy.NON_PRODUCT_RISK_CATEGORIES

    @pytest.mark.parametrize("text", ADVERSARIAL_SENSITIVE_VARIATIONS)
    def test_adversarial_sensitive_data_variations(self, text):
        cat = DecisionRelevancePolicy.infer_category(text, RiskCategory.UNKNOWN)
        assert cat in (RiskCategory.PRIVACY, RiskCategory.SECURITY)
        assert cat in DecisionRelevancePolicy.NON_PRODUCT_RISK_CATEGORIES

    @pytest.mark.parametrize("text,expected_non_privacy", NON_PERSONAL_DATA_COUNTEREXAMPLES)
    def test_non_personal_data_does_not_false_positive_as_privacy_security(self, text, expected_non_privacy):
        assert DecisionRelevancePolicy.is_sensitive_data_or_privacy_risk(text) is False
        cat = DecisionRelevancePolicy.infer_category(text, RiskCategory.UNKNOWN)
        assert cat not in (RiskCategory.PRIVACY, RiskCategory.SECURITY)

    def test_structured_category_primary_rule(self):
        """Se declared_category for fornecida, tem prioridade sobre o fallback léxico."""
        cat = DecisionRelevancePolicy.infer_category(
            vulnerability_text="grave risco de segurança e criptografia",
            declared_category=RiskCategory.MARKET,
        )
        assert cat == RiskCategory.MARKET


class TestDecisionRelevanceAndArbitrationInDiscovery:
    """Testes para Seção 9, 13 e 14 (Relevância decisória e arbitragem em Descoberta)."""

    def test_sensitive_data_risk_is_later_in_discovery_without_explicit_request(self):
        vuln = "Armazenamento de mensagens de clientes pode conter dados pessoais sensíveis"
        rel = DecisionRelevancePolicy.evaluate_vulnerability_relevance(
            vulnerability_text=vuln,
            severity="HIGH",
            category=RiskCategory.UNKNOWN,
            stage=IdeaStage.DISCOVERY,
            original_idea="SaaS simples de recuperação de orçamentos no WhatsApp com infraestrutura barata.",
        )
        assert rel == DecisionRelevance.LATER

    def test_sensitive_data_risk_is_critical_now_if_user_explicitly_requests(self):
        vuln = "Armazenamento de mensagens de clientes pode conter dados pessoais sensíveis"
        rel = DecisionRelevancePolicy.evaluate_vulnerability_relevance(
            vulnerability_text=vuln,
            severity="HIGH",
            category=RiskCategory.UNKNOWN,
            stage=IdeaStage.DISCOVERY,
            original_idea="Quero focar agora na segurança e na proteção de dados dos clientes.",
        )
        assert rel == DecisionRelevance.CRITICAL_NOW

    def test_next_action_arbitration_in_discovery_rejects_security_override(self):
        fp_action = "Entrevistar 20 pequenos negócios para validar se perdem vendas por falta de follow-up."
        esc_action = "Realizar auditoria de segurança (pen test + revisão de RBAC) focada no armazenamento de PII."
        long_doc = "SaaS de orçamentos no WhatsApp. Custos de infraestrutura devem ser baixos."

        final_action, changed = NextActionArbitrationPolicy.arbitrate(
            first_pass_next_action=fp_action,
            escalation_candidate_next_action=esc_action,
            stage=IdeaStage.DISCOVERY,
            original_idea=long_doc,
            candidate_risk_category=RiskCategory.SECURITY,
        )
        assert final_action == fp_action
        assert changed is False

    def test_next_action_arbitration_allows_security_when_user_explicitly_requested(self):
        fp_action = "Entrevistar 20 pequenos negócios."
        esc_action = "Realizar auditoria de segurança (pen test + revisão de RBAC)."
        explicit_doc = "Faça uma auditoria de segurança na nossa ideia de SaaS."

        final_action, changed = NextActionArbitrationPolicy.arbitrate(
            first_pass_next_action=fp_action,
            escalation_candidate_next_action=esc_action,
            stage=IdeaStage.DISCOVERY,
            original_idea=explicit_doc,
            candidate_risk_category=RiskCategory.SECURITY,
        )
        assert final_action == esc_action
        assert changed is True

    def test_is_non_product_implementation_override_detects_security_mitigation(self):
        mutated = (
            "Se a base de dados aplicar criptografia em repouso para todos os campos que podem conter PII "
            "e a camada de API implementar controle de acesso baseado em papéis (RBAC) estrito..."
        )
        orig_mechanism = "Integração via WhatsApp Business API que captura mensagens e lembra o vendedor de responder orçamentos."
        assert DecisionRelevancePolicy.is_non_product_implementation_override(
            candidate_text=mutated,
            original_mechanism=orig_mechanism,
        ) is True
