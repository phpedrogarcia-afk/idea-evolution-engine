"""
tests/adversarial/test_adversarial_decision_relevance.py
Suíte de testes adversariais e de conformidade para Relevância Decisória e Qualidade de Resposta
(FIOIDEIAS-V1.1-RQ-01).

Cobre:
1. Caso Canônico de Regressão WhatsApp SaaS em Descoberta (Severity != Priority).
2. Contra-regressão de Segurança em Pré-Produção (Segurança torna-se prioridade agora).
3. Caso de Controle com Solicitação Explícita de Segurança pelo Usuário.
4. Caso de Controle com Bloqueador Fatal de Viabilidade Técnica.
5. Caso de Controle com Decisão Normativa Humana Soberana (Zero chamadas extras).
6. Caso de Mecanismos Concorrentes com Linha de Base de Status Quo Gratuito.
7. Guarda contra Falsa Precisão Numérica (<200 ms sem evidência).
8. Preservação de Critérios Estruturados de Falseamento.
9. Invariantes de Autoridade e Prova de Proveniência (USER_EXPLICIT, VALID_USER_DERIVATION, MODEL_HYPOTHESIS).
10. Rubrica de Avaliação de Qualidade Humana por Dimensão.
11. Invariante Lean L1: max_model_calls <= 2.
"""

import unittest
import tempfile
from pathlib import Path
from typing import Dict, Any

from src.idea_evolution.domain.state import PromotionAuthorityBasis, OntologyState
from src.idea_evolution.domain.epistemic_contracts import SourceAnchor
from src.idea_evolution.domain.decision_relevance import (
    IdeaStage,
    RiskCategory,
    DecisionRelevance,
    AlternativeCategory,
    FalsificationCriterion,
    MetricEvidenceBasis,
    RequirementType,
    StageProvenanceBasis,
    IdeaStageAssessment,
    IdeaStageGroundingPolicy,
    FalsePrecisionGuard,
    DecisionRelevancePolicy,
    NextActionArbitrationPolicy,
)
from src.idea_evolution.artifacts.evolution_artifact import (
    FROZEN_LEAN_CORE_HASH_V1_0,
    FROZEN_LEAN_CORE_HASH_V1_1,
)
from src.idea_evolution.domain.early_epistemic_gate import (
    LeanFirstPassOutput,
    FocusedEscalationOutput,
    LeanCandidateMechanism,
    LeanVulnerability,
    GateOutcome,
    EscalationReason,
    EarlyEpistemicGate,
)
from src.idea_evolution.orchestration.lean_loop import LeanLoopRunner, LEAN_L1_MAX_MODEL_CALLS
from src.idea_evolution.artifacts.mapper import EvolutionArtifactMapper
from src.idea_evolution.providers.fake import FakeModelRunner


def evaluate_human_quality_rubric(artifact) -> Dict[str, str]:
    """
    Rubrica determinística de avaliação de qualidade humana por dimensão (Seção 19).
    NÃO emite score numérico artificial; emite julgamentos explícitos por dimensão.
    """
    judgments = {}

    # 1. INTENT_FIDELITY
    if artifact.original_idea.strip() and artifact.human_intent.strip():
        judgments["INTENT_FIDELITY"] = "PASS_PRESERVED"
    else:
        judgments["INTENT_FIDELITY"] = "FAIL_DRIFT_OR_MISSING"

    # 2. STAGE_ALIGNMENT
    # Refinamento não pode se transformar em implementação de infraestrutura técnica se a ideia for inicial
    is_infra = any(t in artifact.refined_idea.lower() for t in ["e2ee", "aes-256", "tls 1.3", "certificate pinning"])
    if is_infra and not DecisionRelevancePolicy.is_user_explicit_security_request(artifact.original_idea):
        judgments["STAGE_ALIGNMENT"] = "FAIL_TECH_INFRA_MUTATION"
    else:
        judgments["STAGE_ALIGNMENT"] = "PASS_ALIGNED"

    # 3. DECISION_RELEVANCE
    # Próximo passo não pode ser 'implementar criptografia' em descoberta
    rec_lower = artifact.recommended_next_action.lower()
    if any(kw in rec_lower for kw in ["implementar criptografia", "desenvolver e2ee", "configurar tls"]):
        if not DecisionRelevancePolicy.is_user_explicit_security_request(artifact.original_idea):
            judgments["DECISION_RELEVANCE"] = "FAIL_IRRELEVANT_IMPL_BEFORE_DISCOVERY"
        else:
            judgments["DECISION_RELEVANCE"] = "PASS_EXPLICIT_SECURITY"
    else:
        judgments["DECISION_RELEVANCE"] = "PASS_ACTIONABLE_NOW"

    # 4. UNSUPPORTED_SPECIFICITY
    has_unsupported_metrics = len(FalsePrecisionGuard.detect_unsupported_metrics(artifact.refined_idea, artifact.original_idea)) > 0
    if has_unsupported_metrics:
        judgments["UNSUPPORTED_SPECIFICITY"] = "FAIL_UNSUPPORTED_NUMERICAL_PRECISION"
    else:
        judgments["UNSUPPORTED_SPECIFICITY"] = "PASS_GUARDED"

    # 5. FALSIFIABILITY
    if any("validar" in rec_lower or "teste" in rec_lower or "entrevistar" in rec_lower or "falsifica" in rec_lower for _ in [1]):
        judgments["FALSIFIABILITY"] = "PASS_EMPIRICALLY_TESTABLE"
    else:
        judgments["FALSIFIABILITY"] = "WEAK"

    # 6. ACTIONABILITY
    if artifact.recommended_next_action and len(artifact.recommended_next_action.strip()) > 10:
        judgments["ACTIONABILITY"] = "PASS_CLEAR_NEXT_STEP"
    else:
        judgments["ACTIONABILITY"] = "FAIL_VAGUE"

    # 7. AUTHORITY_PRESERVATION
    if (
        artifact.original_idea_authority == PromotionAuthorityBasis.USER_EXPLICIT
        and artifact.intent_provenance in (PromotionAuthorityBasis.VALID_USER_DERIVATION, PromotionAuthorityBasis.USER_EXPLICIT)
        and artifact.refined_idea_authority == PromotionAuthorityBasis.MODEL_HYPOTHESIS
    ):
        judgments["AUTHORITY_PRESERVATION"] = "PASS_STRICT_BOUNDARIES"
    else:
        judgments["AUTHORITY_PRESERVATION"] = "FAIL_SPOOFED"

    return judgments


