#!/usr/bin/env python3
"""
tests/continuity/test_continuity.py
Suíte de testes adversariais da infraestrutura de continuidade cognitiva do IEE.
Verifica se uma nova IA consegue navegar, recuperar estado e evitar armadilhas de contexto.
"""

import sys
import os
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST_PATH = REPO_ROOT / "docs" / "context" / "context-manifest.json"


class TestContinuityHardening(unittest.TestCase):

    def test_01_fresh_ai_entry(self):
        """TEST 1: Fresh AI — AI-START-HERE.md fornece orientação inequívoca."""
        start_doc = REPO_ROOT / "AI-START-HERE.md"
        self.assertTrue(start_doc.exists(), "AI-START-HERE.md deve existir.")
        content = start_doc.read_text(encoding="utf-8")
        
        self.assertIn("Idea Evolution Engine", content)
        self.assertIn("FASE 0", content)
        self.assertIn("SIMPLE IDEA EVOLUTION LOOP", content)
        self.assertIn("FAST ENTRY", content)
        self.assertIn("Progress over prose", content)
        self.assertIn("Capability != Authority", content)

    def test_02_interrupted_work_recovery(self):
        """TEST 2: Interrupted Work — Nova IA recupera tarefa ativa e próximo passo sem perda."""
        curr_state = REPO_ROOT / "docs" / "context" / "CURRENT-STATE.md"
        self.assertTrue(curr_state.exists())
        content = curr_state.read_text(encoding="utf-8")
        
        self.assertIn("Último Checkpoint Imutável", content)
        self.assertIn("Tarefa Ativa Atual", content)
        self.assertIn("Próximo Passo Exato", content)
        self.assertIn("DO-NOT-DO", content)

    def test_03_target_trap(self):
        """TEST 3: Target Trap — Documentos em docs/architecture/ são marcados como TARGET e não CURRENT."""
        arch_docs = list((REPO_ROOT / "docs" / "architecture").glob("*.md"))
        self.assertGreater(len(arch_docs), 0)
        
        for doc in arch_docs:
            content = doc.read_text(encoding="utf-8")
            self.assertTrue(
                "TARGET" in content or "DESIGN_HYPOTHESIS" in content,
                f"Documento de arquitetura {doc.name} deve ser explicitamente marcado como TARGET/DESIGN_HYPOTHESIS."
            )

    def test_04_research_trap(self):
        """TEST 4: Research Trap — Documentos em docs/research/ são marcados como RESEARCH/DOADORES e não implementação."""
        donor_docs = list((REPO_ROOT / "docs" / "research" / "donors").glob("*.md"))
        self.assertGreater(len(donor_docs), 0)
        
        for doc in donor_docs:
            content = doc.read_text(encoding="utf-8")
            self.assertTrue(
                "AUTÓPSIA" in content or "STATUS:" in content or "Level" in content,
                f"Documento de doador {doc.name} deve conter metadados explícitos de autópsia/status."
            )

    def test_05_conflict_detection_and_fail_closed(self):
        """TEST 5: Conflict Detection — Verificação de que contradições são mapeadas e não suavizadas."""
        contra_doc = REPO_ROOT / "docs" / "context" / "CONTRADICTIONS.md"
        self.assertTrue(contra_doc.exists())
        content = contra_doc.read_text(encoding="utf-8")
        
        self.assertIn("CON-001", content)
        self.assertIn("Source A", content)
        self.assertIn("Source B", content)
        self.assertIn("Type", content)

    def test_06_checkpoint_integrity(self):
        """TEST 6: Checkpoint Integrity — O latest checkpoint existe em MD e JSON com campos válidos."""
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        
        latest_cp = manifest.get("latest_checkpoint")
        self.assertIsNotNone(latest_cp)
        
        cp_json = REPO_ROOT / "docs" / "context" / "checkpoints" / f"{latest_cp}.json"
        cp_md = REPO_ROOT / "docs" / "context" / "checkpoints" / f"{latest_cp}.md"
        
        self.assertTrue(cp_json.exists(), f"Arquivo {cp_json} deve existir.")
        self.assertTrue(cp_md.exists(), f"Arquivo {cp_md} deve existir.")
        
        with open(cp_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.assertEqual(data["checkpoint_id"], latest_cp)
        self.assertIn("repository", data)
        self.assertIn("next_exact_action", data)

    def test_07_simple_mvp_recognition(self):
        """TEST 7: Simple MVP Recognition — Reconhece que o próximo produto pretendido é o Simple Loop e não o DCE completo."""
        curr_state = REPO_ROOT / "docs" / "context" / "CURRENT-STATE.md"
        content = curr_state.read_text(encoding="utf-8")
        self.assertIn("SIMPLE IDEA EVOLUTION LOOP", content)
        self.assertIn("MVP Heurístico", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
