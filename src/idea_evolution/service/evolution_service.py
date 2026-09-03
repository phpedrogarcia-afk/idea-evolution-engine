"""
src/idea_evolution/service/evolution_service.py
Camada de Serviço de Aplicação (Service Boundary) do FioIdeias V1 (P1).

Encapsula o núcleo científico Lean L1 (LeanLoopRunner + EarlyEpistemicGate)
fornecendo uma interface estável de produto para chamadores (CLI, APIs futuras).
"""

from __future__ import annotations
from typing import Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime

from src.idea_evolution.providers.base import ModelRunner
from src.idea_evolution.orchestration.lean_loop import LeanLoopRunner, LeanRunResult
from src.idea_evolution.orchestration.baseline import BaselineRunner
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.domain.epistemic_contracts import NegativeKnowledgeRecord
from src.idea_evolution.service.contracts import (
    EvolutionRequest,
    EvolutionResponse,
    TreatmentMode,
    ServiceFailureType,
)


class IdeaEvolutionService:
    """
    Fachada de Serviço de Aplicação para Maturação de Ideias no FioIdeias V1.
    Garante que o Lean L1 seja a rota padrão e protege contra uso acidental da Condição B.
    """

    def __init__(
        self,
        runner: ModelRunner,
        default_treatment: TreatmentMode = TreatmentMode.LEAN_L1,
        runs_dir: Optional[Path] = None,
        negative_knowledge_pool: Optional[List[NegativeKnowledgeRecord]] = None,
    ):
        self.runner = runner
        self.default_treatment = default_treatment
        self.runs_dir = runs_dir
        self.negative_knowledge_pool = negative_knowledge_pool or []

    def evolve(self, request: EvolutionRequest) -> EvolutionResponse:
        """Executa a evolução de uma ideia conforme o contrato de requisição."""
        run_id_str = request.run_id or f"RUN-{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # 1. Validação mínima de entrada em nível de aplicação
        validation_err = request.validate_input()
        if validation_err:
            return EvolutionResponse(
                success=False,
                run_id=run_id_str,
                treatment_used=request.treatment_mode,
                raw_idea=request.raw_idea or "",
                terminal_status="INVALID_INPUT",
                failure_type=ServiceFailureType.INVALID_INPUT,
                error_message=validation_err,
            )

        treatment = request.treatment_mode or self.default_treatment

        # 2. Rota Padrão de Produto: LEAN_L1 (Condição C)
        if treatment == TreatmentMode.LEAN_L1:
            return self._execute_lean(request, run_id_str)

        # 3. Rota de Contingência / Sanity: FAST_FALLBACK (Condição A)
        elif treatment == TreatmentMode.FAST_FALLBACK:
            return self._execute_fast_fallback(request, run_id_str)

        # 4. Rota Suspensa de Pesquisa: SUSPENDED_DEEP_LOOP (Condição B)
        elif treatment == TreatmentMode.SUSPENDED_DEEP_LOOP:
            return self._execute_suspended_deep_loop(request, run_id_str)

        else:
            return EvolutionResponse(
                success=False,
                run_id=run_id_str,
                treatment_used=treatment,
                raw_idea=request.raw_idea,
                terminal_status="UNKNOWN_TREATMENT",
                failure_type=ServiceFailureType.INVALID_INPUT,
                error_message=f"Modo de tratamento desconhecido: {treatment}",
            )

    def evolve_idea(
        self,
        raw_idea: str,
        treatment_mode: TreatmentMode = TreatmentMode.LEAN_L1,
        run_id: Optional[str] = None,
        model_name: Optional[str] = None,
    ) -> EvolutionResponse:
        """Método de conveniência para invocar o serviço a partir de texto cru."""
        req = EvolutionRequest(
            raw_idea=raw_idea,
            treatment_mode=treatment_mode,
            run_id=run_id,
            model_name=model_name,
        )
        return self.evolve(req)

    # ---------------------------------------------------------------------------
    # Executores Internos
    # ---------------------------------------------------------------------------

    def _execute_lean(self, request: EvolutionRequest, run_id: str) -> EvolutionResponse:
        """Delega a execução ao orquestrador imutável LeanLoopRunner."""
        lean_runner = LeanLoopRunner(
            runner=self.runner,
            model_name=request.model_name,
            negative_knowledge_pool=self.negative_knowledge_pool,
            runs_dir=self.runs_dir,
        )

        try:
            lean_res: LeanRunResult = lean_runner.run(
                original_idea=request.raw_idea,
                run_id=run_id,
            )
        except Exception as e:
            return EvolutionResponse(
                success=False,
                run_id=run_id,
                treatment_used=TreatmentMode.LEAN_L1,
                raw_idea=request.raw_idea,
                terminal_status="INTERNAL_APPLICATION_FAILURE",
                failure_type=ServiceFailureType.INTERNAL_APPLICATION_FAILURE,
                error_message=f"Exceção não tratada na camada de serviço: {str(e)}",
            )

        # Mapeamento do resultado do Lean L1
        status = lean_res.terminal_status

        # Caso de falha na primeira passada (ex: erro de provider ou JSON corrompido)
        if status == "FIRST_PASS_FAILED":
            failure_type = ServiceFailureType.STRUCTURED_OUTPUT_FAILURE
            return EvolutionResponse(
                success=False,
                run_id=lean_res.run_id,
                treatment_used=TreatmentMode.LEAN_L1,
                raw_idea=request.raw_idea,
                terminal_status=status,
                total_model_calls=lean_res.total_model_calls,
                decision_progress_detected=False,
                failure_type=failure_type,
                error_message="Falha na análise inicial da ideia pelo modelo.",
                lean_result=lean_res,
            )

        # Parada deliberada por decisão normativa humana (não é crash!)
        human_req = (status == "HUMAN_DECISION_REQUIRED") or lean_res.human_decision_requested

        # Parada deliberada por ausência de trabalho útil (STOP_NO_USEFUL_WORK)
        fail_type = ServiceFailureType.DOMAIN_DECISION_OR_STOP if status == "STOP_NO_USEFUL_WORK" else None

        return EvolutionResponse(
            success=True,
            run_id=lean_res.run_id,
            treatment_used=TreatmentMode.LEAN_L1,
            raw_idea=request.raw_idea,
            terminal_status=status,
            total_model_calls=lean_res.total_model_calls,
            human_decision_requested=human_req,
            decision_progress_detected=lean_res.decision_progress_detected,
            failure_type=fail_type,
            lean_result=lean_res,
        )

    def _execute_fast_fallback(self, request: EvolutionRequest, run_id: str) -> EvolutionResponse:
        """Executa a Condição A (Baseline) como fallback rápido explícito."""
        baseline_runner = BaselineRunner(
            runner=self.runner,
            model_name=request.model_name,
        )

        try:
            base_res = baseline_runner.run(
                original_idea=request.raw_idea,
                run_id=run_id,
                runs_dir=self.runs_dir,
            )
        except Exception as e:
            return EvolutionResponse(
                success=False,
                run_id=run_id,
                treatment_used=TreatmentMode.FAST_FALLBACK,
                raw_idea=request.raw_idea,
                terminal_status="INTERNAL_APPLICATION_FAILURE",
                failure_type=ServiceFailureType.INTERNAL_APPLICATION_FAILURE,
                error_message=f"Exceção no fallback rápido: {str(e)}",
            )

        success = base_res.get("success", False)
        error_msg = base_res.get("error")

        return EvolutionResponse(
            success=success,
            run_id=run_id,
            treatment_used=TreatmentMode.FAST_FALLBACK,
            raw_idea=request.raw_idea,
            terminal_status="COMPLETED" if success else "BASELINE_FAILED",
            total_model_calls=1,
            failure_type=None if success else ServiceFailureType.PROVIDER_FAILURE,
            error_message=error_msg,
            baseline_result=base_res,
        )

    def _execute_suspended_deep_loop(self, request: EvolutionRequest, run_id: str) -> EvolutionResponse:
        """Execução controlada da Condição B para pesquisa interna/experimental."""
        if not request.allow_experimental_deep_loop:
            return EvolutionResponse(
                success=False,
                run_id=run_id,
                treatment_used=TreatmentMode.SUSPENDED_DEEP_LOOP,
                raw_idea=request.raw_idea,
                terminal_status="SUSPENDED_TREATMENT_BLOCKED",
                failure_type=ServiceFailureType.INVALID_INPUT,
                error_message=(
                    "A Condição B (Simple Loop) está formalmente suspensa do caminho padrão de produto V1. "
                    "Para fins exclusivos de pesquisa interna isolada, passe allow_experimental_deep_loop=True."
                ),
            )

        simple_runner = SimpleLoopRunner(
            runner=self.runner,
            model_name=request.model_name,
            runs_dir=self.runs_dir,
        )

        try:
            state = simple_runner.run(
                original_idea=request.raw_idea,
                run_id=run_id,
            )
        except Exception as e:
            return EvolutionResponse(
                success=False,
                run_id=run_id,
                treatment_used=TreatmentMode.SUSPENDED_DEEP_LOOP,
                raw_idea=request.raw_idea,
                terminal_status="INTERNAL_APPLICATION_FAILURE",
                failure_type=ServiceFailureType.INTERNAL_APPLICATION_FAILURE,
                error_message=f"Exceção no loop profundo suspenso: {str(e)}",
            )

        success = (state.run_status.value == "COMPLETED")
        return EvolutionResponse(
            success=success,
            run_id=run_id,
            treatment_used=TreatmentMode.SUSPENDED_DEEP_LOOP,
            raw_idea=request.raw_idea,
            terminal_status=state.run_status.value,
            total_model_calls=state.reconstruction_attempts + 1,  # Telemetria nominal
            failure_type=None if success else ServiceFailureType.DOMAIN_DECISION_OR_STOP,
        )
