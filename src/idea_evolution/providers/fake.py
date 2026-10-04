"""
src/idea_evolution/providers/fake.py
Executor Fake/Mock para testes 100% determinísticos e offline do Simple Loop MVP.
"""

from typing import Type, TypeVar, Optional, Dict, Any, Callable
from copy import deepcopy
import json
import time
from pydantic import BaseModel
from src.idea_evolution.providers.base import ModelRunner, ModelResponse, ModelUsage
from src.idea_evolution.stages.contracts import (
    UnderstandOutput,
    AttackOutput,
    CritiqueOutput,
    RevisionOutput,
    AlternativesOutput,
    RealityCheckOutput,
    SynthesizeOutput,
    FinalReviewOutput,
    BaselineRefineOutput,
    IssueDetail,
    AlternativeItem,
    RejectedItem,
)

T = TypeVar("T", bound=BaseModel)


class FakeModelRunner(ModelRunner):
    """
    Simulador determinístico de inferência de LLM.
    Permite injetar respostas sob medida ou gerar mocks válidos padrão para cada estágio.
    """

    def __init__(
        self,
        provider: str = "fake",
        default_model: str = "fake-model-v1",
        custom_responses: Optional[Dict[str, Any]] = None,
        should_fail_schema_stages: Optional[Dict[str, int]] = None,
        trigger_reconstruction: bool = False,
        trigger_essence_drift: bool = False,
    ):
        self.provider = provider
        self.default_model = default_model
        self.custom_responses = custom_responses or {}
        self.should_fail_schema_stages = should_fail_schema_stages or {}
        self.trigger_reconstruction = trigger_reconstruction
        self.trigger_essence_drift = trigger_essence_drift
        self.call_counts: Dict[str, int] = {}
        self.prompt_history: Dict[str, list[str]] = {}

    @staticmethod
    def _legacy_first_pass_fixture_with_m2_fields(data: Dict[str, Any], prompt_text: str) -> Dict[str, Any]:
        """Keep older focused fake fixtures usable while M2 tests provide explicit rich output."""
        enriched = deepcopy(data)
        marker = "IDEIA HUMANA:\n"
        source_tail = prompt_text.split(marker, 1)[1] if marker in prompt_text else ""
        original_idea = source_tail.split("\n\nCONTRATO DE MATURAÇÃO:", 1)[0]
        if not original_idea:
            original_idea = source_tail.split("\n\nDIRETRIZES DE QUALIDADE", 1)[0]
        original_idea = original_idea.strip()

        primary = enriched.get("primary_mechanism")
        if not isinstance(primary, dict):
            return enriched
        first_intent_id = "I-CORE-1"
        ledger = enriched.get("intent_ledger")
        if ledger is None:
            human_intent = enriched.get("human_intent") or original_idea or "Intenção da ideia de teste."
            treatment = enriched.get("current_form") or primary.get("mechanism") or human_intent
            ledger = [{
                "intent_id": first_intent_id,
                "source_quote": original_idea,
                "interpretation": human_intent,
                "importance": "CORE_INTENT",
                "origin_type": "USER_EXPLICIT",
                "treatment_in_current_form": treatment,
                "status": "PRESERVED",
            }]
            enriched["intent_ledger"] = ledger
        if ledger:
            first_intent_id = ledger[0].get("intent_id", first_intent_id)

        enriched.setdefault("current_form", primary.get("mechanism") or enriched.get("human_intent") or original_idea)
        enriched.setdefault("useful_insights", [])
        enriched.setdefault("open_decisions", [])
        enriched.setdefault("proposed_next_action", "Investigar a incerteza mais relevante antes de implementar.")
        uncertainties = enriched.get("remaining_uncertainties") or enriched.get("material_ambiguities") or []
        if not enriched.get("proposed_next_action_target_uncertainty"):
            enriched["proposed_next_action_target_uncertainty"] = uncertainties[0] if uncertainties else ""

        primary.setdefault("intent_ids", [first_intent_id])
        for alternative in enriched.get("competing_alternatives") or []:
            if isinstance(alternative, dict):
                alternative.setdefault("intent_ids", [first_intent_id])
        return enriched

    def generate(
        self,
        prompt_text: str,
        output_schema: Type[T],
        stage_name: str,
        model_name: Optional[str] = None,
        max_repairs: int = 1,
    ) -> ModelResponse:
        self.call_counts[stage_name] = self.call_counts.get(stage_name, 0) + 1
        call_idx = self.call_counts[stage_name]
        self.prompt_history.setdefault(stage_name, []).append(prompt_text)

        # Simular falha de schema se solicitado
        fail_times = self.should_fail_schema_stages.get(stage_name, 0)
        if fail_times > 0 and call_idx <= fail_times:
            # Se for apenas 1 tentativa de falha e max_repairs >= 1, o próximo repair terá sucesso
            if call_idx < fail_times or max_repairs == 0:
                raw_invalid = "INVALID_JSON_GARBAGE_ERROR"
                return ModelResponse(
                    parsed=None,
                    raw_text=raw_invalid,
                    provider=self.provider,
                    model=model_name or self.default_model,
                    retry_count=call_idx,
                    error=f"JSONDecodeError: invalid format on {stage_name}",
                )

        # Se houver resposta customizada injetada
        if stage_name in self.custom_responses:
            data = self.custom_responses[stage_name]
            if callable(data):
                data = data(prompt_text, call_idx)
            if isinstance(data, dict):
                if output_schema.__name__ == "LeanFirstPassOutput":
                    data = self._legacy_first_pass_fixture_with_m2_fields(data, prompt_text)
                parsed = output_schema.model_validate(data)
                return ModelResponse(
                    parsed=parsed,
                    raw_text=json.dumps(data, indent=2),
                    provider=self.provider,
                    model=model_name or self.default_model,
                    usage=ModelUsage(prompt_tokens=150, completion_tokens=100, total_tokens=250),
                )

        # Respostas padrão determinísticas por tipo de schema
        default_obj = self._generate_default_for_schema(output_schema, stage_name, call_idx)
        if output_schema.__name__ == "LeanFirstPassOutput":
            default_data = self._legacy_first_pass_fixture_with_m2_fields(
                default_obj.model_dump(exclude_defaults=True), prompt_text
            )
            default_obj = output_schema.model_validate(default_data)
        raw_text = default_obj.model_dump_json(indent=2)
        return ModelResponse(
            parsed=default_obj,
            raw_text=raw_text,
            provider=self.provider,
            model=model_name or self.default_model,
            usage=ModelUsage(prompt_tokens=200, completion_tokens=150, total_tokens=350),
            latency_seconds=0.01,
        )

    def _generate_default_for_schema(self, schema: Type[T], stage_name: str, call_idx: int) -> BaseModel:
        if schema == UnderstandOutput:
            return UnderstandOutput(
                interpreted_problem="Dificuldade do usuário em organizar e maturar ideias dispersas de forma estruturada.",
                human_intent="Ajudar seres humanos a transformar ideias cruas em hipóteses acionáveis sem perda de intenção.",
                proposed_mechanism="Processo sequencial de clarificação e estruturação de ideias.",
                explicit_mechanism="Processo sequencial de clarificação e estruturação de ideias.",
                inferred_candidates=[],
                actors_or_users=["Criadores", "Engenheiros", "Pesquisadores"],
                assumptions=["Usuários valorizam rastreabilidade e crítica rigorosa mais do que bajulação."],
                ambiguities=["Qual o formato ideal de teste de realidade para produtos puramente de software?"],
                strengths=["Simplicidade arquitetural", "Rastreabilidade completa"],
                structured_idea="Ferramenta de clarificação de ideias que recebe uma formulação vaga e produz uma representação estruturada.",
            )

        if schema == AttackOutput:
            return AttackOutput(
                critical_issues=[
                    IssueDetail(
                        issue="Risco de sobrecarga de tokens e latência excessiva se o loop não tiver condições de parada estritas.",
                        why_it_matters="Pode inviabilizar o custo por ideia processada.",
                        severity="HIGH",
                        affected_part="Orquestração e limites de ciclo",
                    ),
                    IssueDetail(
                        issue="Críticas podem se tornar genéricas se os prompts não impuserem Truth Over Agreement.",
                        why_it_matters="Reduz o Decision Delta e gera valor perceptual ilusório.",
                        severity="MEDIUM",
                        affected_part="Prompts de ataque",
                    ),
                ],
                fragile_assumptions=["Modelos de linguagem respeitam esquemas complexos sem reparo mecânico."],
                contradictions=[],
                failure_modes=["Loop infinito em caso de rejeição perpétua no estágio de revisão final."],
                missing_information=["Dados sobre preferências de formato de saída entre diferentes perfis de usuário."],
                overclaims=["Afirmar que o sistema garante que a ideia terá sucesso no mercado."],
            )

        if schema == CritiqueOutput:
            return CritiqueOutput(
                critical_issues=[
                    IssueDetail(
                        issue=f"Crítica focada ({stage_name}): Premissa de validação sem atrito precisa de teste empírico.",
                        why_it_matters="Pode falhar em situações reais fora do laboratório.",
                        severity="HIGH",
                        affected_part="Viabilidade operacional",
                    )
                ],
                fragile_assumptions=["Usuário aceitará críticas severas à sua ideia inicial."],
                contradictions=[],
                failure_modes=["Rejeição emocional pelo usuário."],
                missing_information=[],
            )

        if schema == RevisionOutput:
            return RevisionOutput(
                revised_idea="Ideia revisada incorporando filtros de bounded retry e contratos estritos de estágio.",
                changes_applied=["Adicionado limite mecânico de 1 ciclo de reconstrução."],
                issues_addressed=["Sobrecarga de tokens e latência."],
                intent_preserved=True,
                justification="Os limites protegem a viabilidade sem comprometer o rigor investigativo.",
            )

        if schema == AlternativesOutput:
            return AlternativesOutput(
                alternatives=[
                    AlternativeItem(
                        mechanism="Executar pipeline sequencial determinístico com contratos estritos Pydantic.",
                        addresses_issues=["Latência e quebra de schemas"],
                        preserves_intent=True,
                        tradeoffs=["Menor flexibilidade dinâmica em favor de 100% de previsibilidade."],
                        novelty_or_difference="Separação total entre kernel determinístico e funções semânticas.",
                    ),
                    AlternativeItem(
                        mechanism="Utilizar um único modelo com prompt estruturado em múltiplas seções.",
                        addresses_issues=["Custo de coordenação"],
                        preserves_intent=True,
                        tradeoffs=["Menor isolamento de contexto e menor severidade crítica."],
                        novelty_or_difference="Baseline de prompt único.",
                    ),
                ]
            )

        if schema == RealityCheckOutput:
            return RealityCheckOutput(
                target_core_mechanism="Pipeline determinístico de 6 estágios em Python com validação de schemas Pydantic e imutabilidade do input.",
                feasibility_notes=["A camada fina sobre Pydantic roda em < 50ms localmente sem overhead de rede."],
                reality_dependencies=["Disponibilidade de chave de API para o modo real ou execução offline com mocks."],
                claims_needing_evidence=["Afirmação de que o loop produz saídas percebidas como mais úteis que o baseline."],
                potential_blockers=["Falta de conectividade externa em ambientes isolados."],
                candidate_tests=[
                    "Executar teste cego A/B comparando o Simple Loop contra o prompt único sobre 3 fixtures padronizadas.",
                    "Medir a taxa de conformidade de schema em 100 execuções sucessivas do pipeline determinístico.",
                ],
                exploratory_candidate_tests=[],
            )

        if schema == SynthesizeOutput:
            from src.idea_evolution.stages.contracts import AcceptedChangeItem
            return SynthesizeOutput(
                refined_idea="Idea Evolution Engine (Simple Loop): Motor sequencial CLI que recebe uma ideia humana crua, submete a 6 estágios dirigidos, valida esquemas e devolve um pacote de maturação estruturado com rastreabilidade total.",
                core_mechanism="Pipeline determinístico de 6 estágios em Python com validação de schemas Pydantic e imutabilidade do input.",
                core_mechanism_justification="Atende à intenção humana de estruturação com máxima previsibilidade e zero dependências de rede.",
                core_mechanism_basis="VALID_USER_DERIVATION",
                accepted_changes=[
                    AcceptedChangeItem(
                        proposal="Implementação de contratos Pydantic estritos para cada estágio.",
                        promotion_reason="Garante contenção total de tipos e validação estrita sem alucinação de dados.",
                        promotion_basis="VALID_USER_DERIVATION",
                        source_stage="ALTERNATIVES",
                        evidence_or_decision_basis="Contratos determinísticos",
                    ),
                    AcceptedChangeItem(
                        proposal="Isolamento do kernel determinístico contra alucinações de estado.",
                        promotion_reason="Impede mutação arbitrária de campos constitucionais.",
                        promotion_basis="VALID_USER_DERIVATION",
                        source_stage="ALTERNATIVES",
                        evidence_or_decision_basis="Constituição v1.0",
                    ),
                    AcceptedChangeItem(
                        proposal="Preservação imutável da ideia original.",
                        promotion_reason="Protege a intenção humana inicial contra essence drift.",
                        promotion_basis="USER_EXPLICIT",
                        source_stage="UNDERSTAND",
                        evidence_or_decision_basis="Regra de fidelidade",
                    ),
                ],
                candidate_possibilities=[
                    "Modo de auditoria interativo com checkpoints gráficos no terminal.",
                    "Suporte a plugins de exportação para ferramentas de issue tracking.",
                ],
                rejected_changes=[
                    RejectedItem(
                        proposal="Adicionar banco de dados vetorial e interface gráfica web.",
                        reason_rejected="Viola o princípio Simple Before Platform e expande desnecessariamente o escopo do MVP.",
                        source_stage="ALTERNATIVES",
                    )
                ],
                remaining_uncertainties=["Calibração ótima da severidade do prompt ATTACK para diferentes domínios de ideias."],
                known_risks=["Custo computacional se executado sobre modelos proprietários de altíssimo custo sem controle de budget."],
                recommended_next_step="Executar experimento EXP-M04-001 comparando a saída do loop com o baseline de prompt único.",
            )

        if schema == FinalReviewOutput:
            # Se for para forçar reconstrução na primeira chamada
            if self.trigger_reconstruction and call_idx == 1:
                return FinalReviewOutput(
                    material_issues_remaining=["Persistem dúvidas sobre o limite de reconstrução no pipeline."],
                    essence_drift_detected=False,
                    speculative_accretion_detected=False,
                    unresolved_critical_issue=True,
                    recommendation="RECONSTRUCT",
                    review_summary="Recomendada uma rodada adicional de reconstrução para sanar a ambiguidade de limites.",
                )

            # Se for para forçar essence drift
            if self.trigger_essence_drift:
                return FinalReviewOutput(
                    material_issues_remaining=[],
                    essence_drift_detected=True,
                    speculative_accretion_detected=True,
                    drift_explanation="A síntese transformou um aplicativo de bookmarks em um sistema operacional distribuído com blockchain.",
                    unresolved_critical_issue=True,
                    recommendation="RECONSTRUCT",
                    review_summary="Desvio de essência crítico e inchaço especulativo detectados.",
                )

            return FinalReviewOutput(
                material_issues_remaining=[],
                essence_drift_detected=False,
                speculative_accretion_detected=False,
                drift_explanation="",
                unresolved_critical_issue=False,
                recommendation="REFINED_IDEA_READY",
                review_summary="O loop concluiu com sucesso todas as etapas de maturação sem desvio de essência.",
            )

        if schema == BaselineRefineOutput:
            return BaselineRefineOutput(
                summary="Refinamento genérico direto da ideia proposta.",
                strengths=["Ideia promissora com apelo para produtividade."],
                weaknesses=["Falta detalhamento dos estágios e dos modos de falha."],
                refined_version="Uma ferramenta inteligente para captura e organização de ideias com auxílio de IA.",
                next_steps=["Criar um protótipo e testar com usuários."],
            )

        # Suporte aos schemas do Lean IEE L1
        try:
            from src.idea_evolution.domain.early_epistemic_gate import (
                LeanFirstPassOutput,
                FocusedEscalationOutput,
                LeanCandidateMechanism,
                LeanVulnerability,
                EscalationReason,
            )
            from src.idea_evolution.domain.state import PromotionAuthorityBasis

            if schema == LeanFirstPassOutput:
                return LeanFirstPassOutput(
                    interpreted_problem="Dificuldade em estruturar ideias dispersas de forma clara.",
                    human_intent="Ajudar pessoas a transformar ideias vagas em projetos claros.",
                    primary_mechanism=LeanCandidateMechanism(
                        mechanism="Questionário guiado mínimo com exportação direta.",
                        is_explicit_in_source=False,
                        claimed_basis=PromotionAuthorityBasis.MODEL_HYPOTHESIS,
                        justification="Hipótese plausível para estruturação de projetos.",
                        tradeoffs=["Pode limitar ideação livre."],
                    ),
                    competing_alternatives=[],
                    key_assumptions=["Usuário deseja clareza rápida."],
                    material_ambiguities=[],
                    material_vulnerabilities=[],
                    remaining_uncertainties=[],
                    requires_human_normative_choice=False,
                    human_choice_description="",
                    proposed_next_action="Criar mock do questionário guiado.",
                )

            if schema == FocusedEscalationOutput:
                return FocusedEscalationOutput(
                    escalation_reason=EscalationReason.MATERIAL_VULNERABILITY,
                    target_hypothesis="Questionário guiado mínimo com exportação direta.",
                    focused_critique_or_analysis="Análise focada de vulnerabilidade completada com sucesso.",
                    resolved_tradeoffs=["Definido limite de 5 perguntas para evitar fadiga."],
                    discriminating_tests=["Teste A/B com 10 usuários medindo taxa de conclusão."],
                    hypothesis_mutated=False,
                    mutated_hypothesis_description="",
                    decision_progress_made=True,
                    updated_next_action="Construir protótipo com limite de 5 perguntas.",
                )
        except ImportError:
            pass

        raise ValueError(f"Schema desconhecido para FakeModelRunner: {schema}")

