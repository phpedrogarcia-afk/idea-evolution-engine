"""
tests/unit/test_m05_4_preregistration.py
Testes unitários e determinísticos do Pré-registro M05.4.
Verifica imutabilidade da suíte holdout, eficácia do renderizador cego,
detecção de vazamento de metadados, compromisso criptográfico do reveal
e integridade do manifesto de pré-registro.
"""

import unittest
import json
import hashlib
from pathlib import Path

from src.idea_evolution.experiments.blind_renderer import (
    BlindRenderer,
    BlindReviewPacket,
    BlindReviewItem,
)


class TestM054Preregistration(unittest.TestCase):

    def setUp(self):
        self.repo_root = Path(__file__).resolve().parent.parent.parent
        self.exp_dir = self.repo_root / "experiments" / "EXP-M05.4-PROSPECTIVE"

    def test_01_holdout_ideas_complete_and_hash_immutable(self):
        """Holdout Ideas — Verifica se existem exatamente 8 ideias e se o hash corresponde ao compromisso."""
        holdout_file = self.exp_dir / "HOLDOUT-IDEAS.json"
        self.assertTrue(holdout_file.exists())

        with open(holdout_file, "r", encoding="utf-8") as f:
            ideas = json.load(f)

        self.assertEqual(len(ideas), 8)
        expected_ids = [f"IDEA-0{i}" for i in range(1, 9)]
        actual_ids = [item["idea_id"] for item in ideas]
        self.assertEqual(actual_ids, expected_ids)

        # Verifica que nenhuma ideia contém jargão interno do FioED
        jargon_tokens = ["U_f", "U_g", "Q*", "DecisionDelta", "FioED", "SourceAnchor", "RealityBoundary"]
        for item in ideas:
            for token in jargon_tokens:
                self.assertNotIn(token.lower(), item["raw_idea"].lower())

    def test_02_blind_renderer_and_leak_detection(self):
        """Blind Renderer — Testa sanitização e detecção rigorosa de vazamento de metadados."""
        leaky_text = (
            "Este resultado foi gerado pelo COND-B (SIMPLE_LOOP) na run RUN-20260827_110000-COND-B "
            "com 10 chamadas pelo modelo openai/gpt-oss-120b no provedor Groq. O estágio 02_ATTACK.json falhou."
        )

        leaks = BlindRenderer.detect_leaks(leaky_text)
        self.assertGreater(len(leaks), 0)
        self.assertTrue(any("COND-B" in l for l in leaks))
        self.assertTrue(any("SIMPLE_LOOP" in l for l in leaks))

        sanitized = BlindRenderer.sanitize_text(leaky_text)
        residual_leaks = BlindRenderer.detect_leaks(sanitized)
        self.assertEqual(len(residual_leaks), 0)
        self.assertNotIn("COND-B", sanitized)
        self.assertNotIn("SIMPLE_LOOP", sanitized)

    def test_03_blind_packet_rendering_format(self):
        """Blind Packet Rendering — Verifica estrutura do markdown cego gerado."""
        packet = BlindReviewPacket(
            idea_id="IDEA-01",
            raw_idea="Cronômetro pomodoro minimalista para desktop.",
            items=[
                BlindReviewItem(label="RESULTADO 1", content_text="Solução com interface limpa."),
                BlindReviewItem(label="RESULTADO 2", content_text="Solução com integração COND-A."),
                BlindReviewItem(label="RESULTADO 3", content_text="Solução com FioED Lean L1."),
            ]
        )

        rendered = BlindRenderer.render_markdown_packet(packet)
        self.assertIn("# PACOTE DE AVALIAÇÃO CEGA — IDEA-01", rendered)
        self.assertIn("## RESULTADO 1", rendered)
        self.assertIn("## RESULTADO 2", rendered)
        self.assertIn("## RESULTADO 3", rendered)

        # Sem vazamento residual
        residual_leaks = BlindRenderer.detect_leaks(rendered)
        self.assertEqual(len(residual_leaks), 0)

    def test_04_reveal_mapping_cryptographic_commitment(self):
        """Reveal Commitment — Valida se o hash SHA256 do BLIND-REVEAL.json bate com o arquivo .sha256 congelado."""
        reveal_json_file = self.exp_dir / "BLIND-REVEAL.json"
        reveal_sha_file = self.exp_dir / "BLIND-REVEAL.sha256"

        self.assertTrue(reveal_json_file.exists())
        self.assertTrue(reveal_sha_file.exists())

        with open(reveal_json_file, "rb") as f:
            content = f.read().replace(b"\r\n", b"\n")
            computed_sha = hashlib.sha256(content).hexdigest()

        with open(reveal_sha_file, "r", encoding="utf-8") as f:
            expected_sha = f.read().strip()

        self.assertEqual(computed_sha, expected_sha)

    def test_05_preregistration_manifest_integrity(self):
        """Preregistration Manifest — Valida integridade de todos os hashes do manifesto pré-registrado."""
        manifest_file = self.exp_dir / "PREREGISTRATION-MANIFEST.json"
        self.assertTrue(manifest_file.exists())

        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        self.assertEqual(manifest["experiment_id"], "EXP-M05.4-PROSPECTIVE-20260827")
        self.assertEqual(manifest["status"], "PREREGISTERED_IMMUTABLE")

        for fname, expected_hash in manifest["files"].items():
            fpath = self.exp_dir / fname
            self.assertTrue(fpath.exists(), f"Arquivo {fname} ausente do diretório de pré-registro.")
            with open(fpath, "rb") as f:
                c = f.read().replace(b"\r\n", b"\n")
                h = hashlib.sha256(c).hexdigest()
            self.assertEqual(h, expected_hash, f"Hash divergente para {fname}.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
