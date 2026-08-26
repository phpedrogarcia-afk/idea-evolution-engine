"""
src/idea_evolution/tracing/tracer.py
Persistência estruturada, telemetria e rastreamento de execuções (RunTracer).
"""

from pathlib import Path
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from src.idea_evolution.domain.state import SimpleIdeaState
from src.idea_evolution.stages.stage_base import StageExecutionResult

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
RUNS_DIR = REPO_ROOT / "runs"


class RunTracer:
    """Gerencia a criação do diretório do run, salvamento incremental de estágios e artefatos finais."""

    def __init__(self, run_id: Optional[str] = None, runs_dir: Optional[Path] = None):
        self.runs_root = runs_dir or RUNS_DIR
        self.runs_root.mkdir(parents=True, exist_ok=True)
        self.run_id = run_id or self._generate_run_id()
        self.run_dir = self.runs_root / self.run_id
        self.stages_dir = self.run_dir / "stages"
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.stages_dir.mkdir(parents=True, exist_ok=True)

        self.stage_records: List[Dict[str, Any]] = []
        self.start_time = time.time()

    def _generate_run_id(self) -> str:
        date_str = datetime.now().strftime("%Y%m%d")
        existing = list(self.runs_root.glob(f"RUN-{date_str}-*"))
        next_seq = len(existing) + 1
        return f"RUN-{date_str}-{next_seq:03d}"

    def record_input(self, original_idea: str, metadata: Optional[Dict[str, Any]] = None):
        input_file = self.run_dir / "input.json"
        data = {
            "run_id": self.run_id,
            "created_at": datetime.now().isoformat(),
            "original_idea": original_idea,
            "metadata": metadata or {},
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
            "timestamp": datetime.now().isoformat(),
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
            "reconstruction_count": state.reconstruction_count,
            "essence_drift_detected": state.essence_drift_detected,
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
            "stages": self.stage_records,
        }
        trace_file.write_text(json.dumps(trace_data, indent=2, ensure_ascii=False), encoding="utf-8")
