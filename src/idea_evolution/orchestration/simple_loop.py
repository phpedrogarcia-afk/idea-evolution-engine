"""
src/idea_evolution/orchestration/simple_loop.py
Orquestrador do Simple Idea Evolution Loop (v0.1) com topologia corrigida (Synthesize antes de RealityCheck) e rastreabilidade total.
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
import json

from src.idea_evolution.domain.state import SimpleIdeaState, RunStatus
from src.idea_evolution.config.routing import ModelRoutingConfig
from src.idea_evolution.providers.base import ModelRunner
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.providers.router import RunnerRouter
from src.idea_evolution.tracing.tracer import RunTracer

from src.idea_evolution.stages.understand import UnderstandStage
from src.idea_evolution.stages.attack import AttackStage
from src.idea_evolution.stages.alternatives import AlternativesStage
from src.idea_evolution.stages.reality_check import RealityCheckStage
from src.idea_evolution.stages.synthesize import SynthesizeStage
from src.idea_evolution.stages.final_review import FinalReviewStage
from src.idea_evolution.stages.critique import LogicalCritiqueStage, FeasibilityCritiqueStage
from src.idea_evolution.stages.revision import RevisionStage
from src.idea_evolution.stages.contracts import FinalReviewOutput


class SimpleLoopRunner:
    """
    Controlador central de execução do Simple Loop.
    Suporta topologia padrão (6 estágios) e iterativa (9 estágios).
    Garante que o kernel determinístico governe o avanço de estado e controle de reconstrução.
    """

    def __init__(
        self,
        runner: Optional[ModelRunner] = None,
        router: Optional[RunnerRouter] = None,
        config: Optional[ModelRoutingConfig] = None,
        topology: str = "STANDARD_6_STAGE",  # STANDARD_6_STAGE | ITERATIVE_CRITIQUE_REVISION
        stage_models: Optional[Dict[str, str]] = None,
        runs_dir: Optional[Path] = None,
    ):
        self.topology = topology
        self.stage_models = stage_models or {}
        self.runs_dir = runs_dir

        if router is not None:
            self.router = router
        elif config is not None:
            self.router = RunnerRouter(config=config)
        elif runner is not None:
            self.router = RunnerRouter(
                config=ModelRoutingConfig.default_single_model(),
                custom_runners={"default": runner},
            )
        else:
            fake = FakeModelRunner()
            self.router = RunnerRouter(
                config=ModelRoutingConfig.default_single_model(),
                custom_runners={"default": fake},
            )

    def get_required_stages(self) -> List[str]:
        """Retorna os nomes canônicos de estágios exigidos pela topologia ativa (Synthesize -> RealityCheck)."""
        if self.topology == "ITERATIVE_CRITIQUE_REVISION":
            return [
                "UNDERSTAND",
                "CRITIQUE_1",
                "REVISION_1",
                "CRITIQUE_2",
                "REVISION_2",
                "ALTERNATIVES",
                "SYNTHESIZE",
                "REALITY_CHECK",
                "FINAL_REVIEW",
            ]
        return [
            "UNDERSTAND",
            "ATTACK",
            "ALTERNATIVES",
            "SYNTHESIZE",
            "REALITY_CHECK",
            "FINAL_REVIEW",
        ]

    def run(self, original_idea: str, run_id: Optional[str] = None) -> SimpleIdeaState:
        tracer = RunTracer(run_id=run_id, runs_dir=self.runs_dir)
        routing_hash = self.router.config.compute_hash()
        tracer.record_input(
            original_idea,
            metadata={
                "topology": self.topology,
                "routing_config_hash": routing_hash,
                "routing_schema_version": self.router.config.schema_version,
            },
        )

        state = SimpleIdeaState(
            run_id=tracer.run_id,
            original_idea=original_idea,
            status=RunStatus.RUNNING,
        )

        step_counter = 1

        try:
            # 1. UNDERSTAND
            understand_stage = UnderstandStage()
            runner, model_name, alias = self.router.get_runner_for_stage(understand_stage.stage_id)
            model = self.stage_models.get(understand_stage.stage_id) or model_name
            res = understand_stage.execute(state, runner, model_name=model, logical_alias=alias)
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
                r, m, a = self.router.get_runner_for_stage(critique1.stage_id)
                m = self.stage_models.get(critique1.stage_id) or m
                res = critique1.execute(state, r, model_name=m, logical_alias=a)
                tracer.record_stage_result(step_counter, res)
                step_counter += 1
                if not res.success:
                    state.status = RunStatus.FAILED
                    tracer.persist_final_state(state)
                    return state

                rev1 = RevisionStage(revision_index=1)
                r, m, a = self.router.get_runner_for_stage(rev1.stage_id)
                m = self.stage_models.get(rev1.stage_id) or m
                res = rev1.execute(state, r, model_name=m, logical_alias=a)
                tracer.record_stage_result(step_counter, res)
                step_counter += 1
                if not res.success:
                    state.status = RunStatus.FAILED
                    tracer.persist_final_state(state)
                    return state

                critique2 = FeasibilityCritiqueStage()
                r, m, a = self.router.get_runner_for_stage(critique2.stage_id)
                m = self.stage_models.get(critique2.stage_id) or m
                res = critique2.execute(state, r, model_name=m, logical_alias=a)
                tracer.record_stage_result(step_counter, res)
                step_counter += 1
                if not res.success:
                    state.status = RunStatus.FAILED
                    tracer.persist_final_state(state)
                    return state

                rev2 = RevisionStage(revision_index=2)
                r, m, a = self.router.get_runner_for_stage(rev2.stage_id)
                m = self.stage_models.get(rev2.stage_id) or m
                res = rev2.execute(state, r, model_name=m, logical_alias=a)
                tracer.record_stage_result(step_counter, res)
                step_counter += 1
                if not res.success:
                    state.status = RunStatus.FAILED
                    tracer.persist_final_state(state)
                    return state

            else:
                # Condição B: ATTACK Padrão
                attack_stage = AttackStage()
                r, m, a = self.router.get_runner_for_stage(attack_stage.stage_id)
                m = self.stage_models.get(attack_stage.stage_id) or m
                res = attack_stage.execute(state, r, model_name=m, logical_alias=a)
                tracer.record_stage_result(step_counter, res)
                step_counter += 1
                if not res.success:
                    state.status = RunStatus.FAILED
                    tracer.persist_final_state(state)
                    return state

            # 3. ALTERNATIVES
            alt_stage = AlternativesStage()
            r, m, a = self.router.get_runner_for_stage(alt_stage.stage_id)
            m = self.stage_models.get(alt_stage.stage_id) or m
            res = alt_stage.execute(state, r, model_name=m, logical_alias=a)
            tracer.record_stage_result(step_counter, res)
            step_counter += 1
            if not res.success:
                state.status = RunStatus.FAILED
                tracer.persist_final_state(state)
                return state

            # 4. SYNTHESIZE (Seleciona o CORE e define os limites ontológicos)
            synth_stage = SynthesizeStage()
            r, m, a = self.router.get_runner_for_stage(synth_stage.stage_id)
            m = self.stage_models.get(synth_stage.stage_id) or m
            res = synth_stage.execute(state, r, model_name=m, logical_alias=a)
            tracer.record_stage_result(step_counter, res)
            step_counter += 1
            if not res.success:
                state.status = RunStatus.FAILED
                tracer.persist_final_state(state)
                return state

            # 5. REALITY_CHECK (Testa estritamente o CORE aceito na Síntese)
            reality_stage = RealityCheckStage()
            r, m, a = self.router.get_runner_for_stage(reality_stage.stage_id)
            m = self.stage_models.get(reality_stage.stage_id) or m
            res = reality_stage.execute(state, r, model_name=m, logical_alias=a)
            tracer.record_stage_result(step_counter, res)
            step_counter += 1
            if not res.success:
                state.status = RunStatus.FAILED
                tracer.persist_final_state(state)
                return state

            # 6. FINAL_REVIEW
            review_stage = FinalReviewStage()
            r, m, a = self.router.get_runner_for_stage(review_stage.stage_id)
            m = self.stage_models.get(review_stage.stage_id) or m
            res = review_stage.execute(state, r, model_name=m, logical_alias=a)
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

                # Reexecutar alternativas -> synthesize -> reality_check -> final_review (attempt=2)
                r, m, a = self.router.get_runner_for_stage(alt_stage.stage_id)
                m = self.stage_models.get(alt_stage.stage_id) or m
                res_alt = alt_stage.execute(state, r, model_name=m, logical_alias=a, attempt=2)
                tracer.record_stage_result(step_counter, res_alt)
                step_counter += 1

                r, m, a = self.router.get_runner_for_stage(synth_stage.stage_id)
                m = self.stage_models.get(synth_stage.stage_id) or m
                res_synth = synth_stage.execute(state, r, model_name=m, logical_alias=a, attempt=2)
                tracer.record_stage_result(step_counter, res_synth)
                step_counter += 1

                r, m, a = self.router.get_runner_for_stage(reality_stage.stage_id)
                m = self.stage_models.get(reality_stage.stage_id) or m
                res_real = reality_stage.execute(state, r, model_name=m, logical_alias=a, attempt=2)
                tracer.record_stage_result(step_counter, res_real)
                step_counter += 1

                r, m, a = self.router.get_runner_for_stage(review_stage.stage_id)
                m = self.stage_models.get(review_stage.stage_id) or m
                res_review2 = review_stage.execute(state, r, model_name=m, logical_alias=a, attempt=2)
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
