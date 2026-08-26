"""
src/idea_evolution/providers/fake.py
Executor Fake/Mock para testes 100% determinísticos e offline do Simple Loop MVP.
"""

from typing import Type, TypeVar, Optional, Dict, Any, Callable
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
                proposed_mechanism="Pipeline sequencial dirigido de funções de IA com persistência determinística de estado.",
                actors_or_users=["Criadores", "Engenheiros", "Pesquisadores"],
                assumptions=["Usuários valorizam rastreabilidade e crítica rigorosa mais do que bajulação."],
                ambiguities=["Qual o formato ideal de teste de realidade para produtos puramente de software?"],
                strengths=["Simplicidade arquitetural", "Rastreabilidade completa"],
                structured_idea="Sistema de evolução de ideias composto por estágios especializados de compreensão, ataque, alternativas e síntese.",
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
                feasibility_notes=["A camada fina sobre Pydantic roda em < 50ms localmente sem overhead de rede."],
                reality_dependencies=["Disponibilidade de chave de API para o modo real ou execução offline com mocks."],
                claims_needing_evidence=["Afirmação de que o loop produz saídas percebidas como mais úteis que o baseline."],
                potential_blockers=["Falta de conectividade externa em ambientes isolados."],
                candidate_tests=[
                    "Executar teste cego A/B comparando o Simple Loop contra o prompt único sobre 3 fixtures padronizadas.",
                    "Medir a taxa de conformidade de schema em 100 execuções sucessivas.",
                ],
            )

        if schema == SynthesizeOutput:
            return SynthesizeOutput(
                refined_idea="Idea Evolution Engine (Simple Loop): Motor sequencial CLI que recebe uma ideia humana crua, submete a 6 estágios dirigidos, valida esquemas e devolve um pacote de maturação estruturado com rastreabilidade total.",
                accepted_changes=[
                    "Implementação de contratos Pydantic estritos para cada estágio.",
                    "Isolamento do kernel determinístico contra alucinações de estado.",
                    "Preservação imutável da ideia original.",
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
                    unresolved_critical_issue=True,
                    recommendation="RECONSTRUCT",
                    review_summary="Recomendada uma rodada adicional de reconstrução para sanar a ambiguidade de limites.",
                )

            # Se for para forçar essence drift
            if self.trigger_essence_drift:
                return FinalReviewOutput(
                    material_issues_remaining=[],
                    essence_drift_detected=True,
                    drift_explanation="A síntese transformou um aplicativo de bookmarks em um sistema operacional distribuído.",
                    unresolved_critical_issue=True,
                    recommendation="RECONSTRUCT",
                    review_summary="Desvio de essência crítico detectado.",
                )

            return FinalReviewOutput(
                material_issues_remaining=[],
                essence_drift_detected=False,
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

        raise ValueError(f"Schema desconhecido para FakeModelRunner: {schema}")
