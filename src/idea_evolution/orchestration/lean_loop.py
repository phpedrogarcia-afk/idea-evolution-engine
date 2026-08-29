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

    def run(self, original_idea: str, run_id: Optional[str] = None, human_intervention_flag: bool = False) -> LeanRunResult:
        tracer = RunTracer(run_id=run_id, runs_dir=self.runs_dir)
        tracer.record_input(original_idea, metadata={"topology": "LEAN_IEE_L1", "max_allowed_calls": LEAN_L1_MAX_MODEL_CALLS})

        # 1. Ancoragem primária da fonte humana
        source_anchor = SourceAnchor.create_human_input_anchor(original_idea)
        calls_used = 0

        # 2. Passo 1: Lean First Pass (Chamada 1)
        first_pass_prompt_template = (
            "Você é o analista do Lean Idea Evolution Engine.\n"
            "Analise a ideia original abaixo e produza uma estruturação mínima focada em intenção, mecanismo e riscos:\n"
            "IDEIA HUMANA:\n{idea}\n"
        )
        user_prompt_1 = first_pass_prompt_template.replace("{idea}", original_idea)

        calls_used += 1
        res_1: ModelResponse = self.runner.generate(
            prompt_text=user_prompt_1,
            output_schema=LeanFirstPassOutput,
            stage_name="LEAN_FIRST_PASS",
            model_name=self.model_name,
        )

        first_pass_output: Optional[LeanFirstPassOutput] = res_1.parsed  # type: ignore

        # Prevenção de falha por first_pass nulo (fail-closed sem dereferência indevida)
        if first_pass_output is None:
            failed_md = f"# Pacote Lean de Maturação — Run {tracer.run_id}\n\n**Status:** `FIRST_PASS_FAILED` | **Chamadas de Modelo Utilizadas:** {calls_used} (Max: {LEAN_L1_MAX_MODEL_CALLS})\n\n---\n\n### Falha na Execução\nNão foi possível gerar a análise inicial da ideia: {res_1.error or 'Erro de validação ou geração estruturada.'}"
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
                "error": res_1.error,
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
                    f"Mecanismo Alvo: {first_pass_output.primary_mechanism.mechanism}\n"
                    "Resolva estritamente a incerteza especificada sem reescrever dimensões não relacionadas.\n"
                )

                res_2: ModelResponse = self.runner.generate(
                    prompt_text=escalation_prompt,
                    output_schema=FocusedEscalationOutput,
                    stage_name="FOCUSED_ESCALATION",
                    model_name=self.model_name,
                )
                escalation_output = res_2.parsed  # type: ignore

                # Harvest Magentic-One: Stall / Progress Detection
                if escalation_output and not escalation_output.decision_progress_made:
                    decision_progress = False
                    terminal_status = "NO_DECISION_PROGRESS"
                else:
                    terminal_status = "COMPLETED_WITH_FOCUSED_ESCALATION"

        # 5. Construir DecisionDeltaRecord
        delta_id = f"DELTA-{tracer.run_id[:8]}"
        before_unc = first_pass_output.remaining_uncertainties.copy()
        after_unc = before_unc.copy()
        resolved = []
        next_action_chg = False

        if escalation_output:
            if escalation_output.focused_critique_or_analysis:
                resolved.append(f"Crítica focada em {gate_result.escalation_reason.value}")
            if escalation_output.resolved_tradeoffs:
                resolved.extend(escalation_output.resolved_tradeoffs)
            if escalation_output.updated_next_action and escalation_output.updated_next_action != first_pass_output.proposed_next_action:
                next_action_chg = True

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
    ) -> str:
        lines = []
        lines.append(f"# Pacote Lean de Maturação — Run {run_id}\n")
        lines.append(f"**Status:** `{terminal_status}` | **Chamadas de Modelo Utilizadas:** {calls_used} (Max: {LEAN_L1_MAX_MODEL_CALLS})\n")
        lines.append("---\n")
        lines.append("## 1. Fonte Humana Imutável (SourceAnchor)\n")
        lines.append(f"> {original_idea.strip()}\n\n")

        lines.append("## 2. Intenção & Problema Estruturado (Lean First Pass)\n")
        lines.append(f"- **Intenção do Usuário:** {first_pass.human_intent}")
        lines.append(f"- **Problema Interpretado:** {first_pass.interpreted_problem}\n")

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
                lines.append(f"{idx}. **{alt.mechanism}** (Base: `{alt.claimed_basis.value}`)")
                if alt.tradeoffs:
                    lines.append(f"   - *Tradeoffs:* {', '.join(alt.tradeoffs)}")
            lines.append("\n")

        lines.append("## 5. Avaliação do Early Epistemic Gate (Custo = 0 chamadas)\n")
        lines.append(f"- **Veredito do Gate:** `{gate_result.outcome.value}`")
        lines.append(f"- **Motivo de Escalação:** `{gate_result.escalation_reason.value}`")
        lines.append(f"- **Explicação:** {gate_result.explanation}")
        lines.append(f"- **Autoridade Usurpada Detectada:** `{gate_result.authority_spoofing_detected}`")
        lines.append(f"- **Candidatos Não Ancorados:** {gate_result.unsupported_candidate_count}\n")

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
        next_act = escalation_output.updated_next_action if (escalation_output and escalation_output.updated_next_action) else first_pass.proposed_next_action
        lines.append(f"{next_act or 'Validar protótipo diretamente com o usuário.'}\n")

        return "\n".join(lines)
