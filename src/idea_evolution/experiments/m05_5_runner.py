"""
src/idea_evolution/experiments/m05_5_runner.py
Executor do experimento de replicação controlada M05.5.

Idêntico semanticamente ao M05.4, com as únicas diferenças:
- Diretório de experimento: EXP-M05.5-CONTROLLED-REPLICATION-20260831
- Holdout ideas: REP-01 a REP-08 (novas, independentes do M05.4)
- Mapeamento de blinding: Revisão 1 independente
- Nenhuma alteração nos runners, providers, modelos ou topologia de stages.
"""

from __future__ import annotations
import os
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from src.idea_evolution.providers.native import NativeModelRunner
from src.idea_evolution.orchestration.baseline import BaselineRunner
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.orchestration.lean_loop import LeanLoopRunner
from src.idea_evolution.experiments.blind_renderer import BlindRenderer, BlindReviewPacket, BlindReviewItem
from src.idea_evolution.domain.early_epistemic_gate import DecisionDeltaEventType


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
EXP_DIR = REPO_ROOT / "experiments" / "EXP-M05.5-CONTROLLED-REPLICATION-20260831"
ATTEMPT_DIR = EXP_DIR / "REAL-EXECUTION-ATTEMPT-001"
RAW_DIR = ATTEMPT_DIR / "raw"

EXPECTED_PROVIDER = "groq"
EXPECTED_MODEL = "openai/gpt-oss-120b"
EXPERIMENT_ID = "EXP-M05.5-CONTROLLED-REPLICATION-20260831"
ATTEMPT_ID = "REAL-EXECUTION-ATTEMPT-001"


def calculate_sha256_text(text: str) -> str:
    norm = text.encode("utf-8").replace(b"\r\n", b"\n")
    return hashlib.sha256(norm).hexdigest()


