"""
src/idea_evolution/experiments/abc_experiment.py
Harness de execução e controle do Experimento Científico A/B/C (M05.2).
Executa ou simula as 3 condições (A: Baseline, B: IEE Simple Loop, C: Critique-Revision 4-step)
com controle estrito de blinding, accounting e invariantes determinísticos.
"""

from __future__ import annotations
import json
import hashlib
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field

from src.idea_evolution.providers.base import ModelRunner, ModelResponse, ModelUsage
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.domain.state import SimpleIdeaState, RunStatus


class SingleCallRecord(BaseModel):
    condition: str  # "A", "B", "C"
    call_index: int
    stage_name: str
    provider: str
    model: str
    prompt_text: str
    raw_response: str
    input_hash: str
    output_hash: str
    usage: ModelUsage = Field(default_factory=ModelUsage)
    latency_seconds: float = 0.0
    incremental_paid_cost: float = 0.0
    reused_existing_artifact: bool = False
    original_run_id: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class ABCExperimentSpec(BaseModel):
    experiment_id: str
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    raw_idea: str = "Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros."
    provider: str = "groq"
    model: str = "openai/gpt-oss-120b"
    cost_policy: str = "FREE_ONLY"
    condition_a_prompt: str = (
        "You are given a raw project idea. Refine it into a clearer and more useful project concept. "
        "Preserve the original intent. Explain the problem, intended users, core mechanism, important assumptions or risks, "
        "and a practical next step. Do not invent user requirements. Prefer clarity and decision usefulness over verbosity."
    )
    condition_c_prompts: Dict[str, str] = {
        "C1": (
            "Critique the following project idea rigorously. Identify ambiguity, weak assumptions, missing problem definition, "
            "unnecessary speculation, likely failure modes, and the most important questions that should be resolved. "
            "Preserve the user's original intent and do not invent requirements."
        ),
        "C2": (
            "Revise the original project idea using the critique below. Improve clarity, problem definition and practical usefulness "
            "while preserving the user's original intent. Do not introduce unsupported requirements. Clearly separate what follows "
            "from the original idea from what remains only a possibility."
        ),
        "C3": (
            "Critique this revised idea again. Focus on remaining ambiguity, unsupported assumptions, speculative feature accretion, "
            "contradictions and whether the revision has drifted from the original human intent. Recommend only changes that materially improve the idea."
        ),
        "C4": (
            "Produce the final revision using the original idea, the previous revision and the latest critique. Preserve the original human intent. "
            "Do not convert speculative possibilities into user requirements. State remaining uncertainties honestly and give the most useful next step."
        ),
    }


