"""
src/idea_evolution/tracing/tracer.py
Persistência estruturada, telemetria e rastreamento de execuções (RunTracer) com Run ID imutável resistente a colisão.
"""

from pathlib import Path
import json
import time
import uuid
import os
import subprocess
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from src.idea_evolution.domain.state import SimpleIdeaState
from src.idea_evolution.stages.stage_base import StageExecutionResult

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
RUNS_DIR = REPO_ROOT / "runs"


def _get_git_commit() -> str:
    try:
        res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(REPO_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=2,
        )
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        pass
    return "UNKNOWN"


class RunTracer:
    """
    Gerencia a criação do diretório do run, salvamento incremental de estágios e artefatos finais.
    Garante identidade imutável de Run ID resistente a concorrência e independente do sistema de arquivos.
    """

    def __init__(self, run_id: Optional[str] = None, runs_dir: Optional[Path] = None):
        self.runs_root = runs_dir or RUNS_DIR
        self.runs_root.mkdir(parents=True, exist_ok=True)
        self.run_id = run_id or self.generate_immutable_run_id()
        self.run_dir = self.runs_root / self.run_id
        self.stages_dir = self.run_dir / "stages"
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.stages_dir.mkdir(parents=True, exist_ok=True)

        self.stage_records: List[Dict[str, Any]] = []
        self.start_time = time.time()
        self.git_commit = _get_git_commit()

    @classmethod
    def generate_immutable_run_id(cls) -> str:
        """
        Gera um Run ID com garantia estrita de unicidade e não reutilização:
        RUN-<UTC_YYYYMMDD_HHMMSS>-<UUID4_HEX8>
        Não depende de listagem de diretório ou contadores em memória.
        """
        utc_now = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        suffix = uuid.uuid4().hex[:8]
        return f"RUN-{utc_now}-{suffix}"

    def record_input(self, original_idea: str, metadata: Optional[Dict[str, Any]] = None):
        input_file = self.run_dir / "input.json"
        meta = metadata or {}
        meta.update({
            "git_commit": self.git_commit,
            "environment_pid": os.getpid(),
        })
        data = {
            "run_id": self.run_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "original_idea": original_idea,
            "metadata": meta,
        }
        input_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def record_stage_result(self, step_number: int, result: StageExecutionResult):
        stage_filename = f"{step_number:02d}_{result.stage_id}.json"
        stage_file = self.stages_dir / stage_filename

        record = {
            "step_number": step_number,
            "stage_id": result.stage_id,
            "stage_version": result.stage_version,
            "logical_alias": result.logical_alias,
            "provider": result.provider,
            "model": result.model,
            "prompt_id": result.prompt_id,
            "prompt_version": result.prompt_version,
            "attempt": result.attempt,
            "success": result.success,
            "retry_count": result.retry_count,
            "latency_seconds": result.latency_seconds,
            "delta_summary": result.delta_summary,
            "raw_response": result.raw_response,
            "parsed_output": result.output.model_dump() if result.output else None,
            "error": result.error,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.stage_records.append(record)
        stage_file.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")

    def persist_final_state(self, state: SimpleIdeaState):
        state_file = self.run_dir / "state.json"
        state_file.write_text(state.model_dump_json(indent=2), encoding="utf-8")

        final_json_file = self.run_dir / "final.json"
        final_data = {
            "run_id": self.run_id,
            "status": state.status.value,
            "original_idea": state.original_idea,
            "human_intent": state.human_intent,
            "refined_idea": state.current_idea,
            "core_mechanism": state.core_mechanism,
            "core_mechanism_basis": state.core_mechanism_basis.value,
            "core_mechanism_hash": state.core_mechanism_hash,
            "tested_core_hash": state.tested_core_hash,
            "reconstruction_count": state.reconstruction_count,
            "essence_drift_detected": state.essence_drift_detected,
            "ontology_contradiction_detected": state.ontology_contradiction_detected,
            "critical_issues_count": len(state.critical_issues),
            "alternatives_count": len(state.alternatives),
            "accepted_changes_count": len(state.accepted_changes),
            "rejected_changes_count": len(state.rejected_changes),
            "recommended_next_step": state.recommended_next_step,
        }
        final_json_file.write_text(json.dumps(final_data, indent=2, ensure_ascii=False), encoding="utf-8")

        final_md_file = self.run_dir / "final.md"
        final_md_file.write_text(state.to_human_markdown(), encoding="utf-8")

        # Trace completo
        trace_file = self.run_dir / "trace.json"
        total_duration = time.time() - self.start_time
        trace_data = {
            "run_id": self.run_id,
            "status": state.status.value,
            "total_duration_seconds": total_duration,
            "total_stages_executed": len(self.stage_records),
            "git_commit": self.git_commit,
            "stages": self.stage_records,
        }
        trace_file.write_text(json.dumps(trace_data, indent=2, ensure_ascii=False), encoding="utf-8")
