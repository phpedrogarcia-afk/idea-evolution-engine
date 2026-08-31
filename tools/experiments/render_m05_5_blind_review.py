#!/usr/bin/env python3
"""
tools/experiments/render_m05_5_blind_review.py
Renderizador de Pacote de Revisão Cega Humana para M05.5.

Architectural Invariant:
  BLIND_RENDERING_PLANE_HAS_NO_MODEL_EXECUTION = True

Responsabilidades:
  1. Carregar artefatos brutos congelados de REAL-EXECUTION-ATTEMPT-001/raw/.
  2. Carregar arquivo de revelação selada BLIND-REVEAL-REV2.json.
  3. Renderizar BLIND-REVIEW-PACKET.md desidentificado e aleatorizado.
  4. Executar auditoria de vazamento (leak audit) sem expor mapeamento nem segredos.
  5. Gerar formulário de revisão humana M05.5-HUMAN-REVIEW-FORM.md.
"""

from __future__ import annotations
import os
import sys
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional

BLIND_RENDERING_PLANE_HAS_NO_MODEL_EXECUTION = True

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.idea_evolution.experiments.blind_renderer import BlindRenderer, BlindReviewPacket, BlindReviewItem

EXP_DIR = REPO_ROOT / "experiments" / "EXP-M05.5-CONTROLLED-REPLICATION-20260831"
ATTEMPT_DIR = EXP_DIR / "REAL-EXECUTION-ATTEMPT-001"
RAW_DIR = ATTEMPT_DIR / "raw"


def calculate_sha256_text(text: str) -> str:
    norm = text.encode("utf-8").replace(b"\r\n", b"\n")
    return hashlib.sha256(norm).hexdigest()