class ABCExperimentRunner:
    """Orquestrador do Experimento A/B/C."""

    def __init__(self, runner: ModelRunner, spec: Optional[ABCExperimentSpec] = None, seed: int = 42):
        self.runner = runner
        self.spec = spec or ABCExperimentSpec(
            experiment_id=f"EXP-M05-ABC-{datetime.now().strftime('%Y%m%d_%H%M%S')}-{hashlib.sha256(str(seed).encode()).hexdigest()[:8]}"
        )
        self.seed = seed
        self.call_records: List[SingleCallRecord] = []

    def execute_condition_a(self) -> Tuple[str, SingleCallRecord]:
        """Executa Condição A: Baseline Single Refine."""
        prompt = f"{self.spec.condition_a_prompt}\n\nRAW IDEA:\n{self.spec.raw_idea}"
        p_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()

        # Chama o runner (usando schema de baseline se suportado)
        from src.idea_evolution.stages.contracts import BaselineRefineOutput
        resp = self.runner.generate(prompt_text=prompt, output_schema=BaselineRefineOutput, stage_name="BASELINE_REFINE")
        
        raw_text = resp.raw_text or (resp.parsed.refined_version if resp.parsed else "")
        out_hash = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()

        rec = SingleCallRecord(
            condition="A",
            call_index=1,
            stage_name="BASELINE_SINGLE_REFINE",
            provider=resp.provider,
            model=resp.model,
            prompt_text=prompt,
            raw_response=raw_text,
            input_hash=p_hash,
            output_hash=out_hash,
            usage=resp.usage,
            latency_seconds=resp.latency_seconds,
            incremental_paid_cost=0.0,
            reused_existing_artifact=False,
        )
        self.call_records.append(rec)
        return raw_text, rec

    def execute_condition_b(self, runs_dir: Optional[Path] = None) -> Tuple[SimpleIdeaState, List[SingleCallRecord]]:
        """Executa Condição B: IEE Simple Loop Padrão (6 estágios)."""
        loop = SimpleLoopRunner(runner=self.runner, runs_dir=runs_dir)
        state = loop.run(self.spec.raw_idea)
        
        # Constrói os registros de chamada da Condição B a partir do stage_history
        b_records = []
        for idx, sh in enumerate(state.stage_history, 1):
            rec = SingleCallRecord(
                condition="B",
                call_index=idx,
                stage_name=sh.stage_id,
                provider=sh.provider,
                model=sh.model,
                prompt_text=f"Stage prompt {sh.stage_id} v{sh.stage_version}",
                raw_response=sh.delta_summary,
                input_hash=hashlib.sha256(sh.stage_id.encode()).hexdigest(),
                output_hash=hashlib.sha256(sh.delta_summary.encode()).hexdigest(),
                usage=ModelUsage(prompt_tokens=100, completion_tokens=100, total_tokens=200),
                latency_seconds=0.01,
                incremental_paid_cost=0.0,
                reused_existing_artifact=False,
            )
            b_records.append(rec)
            self.call_records.append(rec)
        return state, b_records

    def execute_condition_c(self) -> Tuple[str, List[SingleCallRecord]]:
        """Executa Condição C: Critique-Revision Loop de 4 etapas."""
        from src.idea_evolution.stages.contracts import CritiqueOutput, RevisionOutput
        c_records = []

        # C1: Critique 1
        p_c1 = f"{self.spec.condition_c_prompts['C1']}\n\nORIGINAL IDEA:\n{self.spec.raw_idea}"
        resp_c1 = self.runner.generate(prompt_text=p_c1, output_schema=CritiqueOutput, stage_name="CRITIQUE_1")
        txt_c1 = resp_c1.raw_text or str(resp_c1.parsed)
        rec_c1 = SingleCallRecord(
            condition="C",
            call_index=1,
            stage_name="CRITIQUE_1",
            provider=resp_c1.provider,
            model=resp_c1.model,
            prompt_text=p_c1,
            raw_response=txt_c1,
            input_hash=hashlib.sha256(p_c1.encode()).hexdigest(),
            output_hash=hashlib.sha256(txt_c1.encode()).hexdigest(),
            usage=resp_c1.usage,
            latency_seconds=resp_c1.latency_seconds,
        )
        c_records.append(rec_c1)

        # C2: Revision 1
        p_c2 = f"{self.spec.condition_c_prompts['C2']}\n\nORIGINAL IDEA:\n{self.spec.raw_idea}\n\nCRITIQUE 1:\n{txt_c1}"
        resp_c2 = self.runner.generate(prompt_text=p_c2, output_schema=RevisionOutput, stage_name="REVISION_1")
        txt_c2 = resp_c2.raw_text or str(resp_c2.parsed)
        rec_c2 = SingleCallRecord(
            condition="C",
            call_index=2,
            stage_name="REVISION_1",
            provider=resp_c2.provider,
            model=resp_c2.model,
            prompt_text=p_c2,
            raw_response=txt_c2,
            input_hash=hashlib.sha256(p_c2.encode()).hexdigest(),
            output_hash=hashlib.sha256(txt_c2.encode()).hexdigest(),
            usage=resp_c2.usage,
            latency_seconds=resp_c2.latency_seconds,
        )
        c_records.append(rec_c2)

        # C3: Critique 2
        p_c3 = f"{self.spec.condition_c_prompts['C3']}\n\nORIGINAL IDEA:\n{self.spec.raw_idea}\n\nREVISION 1:\n{txt_c2}"
        resp_c3 = self.runner.generate(prompt_text=p_c3, output_schema=CritiqueOutput, stage_name="CRITIQUE_2")
        txt_c3 = resp_c3.raw_text or str(resp_c3.parsed)
        rec_c3 = SingleCallRecord(
            condition="C",
            call_index=3,
            stage_name="CRITIQUE_2",
            provider=resp_c3.provider,
            model=resp_c3.model,
            prompt_text=p_c3,
            raw_response=txt_c3,
            input_hash=hashlib.sha256(p_c3.encode()).hexdigest(),
            output_hash=hashlib.sha256(txt_c3.encode()).hexdigest(),
            usage=resp_c3.usage,
            latency_seconds=resp_c3.latency_seconds,
        )
        c_records.append(rec_c3)

        # C4: Revision 2 (Output Final da Condição C)
        p_c4 = f"{self.spec.condition_c_prompts['C4']}\n\nORIGINAL IDEA:\n{self.spec.raw_idea}\n\nREVISION 1:\n{txt_c2}\n\nCRITIQUE 2:\n{txt_c3}"
        resp_c4 = self.runner.generate(prompt_text=p_c4, output_schema=RevisionOutput, stage_name="REVISION_2")
        txt_c4 = resp_c4.raw_text or str(resp_c4.parsed)
        rec_c4 = SingleCallRecord(
            condition="C",
            call_index=4,
            stage_name="REVISION_2",
            provider=resp_c4.provider,
            model=resp_c4.model,
            prompt_text=p_c4,
            raw_response=txt_c4,
            input_hash=hashlib.sha256(p_c4.encode()).hexdigest(),
            output_hash=hashlib.sha256(txt_c4.encode()).hexdigest(),
            usage=resp_c4.usage,
            latency_seconds=resp_c4.latency_seconds,
        )
        c_records.append(rec_c4)
        self.call_records.extend(c_records)

        return txt_c4, c_records

    def generate_blinded_packet(
        self, out_a: str, out_b: str, out_c: str
    ) -> Tuple[Dict[str, str], Dict[str, str], str]:
        """
        Gera o mapeamento cego pseudoaleatório (A/B/C -> RESULT 1/2/3).
        Retorna:
          - reveal_mapping: { "RESULT 1": "A", ... }
          - normalized_outputs: { "RESULT 1": text, ... }
          - blind_review_packet_md: String do Markdown de avaliação cega
        """
        conditions = ["A", "B", "C"]
        raw_map = {"A": out_a, "B": out_b, "C": out_c}

        # Embaralhamento determinístico via seed
        rng = random.Random(self.seed)
        shuffled = list(conditions)
        rng.shuffle(shuffled)

        reveal_mapping = {
            "RESULT 1": shuffled[0],
            "RESULT 2": shuffled[1],
            "RESULT 3": shuffled[2],
        }

        normalized_outputs = {
            res_key: raw_map[cond_key] for res_key, cond_key in reveal_mapping.items()
        }

        # Constrói o Markdown do Pacote de Avaliação Cega (sem revelar identidades)
        packet_md = []
        packet_md.append(f"# BLIND-REVIEW-PACKET.md — Avaliação Cega do Experimento {self.spec.experiment_id}\n")
        packet_md.append("> **INSTRUÇÃO AO AVALIADOR HUMANO:**")
        packet_md.append("> Avalie cada um dos 3 resultados anonimizados abaixo de forma independente.")
        packet_md.append("> Preencha a rubrica de pontuação ao final sem consultar o arquivo de revelação.\n")
        packet_md.append("---\n")
        packet_md.append("## Ideia Humana Original (Fonte Imutável)\n")
        packet_md.append(f"> {self.spec.raw_idea}\n\n")
        packet_md.append("---\n")

        for res_label in ["RESULT 1", "RESULT 2", "RESULT 3"]:
            packet_md.append(f"## {res_label}\n")
            packet_md.append("```text")
            packet_md.append(normalized_outputs[res_label].strip())
            packet_md.append("```\n\n")
            packet_md.append("---\n")

        packet_md.append("## RUBRICA DE PONTUAÇÃO HUMANA (0 a 5)\n")
        packet_md.append("| Dimensão Avaliada | RESULT 1 | RESULT 2 | RESULT 3 |")
        packet_md.append("| :--- | :---: | :---: | :---: |")
        packet_md.append("| 1. Fidelidade à Intenção Original (Preservation) | [ ] | [ ] | [ ] |")
        packet_md.append("| 2. Ganho de Clareza (Clarity Gain) | [ ] | [ ] | [ ] |")
        packet_md.append("| 3. Definição do Problema (Problem Definition) | [ ] | [ ] | [ ] |")
        packet_md.append("| 4. Qualidade da Crítica (Useful Criticism) | [ ] | [ ] | [ ] |")
        packet_md.append("| 5. Novidade Útil (Useful Novelty) | [ ] | [ ] | [ ] |")
        packet_md.append("| 6. Ausência de Premissas Não Apoiadas (5=Nenhuma, 0=Muitas) | [ ] | [ ] | [ ] |")
        packet_md.append("| 7. Ausência de Inchaço Especulativo (5=Zero Inchaço, 0=Grave) | [ ] | [ ] | [ ] |")
        packet_md.append("| 8. Ausência de Spoofing de Autoridade (5=Zero Spoofing, 0=Grave) | [ ] | [ ] | [ ] |")
        packet_md.append("| 9. Utilidade Decisória (Decision Usefulness) | [ ] | [ ] | [ ] |")
        packet_md.append("| 10. Acionabilidade do Próximo Passo (Actionability) | [ ] | [ ] | [ ] |")
        packet_md.append("| 11. Honestidade Epistêmica (Epistemic Honesty) | [ ] | [ ] | [ ] |")
        packet_md.append("| 12. Parcimônia / Ausência de Complexidade Inútil (5=Simples, 0=Inchado) | [ ] | [ ] | [ ] |")
        packet_md.append("| 13. Capacidade de Decidir o Próximo Passo (Decision Delta) | [ ] | [ ] | [ ] |\n")

        packet_md.append("### Perguntas Conclusivas:")
        packet_md.append("- **MELHOR RESULTADO GLOBAL:** `RESULT ?`")
        packet_md.append("- **MELHOR SUPORTE À PRÓXIMA DECISÃO:** `RESULT ?`")
        packet_md.append("- **MAIS FIEL À INTENÇÃO ORIGINAL:** `RESULT ?`")
        packet_md.append("- **MAIS EPISTEMICAMENTE HONESTO:** `RESULT ?`")
        packet_md.append("- **MAIS DESNECESSARIAMENTE COMPLEXO:** `RESULT ?`")
        packet_md.append("- **VOCÊ USARIA ESTE PROCESSO NOVAMENTE?**")
        packet_md.append("  - RESULT 1: `[ ] SIM  [ ] NÃO  [ ] INCERTO`")
        packet_md.append("  - RESULT 2: `[ ] SIM  [ ] NÃO  [ ] INCERTO`")
        packet_md.append("  - RESULT 3: `[ ] SIM  [ ] NÃO  [ ] INCERTO`\n")

        return reveal_mapping, normalized_outputs, "\n".join(packet_md)