class M055ReplicationExecutor:
    """Orquestrador de execução da replicação controlada M05.5."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY_MISSING: Não é possível executar M05.5 sem a chave Groq."
            )

        self.runner = NativeModelRunner(
            provider=EXPECTED_PROVIDER,
            api_key=self.api_key,
            default_model=EXPECTED_MODEL,
        )
        RAW_DIR.mkdir(parents=True, exist_ok=True)

    def load_holdout_ideas(self) -> List[Dict[str, str]]:
        holdout_file = EXP_DIR / "HOLDOUT-IDEAS.json"
        with open(holdout_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["ideas"]

    def load_blind_mappings(self, sealed_reveal_path: Path) -> Dict[str, Dict[str, str]]:
        with open(sealed_reveal_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["mappings"]

    def run_condition_a(self, idea_id: str, raw_idea: str) -> Dict[str, Any]:
        """Executa Condição A: Baseline Single Refine (1 chamada)."""
        runs_dir = RAW_DIR / "runs_a"
        runs_dir.mkdir(parents=True, exist_ok=True)
        baseline_runner = BaselineRunner(runner=self.runner, model_name=EXPECTED_MODEL)

        start_t = time.time()
        result = baseline_runner.run(
            original_idea=raw_idea,
            run_id=f"EXP-M05.5-{idea_id}-COND-A",
            runs_dir=runs_dir,
        )
        lat = time.time() - start_t

        output_data = result.get("parsed_output", {})
        summary = output_data.get("summary", "")
        refined = output_data.get("refined_version", "")
        strengths = output_data.get("strengths", [])
        weaknesses = output_data.get("weaknesses", [])
        next_steps = output_data.get("next_steps", [])

        rendered_text = (
            f"### Resumo\n{summary}\n\n"
            f"### Versão Refinada\n{refined}\n\n"
            f"### Pontos Fortes e Fracos\n"
            f"- **Fortes:** {', '.join(strengths)}\n"
            f"- **Fracos:** {', '.join(weaknesses)}\n\n"
            f"### Próximos Passos\n{', '.join(next_steps)}"
        )

        raw_artifact_file = RAW_DIR / f"{idea_id}_condition_a.json"
        raw_payload = {
            "experiment_id": EXPERIMENT_ID,
            "attempt_id": ATTEMPT_ID,
            "idea_id": idea_id,
            "condition": "CONDITION_A",
            "raw_idea": raw_idea,
            "latency_seconds": lat,
            "model_calls": 1,
            "success": result.get("success", False),
            "error": result.get("error"),
            "parsed_output": output_data,
            "rendered_semantic_text": rendered_text,
        }
        with open(raw_artifact_file, "w", encoding="utf-8") as f:
            json.dump(raw_payload, f, indent=2, ensure_ascii=False)

        return raw_payload

    def run_condition_b(self, idea_id: str, raw_idea: str) -> Dict[str, Any]:
        """Executa Condição B: Standard 6-stage Simple Loop (até 10 chamadas)."""
        from src.idea_evolution.config.routing import ModelRoutingConfig, ModelDefinition
        from src.idea_evolution.providers.router import RunnerRouter

        runs_dir = RAW_DIR / "runs_b"
        runs_dir.mkdir(parents=True, exist_ok=True)

        config = ModelRoutingConfig(
            models={
                "default": ModelDefinition(
                    provider=self.runner.provider,
                    model=self.runner.default_model,
                )
            },
            routes={},
            default_model_alias="default",
        )
        router = RunnerRouter(config=config, custom_runners={"default": self.runner})
        simple_runner = SimpleLoopRunner(
            router=router,
            topology="STANDARD_6_STAGE",
            runs_dir=runs_dir,
        )

        start_t = time.time()
        state = simple_runner.run(
            original_idea=raw_idea,
            run_id=f"EXP-M05.5-{idea_id}-COND-B",
        )
        lat = time.time() - start_t

        rendered_text = (
            f"### Ideia Refinada Final\n{state.current_idea or state.original_idea}\n\n"
            f"### Intenção Humana Preservada\n{state.human_intent}\n\n"
            f"### Mecanismo Central\n{state.core_mechanism}\n\n"
            f"### Incertezas Críticas Remanescentes\n"
            + "\n".join(f"- {u}" for u in state.remaining_uncertainties)
            + f"\n\n### Próxima Ação Recomendada\n{state.recommended_next_step}"
        )

        calls = len(state.stage_history)
        raw_artifact_file = RAW_DIR / f"{idea_id}_condition_b.json"
        raw_payload = {
            "experiment_id": EXPERIMENT_ID,
            "attempt_id": ATTEMPT_ID,
            "idea_id": idea_id,
            "condition": "CONDITION_B",
            "raw_idea": raw_idea,
            "latency_seconds": lat,
            "model_calls": calls,
            "terminal_status": state.status.value,
            "reconstruction_count": state.reconstruction_count,
            "stages_executed": [s.stage_id for s in state.stage_history],
            "rendered_semantic_text": rendered_text,
        }

        with open(raw_artifact_file, "w", encoding="utf-8") as f:
            json.dump(raw_payload, f, indent=2, ensure_ascii=False)

        return raw_payload

    def run_condition_c(self, idea_id: str, raw_idea: str) -> Dict[str, Any]:
        """Executa Condição C: Lean L1 / FioED (máximo 2 chamadas)."""
        runs_dir = RAW_DIR / "runs_c"
        runs_dir.mkdir(parents=True, exist_ok=True)
        lean_runner = LeanLoopRunner(
            runner=self.runner,
            model_name=EXPECTED_MODEL,
            runs_dir=runs_dir,
        )

        start_t = time.time()
        result = lean_runner.run(
            original_idea=raw_idea,
            run_id=f"EXP-M05.5-{idea_id}-COND-C",
        )
        lat = time.time() - start_t

        rendered_text = result.final_markdown or ""
        if not rendered_text and result.first_pass:
            fp = result.first_pass
            rendered_text = (
                f"### Intenção Central\n{fp.core_intent}\n\n"
                f"### Mecanismo Proposto\n{fp.primary_mechanism.mechanism}\n\n"
                f"### Vulnerabilidades Identificadas\n"
                + "\n".join(
                    f"- **{v.risk_level}:** {v.vulnerability}" for v in fp.vulnerabilities
                )
                + "\n\n### Próxima Ação Recomendada\n"
                f"{fp.recommended_action}"
            )

        raw_artifact_file = RAW_DIR / f"{idea_id}_condition_c.json"
        raw_payload = {
            "experiment_id": EXPERIMENT_ID,
            "attempt_id": ATTEMPT_ID,
            "idea_id": idea_id,
            "condition": "CONDITION_C",
            "raw_idea": raw_idea,
            "latency_seconds": lat,
            "model_calls": result.total_model_calls,
            "terminal_status": result.terminal_status,
            "gate_outcome": result.gate_result.outcome.value if result.gate_result else "UNKNOWN",
            "human_decision_requested": result.human_decision_requested,
            "rendered_semantic_text": rendered_text,
        }
        with open(raw_artifact_file, "w", encoding="utf-8") as f:
            json.dump(raw_payload, f, indent=2, ensure_ascii=False)

        return raw_payload

    def _validate_model_routing(self) -> None:
        """Fail-fast preflight: verify frozen provider/model before any provider call."""
        from src.idea_evolution.config.routing import ModelRoutingConfig, ModelDefinition
        from src.idea_evolution.providers.router import RunnerRouter
        from src.idea_evolution.config.catalog import ModelCatalog
        import tempfile

        actual_provider = getattr(self.runner, "provider", None)
        if actual_provider != EXPECTED_PROVIDER:
            raise RuntimeError(
                f"PROVIDER_SPEC_VIOLATION: expected '{EXPECTED_PROVIDER}', got '{actual_provider}'."
            )
        actual_model = getattr(self.runner, "default_model", None)
        if actual_model != EXPECTED_MODEL:
            raise RuntimeError(
                f"MODEL_SPEC_VIOLATION: expected '{EXPECTED_MODEL}', got '{actual_model}'."
            )

        baseline_runner = BaselineRunner(runner=self.runner, model_name=EXPECTED_MODEL)
        if baseline_runner.model_name != EXPECTED_MODEL:
            raise RuntimeError(
                f"BaselineRunner model mismatch: expected {EXPECTED_MODEL}, "
                f"got {baseline_runner.model_name}"
            )

        config_b = ModelRoutingConfig(
            models={
                "default": ModelDefinition(provider=EXPECTED_PROVIDER, model=EXPECTED_MODEL)
            },
            routes={},
            default_model_alias="default",
        )
        router_b = RunnerRouter(config=config_b, custom_runners={"default": self.runner})
        catalog = ModelCatalog()
        expected_stages = [
            "UNDERSTAND", "ATTACK", "ALTERNATIVES", "SYNTHESIZE", "REALITY_CHECK", "FINAL_REVIEW"
        ]
        for stage in expected_stages:
            alias, model_def = router_b.config.resolve_stage(stage, catalog=catalog)
            if alias != "default":
                raise RuntimeError(f"Condition B stage {stage} resolved to wrong alias: {alias}")
            if model_def.provider != EXPECTED_PROVIDER or model_def.model != EXPECTED_MODEL:
                raise RuntimeError(
                    f"Condition B stage {stage} model/provider mismatch."
                )

        lean_runner = LeanLoopRunner(
            runner=self.runner,
            model_name=EXPECTED_MODEL,
            runs_dir=Path(tempfile.mkdtemp()),
        )
        if lean_runner.model_name != EXPECTED_MODEL:
            raise RuntimeError(
                f"LeanLoopRunner model mismatch: expected {EXPECTED_MODEL}, "
                f"got {lean_runner.model_name}"
            )

    def execute_all(self, sealed_reveal_path: Path) -> Dict[str, Any]:
        """Execute all 24 cells sequentially."""
        self._validate_model_routing()

        ideas = self.load_holdout_ideas()
        mappings = self.load_blind_mappings(sealed_reveal_path)
        raw_manifest_entries: List[Dict[str, Any]] = []
        blind_packets: List[BlindReviewPacket] = []

        total_calls = 0
        calls_by_cond: Dict[str, int] = {
            "CONDITION_A": 0, "CONDITION_B": 0, "CONDITION_C": 0
        }

        print(f"Iniciando execução de replicação M05.5 nas 8 ideias holdout...")
        print(f"Provider: {EXPECTED_PROVIDER}, Model: {EXPECTED_MODEL}")

        for idx, item in enumerate(ideas, 1):
            idea_id = item["idea_id"]
            raw_idea = item["raw_idea"]
            suite_class = item.get("suite_class", "UNKNOWN")
            print(f"[{idx}/8] {idea_id} ({suite_class})...")

            res_a = self.run_condition_a(idea_id, raw_idea)
            res_b = self.run_condition_b(idea_id, raw_idea)
            res_c = self.run_condition_c(idea_id, raw_idea)

            calls_by_cond["CONDITION_A"] += res_a["model_calls"]
            calls_by_cond["CONDITION_B"] += res_b["model_calls"]
            calls_by_cond["CONDITION_C"] += res_c["model_calls"]
            total_calls += res_a["model_calls"] + res_b["model_calls"] + res_c["model_calls"]

            for cond_name, res_obj in [
                ("CONDITION_A", res_a),
                ("CONDITION_B", res_b),
                ("CONDITION_C", res_c),
            ]:
                fpath = RAW_DIR / f"{idea_id}_{cond_name.lower()}.json"
                h = calculate_sha256_text(fpath.read_text(encoding="utf-8"))
                raw_manifest_entries.append({
                    "idea_id": idea_id,
                    "condition": cond_name,
                    "raw_artifact_file": str(fpath.relative_to(EXP_DIR)),
                    "sha256": h,
                    "model_calls": res_obj["model_calls"],
                    "latency_seconds": res_obj["latency_seconds"],
                })

            # Build blind review packet using frozen mapping
            idea_mapping = mappings[idea_id]
            cond_res_map = {
                "CONDITION_A": res_a["rendered_semantic_text"],
                "CONDITION_B": res_b["rendered_semantic_text"],
                "CONDITION_C": res_c["rendered_semantic_text"],
            }
            items = [
                BlindReviewItem(
                    label="RESULTADO 1",
                    content_text=cond_res_map[idea_mapping["RESULT_1"]],
                ),
                BlindReviewItem(
                    label="RESULTADO 2",
                    content_text=cond_res_map[idea_mapping["RESULT_2"]],
                ),
                BlindReviewItem(
                    label="RESULTADO 3",
                    content_text=cond_res_map[idea_mapping["RESULT_3"]],
                ),
            ]
            blind_packets.append(
                BlindReviewPacket(idea_id=idea_id, raw_idea=raw_idea, items=items)
            )

        # Save RAW-EXECUTION-MANIFEST.json
        raw_manifest_path = ATTEMPT_DIR / "RAW-EXECUTION-MANIFEST.json"
        with open(raw_manifest_path, "w", encoding="utf-8") as f:
            json.dump({
                "experiment_id": EXPERIMENT_ID,
                "attempt_id": ATTEMPT_ID,
                "executed_at": datetime.now().isoformat(),
                "provider": EXPECTED_PROVIDER,
                "model": EXPECTED_MODEL,
                "total_cells": len(raw_manifest_entries),
                "total_real_model_calls": total_calls,
                "calls_by_condition": calls_by_cond,
                "entries": raw_manifest_entries,
            }, f, indent=2, ensure_ascii=False)

        # Render BLIND-REVIEW-PACKET.md
        full_packet_md_lines = [
            "# PACOTE DE AVALIAÇÃO CEGA COMPLETO — M05.5 REPLICAÇÃO CONTROLADA",
            "",
            "> **AVISO AO REVISOR HUMANO:**",
            "> Este documento contém as 8 ideias holdout avaliadas pelas três condições anônimas (RESULTADO 1, RESULTADO 2, RESULTADO 3).",
            "> A ordem dos resultados foi aleatorizada de forma independente para cada ideia sob compromisso criptográfico prévio.",
            "> Preencha o formulário de revisão humana e congele suas notas antes de abrir qualquer mapeamento de revelação.",
            "",
        ]

        for p in blind_packets:
            full_packet_md_lines.append(BlindRenderer.render_markdown_packet(p))
            full_packet_md_lines.append("\n\n============================================================\n\n")

        packet_text = "\n".join(full_packet_md_lines)
        packet_path = EXP_DIR / "BLIND-REVIEW-PACKET.md"
        with open(packet_path, "w", encoding="utf-8") as f:
            f.write(packet_text)

        leaks = BlindRenderer.detect_leaks(packet_text)

        return {
            "total_cells": len(raw_manifest_entries),
            "total_calls": total_calls,
            "calls_by_condition": calls_by_cond,
            "leak_count": len(leaks),
            "leaks": leaks,
            "packet_hash": calculate_sha256_text(packet_text),
        }