def render_blind_packet(
    reveal_file: Path,
    output_packet_path: Optional[Path] = None,
    output_form_path: Optional[Path] = None,
) -> Dict[str, Any]:
    if not RAW_DIR.is_dir():
        raise FileNotFoundError(f"Diretório de artefatos brutos não encontrado: {RAW_DIR}")

    if not reveal_file.is_file():
        raise FileNotFoundError(f"Arquivo de revelação selada não encontrado: {reveal_file}")

    with open(reveal_file, "r", encoding="utf-8") as f:
        reveal_data = json.load(f)
        mappings = reveal_data["mappings"]

    holdout_file = EXP_DIR / "HOLDOUT-IDEAS.json"
    with open(holdout_file, "r", encoding="utf-8") as f:
        holdout_data = json.load(f)
        ideas = holdout_data["ideas"]

    blind_packets: List[BlindReviewPacket] = []

    for item in ideas:
        idea_id = item["idea_id"]
        raw_idea = item["raw_idea"]

        file_a = RAW_DIR / f"{idea_id}_condition_a.json"
        file_b = RAW_DIR / f"{idea_id}_condition_b.json"
        file_c = RAW_DIR / f"{idea_id}_condition_c.json"

        data_a = json.loads(file_a.read_text(encoding="utf-8"))
        data_b = json.loads(file_b.read_text(encoding="utf-8"))
        data_c = json.loads(file_c.read_text(encoding="utf-8"))

        idea_mapping = mappings[idea_id]
        cond_map = {
            "CONDITION_A": data_a["rendered_semantic_text"],
            "CONDITION_B": data_b["rendered_semantic_text"],
            "CONDITION_C": data_c["rendered_semantic_text"],
        }

        items = [
            BlindReviewItem(label="RESULTADO 1", content_text=cond_map[idea_mapping["RESULT_1"]]),
            BlindReviewItem(label="RESULTADO 2", content_text=cond_map[idea_mapping["RESULT_2"]]),
            BlindReviewItem(label="RESULTADO 3", content_text=cond_map[idea_mapping["RESULT_3"]]),
        ]
        blind_packets.append(BlindReviewPacket(idea_id=idea_id, raw_idea=raw_idea, items=items))

    # Montar BLIND-REVIEW-PACKET.md
    packet_lines = [
        "# PACOTE DE AVALIAÇÃO CEGA COMPLETO — M05.5 REPLICAÇÃO CONTROLADA",
        "",
        "> **AVISO AO REVISOR HUMANO:**",
        "> Este documento contém as 8 novas ideias holdout avaliadas por três condições anônimas (RESULTADO 1, RESULTADO 2, RESULTADO 3).",
        "> A ordem dos resultados foi aleatorizada de forma independente para cada ideia sob compromisso criptográfico prévio (Rev2).",
        "> Preencha o arquivo `M05.5-HUMAN-REVIEW-FORM.md` e congele suas notas antes de abrir qualquer mapeamento de revelação.",
        "",
    ]

    for p in blind_packets:
        packet_lines.append(BlindRenderer.render_markdown_packet(p))
        packet_lines.append("\n\n============================================================\n\n")

    packet_text = "\n".join(packet_lines)
    out_packet = output_packet_path or (EXP_DIR / "BLIND-REVIEW-PACKET.md")
    out_packet.write_text(packet_text, encoding="utf-8")

    leaks = BlindRenderer.detect_leaks(packet_text)

    # Montar Formulário de Revisão Humana
    form_lines = [
        "# M05.5-HUMAN-REVIEW-FORM.md — Formulário de Avaliação Humana Cega (M05.5)",
        "",
        "> **INSTRUÇÕES PARA O AVALIADOR HUMANO:**",
        "> Avalie cada ideia holdout (REP-01 a REP-08) comparando os 3 resultados anônimos (RESULTADO 1, RESULTADO 2, RESULTADO 3).",
        "> Atribua notas de 1 a 5 para cada dimensão e defina o ranking ordinal (1º = 3pts, 2º = 2pts, 3º = 1pt).",
        "> Escolha também com qual resultado você continuaria o desenvolvimento (CONTINUE).",
        "",
        "---",
        "",
    ]

    for item in ideas:
        idea_id = item["idea_id"]
        raw_idea = item["raw_idea"]
        form_lines.extend([
            f"## {idea_id}",
            f"**Ideia Original:** {raw_idea}",
            "",
            "### Pontuação Dimensional (1 a 5)",
            "| Dimensão | RESULTADO 1 | RESULTADO 2 | RESULTADO 3 |",
            "|---|---|---|---|",
            "| 1. Preservação de Intenção | | | |",
            "| 2. Ganho de Clareza | | | |",
            "| 3. Crítica Útil | | | |",
            "| 4. Novidade Útil | | | |",
            "| 5. Controle de Premissas | | | |",
            "| 6. Utilidade Decisória | | | |",
            "| 7. Honestidade Epistêmica | | | |",
            "| 8. Preservação Criativa | | | |",
            "| 9. Moderação Apropriada | | | |",
            "| 10. Acionabilidade Pertinente | | | |",
            "| **TOTAL SECUNDÁRIO** | | | |",
            "",
            "### Ranking Ordinal e Decisão",
            "- **1º Lugar (Melhor - 3 pts):** RESULTADO_",
            "- **2º Lugar (Intermediário - 2 pts):** RESULTADO_",
            "- **3º Lugar (Pior - 1 pt):** RESULTADO_",
            "- **PROCESS_WITH_WHICH_I_WOULD_CONTINUE:** RESULTADO_",
            "",
            "### Observações Qualitativas",
            "- ",
            "",
            "---",
            "",
        ])

    form_text = "\n".join(form_lines)
    out_form = output_form_path or (EXP_DIR / "M05.5-HUMAN-REVIEW-FORM.md")
    out_form.write_text(form_text, encoding="utf-8")

    return {
        "packet_path": str(out_packet),
        "packet_sha256": calculate_sha256_text(packet_text),
        "form_path": str(out_form),
        "form_sha256": calculate_sha256_text(form_text),
        "total_ideas": len(blind_packets),
        "leak_count": len(leaks),
        "leaks": leaks,
    }


if __name__ == "__main__":
    sealed = Path(r"C:\Users\phped\.fioideias\sealed\EXP-M05.5-CONTROLLED-REPLICATION-20260831\BLIND-REVEAL-REV2.json")
    res = render_blind_packet(reveal_file=sealed)
    print("PACKET_RENDERED_OK")
    print("PACKET_SHA256:", res["packet_sha256"])
    print("LEAK_COUNT:", res["leak_count"])
