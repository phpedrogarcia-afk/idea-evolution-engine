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
from src.idea_evolution.artifacts.mapper import EvolutionArtifactMapper
from src.idea_evolution.config.catalog import ModelCatalog
from src.idea_evolution.config.cost_policy import (
    ProviderConfig,
    CostEligibility,
    ZeroCostGuard,
    sanitize_secret_text,
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
        provider_config: Optional[ProviderConfig] = None,
        catalog: Optional[ModelCatalog] = None,
    ):
        self.runner = runner
        self.default_treatment = default_treatment
        self.runs_dir = runs_dir
        self.negative_knowledge_pool = negative_knowledge_pool or []
        self.provider_config = provider_config
        self.catalog = catalog or ModelCatalog()

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

        # 2. Resolução e validação da fronteira de provedor e guarda de custo zero (P4)
        effective_provider_config = request.provider_config or self.provider_config
        if effective_provider_config is None:
            effective_provider_config = ProviderConfig.infer_from_runner(
                self.runner, model_name=request.model_name, catalog=self.catalog
            )

        is_valid, block_reason = ZeroCostGuard.validate_provider_config(
            effective_provider_config, catalog=self.catalog
        )
        if not is_valid:
            fail_type = (
                ServiceFailureType.STRUCTURED_OUTPUT_FAILURE
                if "STRUCTURED_OUTPUT" in (block_reason or "")
                else ServiceFailureType.COST_POLICY_BLOCKED
            )
            return EvolutionResponse(
                success=False,
                run_id=run_id_str,
                treatment_used=treatment,
                raw_idea=request.raw_idea or "",
                terminal_status="COST_POLICY_BLOCKED" if fail_type == ServiceFailureType.COST_POLICY_BLOCKED else "STRUCTURED_OUTPUT_FAILURE",
                failure_type=fail_type,
                error_message=sanitize_secret_text(block_reason or "Bloqueado pela governança de custo zero."),
                provider_config=effective_provider_config,
            )

        # 3. Rota Padrão de Produto: LEAN_L1 (Condição C)
        if treatment == TreatmentMode.LEAN_L1:
            return self._execute_lean(request, run_id_str, provider_config=effective_provider_config)

        # 4. Rota de Contingência / Sanity: FAST_FALLBACK (Condição A)
        elif treatment == TreatmentMode.FAST_FALLBACK:
            return self._execute_fast_fallback(request, run_id_str, provider_config=effective_provider_config)

        # 5. Rota Suspensa de Pesquisa: SUSPENDED_DEEP_LOOP (Condição B)
        elif treatment == TreatmentMode.SUSPENDED_DEEP_LOOP:
            return self._execute_suspended_deep_loop(request, run_id_str, provider_config=effective_provider_config)

        else:
            return EvolutionResponse(
                success=False,
                run_id=run_id_str,
                treatment_used=treatment,
                raw_idea=request.raw_idea,
                terminal_status="UNKNOWN_TREATMENT",
                failure_type=ServiceFailureType.INVALID_INPUT,
                error_message=f"Modo de tratamento desconhecido: {treatment}",
                provider_config=effective_provider_config,
            )

    def evolve_idea(
        self,
        raw_idea: str,
        treatment_mode: TreatmentMode = TreatmentMode.LEAN_L1,
        run_id: Optional[str] = None,
        model_name: Optional[str] = None,
        provider_config: Optional[ProviderConfig] = None,
    ) -> EvolutionResponse:
        """Método de conveniência para invocar o serviço a partir de texto cru."""
        req = EvolutionRequest(
            raw_idea=raw_idea,
            treatment_mode=treatment_mode,
            run_id=run_id,
            model_name=model_name,
            provider_config=provider_config,
        )
        return self.evolve(req)

    # ---------------------------------------------------------------------------
    # Executores Internos
    # ---------------------------------------------------------------------------

    def _execute_lean(
        self,
        request: EvolutionRequest,
        run_id: str,
        provider_config: Optional[ProviderConfig] = None,
    ) -> EvolutionResponse:
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
            err_sanitized = sanitize_secret_text(str(e))
            fail_type = self._classify_error(err_sanitized, default=ServiceFailureType.INTERNAL_APPLICATION_FAILURE)
            return EvolutionResponse(
                success=False,
                run_id=run_id,
                treatment_used=TreatmentMode.LEAN_L1,
                raw_idea=request.raw_idea,
                terminal_status="INTERNAL_APPLICATION_FAILURE" if fail_type == ServiceFailureType.INTERNAL_APPLICATION_FAILURE else fail_type.value,
                failure_type=fail_type,
                error_message=f"Falha na camada de serviço: {err_sanitized}",
                provider_config=provider_config,
            )

        # Mapeamento do resultado do Lean L1
        status = lean_res.terminal_status

        # Caso de falha na primeira passada (ex: erro de provider ou JSON corrompido)
        if status == "FIRST_PASS_FAILED":
            raw_err = ""
            if lean_res.final_markdown and "Não foi possível gerar a análise inicial da ideia:" in lean_res.final_markdown:
                raw_err = lean_res.final_markdown.split("Não foi possível gerar a análise inicial da ideia:")[-1].strip()
            err_sanitized = sanitize_secret_text(raw_err)
            failure_type = self._classify_error(err_sanitized, default=ServiceFailureType.STRUCTURED_OUTPUT_FAILURE)
            err_msg = (
                f"Falha na análise inicial da ideia pelo modelo: {err_sanitized}"
                if err_sanitized
                else "Falha na análise inicial da ideia pelo modelo."
            )
            return EvolutionResponse(
                success=False,
                run_id=lean_res.run_id,
                treatment_used=TreatmentMode.LEAN_L1,
                raw_idea=request.raw_idea,
                terminal_status=status,
                total_model_calls=lean_res.total_model_calls,
                decision_progress_detected=False,
                failure_type=failure_type,
                error_message=err_msg,
                lean_result=lean_res,
                provider_config=provider_config,
            )

        # Parada deliberada por decisão normativa humana (não é crash!)
        human_req = (status == "HUMAN_DECISION_REQUIRED") or lean_res.human_decision_requested

        # Parada deliberada por ausência de trabalho útil (STOP_NO_USEFUL_WORK)
        fail_type = ServiceFailureType.DOMAIN_DECISION_OR_STOP if status == "STOP_NO_USEFUL_WORK" else None

        # Geração determinística do EvolutionArtifact de produto (Custo = 0 chamadas)
        artifact = EvolutionArtifactMapper.map_lean_result(
            lean_res,
            original_idea=request.raw_idea,
            model_name=request.model_name or getattr(self.runner, "default_model", None),
            provider=getattr(self.runner, "provider", None),
        )

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
            artifact=artifact,
            provider_config=provider_config,
        )

    def _execute_fast_fallback(
        self,
        request: EvolutionRequest,
        run_id: str,
        provider_config: Optional[ProviderConfig] = None,
    ) -> EvolutionResponse:
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
            err_sanitized = sanitize_secret_text(str(e))
            fail_type = self._classify_error(err_sanitized, default=ServiceFailureType.INTERNAL_APPLICATION_FAILURE)
            return EvolutionResponse(
                success=False,
                run_id=run_id,
                treatment_used=TreatmentMode.FAST_FALLBACK,
                raw_idea=request.raw_idea,
                terminal_status="INTERNAL_APPLICATION_FAILURE",
                failure_type=fail_type,
                error_message=f"Exceção no fallback rápido: {err_sanitized}",
                provider_config=provider_config,
            )

        success = base_res.get("success", False)
        error_msg = base_res.get("error")
        sanitized_error = sanitize_secret_text(error_msg) if error_msg else None

        artifact = None
        if success:
            artifact = EvolutionArtifactMapper.map_baseline_result(
                base_res,
                original_idea=request.raw_idea,
                run_id=run_id,
                model_name=request.model_name or getattr(self.runner, "default_model", None),
                provider=getattr(self.runner, "provider", None),
            )

        fail_type = None if success else self._classify_error(sanitized_error or "", default=ServiceFailureType.PROVIDER_FAILURE)

        return EvolutionResponse(
            success=success,
            run_id=run_id,
            treatment_used=TreatmentMode.FAST_FALLBACK,
            raw_idea=request.raw_idea,
            terminal_status="COMPLETED" if success else "BASELINE_FAILED",
            total_model_calls=1,
            failure_type=fail_type,
            error_message=sanitized_error,
            baseline_result=base_res,
            artifact=artifact,
            provider_config=provider_config,
        )

    def _execute_suspended_deep_loop(
        self,
        request: EvolutionRequest,
        run_id: str,
        provider_config: Optional[ProviderConfig] = None,
    ) -> EvolutionResponse:
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
                provider_config=provider_config,
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
            err_sanitized = sanitize_secret_text(str(e))
            fail_type = self._classify_error(err_sanitized, default=ServiceFailureType.INTERNAL_APPLICATION_FAILURE)
            return EvolutionResponse(
                success=False,
                run_id=run_id,
                treatment_used=TreatmentMode.SUSPENDED_DEEP_LOOP,
                raw_idea=request.raw_idea,
                terminal_status="INTERNAL_APPLICATION_FAILURE",
                failure_type=fail_type,
                error_message=f"Exceção no loop profundo suspenso: {err_sanitized}",
                provider_config=provider_config,
            )

        stat_val = state.status.value if hasattr(state, "status") else getattr(state, "run_status", "COMPLETED")
        success = (stat_val in ("COMPLETED", "REFINED_IDEA_READY"))
        artifact = None
        if success:
            artifact = EvolutionArtifactMapper.map_simple_state(
                state,
                run_id=run_id,
                model_name=request.model_name or getattr(self.runner, "default_model", None),
                provider=getattr(self.runner, "provider", None),
            )

        return EvolutionResponse(
            success=success,
            run_id=run_id,
            treatment_used=TreatmentMode.SUSPENDED_DEEP_LOOP,
            raw_idea=request.raw_idea,
            terminal_status=stat_val,
            total_model_calls=getattr(state, "reconstruction_attempts", 0) + 1,  # Telemetria nominal
            failure_type=None if success else ServiceFailureType.DOMAIN_DECISION_OR_STOP,
            artifact=artifact,
            provider_config=provider_config,
        )

    @staticmethod
    def _classify_error(
        err_text: str,
        default: ServiceFailureType = ServiceFailureType.PROVIDER_FAILURE,
    ) -> ServiceFailureType:
        """Classifica erros de provedor/transporte na taxonomia tipada de ServiceFailureType."""
        low = err_text.lower()
        if any(k in low for k in ["401", "403", "unauthorized", "api_key_absent", "forbidden", "auth_failure", "invalid api key"]):
            return ServiceFailureType.PROVIDER_AUTH_FAILURE
        if any(k in low for k in ["429", "rate limit", "rate_limit", "quota", "too many requests", "tpm", "rpm"]):
            return ServiceFailureType.PROVIDER_RATE_LIMIT
        if any(k in low for k in ["500", "502", "503", "504", "internal server error", "bad gateway", "service unavailable", "gateway timeout"]):
            return ServiceFailureType.PROVIDER_SERVER_FAILURE
        if any(k in low for k in ["connection refused", "timeout", "timed out", "urlopen error", "network unreachable", "dns", "connection reset"]):
            return ServiceFailureType.PROVIDER_UNAVAILABLE
        if any(k in low for k in ["cost_policy", "cost_limit", "unknown_cost"]):
            return ServiceFailureType.COST_POLICY_BLOCKED
        if any(k in low for k in ["validation_error", "json_schema", "schema_invalid", "jsondecodeerror", "structured_output"]):
            return ServiceFailureType.STRUCTURED_OUTPUT_FAILURE
        return default