class TestAdversarialDecisionRelevance(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.runs_dir = Path(self.temp_dir.name)
        self.whatsapp_idea = (
            "Um SaaS para ajudar pequenas empresas a recuperar orçamentos e cotações esquecidas no WhatsApp. "
            "O vendedor marca uma mensagem com a tag de cotação e o sistema agenda lembretes de follow-up automáticos."
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_whatsapp_saas_discovery_regression_case(self):
        """
        Caso Canônico de Regressão (Seção 16 & 21):
        - Ideia em estágio de DESCOBERTA / VALIDAÇÃO.
        - Risco de segurança/privacidade rotulado como HIGH severidade.
        - Incertezas de negócio: adoção manual, disposição a pagar, status quo gratuito (etiquetas).
        - A escalação NÃO pode priorizar segurança sobre falseamento de negócio.
        - A ideia refinada NÃO pode mutar para arquitetura de criptografia (E2EE, AES-256).
        - A métrica não ancorada '<200 ms' deve ser rejeitada/sanitizada.
        - O próximo passo final DEVE pertencer à classe de falseamento de descoberta.
        """
        first_pass = {
            "interpreted_problem": "Pequenas empresas perdem vendas porque cotações enviadas no WhatsApp são esquecidas sem follow-up.",
            "human_intent": "Recuperar cotações esquecidas no WhatsApp com marcação simples e lembretes.",
            "primary_mechanism": {
                "mechanism": "Sistema de marcação manual com lembretes automáticos de follow-up para vendedores",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
                "justification": "Estrutura central extraída da ideia do usuário",
                "tradeoffs": ["Depende da disciplina do vendedor em etiquetar"],
                "alternative_category": "OTHER",
            },
            "competing_alternatives": [
                {
                    "mechanism": "Etiquetas nativas gratuitas do WhatsApp Business",
                    "is_explicit_in_source": False,
                    "claimed_basis": "MODEL_HYPOTHESIS",
                    "justification": "Status quo gratuito utilizado atualmente",
                    "tradeoffs": ["Gratuito, mas sem lembretes automatizados"],
                    "alternative_category": "STATUS_QUO",
                },
                {
                    "mechanism": "Planilha Excel / Google Sheets compartilhada",
                    "is_explicit_in_source": False,
                    "claimed_basis": "MODEL_HYPOTHESIS",
                    "justification": "Substituto comum de baixo custo",
                    "tradeoffs": ["Exige digitação dupla fora do WhatsApp"],
                    "alternative_category": "SUBSTITUTE",
                },
            ],
            "key_assumptions": [
                "Vendedores esquecem de cobrar clientes",
                "Lojistas estão dispostos a pagar mensalidade por isso",
            ],
            "material_ambiguities": [],
            "material_vulnerabilities": [
                {
                    "vulnerability": "Vazamento de conversas e conformidade LGPD no armazenamento de chats",
                    "why_it_matters": "Multas regulatórias e quebra de confiança dos clientes",
                    "severity": "HIGH",
                    "affected_aspect": "Privacidade",
                    "category": "SECURITY",
                    "decision_relevance": "LATER",
                },
                {
                    "vulnerability": "Falta de adesão do vendedor em marcar mensagens manualmente",
                    "why_it_matters": "Inviabiliza a captura das cotações na origem",
                    "severity": "HIGH",
                    "affected_aspect": "Adoção do Usuário",
                    "category": "USER_BEHAVIOR",
                    "decision_relevance": "CRITICAL_NOW",
                },
            ],
            "remaining_uncertainties": [
                "Disposição a pagar de pequenas empresas frente a etiquetas gratuitas",
            ],
            "requires_human_normative_choice": False,
            "human_choice_description": "",
            "proposed_next_action": "Validar com 5 lojistas se a dor de esquecimento compensa o atrito de marcação manual.",
            "idea_stage": "DISCOVERY",
            "idea_stage_justification": "Ideia conceitual inicial sem base de usuários ativos ou produto construído.",
            "falsification_criteria": [
                {
                    "hypothesis": "Lojistas esquecem cotações e pagarão por follow-up",
                    "what_would_kill_it": "Lojistas afirmarem que etiquetas gratuitas já resolvem 100% ou se recusarem a marcar manualmente",
                    "lowest_cost_discriminating_test": "Teste concierge manual de 3 dias com 5 lojistas usando etiquetas",
                }
            ],
            "engineering_requirements": [
                "Criptografia de dados em repouso na infraestrutura de persistência"
            ],
        }

        # Simulação da escalação focada que tentou mutar a hipótese para segurança e inventou <200ms
        escalation_mutated = {
            "escalation_reason": "MATERIAL_VULNERABILITY",
            "target_hypothesis": "Sistema de marcação manual",
            "focused_critique_or_analysis": "Análise de segurança: implementar TLS 1.3 e latência <200 ms.",
            "resolved_tradeoffs": ["Adotada cifra AES-256"],
            "discriminating_tests": ["Teste de penetração e auditoria criptográfica"],
            "hypothesis_mutated": True,
            "mutated_hypothesis_description": "Plataforma de mensagens com criptografia E2EE, cifra AES-256 e latência <200 ms",
            "decision_progress_made": True,
            "updated_next_action": "Implementar criptografia de ponta a ponta com E2EE e AES-256 no backend",
            "candidate_updated_next_action": "Implementar criptografia de ponta a ponta com E2EE e AES-256 no backend",
        }

        fake_runner = FakeModelRunner(
            custom_responses={
                "LEAN_FIRST_PASS": first_pass,
                "FOCUSED_ESCALATION": escalation_mutated,
            }
        )
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)
        result = lean_runner.run(self.whatsapp_idea)

        # Mapeia para EvolutionArtifact
        artifact = EvolutionArtifactMapper.map_lean_result(result)

        # 1. SEGURANÇA REGISTRADA E SEVERIDADE PRESERVADA
        security_critiques = [c for c in artifact.critique if "lgpd" in c.vulnerability.lower() or "vazamento" in c.vulnerability.lower() or "segurança" in c.vulnerability.lower()]
        self.assertTrue(len(security_critiques) >= 1)
        self.assertEqual(security_critiques[0].severity, "HIGH")

        # 2. SEGURANÇA NÃO SE TORNA A PRIORIDADE GLOBAL IMEDIATA (SEVERITY != PRIORITY)
        # O gate priorizou a incerteza de USER_BEHAVIOR (CRITICAL_NOW) sobre a de SECURITY (LATER)
        first_vuln = result.first_pass.material_vulnerabilities[0]
        self.assertEqual(first_vuln.category, RiskCategory.SECURITY)
        self.assertEqual(first_vuln.decision_relevance, DecisionRelevance.LATER)

        user_behavior_vuln = result.first_pass.material_vulnerabilities[1]
        self.assertEqual(user_behavior_vuln.category, RiskCategory.USER_BEHAVIOR)
        self.assertEqual(user_behavior_vuln.decision_relevance, DecisionRelevance.CRITICAL_NOW)

        # 3. HIPÓTESE DE PRODUTO NÃO FOI MUTADA PARA CRIPTOGRAFIA/SEGURANÇA
        self.assertNotIn("E2EE", artifact.refined_idea)
        self.assertNotIn("AES-256", artifact.refined_idea)
        self.assertIn("marcação", artifact.refined_idea.lower())

        # 4. AFIRMAÇÃO NÃO SUPORTADA DE LATÊNCIA <200 MS REJEITADA / REBAIXADA
        self.assertNotIn("<200 ms", artifact.refined_idea)
        for crit in artifact.critique:
            self.assertNotIn("<200 ms", crit.vulnerability)

        # 5. PRÓXIMO PASSO FINAL PERTENCE À CLASSE DE FALSEAMENTO DE DESCOBERTA
        self.assertNotIn("implementar criptografia", artifact.recommended_next_action.lower())
        self.assertNotIn("desenvolver e2ee", artifact.recommended_next_action.lower())
        self.assertTrue(
            "validar" in artifact.recommended_next_action.lower()
            or "lojistas" in artifact.recommended_next_action.lower()
            or "etiquetas" in artifact.recommended_next_action.lower()
        )

        # 6. RUBRICA DE AVALIAÇÃO DE QUALIDADE HUMANA
        rubric = evaluate_human_quality_rubric(artifact)
        self.assertEqual(rubric["INTENT_FIDELITY"], "PASS_PRESERVED")
        self.assertEqual(rubric["STAGE_ALIGNMENT"], "PASS_ALIGNED")
        self.assertEqual(rubric["DECISION_RELEVANCE"], "PASS_ACTIONABLE_NOW")
        self.assertEqual(rubric["UNSUPPORTED_SPECIFICITY"], "PASS_GUARDED")
        self.assertEqual(rubric["FALSIFIABILITY"], "PASS_EMPIRICALLY_TESTABLE")
        self.assertEqual(rubric["ACTIONABILITY"], "PASS_CLEAR_NEXT_STEP")
        self.assertEqual(rubric["AUTHORITY_PRESERVATION"], "PASS_STRICT_BOUNDARIES")

    def test_preproduction_security_countercase(self):
        """
        Contra-regressão de Segurança em Pré-Produção (Seção 17):
        - Estágio = PRE_PRODUCTION.
        - Hipótese de negócio já validada.
        - Defeito crítico de segurança existente.
        - O sistema DEVE reconhecer que em PRE_PRODUCTION, segurança HIGH é CRITICAL_NOW!
        """
        first_pass = LeanFirstPassOutput(
            interpreted_problem="Processamento de pagamentos médicos em fase final de homologação.",
            human_intent="Homologar gateway de pagamento para clínicas médicas.",
            primary_mechanism=LeanCandidateMechanism(
                mechanism="Gateway de checkout com conciliação bancária",
                is_explicit_in_source=True,
                claimed_basis=PromotionAuthorityBasis.USER_EXPLICIT,
                justification="Definido pelo usuário",
            ),
            key_assumptions=[],
            material_ambiguities=[],
            material_vulnerabilities=[
                LeanVulnerability(
                    vulnerability="Tokens de API de provedor e chaves privadas expostos em logs de auditoria",
                    why_it_matters="Comprometimento total das credenciais financeiras da clínica",
                    severity="HIGH",
                    category=RiskCategory.SECURITY,
                    decision_relevance=DecisionRelevance.UNKNOWN,
                )
            ],
            remaining_uncertainties=[],
            requires_human_normative_choice=False,
            proposed_next_action="Realizar lançamento piloto com 10 clínicas.",
            idea_stage=IdeaStage.PRE_PRODUCTION,
        )

        anchor = SourceAnchor.create_human_input_anchor("Homologação de pagamentos médicos pré-produção")
        eval_result = EarlyEpistemicGate.evaluate(
            source_anchor=anchor,
            first_pass=first_pass,
        )

        # Em PRE_PRODUCTION, segurança HIGH legítima DEVE ser escalada como prioridade agora
        self.assertEqual(eval_result.outcome, GateOutcome.ESCALATE_FOCUSED)
        self.assertEqual(eval_result.escalation_reason, EscalationReason.MATERIAL_VULNERABILITY)
        self.assertEqual(first_pass.material_vulnerabilities[0].decision_relevance, DecisionRelevance.CRITICAL_NOW)
        self.assertIn("CRITICAL_NOW", eval_result.rent_record.expected_decision_delta)

    def test_explicit_user_security_request_case(self):
        """
        Caso de Controle: Solicitação Explícita de Segurança pelo Usuário (Seção 18).
        Mesmo em estágio DISCOVERY, se o usuário pede expressamente análise de segurança,
        a segurança DEVE ser tratada como prioridade imediata.
        """
        idea_with_security_prompt = "Preciso de uma análise rigorosa da segurança e privacidade dos dados de um SaaS de mensagens."
        first_pass = LeanFirstPassOutput(
            interpreted_problem="Análise de riscos de segurança em mensagens.",
            human_intent="Avaliar postura de segurança e privacidade.",
            primary_mechanism=LeanCandidateMechanism(
                mechanism="Arquitetura de mensageria com auditoria de segurança",
                is_explicit_in_source=False,
                claimed_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
            ),
            material_vulnerabilities=[
                LeanVulnerability(
                    vulnerability="Ausência de rotação de chaves e risco de interceptação",
                    why_it_matters="Vulnerabilidade crítica de segurança",
                    severity="HIGH",
                    category=RiskCategory.SECURITY,
                )
            ],
            idea_stage=IdeaStage.DISCOVERY,
        )

        anchor = SourceAnchor.create_human_input_anchor(idea_with_security_prompt)
        eval_result = EarlyEpistemicGate.evaluate(
            source_anchor=anchor,
            first_pass=first_pass,
        )

        self.assertEqual(eval_result.outcome, GateOutcome.ESCALATE_FOCUSED)
        self.assertEqual(eval_result.escalation_reason, EscalationReason.MATERIAL_VULNERABILITY)
        self.assertEqual(first_pass.material_vulnerabilities[0].decision_relevance, DecisionRelevance.CRITICAL_NOW)

    def test_technical_feasibility_blocker_case(self):
        """
        Caso de Controle: Bloqueador Fatal de Viabilidade Técnica em Descoberta (Seção 18).
        Uma inviabilidade técnica central (ex: API impossível) em DISCOVERY é CRITICAL_NOW.
        """
        first_pass = LeanFirstPassOutput(
            interpreted_problem="Integração de WhatsApp.",
            human_intent="Automatizar leitura de WhatsApp pessoal.",
            primary_mechanism=LeanCandidateMechanism(
                mechanism="Interceptação direta de pacotes do WhatsApp sem API oficial",
                is_explicit_in_source=False,
                claimed_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
            ),
            material_vulnerabilities=[
                LeanVulnerability(
                    vulnerability="Bloqueio imediato do chip e banimento permanente da conta pelo WhatsApp por tráfego não oficial",
                    why_it_matters="Inviabiliza totalmente a operação do produto no dia 1",
                    severity="HIGH",
                    category=RiskCategory.TECHNICAL_FEASIBILITY,
                )
            ],
            idea_stage=IdeaStage.DISCOVERY,
        )

        anchor = SourceAnchor.create_human_input_anchor("Automação de WhatsApp via interceptação de pacotes")
        eval_result = EarlyEpistemicGate.evaluate(
            source_anchor=anchor,
            first_pass=first_pass,
        )

        self.assertEqual(eval_result.outcome, GateOutcome.ESCALATE_FOCUSED)
        self.assertEqual(eval_result.escalation_reason, EscalationReason.MATERIAL_VULNERABILITY)
        self.assertEqual(first_pass.material_vulnerabilities[0].decision_relevance, DecisionRelevance.CRITICAL_NOW)

    def test_human_normative_choice_control_case(self):
        """
        Caso de Controle: Decisão Normativa Humana Soberana (Seção 18).
        Missing Human Authority -> REQUEST_HUMAN_DECISION com 0 chamadas adicionais de IA.
        """
        first_pass = {
            "interpreted_problem": "Bifurcação de modelo de negócio.",
            "human_intent": "Definir se a plataforma deve monetizar cobrando de quem contrata ou cobrando de quem presta o serviço.",
            "primary_mechanism": {
                "mechanism": "Cobrança mista",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": ["Decisão normativa sobre quem deve pagar"],
            "material_vulnerabilities": [],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": True,
            "human_choice_description": "Definir se o modelo cobrará do contratante ou do prestador.",
            "proposed_next_action": "Definir preferência de modelo.",
        }

        fake_runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": first_pass})
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)
        result = lean_runner.run("Ideia de marketplace de serviços gerais")

        self.assertEqual(result.total_model_calls, 1)
        self.assertEqual(result.gate_result.outcome, GateOutcome.REQUEST_HUMAN_DECISION)
        self.assertEqual(result.terminal_status, "HUMAN_DECISION_REQUIRED")
        self.assertTrue(result.human_decision_requested)

    def test_false_precision_guard_detection_and_downgrade(self):
        """
        Guarda contra Falsa Precisão Numérica (Seção 11).
        Verifica detecção e rebaixamento de métricas inventadas sem evidência.
        """
        text_with_fake_precision = "O sistema garante latência <200 ms e uptime de 99.99% com resposta em 50ms."
        source_anchor_text = "Quero um app simples de mensagens."

        unsupported = FalsePrecisionGuard.detect_unsupported_metrics(text_with_fake_precision, source_anchor_text)
        self.assertTrue(len(unsupported) >= 2)
        self.assertIn("<200 ms", unsupported)

        sanitized, downgraded = FalsePrecisionGuard.sanitize_unsupported_precision(text_with_fake_precision, source_anchor_text)
        self.assertTrue(downgraded)
        self.assertNotIn("<200 ms", sanitized)
        self.assertIn("MÉTRICA NÃO MEDIDA", sanitized)

    def test_falsification_criteria_structure_and_preservation(self):
        """
        Critérios Estruturados de Falseamento (Seção 12).
        Verifica que o contrato tipado preserva hipótese, evento destrutivo e teste discriminativo.
        """
        fc = FalsificationCriterion(
            hypothesis="Vendedores usarão etiquetas para recuperar cotações",
            what_would_kill_it="Taxa de abandono superior a 80% nos primeiros 2 dias",
            lowest_cost_discriminating_test="Acompanhar 3 vendedores por 1 dia sem software",
        )
        self.assertEqual(fc.hypothesis, "Vendedores usarão etiquetas para recuperar cotações")
        self.assertIn("80%", fc.what_would_kill_it)
        self.assertIn("sem software", fc.lowest_cost_discriminating_test)

    def test_authority_and_provenance_invariants(self):
        """
        Verificação Estrita de Invariantes de Autoridade e Prova de Proveniência (Seção 23).
        """
        idea_text = "Um aplicativo para gerenciar estoque de pequenas padarias."
        first_pass = {
            "interpreted_problem": "Padarias perdem insumos perecíveis por falta de controle simples.",
            "human_intent": "Gerenciar estoque de pequenas padarias sem ERP pesado.",
            "primary_mechanism": {
                "mechanism": "Controle visual de validade com alertas coloridos",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": [],
            "material_vulnerabilities": [],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Testar em uma padaria amiga",
            "idea_stage": "DISCOVERY",
        }

        fake_runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": first_pass})
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)
        result = lean_runner.run(idea_text)
        artifact = EvolutionArtifactMapper.map_lean_result(result)

        # Prova formal dos 5 invariantes inegociáveis
        self.assertEqual(artifact.original_idea_authority, PromotionAuthorityBasis.USER_EXPLICIT)
        self.assertEqual(artifact.intent_provenance, PromotionAuthorityBasis.VALID_USER_DERIVATION)
        self.assertEqual(artifact.refined_idea_authority, PromotionAuthorityBasis.MODEL_HYPOTHESIS)
        self.assertEqual(artifact.source_anchor.original_content, idea_text)
        self.assertTrue(result.total_model_calls <= LEAN_L1_MAX_MODEL_CALLS)

    def test_false_precision_guard_generalized_comprehensive(self):
        """
        Teste exaustivo da generalização do FalsePrecisionGuard (Seção 10):
        Verifica os 6 casos mínimos de números/métricas não suportadas:
        - <200 ms
        - 99.9%
        - R$ 12.37
        - 3.4x
        - 85% conversion
        - 50 ms latency
        E verifica os 5 casos suportados por base de evidência legítima:
        - USER_SUPPLIED
        - DETERMINISTIC_CALCULATION
        - MEASURED
        - EXTERNAL_EVIDENCE
        - EXPLICIT_HYPOTHESIS
        """
        # 1. Casos não suportados (devem ser detectados)
        unsupported_cases = [
            ("<200 ms", "<200 ms"),
            ("99.9%", "99.9%"),
            ("R$ 12.37", "R$ 12.37"),
            ("3.4x", "3.4x"),
            ("85% conversion", "85% conversion"),
            ("50 ms latency", "50 ms latency"),
        ]
        for expr, expected_token in unsupported_cases:
            detected = FalsePrecisionGuard.detect_unsupported_metrics(f"O resultado projetado é {expr}.")
            self.assertTrue(
                len(detected) > 0,
                f"Falha ao detectar métrica não suportada: {expr}"
            )
            sanitized, downgraded = FalsePrecisionGuard.sanitize_unsupported_precision(f"Meta de {expr} fixada.")
            self.assertTrue(downgraded, f"Falha ao rebaixar métrica não suportada: {expr}")
            self.assertIn("MÉTRICA NÃO MEDIDA", sanitized)

        # 2. Casos suportados (NÃO devem ser rebaixados nem marcados como falsos)
        # 2.1 USER_SUPPLIED via texto fonte original
        src_text = "Quero vender a assinatura por R$ 12.37 e garantir resposta em <200 ms."
        cand_text = "Plataforma com preço de R$ 12.37 e tempo <200 ms."
        detected_user = FalsePrecisionGuard.detect_unsupported_metrics(cand_text, source_text=src_text)
        self.assertEqual(detected_user, [])

        # 2.2 USER_SUPPLIED via flag de base de evidência
        self.assertEqual(
            FalsePrecisionGuard.detect_unsupported_metrics("R$ 12.37", evidence_basis=MetricEvidenceBasis.USER_SUPPLIED),
            []
        )

        # 2.3 DETERMINISTIC_CALCULATION (via tag ou flag)
        self.assertEqual(
            FalsePrecisionGuard.detect_unsupported_metrics("[CALCULADO: 3.4x baseado na relação de custos]"),
            []
        )
        self.assertEqual(
            FalsePrecisionGuard.detect_unsupported_metrics("3.4x", evidence_basis=MetricEvidenceBasis.DETERMINISTIC_CALCULATION),
            []
        )

        # 2.4 MEASURED (via tag ou flag)
        self.assertEqual(
            FalsePrecisionGuard.detect_unsupported_metrics("[MEDIDO: 50 ms latency em benchmark local]"),
            []
        )
        self.assertEqual(
            FalsePrecisionGuard.detect_unsupported_metrics("50 ms latency", evidence_basis=MetricEvidenceBasis.MEASURED),
            []
        )

        # 2.5 EXTERNAL_EVIDENCE (via tag ou flag)
        self.assertEqual(
            FalsePrecisionGuard.detect_unsupported_metrics("[EVIDÊNCIA: 85% conversion segundo estudo de mercado]"),
            []
        )
        self.assertEqual(
            FalsePrecisionGuard.detect_unsupported_metrics("85% conversion", evidence_basis=MetricEvidenceBasis.EXTERNAL_EVIDENCE),
            []
        )

        # 2.6 EXPLICIT_HYPOTHESIS (via tag ou flag)
        self.assertEqual(
            FalsePrecisionGuard.detect_unsupported_metrics("[HIPÓTESE: meta de 99.9% de uptime para testar viabilidade]"),
            []
        )
        self.assertEqual(
            FalsePrecisionGuard.detect_unsupported_metrics("99.9%", evidence_basis=MetricEvidenceBasis.EXPLICIT_HYPOTHESIS),
            []
        )

    def test_decision_relevance_policy_generalized_no_overfit(self):
        """
        Verifica que DecisionRelevancePolicy opera estritamente sobre conceitos tipados (Seção 11):
        - Estágio da ideia (IdeaStage)
        - Categoria de risco (RiskCategory)
        - Relevância decisória (DecisionRelevance)
        - Severidade vs Prioridade (Severity != Priority)
        Sem qualquer overfit ou hardcoding de nichos específicos.
        """
        # Teste com domínio genérico (sem WhatsApp/SaaS/nomes específicos)
        # Em DISCOVERY, risco de conformidade/segurança HIGH deve ter relevância LATER
        relevance_disc = DecisionRelevancePolicy.evaluate_vulnerability_relevance(
            vulnerability_text="Ausência de política formal de conformidade documental",
            severity="HIGH",
            category=RiskCategory.COMPLIANCE,
            stage=IdeaStage.DISCOVERY,
            original_idea="Ideia de clube de assinatura de cafés artesanais.",
        )
        self.assertEqual(relevance_disc, DecisionRelevance.LATER)

        # Em DISCOVERY, risco de comportamento do usuário HIGH deve ter relevância CRITICAL_NOW
        relevance_user = DecisionRelevancePolicy.evaluate_vulnerability_relevance(
            vulnerability_text="Assinantes cancelam após a primeira remessa por falta de novidade",
            severity="HIGH",
            category=RiskCategory.USER_BEHAVIOR,
            stage=IdeaStage.DISCOVERY,
            original_idea="Ideia de clube de assinatura de cafés artesanais.",
        )
        self.assertEqual(relevance_user, DecisionRelevance.CRITICAL_NOW)

        # Em PRE_PRODUCTION, o mesmo risco de conformidade/segurança HIGH torna-se CRITICAL_NOW
        relevance_preprod = DecisionRelevancePolicy.evaluate_vulnerability_relevance(
            vulnerability_text="Ausência de política formal de conformidade documental",
            severity="HIGH",
            category=RiskCategory.COMPLIANCE,
            stage=IdeaStage.PRE_PRODUCTION,
            original_idea="Ideia de clube de assinatura de cafés artesanais.",
        )
        self.assertEqual(relevance_preprod, DecisionRelevance.CRITICAL_NOW)

    def test_next_action_arbitration_comprehensive_matrix(self):
        """
        Verifica a matriz determinística de arbitragem de próximo passo (Seção 12):
        1. DISCOVERY + HIGH later-stage security -> discovery falsification wins.
        2. PRE_PRODUCTION + critical security -> security may win.
        3. EXPLICIT USER SECURITY REQUEST -> security may win.
        4. HUMAN NORMATIVE CHOICE -> AI does not override human authority.
        """
        fp_action = "Entrevistar 10 potenciais clientes para validar o problema real."
        sec_candidate = "Implementar arquitetura de segurança com criptografia TLS e auditoria."

        # 1. DISCOVERY + HIGH later-stage security -> discovery falsification wins
        action1, chg1 = NextActionArbitrationPolicy.arbitrate(
            first_pass_next_action=fp_action,
            escalation_candidate_next_action=sec_candidate,
            stage=IdeaStage.DISCOVERY,
            original_idea="Sistema de agendamento de consultas veterinárias.",
            candidate_risk_category=RiskCategory.SECURITY,
        )
        self.assertEqual(action1, fp_action)
        self.assertFalse(chg1)

        # 2. PRE_PRODUCTION + critical security -> security candidate wins
        action2, chg2 = NextActionArbitrationPolicy.arbitrate(
            first_pass_next_action=fp_action,
            escalation_candidate_next_action=sec_candidate,
            stage=IdeaStage.PRE_PRODUCTION,
            original_idea="Sistema de agendamento de consultas veterinárias.",
            candidate_risk_category=RiskCategory.SECURITY,
        )
        self.assertEqual(action2, sec_candidate)
        self.assertTrue(chg2)

        # 3. EXPLICIT USER SECURITY REQUEST -> security candidate wins
        action3, chg3 = NextActionArbitrationPolicy.arbitrate(
            first_pass_next_action=fp_action,
            escalation_candidate_next_action=sec_candidate,
            stage=IdeaStage.DISCOVERY,
            original_idea="Sistema com foco em segurança rigorosa e sigilo médico.",
            candidate_risk_category=RiskCategory.SECURITY,
        )
        self.assertEqual(action3, sec_candidate)
        self.assertTrue(chg3)

        # 4. HUMAN NORMATIVE CHOICE -> AI does not override human authority
        action4, chg4 = NextActionArbitrationPolicy.arbitrate(
            first_pass_next_action=fp_action,
            escalation_candidate_next_action=sec_candidate,
            stage=IdeaStage.DISCOVERY,
            original_idea="Sistema de agendamento de consultas veterinárias.",
            requires_human_decision=True,
            human_decision_description="Definir política de cancelamento com ou sem cobrança de taxa.",
        )
        self.assertIn("Decisão humana requerida", action4)
        self.assertIn("Definir política de cancelamento", action4)
        self.assertFalse(chg4)

    def test_engineering_requirement_preserved_in_critique(self):
        """
        Verifica a preservação de requisitos de engenharia sob critique (Seção 9):
        - ENGINEERING_REQUIREMENT_PRESERVED = YES
        - ENGINEERING_REQUIREMENT_MUTATES_PRODUCT = NO
        """
        idea_text = "Plataforma de delivery hiperlocal de quitandas de bairro."
        first_pass = {
            "interpreted_problem": "Quitandas locais perdem vendas para grandes redes.",
            "human_intent": "Conectar quitandas a clientes vizinhos.",
            "primary_mechanism": {
                "mechanism": "Catálogo compartilhado via link web direto",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": [],
            "material_vulnerabilities": [
                {
                    "vulnerability": "Vazamento de banco de dados e tráfego de senhas em texto puro",
                    "why_it_matters": "Comprometimento das credenciais das quitandas",
                    "severity": "HIGH",
                    "category": "SECURITY",
                    "decision_relevance": "LATER",
                },
                {
                    "vulnerability": "Quitandeiros não têm tempo de alimentar o catálogo online no dia a dia",
                    "why_it_matters": "Inviabiliza a atualização dos produtos e gera catálogo fantasma",
                    "severity": "HIGH",
                    "category": "USER_BEHAVIOR",
                    "decision_relevance": "CRITICAL_NOW",
                }
            ],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Validar catálogo com 3 quitandeiros vizinhos",
            "idea_stage": "DISCOVERY",
        }

        # Simula escalação focada que propõe mutação técnica
        escalation_data = {
            "escalation_reason": "MATERIAL_VULNERABILITY",
            "target_hypothesis": "Catálogo compartilhado via link web direto",
            "focus_area": "Segurança de dados",
            "hypothesis_mutated": True,
            "mutated_hypothesis_description": "Implementar criptografia AES-256 e TLS 1.3 com autenticação multifator",
            "focused_critique_or_analysis": "Análise técnica de proteção do tráfego",
            "updated_next_action": "Configurar TLS 1.3 e implementar AES",
            "decision_progress_made": True,
        }

        fake_runner = FakeModelRunner(custom_responses={
            "LEAN_FIRST_PASS": first_pass,
            "FOCUSED_ESCALATION": escalation_data,
        })
        lean_runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)
        result = lean_runner.run(idea_text)
        artifact = EvolutionArtifactMapper.map_lean_result(result)

        # 1. Proposta de produto NÃO foi mutada para requisitos de infraestrutura
        self.assertNotIn("AES-256", artifact.refined_idea)
        self.assertNotIn("TLS 1.3", artifact.refined_idea)
        self.assertIn("catálogo", artifact.refined_idea.lower())

        # 2. Requisito técnico foi PRESERVADO em critique_items
        crit_texts = [c.vulnerability for c in artifact.critique]
        self.assertTrue(
            any("Requisito Técnico/Segurança Identificado" in ct and "AES-256" in ct for ct in crit_texts),
            "Requisito técnico não foi preservado sob critique!"
        )

    def test_frozen_lean_core_hash_separation(self):
        """
        Verifica separação e coexistência de identidades de hash de núcleo (Seção 6):
        - V1_0_1_FROZEN_CORE_IDENTITY_PRESERVED = YES
        - V1_1_CANDIDATE_CORE_IDENTITY_SEPARATE = YES
        """
        self.assertEqual(
            FROZEN_LEAN_CORE_HASH_V1_0,
            "e6785bcaf5af291f438ab467386db640d4c0790e0f7012c40773dd25782e5600",
            "Hash do núcleo científico v1.0.1 foi alterado retroativamente!"
        )
        self.assertNotEqual(
            FROZEN_LEAN_CORE_HASH_V1_0,
            FROZEN_LEAN_CORE_HASH_V1_1,
            "Candidato v1.1 deve ter identidade separada da baseline histórica v1.0.1!"
        )

    # =========================================================================
    # SUÍTE ADVERSARIAL RQ-02: GENERALIZAÇÃO DE ENGENHARIA & GROUNDING DE ESTÁGIO
    # =========================================================================

    def test_case_a_premature_kubernetes_migration_rejected_in_discovery(self):
        """
        Caso A (Seção 11): Proposta prematura de migração para Kubernetes em descoberta.
        Invariante: NON_PRODUCT_IMPLEMENTATION_REQUIREMENT != PRODUCT_REFINEMENT.
        A escalação NÃO pode sequestrar o próximo passo de validação de produto.
        """
        idea_text = (
            "Clube de assinatura de cafés artesanais para entusiastas com envio mensal "
            "e grãos selecionados diretamente de pequenos produtores."
        )
        first_pass = {
            "interpreted_problem": "Amantes de café especial têm dificuldade de encontrar grãos frescos de pequenos produtores.",
            "human_intent": "Entregar cafés especiais selecionados por assinatura mensal.",
            "primary_mechanism": {
                "mechanism": "Curadoria mensal enviada por correio com fichas de degustação",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
            },
            "competing_alternatives": [],
            "key_assumptions": ["Consumidores pagam frete fixo por conveniência de curadoria"],
            "material_ambiguities": [],
            "material_vulnerabilities": [
                {
                    "vulnerability": "Usuários podem achar o frete mensal desproporcional ao preço do café",
                    "why_it_matters": "Inviabiliza a margem e causa cancelamento imediato",
                    "severity": "HIGH",
                    "category": "BUSINESS_MODEL",
                    "decision_relevance": "CRITICAL_NOW",
                },
                {
                    "vulnerability": "Escalabilidade de microsserviços e balanceamento de carga de pedidos",
                    "why_it_matters": "Gargalo técnico sob milhares de requisições simultâneas",
                    "severity": "HIGH",
                    "category": "ENGINEERING",
                    "decision_relevance": "LATER",
                }
            ],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Entrevistar 10 consumidores de café especial sobre interesse e faixa de preço viável",
            "idea_stage": "DISCOVERY",
        }
        escalation_data = {
            "escalation_reason": "MATERIAL_VULNERABILITY",
            "target_hypothesis": "Curadoria mensal enviada por correio",
            "hypothesis_mutated": True,
            "mutated_hypothesis_description": "Migrar para Kubernetes e orquestrar clusters multi-região com Helm e Terraform",
            "focused_critique_or_analysis": "Análise técnica de arquitetura de contêineres e alta disponibilidade",
            "updated_next_action": "Migrar para Kubernetes e orquestrar clusters",
            "decision_progress_made": True,
        }

        fake_runner = FakeModelRunner(custom_responses={
            "LEAN_FIRST_PASS": first_pass,
            "FOCUSED_ESCALATION": escalation_data,
        })
        runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)
        result = runner.run(idea_text)
        artifact = EvolutionArtifactMapper.map_lean_result(result)

        # 1. Próximo passo de descoberta é PRESERVADO (rejeita Kubernetes override)
        self.assertEqual(
            artifact.recommended_next_action,
            "Entrevistar 10 consumidores de café especial sobre interesse e faixa de preço viável"
        )
        # 2. Refinamento de produto NÃO foi corrompido para infraestrutura técnica
        self.assertNotIn("Kubernetes", artifact.refined_idea)
        self.assertIn("curadoria", artifact.refined_idea.lower())
        # 3. Requisito de engenharia foi preservado em critique
        crit_texts = [c.vulnerability for c in artifact.critique]
        self.assertTrue(
            any("Requisito Técnico/Engenharia Identificado" in ct and "Kubernetes" in ct for ct in crit_texts),
            "Requisito de Kubernetes deve ser preservado sob critique como requisito técnico!"
        )

    def test_case_b_premature_rust_rewrite_rejected_in_discovery(self):
        """
        Caso B (Seção 11): Proposta prematura de reescrita em Rust em estágio inicial.
        Invariante: Prevenção de refatoração ou reescrita técnica precoce antes da validação.
        """
        idea_text = "Aplicativo para donos de cães agendarem caminhadas compartilhadas no bairro."
        first_pass = {
            "interpreted_problem": "Donos de cães não têm tempo para passear sozinhos e buscam socialização para seus pets.",
            "human_intent": "Conectar donos de cães vizinhos para caminhadas conjuntas.",
            "primary_mechanism": {
                "mechanism": "Grupos locais geolocalizados para passeios em horários comuns",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": [],
            "material_vulnerabilities": [
                {
                    "vulnerability": "Donos têm receio de agressividade ou brigas entre animais desconhecidos",
                    "why_it_matters": "Impede a primeira caminhada conjunta",
                    "severity": "HIGH",
                    "category": "USER_BEHAVIOR",
                    "decision_relevance": "CRITICAL_NOW",
                }
            ],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Validar se 5 donos de cães do mesmo quarteirão aceitariam passear juntos",
            "idea_stage": "DISCOVERY",
        }
        escalation_data = {
            "escalation_reason": "MATERIAL_VULNERABILITY",
            "target_hypothesis": "Grupos locais geolocalizados",
            "hypothesis_mutated": True,
            "mutated_hypothesis_description": "Reescrever em Rust para garantir segurança de memória e concorrência sem garbage collection",
            "focused_critique_or_analysis": "Análise de latência e controle estrito de memória",
            "updated_next_action": "Reescrever em Rust o backend",
            "decision_progress_made": True,
        }

        fake_runner = FakeModelRunner(custom_responses={
            "LEAN_FIRST_PASS": first_pass,
            "FOCUSED_ESCALATION": escalation_data,
        })
        runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)
        result = runner.run(idea_text)
        artifact = EvolutionArtifactMapper.map_lean_result(result)

        # Rejeita override unilateral de reescrita em Rust
        self.assertEqual(
            artifact.recommended_next_action,
            "Validar se 5 donos de cães do mesmo quarteirão aceitariam passear juntos"
        )
        self.assertNotIn("Rust", artifact.refined_idea)
        crit_texts = [c.vulnerability for c in artifact.critique]
        self.assertTrue(any("Requisito Técnico/Engenharia Identificado" in ct and "Rust" in ct for ct in crit_texts))

    def test_case_c_premature_kafka_event_streaming_rejected_in_discovery(self):
        """
        Caso C (Seção 11): Proposta prematura de introdução de Kafka / Event Streaming.
        Invariante: Broker distribuído não substitui validação de mercado/cliente.
        """
        idea_text = "Marketplace de aluguel de ferramentas pesadas de marcenaria entre artesãos autônomos."
        first_pass = {
            "interpreted_problem": "Marceneiros autônomos precisam de maquinário caro para projetos pontuais sem capital para compra.",
            "human_intent": "Intermediar aluguel seguro de máquinas de marcenaria ociosas.",
            "primary_mechanism": {
                "mechanism": "Catálogo com depósito de caução e termo de vistoria presencial",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": [],
            "material_vulnerabilities": [
                {
                    "vulnerability": "Proprietário teme avaria de ferramenta especializada sem restituição rápida",
                    "why_it_matters": "Inviabiliza a oferta de maquinário",
                    "severity": "HIGH",
                    "category": "USER_BEHAVIOR",
                    "decision_relevance": "CRITICAL_NOW",
                }
            ],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Consultar 3 marcenarias se alugariam suas serras de bancada ociosas com caução",
            "idea_stage": "DISCOVERY",
        }
        escalation_data = {
            "escalation_reason": "MATERIAL_VULNERABILITY",
            "target_hypothesis": "Catálogo com depósito de caução",
            "hypothesis_mutated": True,
            "mutated_hypothesis_description": "Introduzir Kafka para mensageria distribuída de eventos e streaming de telemetria",
            "focused_critique_or_analysis": "Estudo de pipeline assíncrono para processamento de eventos",
            "updated_next_action": "Introduzir Kafka para mensageria distribuída",
            "decision_progress_made": True,
        }

        fake_runner = FakeModelRunner(custom_responses={
            "LEAN_FIRST_PASS": first_pass,
            "FOCUSED_ESCALATION": escalation_data,
        })
        runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)
        result = runner.run(idea_text)
        artifact = EvolutionArtifactMapper.map_lean_result(result)

        self.assertEqual(
            artifact.recommended_next_action,
            "Consultar 3 marcenarias se alugariam suas serras de bancada ociosas com caução"
        )
        self.assertNotIn("Kafka", artifact.refined_idea)

    def test_case_d_security_proposal_rejected_in_discovery(self):
        """
        Caso D (Seção 11): Proposta de segurança/criptografia em descoberta sem solicitação do usuário.
        Invariante: Segurança permanece HIGH em severidade, mas LATER em prioridade imediata.
        """
        idea_text = "Rede de apoio comunitário para doação e troca de livros escolares entre famílias."
        first_pass = {
            "interpreted_problem": "Famílias gastam muito com livros didáticos novos enquanto exemplares usados ficam parados.",
            "human_intent": "Facilitar doação e troca direta de livros didáticos entre famílias.",
            "primary_mechanism": {
                "mechanism": "Vitrine comunitária organizada por série escolar e bairro",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": [],
            "material_vulnerabilities": [
                {
                    "vulnerability": "Famílias não terem incentivo de cadastrar livros antigos sem contrapartida",
                    "why_it_matters": "Gera vitrine vazia e perda de tração",
                    "severity": "HIGH",
                    "category": "USER_BEHAVIOR",
                    "decision_relevance": "CRITICAL_NOW",
                }
            ],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Entrevistar pais de 2 escolas sobre acúmulo de livros didáticos parados",
            "idea_stage": "DISCOVERY",
        }
        escalation_data = {
            "escalation_reason": "MATERIAL_VULNERABILITY",
            "target_hypothesis": "Vitrine comunitária organizada por série",
            "hypothesis_mutated": True,
            "mutated_hypothesis_description": "Implementar criptografia E2EE e certificate pinning TLS 1.3",
            "focused_critique_or_analysis": "Análise de privacidade e cifragem do tráfego",
            "updated_next_action": "Configurar TLS 1.3 e implementar E2EE",
            "decision_progress_made": True,
        }

        fake_runner = FakeModelRunner(custom_responses={
            "LEAN_FIRST_PASS": first_pass,
            "FOCUSED_ESCALATION": escalation_data,
        })
        runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)
        result = runner.run(idea_text)
        artifact = EvolutionArtifactMapper.map_lean_result(result)

        # Não permite takeover de segurança sem pedido explícito
        self.assertEqual(
            artifact.recommended_next_action,
            "Entrevistar pais de 2 escolas sobre acúmulo de livros didáticos parados"
        )
        self.assertNotIn("E2EE", artifact.refined_idea)

    def test_case_e_pre_production_infrastructure_blocker_accepted(self):
        """
        Caso E (Seção 11): Bloqueador de infraestrutura em PRÉ-PRODUÇÃO é aceito legitimamente.
        Contra-caso: Em pré-produção, falha de infraestrutura/segurança É um blocker imediato.
        """
        idea_text = (
            "Sistema de emissão de passagens rodoviárias com piloto já validado em 2 operadoras. "
            "Produto implementado e preparando deploy para produção."
        )
        first_pass = {
            "interpreted_problem": "Operadoras precisam emitir passagens de contingência sem queda de conectividade.",
            "human_intent": "Garantir emissão de passagens em pré-produção para homologação final.",
            "primary_mechanism": {
                "mechanism": "API de reserva síncrona com confirmação imediata",
                "is_explicit_in_source": True,
                "claimed_basis": "USER_EXPLICIT",
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": [],
            "material_vulnerabilities": [
                {
                    "vulnerability": "Queda do cluster pode deixar passageiros sem emissão no momento do embarque",
                    "why_it_matters": "Bloqueador direto de homologação e produção",
                    "severity": "HIGH",
                    "category": "ENGINEERING",
                    "decision_relevance": "CRITICAL_NOW",
                }
            ],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": False,
            "proposed_next_action": "Revisar contratos operacionais",
            "idea_stage": "PRE_PRODUCTION",
        }
        escalation_data = {
            "escalation_reason": "MATERIAL_VULNERABILITY",
            "target_hypothesis": "API de reserva síncrona",
            "hypothesis_mutated": False,
            "focused_critique_or_analysis": "Análise de alta disponibilidade necessária para autorização de produção",
            "updated_next_action": "Configurar cluster Kubernetes redundante com failover automático e TLS para deploy de produção",
            "decision_progress_made": True,
        }

        fake_runner = FakeModelRunner(custom_responses={
            "LEAN_FIRST_PASS": first_pass,
            "FOCUSED_ESCALATION": escalation_data,
        })
        runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)
        result = runner.run(idea_text)
        artifact = EvolutionArtifactMapper.map_lean_result(result)

        # Em pré-produção, o bloqueador de infraestrutura É aceito como próximo passo
        self.assertEqual(
            artifact.recommended_next_action,
            "Configurar cluster Kubernetes redundante com failover automático e TLS para deploy de produção"
        )

    def test_case_f_future_mvp_roadmap_mention_cannot_promote_to_mvp(self):
        """
        Caso F (Seção 12 & 13): Menção a futuro MVP no roadmap NÃO promove o estágio atual para MVP.
        Invariante: MENTIONED_FUTURE_STAGE != CURRENT_IDEA_STAGE.
        """
        idea_text = (
            "Pesquisa exploratória sobre biossensores para monitoramento de hidratação em atletas. "
            "No futuro planejamos lançar um MVP para corredores amadores, mas ainda não validamos a receptividade do público."
        )
        assessment = IdeaStageGroundingPolicy.ground_stage(
            declared_stage=IdeaStage.MVP,
            declared_justification="Texto menciona planejamento de MVP futuro",
            source_text=idea_text,
        )

        # Estágio atual ancorado DEVE ser DISCOVERY, e MVP reconhecido como estágio futuro
        self.assertEqual(assessment.current_stage, IdeaStage.DISCOVERY)
        self.assertIn(IdeaStage.MVP, assessment.mentioned_future_stages)
        self.assertEqual(assessment.basis, StageProvenanceBasis.SOURCE_SUPPORTED_INFERENCE)

    def test_case_g_future_production_mention_cannot_promote_to_pre_production(self):
        """
        Caso G (Seção 12 & 13): Menção a produção futura NÃO promove ideia conceitual para PRE_PRODUCTION.
        Invariante: MODEL_STAGE_INFERENCE != USER_EXPLICIT_STAGE (não fabrica maturidade).
        """
        idea_text = (
            "Ideia conceitual de robô autônomo para limpeza de painéis solares em grandes usinas. "
            "A produção em escala está prevista para 2028 no roadmap, mas hoje o experimento de cliente zero ainda não foi executado."
        )
        assessment = IdeaStageGroundingPolicy.ground_stage(
            declared_stage=IdeaStage.PRE_PRODUCTION,
            declared_justification="Texto menciona produção em escala no roadmap",
            source_text=idea_text,
        )

        self.assertEqual(assessment.current_stage, IdeaStage.DISCOVERY)
        self.assertIn(IdeaStage.PRE_PRODUCTION, assessment.mentioned_future_stages)
        self.assertNotEqual(assessment.current_stage, IdeaStage.PRE_PRODUCTION)

    def test_case_h_explicit_pre_production_accepted(self):
        """
        Caso H (Seção 12 & 13): Usuário explicita que o produto está implementado e piloto validado.
        Contra-caso: Quando a maturidade é explícita na fonte, PRE_PRODUCTION é reconhecido com proveniência.
        """
        idea_text = (
            "Software de telemetria veicular para frotas de entrega urbana. "
            "Produto implementado e piloto validado com 3 transportadoras parceiras; preparando deploy de produção."
        )
        assessment = IdeaStageGroundingPolicy.ground_stage(
            declared_stage=IdeaStage.PRE_PRODUCTION,
            declared_justification="Usuário declara piloto validado e produto implementado",
            source_text=idea_text,
        )

        self.assertEqual(assessment.current_stage, IdeaStage.PRE_PRODUCTION)
        self.assertEqual(assessment.basis, StageProvenanceBasis.USER_EXPLICIT_CURRENT_STAGE)

    def test_case_i_human_normative_authority_sovereign_zero_ai_calls(self):
        """
        Caso I (Seção 14): Decisão normativa humana soberana interrompe inferência extra.
        Invariante: Missing Human Authority -> STOP, No AI call. Exatamente 1 chamada utilizada.
        """
        idea_text = (
            "Algoritmo de triagem de bolsas de estudo que precisa decidir se prioriza "
            "vulnerabilidade de renda per capita ou diversidade regional."
        )
        first_pass = {
            "interpreted_problem": "Vagas limitadas de bolsas de estudo exigem critério de desempate.",
            "human_intent": "Selecionar bolsistas com critério justo e transparente.",
            "primary_mechanism": {
                "mechanism": "Score ponderado combinando renda e região",
                "is_explicit_in_source": False,
                "claimed_basis": "MODEL_HYPOTHESIS",
            },
            "competing_alternatives": [],
            "key_assumptions": [],
            "material_ambiguities": ["Escolha normativa entre priorizar renda extrema ou equilíbrio regional"],
            "material_vulnerabilities": [],
            "remaining_uncertainties": [],
            "requires_human_normative_choice": True,
            "human_choice_description": "Definir se o critério soberano é vulnerabilidade de renda ou cobertura regional.",
            "proposed_next_action": "Apresentar opções de ponderação para o comitê acadêmico",
            "idea_stage": "DISCOVERY",
        }

        fake_runner = FakeModelRunner(custom_responses={"LEAN_FIRST_PASS": first_pass})
        runner = LeanLoopRunner(runner=fake_runner, runs_dir=self.runs_dir)
        result = runner.run(idea_text)
        artifact = EvolutionArtifactMapper.map_lean_result(result)

        # 1. Gate interrompe e solicita autoridade humana soberana
        self.assertEqual(result.gate_result.outcome, GateOutcome.REQUEST_HUMAN_DECISION)
        # 2. Exatamente 1 chamada de modelo utilizada (zero inferência extra paga ou livre)
        self.assertEqual(result.total_model_calls, 1)
        self.assertEqual(result.terminal_status, "HUMAN_DECISION_REQUIRED")
        self.assertTrue(artifact.human_decision_required)
        # 3. Próximo passo é a decisão humana protegida
        self.assertIn("Decisão humana requerida", artifact.recommended_next_action)
        self.assertIn("vulnerabilidade de renda ou cobertura regional", artifact.recommended_next_action)


if __name__ == "__main__":
    unittest.main(verbosity=2)
