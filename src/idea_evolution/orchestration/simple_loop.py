"""
src/idea_evolution/orchestration/simple_loop.py
Orquestrador central do Simple Idea Evolution Loop (Condições B e C) com controle determinístico de estado.
"""

from typing import Optional, Dict, Any, List
from pathlib import Path
from src.idea_evolution.domain.state import SimpleIdeaState, RunStatus
from src.idea_evolution.providers.base import ModelRunner
from src.idea_evolution.tracing.tracer import RunTracer
from src.idea_evolution.stages.understand import UnderstandStage
from src.idea_evolution.stages.attack import AttackStage
from src.idea_evolution.stages.critique import LogicalCritiqueStage, FeasibilityCritiqueStage
from src.idea_evolution.stages.revision import RevisionStage
from src.idea_evolution.stages.alternatives import AlternativesStage
from src.idea_evolution.stages.reality_check import RealityCheckStage
from src.idea_evolution.stages.synthesize import SynthesizeStage
from src.idea_evolution.stages.final_review import FinalReviewStage
from src.idea_evolution.stages.contracts import FinalReviewOutput


class SimpleLoopRunner:
    """
    Controlador do Simple Idea Evolution Loop.
    Garante execução sequencial dos estágios, validação de schemas, persistência e limite de reconstrução.
    """

    def __init__(
        self,
        runner: ModelRunner,
        topology: str = "STANDARD_6_STAGE",  # STANDARD_6_STAGE (Cond B) | ITERATIVE_CRITIQUE_REVISION (Cond C)
        stage_models: Optional[Dict[str, str]] = None,
        runs_dir: Optional[Path] = None,
    ):
        self.runner = runner
        self.topology = topology.upper()
        self.stage_models = stage_models or {}
        self.runs_dir = runs_dir

    def run(self, original_idea: str, run_id: Optional[str] = None) -> SimpleIdeaState:
        tracer = RunTracer(run_id=run_id, runs_dir=self.runs_dir)
        tracer.record_input(original_idea, metadata={"topology": self.topology})

        state = SimpleIdeaState(
            run_id=tracer.run_id,
            original_idea=original_idea,
            status=RunStatus.RUNNING,
        )

        step_counter = 1

        try:
            # 1. UNDERSTAND
            understand_stage = UnderstandStage()
            model = self.stage_models.get(understand_stage.stage_id)
            res = understand_stage.execute(state, self.runner, model_name=model)
            tracer.record_stage_result(step_counter, res)
            step_counter += 1
            if not res.success:
                state.status = RunStatus.FAILED
                tracer.persist_final_state(state)
                return state

            # 2. CRITIQUE / ATTACK PIPELINE
            if self.topology == "ITERATIVE_CRITIQUE_REVISION":
                # Condição C: Crítica 1 -> Revisão 1 -> Crítica 2 -> Revisão 2
                critique1 = LogicalCritiqueStage()
                res = critique1.execute(state, self.runner, model_name=self.stage_models.get(critique1.stage_id))
                tracer.record_stage_result(step_counter, res)
                step_counter += 1
                if not res.success:
                    state.status = RunStatus.FAILED
                    tracer.persist_final_state(state)
                    return state

                rev1 = RevisionStage(revision_index=1)
                res = rev1.execute(state, self.runner, model_name=self.stage_models.get(rev1.stage_id))
                tracer.record_stage_result(step_counter, res)
                step_counter += 1
                if not res.success:
                    state.status = RunStatus.FAILED
                    tracer.persist_final_state(state)
                    return state

                critique2 = FeasibilityCritiqueStage()
                res = critique2.execute(state, self.runner, model_name=self.stage_models.get(critique2.stage_id))
                tracer.record_stage_result(step_counter, res)
                step_counter += 1
                if not res.success:
                    state.status = RunStatus.FAILED
                    tracer.persist_final_state(state)
                    return state

                rev2 = RevisionStage(revision_index=2)
                res = rev2.execute(state, self.runner, model_name=self.stage_models.get(rev2.stage_id))
                tracer.record_stage_result(step_counter, res)
                step_counter += 1
                if not res.success:
                    state.status = RunStatus.FAILED
                    tracer.persist_final_state(state)
                    return state

            else:
                # Condição B: ATTACK Padrão
                attack_stage = AttackStage()
                model = self.stage_models.get(attack_stage.stage_id)
                res = attack_stage.execute(state, self.runner, model_name=model)
                tracer.record_stage_result(step_counter, res)
                step_counter += 1
                if not res.success:
                    state.status = RunStatus.FAILED
                    tracer.persist_final_state(state)
                    return state

            # 3. ALTERNATIVES
            alt_stage = AlternativesStage()
            res = alt_stage.execute(state, self.runner, model_name=self.stage_models.get(alt_stage.stage_id))
            tracer.record_stage_result(step_counter, res)
            step_counter += 1
            if not res.success:
                state.status = RunStatus.FAILED
                tracer.persist_final_state(state)
                return state

            # 4. REALITY_CHECK
            reality_stage = RealityCheckStage()
            res = reality_stage.execute(state, self.runner, model_name=self.stage_models.get(reality_stage.stage_id))
            tracer.record_stage_result(step_counter, res)
            step_counter += 1
            if not res.success:
                state.status = RunStatus.FAILED
                tracer.persist_final_state(state)
                return state

            # 5. SYNTHESIZE
            synth_stage = SynthesizeStage()
            res = synth_stage.execute(state, self.runner, model_name=self.stage_models.get(synth_stage.stage_id))
            tracer.record_stage_result(step_counter, res)
            step_counter += 1
            if not res.success:
                state.status = RunStatus.FAILED
                tracer.persist_final_state(state)
                return state

            # 6. FINAL_REVIEW
            review_stage = FinalReviewStage()
            res = review_stage.execute(state, self.runner, model_name=self.stage_models.get(review_stage.stage_id))
            tracer.record_stage_result(step_counter, res)
            step_counter += 1
            if not res.success:
                state.status = RunStatus.FAILED
                tracer.persist_final_state(state)
                return state

            review_output: FinalReviewOutput = res.output

            # VERIFICAÇÃO DE RECONSTRUÇÃO (No máximo 1 ciclo permitido)
            if (
                review_output.recommendation == "RECONSTRUCT"
                or review_output.unresolved_critical_issue
                or review_output.essence_drift_detected
            ) and state.reconstruction_count < state.max_reconstructions:
                state.reconstruction_count += 1
                state.status = RunStatus.RECONSTRUCTING

                # Reexecutar alternativas -> reality_check -> synthesize -> final_review
                res_alt = alt_stage.execute(state, self.runner, model_name=self.stage_models.get(alt_stage.stage_id))
                tracer.record_stage_result(step_counter, res_alt)
                step_counter += 1

                res_real = reality_stage.execute(state, self.runner, model_name=self.stage_models.get(reality_stage.stage_id))
                tracer.record_stage_result(step_counter, res_real)
                step_counter += 1

                res_synth = synth_stage.execute(state, self.runner, model_name=self.stage_models.get(synth_stage.stage_id))
                tracer.record_stage_result(step_counter, res_synth)
                step_counter += 1

                res_review2 = review_stage.execute(state, self.runner, model_name=self.stage_models.get(review_stage.stage_id))
                tracer.record_stage_result(step_counter, res_review2)
                step_counter += 1

                review_output2: FinalReviewOutput = res_review2.output
                if review_output2.recommendation == "REFINED_IDEA_READY" and not review_output2.essence_drift_detected:
                    state.status = RunStatus.REFINED_IDEA_READY
                else:
                    state.status = RunStatus.REFINEMENT_INCOMPLETE
            elif review_output.recommendation == "REFINED_IDEA_READY" and not review_output.essence_drift_detected:
                state.status = RunStatus.REFINED_IDEA_READY
            else:
                state.status = RunStatus.REFINEMENT_INCOMPLETE

        except Exception as exc:
            state.status = RunStatus.FAILED
            state.remaining_uncertainties.append(f"UNHANDLED_EXCEPTION: {str(exc)}")

        tracer.persist_final_state(state)
        return state
