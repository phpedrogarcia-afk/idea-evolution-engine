"""
src/idea_evolution/orchestration/lean_loop.py
Orquestrador Offline da Arquitetura Lean IEE L1 (LeanLoopRunner).
Executa 1 chamada nominal (Lean First Pass), avalia o Early Epistemic Gate (custo 0),
e executa no máximo 1 escalação focada sob gatilho de incerteza material (MAX CALLS = 2).
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
import json
import hashlib
from datetime import datetime
from pydantic import BaseModel, Field

from src.idea_evolution.domain.state import SimpleIdeaState, RunStatus, PromotionAuthorityBasis, OntologyState
from src.idea_evolution.domain.epistemic_contracts import SourceAnchor, SourceAnchorKind, NegativeKnowledgeRecord, IdeaLineageNode
from src.idea_evolution.domain.early_epistemic_gate import (
    LeanFirstPassOutput,
    FocusedEscalationOutput,
    EarlyEpistemicGate,
    GateOutcome,
    EscalationReason,
    DecisionDeltaRecord,
    EpistemicRentRecord,
    GateEvaluationResult,
)
from src.idea_evolution.domain.decision_relevance import (
    IdeaStage,
    RiskCategory,
    DecisionRelevance,
    FalsePrecisionGuard,
    NextActionArbitrationPolicy,
    DecisionRelevancePolicy,
)
from src.idea_evolution.domain.grounding import AuthorityProofValidator
from src.idea_evolution.providers.base import ModelRunner, ModelResponse
from src.idea_evolution.tracing.tracer import RunTracer

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
PROMPTS_DIR = REPO_ROOT / "prompts"

# Invariante rígido de arquitetura L1
LEAN_L1_MAX_MODEL_CALLS = 2


class LeanRunResult(BaseModel):
    """Resultado final consolidado da execução do LeanLoopRunner."""
    run_id: str
    source_anchor: SourceAnchor
    first_pass: Optional[LeanFirstPassOutput] = None
    gate_result: Optional[GateEvaluationResult] = None
    escalation_result: Optional[FocusedEscalationOutput] = None
    decision_delta: Optional[DecisionDeltaRecord] = None
    epistemic_rent: Optional[EpistemicRentRecord] = None
    total_model_calls: int = 0
    terminal_status: str = "COMPLETED"
    reconstruction_attempts: int = 0  # Sempre 0 em L1 (não herda reconstrução)
    human_decision_requested: bool = False
    decision_progress_detected: bool = True
    final_markdown: str = ""


class LeanLoopRunner:
    """
    Controlador de execução do Lean IEE L1.
    Garante o invariante inegociável LEAN_L1_MAX_MODEL_CALLS <= 2.
    """

    def __init__(
        self,
        runner: ModelRunner,
        model_name: Optional[str] = None,
        negative_knowledge_pool: Optional[List[NegativeKnowledgeRecord]] = None,
        runs_dir: Optional[Path] = None,
    ):
        self.runner = runner
        self.model_name = model_name
        self.negative_knowledge_pool = negative_knowledge_pool or []
        self.runs_dir = runs_dir

    @staticmethod
    def _qualify_quantitative_decision_texts(output: Any, source_text: str) -> None:
        """Mark model-generated numeric criteria/actions unless the source anchors them."""
        for field_name in (
            "proposed_next_action",
            "updated_next_action",
            "candidate_updated_next_action",
            "current_form",
        ):
            value = getattr(output, field_name, None)
            if isinstance(value, str) and value:
                qualified, _ = FalsePrecisionGuard.qualify_quantitative_decision_text(
                    value,
                    source_text=source_text,
                )
                setattr(output, field_name, qualified)

        for criterion in getattr(output, "falsification_criteria", []) or []:
            for field_name in (
                "hypothesis",
                "what_would_kill_it",
                "lowest_cost_discriminating_test",
            ):
                value = getattr(criterion, field_name, "")
                if value:
                    qualified, _ = FalsePrecisionGuard.qualify_quantitative_decision_text(
                        value,
                        source_text=source_text,
                    )
                    setattr(criterion, field_name, qualified)

        for index, test in enumerate(getattr(output, "discriminating_tests", []) or []):
            qualified, _ = FalsePrecisionGuard.qualify_quantitative_decision_text(
                test,
                source_text=source_text,
            )
            output.discriminating_tests[index] = qualified

    @staticmethod
    def _build_first_pass_prompt(idea: str) -> str:
        first_pass_prompt_template = (
            "Você é o analista do Lean Idea Evolution Engine.\n"
            "Faça uma MATURAÇÃO FORTE em uma única primeira passagem. MATURAÇÃO NÃO É REESCRITA, NÃO É RESUMO e NÃO é apenas tornar a ideia mais concreta.\n"
            "Preserve intenção, explore, distinga intenção de implementação, critique e sintetize provisoriamente sem decidir pelo usuário.\n\n"
            "IDEIA HUMANA:\n{idea}\n\n"
            "CONTRATO DE MATURAÇÃO:\n"
            "1. Identifique intenção central (CORE_INTENT), subintenções materiais e restrições explícitas; separe o objetivo do usuário de mecanismos de implementação.\n"
            "2. Preencha intent_ledger para cada item material. USER_EXPLICIT exige source_quote copiada exatamente e contígua da ideia original; não parafraseie nem normalize. Use MODEL_INTERPRETATION para inferências; nunca as apresente como texto explícito.\n"
            "3. Antes de favorecer implementação, avalie se a ideia é OPEN ou NARROW. Em OPEN, explore caminhos materialmente distintos quando úteis; em NARROW, um caminho adequado basta. Não force exatamente três alternativas nem crie diversidade artificial.\n"
            "4. primary_mechanism e competing_alternatives são candidate paths, não a definição da ideia nem decisões do usuário. Para cada um forneça intent_ids atendidos, mecanismo, justificativa e trade-offs. Mecanismos são MODEL_HYPOTHESIS; path_id é atribuído deterministicamente pelo adaptador.\n"
            "5. Explique mecanismos, critique riscos e trade-offs, exponha pressupostos e incertezas. Busque ganho conceitual útil sem forçar novidade. Retorne useful_insights como descrições curtas; a lista pode ser vazia.\n"
            "6. Produza current_form: síntese explícita, provisória e adequada para representar a ideia maturada. Preserve intenção e subintenções materiais; não transforme um candidate path em definição ou decisão final.\n"
            "7. Use open_decisions como perguntas curtas apenas para escolhas genuinamente abertas; isso não significa HUMAN_DECISION_REQUIRED.\n"
            "8. Proponha um próximo passo discriminativo ligado à incerteza que mais poderia mudar a direção. Copie-a exatamente em proposed_next_action_target_uncertainty; use string vazia se nenhuma incerteza aplicável existir.\n"
            "9. Não declare cobertura aprovada: M2 sempre deixa coverage_status=NOT_EVALUATED. O auto-relato do modelo não prova cobertura, contradição ou verdade.\n\n"
            "DIRETRIZES DE QUALIDADE E RELEVÂNCIA DECISÓRIA:\n"
            "1. Identifique o estágio operacional atual da ideia (idea_stage: DISCOVERY, VALIDATION, PROTOTYPE, MVP, PRE_PRODUCTION, etc.). Atenção: MENTIONED_FUTURE_STAGE != CURRENT_IDEA_STAGE. Se menciona futuro MVP/produção ou há validação pendente/não executada, o estágio atual é DISCOVERY/VALIDATION, nunca MVP/PRE_PRODUCTION.\n"
            "2. Distinga severidade de prioridade imediata (Severity != Priority). Em estágio inicial, requisitos não-funcionais de infraestrutura/engenharia e vulnerabilidades de segurança/privacidade/conformidade recebem severidade real, mas relevância decisória LATER; priorize incertezas que possam invalidar a hipótese central de valor.\n"
            "3. Não permita que requisitos de infraestrutura técnica ou segurança redefinam ou mutem a hipótese de produto.\n"
            "4. Nunca introduza alegações numéricas precisas (tempo, latência, porcentagem, moeda ou multiplicadores) sem base de evidência declarada.\n"
            "5. Identifique alternativas concorrentes e a linha de base de status quo gratuito (processos manuais, planilhas, ferramentas existentes, fazer nada), quando pertinente.\n"
            "6. Forneça critérios de falseamento estruturados: hipótese, observação destrutiva e teste discriminativo de menor custo.\n"
            "7. Para CADA vulnerabilidade declare authority={basis,support_ref,derivation}. USER_EXPLICIT exige texto expresso; VALID_USER_DERIVATION exige trecho rastreável e derivação necessária; caso contrário use MODEL_HYPOTHESIS, que não autoriza severidade efetiva ou gate.\n"
            "8. Para escolha normativa declare normative_authority={basis,support_ref,derivation}. Não marque requires_human_normative_choice apenas porque uma decisão humana existirá futuramente.\n"
            "9. Para proposed_next_action declare action_authority={basis,support_ref,derivation}; em DISCOVERY/VALIDATION, prefira reduzir incerteza decision-relevant antes de implementar.\n"
            "10. Para remaining_uncertainties declare uncertainty_authority={basis,support_ref,derivation}. MODEL_HYPOTHESIS pode orientar exploração, mas não aciona escalação sozinha.\n"
        )
        return first_pass_prompt_template.replace("{idea}", idea)

    def run(self, original_idea: str, run_id: Optional[str] = None, human_intervention_flag: bool = False) -> LeanRunResult:
        tracer = RunTracer(run_id=run_id, runs_dir=self.runs_dir)
        tracer.record_input(original_idea, metadata={"topology": "LEAN_IEE_L1", "max_allowed_calls": LEAN_L1_MAX_MODEL_CALLS})

        # 1. Ancoragem primária da fonte humana
        source_anchor = SourceAnchor.create_human_input_anchor(original_idea)
        calls_used = 0

        # 2. Passo 1: Lean First Pass (Chamada 1)
        user_prompt_1 = self._build_first_pass_prompt(original_idea)

        calls_used += 1
        res_1: ModelResponse = self.runner.generate(
            prompt_text=user_prompt_1,
            output_schema=LeanFirstPassOutput,
            stage_name="LEAN_FIRST_PASS",
            model_name=self.model_name,
        )

        first_pass_output: Optional[LeanFirstPassOutput] = res_1.parsed  # type: ignore
        first_pass_error = res_1.error
        if first_pass_output is not None:
            try:
                first_pass_output.validate_strong_maturation(original_idea)
            except (AttributeError, ValueError) as exc:
                first_pass_error = f"Validação M2 do first pass: {exc}"
                first_pass_output = None

        # Prevenção de falha por first_pass nulo (fail-closed sem dereferência indevida)
        if first_pass_output is None:
            failed_md = f"# Pacote Lean de Maturação — Run {tracer.run_id}\n\n**Status:** `FIRST_PASS_FAILED` | **Chamadas de Modelo Utilizadas:** {calls_used} (Max: {LEAN_L1_MAX_MODEL_CALLS})\n\n---\n\n### Falha na Execução\nNão foi possível gerar a análise inicial da ideia: {first_pass_error or 'Erro de validação ou geração estruturada.'}"
            final_data = {
                "run_id": tracer.run_id,
                "topology": "LEAN_IEE_L1",
                "original_idea": original_idea,
                "total_model_calls": calls_used,
                "gate_outcome": "UNKNOWN",
                "escalation_reason": "UNKNOWN",
                "authority_spoofing_detected": False,
                "unsupported_candidate_count": 0,
                "terminal_status": "FIRST_PASS_FAILED",
                "decision_progress_detected": False,
                "error": first_pass_error,
            }
            (tracer.run_dir / "final.json").write_text(json.dumps(final_data, indent=2, ensure_ascii=False), encoding="utf-8")
            (tracer.run_dir / "final.md").write_text(failed_md, encoding="utf-8")
            return LeanRunResult(
                run_id=tracer.run_id,
                source_anchor=source_anchor,
                first_pass=None,
                gate_result=None,
                escalation_result=None,
                decision_delta=None,
                epistemic_rent=None,
                total_model_calls=calls_used,
                terminal_status="FIRST_PASS_FAILED",
                human_decision_requested=False,
                decision_progress_detected=False,
                final_markdown=failed_md,
            )

        # Qualify unsupported quantitative claims before any downstream gate,
        # arbitration, persistence, or human-readable rendering can reuse them.
        self._qualify_quantitative_decision_texts(first_pass_output, original_idea)

        # Sanitização de precisão numérica não ancorada na saída inicial
        sanitized_mech, _ = FalsePrecisionGuard.sanitize_unsupported_precision(
            first_pass_output.primary_mechanism.mechanism, source_text=original_idea
        )
        first_pass_output.primary_mechanism.mechanism = sanitized_mech

        # 3. Avaliação determinística do Early Epistemic Gate (Custo = 0 chamadas)
        gate_result = EarlyEpistemicGate.evaluate(
            source_anchor=source_anchor,
            first_pass=first_pass_output,
            negative_knowledge_pool=self.negative_knowledge_pool,
            human_intervention_flag=human_intervention_flag,
        )

        escalation_output: Optional[FocusedEscalationOutput] = None
        decision_progress = True
        terminal_status = "COMPLETED"
        human_decision_req = (gate_result.outcome == GateOutcome.REQUEST_HUMAN_DECISION)

        # 4. Decisão pós-gate
        if gate_result.outcome == GateOutcome.RETURN_NOW:
            terminal_status = "COMPLETED_DIRECT_ONE_PASS"

        elif gate_result.outcome == GateOutcome.REQUEST_HUMAN_DECISION:
            terminal_status = "HUMAN_DECISION_REQUIRED"

        elif gate_result.outcome == GateOutcome.STOP_NO_USEFUL_WORK:
            terminal_status = "STOP_NO_USEFUL_WORK"

        elif gate_result.outcome == GateOutcome.ESCALATE_FOCUSED:
            # Invariante: Só executa se calls_used < LEAN_L1_MAX_MODEL_CALLS (calls_used = 1 -> 2)
            if calls_used < LEAN_L1_MAX_MODEL_CALLS:
                calls_used += 1
                escalation_prompt = (
                    "Você é o especialista de escalação focada do Lean IEE.\n"
                    f"Razão de Escalação: {gate_result.escalation_reason.value}\n"
                    f"Explicação da Incerteza: {gate_result.explanation}\n"
                    f"Mecanismo Alvo: {first_pass_output.primary_mechanism.mechanism}\n\n"
                    "DIRETRIZES E LIMITES DE ESCOPO:\n"
                    "1. Resolva estritamente a incerteza especificada sem reescrever dimensões não relacionadas.\n"
                    "2. O alvo da escalação NÃO se torna automaticamente a prioridade global do projeto.\n"
                    "3. Não converta mitigação, arquitetura técnica (ex: Kubernetes, Kafka, Rust) ou requisito não-funcional em refinamento da proposta de produto sem justificativa.\n"
                    "4. Não invente métricas de desempenho ou custo sem medição.\n"
                    "5. Retorne candidato a próximo passo (candidate_updated_next_action), não ação final autoritativa.\n"
                    "6. Declare action_authority={basis,support_ref,derivation} para updated_next_action; "
                    "na ausência de âncora use MODEL_HYPOTHESIS e formule a ação como EVIDENCE_NEEDED, não implementação autoritativa.\n"
                )

                res_2: ModelResponse = self.runner.generate(
                    prompt_text=escalation_prompt,
                    output_schema=FocusedEscalationOutput,
                    stage_name="FOCUSED_ESCALATION",
                    model_name=self.model_name,
                )
                escalation_output = res_2.parsed  # type: ignore

                # Sanitização de precisão na resposta de escalação
                if escalation_output:
                    self._qualify_quantitative_decision_texts(escalation_output, original_idea)
                    if escalation_output.mutated_hypothesis_description:
                        sanitized_mut, _ = FalsePrecisionGuard.sanitize_unsupported_precision(
                            escalation_output.mutated_hypothesis_description, source_text=original_idea
                        )
                        escalation_output.mutated_hypothesis_description = sanitized_mut
                    if escalation_output.focused_critique_or_analysis:
                        sanitized_crit, _ = FalsePrecisionGuard.sanitize_unsupported_precision(
                            escalation_output.focused_critique_or_analysis, source_text=original_idea
                        )
                        escalation_output.focused_critique_or_analysis = sanitized_crit

                    if escalation_output.updated_next_action:
                        escalation_action_audit = AuthorityProofValidator.audit_gate_claim(
                            original_idea=original_idea,
                            human_intent=first_pass_output.human_intent,
                            proposition=escalation_output.updated_next_action,
                            claimed_basis=escalation_output.action_authority.basis,
                            derivation_proof=escalation_output.action_authority.derivation,
                            authority_proof_ref=escalation_output.action_authority.support_ref,
                            human_intervention_flag=human_intervention_flag,
                        )
                        escalation_output.next_action_gate_eligible = escalation_action_audit.is_valid
                        gate_result.grounding_records.append(escalation_action_audit)
                        if not escalation_action_audit.is_valid:
                            gate_result.ineligible_gate_claims.append(
                                f"ESCALATION_NEXT_ACTION: {escalation_action_audit.failure_reason}"
                            )
                            if escalation_output.action_authority.basis in (
                                PromotionAuthorityBasis.USER_EXPLICIT,
                                PromotionAuthorityBasis.VALID_USER_DERIVATION,
                            ):
                                gate_result.authority_spoofing_detected = True
                                gate_result.unsupported_candidate_count += 1
                            escalation_output.action_authority.basis = PromotionAuthorityBasis.MODEL_HYPOTHESIS

                # Harvest Magentic-One: Stall / Progress Detection
                if escalation_output and not escalation_output.decision_progress_made:
                    decision_progress = False
                    terminal_status = "NO_DECISION_PROGRESS"
                else:
                    terminal_status = "COMPLETED_WITH_FOCUSED_ESCALATION"

        # 5. Arbitragem determinística do Próximo Passo (Severity != Priority & Next Action Policy)
        stage = getattr(first_pass_output, "idea_stage", IdeaStage.UNKNOWN)
        cand_action = escalation_output.updated_next_action if escalation_output else None
        cand_cat = getattr(gate_result, "escalation_risk_category", RiskCategory.UNKNOWN)
        cand_req_type = DecisionRelevancePolicy.infer_requirement_type(cand_action, cand_cat) if cand_action else None
        final_next_action, next_action_chg = NextActionArbitrationPolicy.arbitrate(
            first_pass_next_action=first_pass_output.proposed_next_action,
            escalation_candidate_next_action=cand_action,
            stage=stage,
            original_idea=original_idea,
            requires_human_decision=human_decision_req,
            human_decision_description=first_pass_output.human_choice_description if first_pass_output else None,
            candidate_risk_category=cand_cat,
            candidate_requirement_type=cand_req_type,
            first_pass_action_basis=first_pass_output.action_authority.basis,
            first_pass_action_gate_eligible=first_pass_output.next_action_gate_eligible,
            escalation_action_basis=(
                escalation_output.action_authority.basis
                if escalation_output else PromotionAuthorityBasis.MODEL_HYPOTHESIS
            ),
            escalation_action_gate_eligible=(
                escalation_output.next_action_gate_eligible if escalation_output else False
            ),
            remaining_uncertainties=(
                list(first_pass_output.remaining_uncertainties)
                + list(first_pass_output.material_ambiguities)
            ),
            falsification_criteria=list(first_pass_output.falsification_criteria),
        )

        # Atualiza a ação no escalation_output se foi arbitrada
        if escalation_output:
            escalation_output.updated_next_action = final_next_action

        # Construir DecisionDeltaRecord
        delta_id = f"DELTA-{tracer.run_id[:8]}"
        before_unc = first_pass_output.remaining_uncertainties.copy()
        after_unc = before_unc.copy()
        resolved = []

        if escalation_output:
            if escalation_output.focused_critique_or_analysis:
                resolved.append(f"Crítica focada em {gate_result.escalation_reason.value}")
            if escalation_output.resolved_tradeoffs:
                resolved.extend(escalation_output.resolved_tradeoffs)

        delta_record = DecisionDeltaRecord(
            delta_id=delta_id,
            before_uncertainties=before_unc,
            after_uncertainties=after_unc,
            resolved_items=resolved,
            new_material_options=[a.mechanism for a in first_pass_output.competing_alternatives],
            rejected_options=[],
            human_decision_required=human_decision_req,
            next_action_changed=next_action_chg,
            created_by_stage="FOCUSED_ESCALATION" if escalation_output else "LEAN_FIRST_PASS",
        )

        # 6. Gerar Markdown Humano do Lean Package
        md = self._render_markdown(
            run_id=tracer.run_id,
            original_idea=original_idea,
            first_pass=first_pass_output,
            gate_result=gate_result,
            escalation_output=escalation_output,
            calls_used=calls_used,
            terminal_status=terminal_status,
            final_next_action=final_next_action,
        )

        # 7. Persistir final.json e final.md via tracer
        final_data = {
            "run_id": tracer.run_id,
            "topology": "LEAN_IEE_L1",
            "original_idea": original_idea,
            "total_model_calls": calls_used,
            "gate_outcome": gate_result.outcome.value,
            "escalation_reason": gate_result.escalation_reason.value,
            "authority_spoofing_detected": gate_result.authority_spoofing_detected,
            "unsupported_candidate_count": gate_result.unsupported_candidate_count,
            "terminal_status": terminal_status,
            "decision_progress_detected": decision_progress,
        }
        (tracer.run_dir / "final.json").write_text(json.dumps(final_data, indent=2, ensure_ascii=False), encoding="utf-8")
        (tracer.run_dir / "final.md").write_text(md, encoding="utf-8")

        return LeanRunResult(
            run_id=tracer.run_id,
            source_anchor=source_anchor,
            first_pass=first_pass_output,
            gate_result=gate_result,
            escalation_result=escalation_output,
            decision_delta=delta_record,
            epistemic_rent=gate_result.rent_record,
            total_model_calls=calls_used,
            terminal_status=terminal_status,
            reconstruction_attempts=0,
            human_decision_requested=human_decision_req,
            decision_progress_detected=decision_progress,
            final_markdown=md,
        )

    def _render_markdown(
        self,
        run_id: str,
        original_idea: str,
        first_pass: LeanFirstPassOutput,
        gate_result: GateEvaluationResult,
        escalation_output: Optional[FocusedEscalationOutput],
        calls_used: int,
        terminal_status: str,
        final_next_action: str = "",
    ) -> str:
        lines = []
        lines.append(f"# Pacote Lean de Maturação — Run {run_id}\n")
        lines.append(f"**Status:** `{terminal_status}` | **Chamadas de Modelo Utilizadas:** {calls_used} (Max: {LEAN_L1_MAX_MODEL_CALLS})\n")
        lines.append("---\n")
        lines.append("## 1. Fonte Humana Imutável (SourceAnchor)\n")
        lines.append(f"> {original_idea.strip()}\n\n")

        lines.append("## 2. Intenção & Problema Estruturado (Lean First Pass)\n")
        lines.append(f"- **Intenção do Usuário:** {first_pass.human_intent}")
        lines.append(f"- **Problema Interpretado:** {first_pass.interpreted_problem}")
        if getattr(first_pass, "idea_stage", None):
            lines.append(f"- **Estágio Interpretado da Ideia:** `{first_pass.idea_stage.value}`")
        lines.append("\n")

        lines.append("## 3. Mecanismo Primário Proposto\n")
        prim = first_pass.primary_mechanism
        lines.append(f"**Mecanismo:** {prim.mechanism}")
        lines.append(f"- **Base de Autoridade Auditada:** `{prim.claimed_basis.value}`")
        if prim.justification:
            lines.append(f"- **Justificativa:** {prim.justification}")
        lines.append("\n")

        if first_pass.competing_alternatives:
            lines.append("## 4. Alternativas Concorrentes Identificadas\n")
            for idx, alt in enumerate(first_pass.competing_alternatives, 1):
                cat_label = f" [{alt.alternative_category.value}]" if getattr(alt, "alternative_category", None) else ""
                lines.append(f"{idx}. **{alt.mechanism}**{cat_label} (Base: `{alt.claimed_basis.value}`)")
                if alt.tradeoffs:
                    lines.append(f"   - *Tradeoffs:* {', '.join(alt.tradeoffs)}")
            lines.append("\n")

        if getattr(first_pass, "falsification_criteria", None):
            lines.append("## 4.1. Critérios de Falseamento Empírico\n")
            for fc in first_pass.falsification_criteria:
                lines.append(f"- **Hipótese:** {fc.hypothesis}")
                lines.append(f"  - *O que a derrubaria:* {fc.what_would_kill_it}")
                lines.append(f"  - *Teste mais barato:* {fc.lowest_cost_discriminating_test}")
            lines.append("\n")

        lines.append("## 5. Avaliação do Early Epistemic Gate (Custo = 0 chamadas)\n")
        lines.append(f"- **Veredito do Gate:** `{gate_result.outcome.value}`")
        lines.append(f"- **Motivo de Escalação:** `{gate_result.escalation_reason.value}`")
        lines.append(f"- **Explicação:** {gate_result.explanation}")
        lines.append(f"- **Autoridade Usurpada Detectada:** `{gate_result.authority_spoofing_detected}`")
        lines.append(f"- **Candidatos Não Ancorados:** {gate_result.unsupported_candidate_count}\n")
        if gate_result.ineligible_gate_claims:
            lines.append("- **Hipóteses sem autoridade de gate (EVIDENCE_NEEDED):**")
            for claim in gate_result.ineligible_gate_claims:
                lines.append(f"  - {claim}")
            lines.append("")

        if escalation_output:
            lines.append("## 6. Resultado da Escalação Focada (Chamada 2)\n")
            lines.append(f"**Incerteza Alvo:** {escalation_output.target_hypothesis}")
            if escalation_output.focused_critique_or_analysis:
                lines.append(f"- **Análise / Crítica:** {escalation_output.focused_critique_or_analysis}")
            if escalation_output.resolved_tradeoffs:
                lines.append(f"- **Trade-offs Resolvidos:** {', '.join(escalation_output.resolved_tradeoffs)}")
            if escalation_output.discriminating_tests:
                lines.append("- **Testes Discriminativos Sugeridos:**")
                for t in escalation_output.discriminating_tests:
                    lines.append(f"  - [ ] {t}")
            lines.append(f"- **Progresso Decisório:** `{escalation_output.decision_progress_made}`\n")

        lines.append("## 7. Próximo Passo Recomendado\n")
        chosen_action = final_next_action or (escalation_output.updated_next_action if (escalation_output and escalation_output.updated_next_action) else first_pass.proposed_next_action)
        chosen_action_eligible = (
            first_pass.next_action_gate_eligible
            and chosen_action == first_pass.proposed_next_action
        ) or (
            escalation_output is not None
            and escalation_output.next_action_gate_eligible
            and chosen_action == escalation_output.updated_next_action
        )
        if not chosen_action_eligible and not gate_result.outcome == GateOutcome.REQUEST_HUMAN_DECISION:
            lines.append("**Status epistêmico:** `EVIDENCE_NEEDED` (`MODEL_HYPOTHESIS`)\n")
        lines.append(f"{chosen_action or 'Validar protótipo diretamente com o usuário.'}\n")

        return "\n".join(lines)
