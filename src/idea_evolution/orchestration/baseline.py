"""
src/idea_evolution/orchestration/baseline.py
Executor do Baseline de Prompt Único (Condição A) para comparação experimental.
"""

from typing import Optional, Dict, Any
from pathlib import Path
import json
from src.idea_evolution.providers.base import ModelRunner, ModelResponse
from src.idea_evolution.stages.contracts import BaselineRefineOutput
from src.idea_evolution.tracing.tracer import RunTracer

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
PROMPTS_DIR = REPO_ROOT / "prompts"


class BaselineRunner:
    """Executa o baseline de prompt único (Condição A)."""

    def __init__(self, runner: ModelRunner, model_name: Optional[str] = None):
        self.runner = runner
        self.model_name = model_name

    def run(self, original_idea: str, run_id: Optional[str] = None, runs_dir: Optional[Path] = None) -> Dict[str, Any]:
        tracer = RunTracer(run_id=run_id, runs_dir=runs_dir)
        tracer.record_input(original_idea, metadata={"topology": "BASELINE_SINGLE_PROMPT"})

        prompt_template = (PROMPTS_DIR / "baseline_refine_v0_1.md").read_text(encoding="utf-8")
        user_prompt = prompt_template.replace("{idea}", original_idea)

        res: ModelResponse = self.runner.generate(
            prompt_text=user_prompt,
            output_schema=BaselineRefineOutput,
            stage_name="BASELINE_REFINE",
            model_name=self.model_name,
        )

        output_data = res.parsed.model_dump() if res.parsed else {}

        # Salvar final.json e final.md
        final_json = tracer.run_dir / "final.json"
        final_data = {
            "run_id": tracer.run_id,
            "topology": "BASELINE_SINGLE_PROMPT",
            "original_idea": original_idea,
            "success": res.error is None,
            "error": res.error,
            "parsed_output": output_data,
        }
        final_json.write_text(json.dumps(final_data, indent=2, ensure_ascii=False), encoding="utf-8")

        final_md = tracer.run_dir / "final.md"
        md_text = [
            f"# Baseline de Refinamento de Ideia — {tracer.run_id}\n",
            "## Ideia Original",
            f"> {original_idea}\n",
            "## Resumo do Modelo",
            f"{output_data.get('summary', '')}\n",
            "## Versão Refinada",
            f"{output_data.get('refined_version', '')}\n",
            "## Pontos Fortes e Fracos",
            f"- **Fortes:** {', '.join(output_data.get('strengths', []))}",
            f"- **Fracos:** {', '.join(output_data.get('weaknesses', []))}\n",
            "## Próximos Passos",
            f"{', '.join(output_data.get('next_steps', []))}\n",
        ]
        final_md.write_text("\n".join(md_text), encoding="utf-8")

        return final_data
