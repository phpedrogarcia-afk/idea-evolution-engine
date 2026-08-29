#!/usr/bin/env python3
"""
tools/experiments/render_m05_4_blind_review.py
Standalone post-execution blind review packet generator.

Architectural Invariant:
  BLIND_RENDERING_PLANE_HAS_NO_MODEL_EXECUTION = True

Responsibilities:
  1. Load frozen raw outputs from attempt directory.
  2. Load external sealed reveal mapping.
  3. Render desensitized, randomized BLIND-REVIEW-PACKET.md.
  4. Perform leak audit against condition names, runner names, stage numbers, etc.
  5. Save packet and report hash without exposing mappings or secret values.

Strict Boundaries:
  - NO ModelRunner / NativeModelRunner imports or execution.
  - NO model calls.
  - NO stdout exposure of mappings or seed values.
"""

from __future__ import annotations
import os
import sys
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional

# Architectural invariant declaration
BLIND_RENDERING_PLANE_HAS_NO_MODEL_EXECUTION = True

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.idea_evolution.experiments.blind_renderer import BlindRenderer, BlindReviewPacket, BlindReviewItem


def calculate_sha256_text(text: str) -> str:
    norm = text.encode("utf-8").replace(b"\r\n", b"\n")
    return hashlib.sha256(norm).hexdigest()


def render_blind_packet(
    attempt_dir: Path,
    reveal_file: Path,
    holdout_file: Optional[Path] = None,
    output_packet_path: Optional[Path] = None,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Renders the blind human review packet from frozen raw artifacts and sealed reveal.
    """
    raw_dir = attempt_dir / "raw"
    if not raw_dir.is_dir():
        raise FileNotFoundError(f"Raw artifacts directory not found at {raw_dir}")

    if not reveal_file.is_file():
        raise FileNotFoundError(f"Sealed reveal file not found at {reveal_file}")

    holdout_path = holdout_file or (REPO_ROOT / "experiments" / "EXP-M05.4-PROSPECTIVE" / "HOLDOUT-IDEAS.json")
    holdout_ideas = json.loads(holdout_path.read_text(encoding="utf-8"))

    # Load secret reveal mappings
    reveal_data = json.loads(reveal_file.read_text(encoding="utf-8"))
    mappings = reveal_data["mappings"]

    blind_packets = []

    for item in holdout_ideas:
        idea_id = item["idea_id"]
        raw_idea = item["raw_idea"]

        raw_a_path = raw_dir / f"{idea_id}_condition_a.json"
        raw_b_path = raw_dir / f"{idea_id}_condition_b.json"
        raw_c_path = raw_dir / f"{idea_id}_condition_c.json"

        if not (raw_a_path.exists() and raw_b_path.exists() and raw_c_path.exists()):
            raise FileNotFoundError(f"Missing raw outputs for idea {idea_id} in {raw_dir}")

        res_a = json.loads(raw_a_path.read_text(encoding="utf-8"))
        res_b = json.loads(raw_b_path.read_text(encoding="utf-8"))
        res_c = json.loads(raw_c_path.read_text(encoding="utf-8"))

        idea_mapping = mappings[idea_id]
        cond_res_map = {
            "CONDITION_A": res_a.get("rendered_semantic_text", ""),
            "CONDITION_B": res_b.get("rendered_semantic_text", ""),
            "CONDITION_C": res_c.get("rendered_semantic_text", ""),
        }

        items = [
            BlindReviewItem(label="RESULTADO 1", content_text=cond_res_map[idea_mapping["RESULT_1"]]),
            BlindReviewItem(label="RESULTADO 2", content_text=cond_res_map[idea_mapping["RESULT_2"]]),
            BlindReviewItem(label="RESULTADO 3", content_text=cond_res_map[idea_mapping["RESULT_3"]]),
        ]
        blind_packets.append(BlindReviewPacket(idea_id=idea_id, raw_idea=raw_idea, items=items))

    # Render markdown document
    full_packet_md_lines = [
        "# PACOTE DE AVALIAÇÃO CEGA COMPLETO — M05.4 PROSPECTIVE RERUN",
        "",
        "> **AVISO AO REVISOR HUMANO:**",
        "> Este documento contém as 8 ideias holdout avaliadas pelas três condições anônimas (RESULTADO 1, RESULTADO 2, RESULTADO 3).",
        "> A ordem dos resultados foi aleatorizada de forma independente para cada ideia sob compromisso criptográfico prévio.",
        "> Preencha o arquivo `M05.4-HUMAN-REVIEW-TEMPLATE.md` e congele suas notas antes de abrir qualquer mapeamento de revelação.",
        "",
    ]
    for p in blind_packets:
        full_packet_md_lines.append(BlindRenderer.render_markdown_packet(p))
        full_packet_md_lines.append("\n\n============================================================\n\n")

    packet_text = "\n".join(full_packet_md_lines)
    dest_path = output_packet_path or (attempt_dir / "BLIND-REVIEW-PACKET.md")
    dest_path.write_text(packet_text, encoding="utf-8")
    packet_sha = calculate_sha256_text(packet_text)

    # Perform strict metadata leak audit
    leaks = BlindRenderer.detect_leaks(packet_text)

    if verbose:
        print(f"Blind review packet generated at: {dest_path}")
        print(f"Packet SHA-256: {packet_sha}")
        print(f"Leak count: {len(leaks)}")
        if leaks:
            print(f"WARNING: Leaks detected: {leaks}")

    return {
        "packet_path": str(dest_path),
        "packet_sha256": packet_sha,
        "leak_count": len(leaks),
        "leaks": leaks,
        "leak_audit_pass": (len(leaks) == 0),
    }


if __name__ == "__main__":
    attempt_path = Path("experiments/EXP-M05.4-PROSPECTIVE-RERUN-20260829/attempt-002")
    reveal_path = Path.home() / ".fioideias" / "sealed" / "EXP-M05.4-PROSPECTIVE-RERUN-20260829" / "BLIND-REVEAL-REV3.json"
    render_blind_packet(attempt_path, reveal_path)
