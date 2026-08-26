#!/usr/bin/env python3
"""
tests/doctrine/test_constitutional_doctrine.py
Suíte de testes adversariais de institucionalização da Constituição Mestra de Construção (v1.0) no IEE.
"""

import sys
import os
import json
import hashlib
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DOCTRINE_DIR = REPO_ROOT / "docs" / "doctrine"
RAW_CONSTITUTION_PATH = DOCTRINE_DIR / "source" / "CONSTRUCTION-CONSTITUTION-v1.0.md"
EXPECTED_CONSTITUTION_SHA256 = "5337f466a6f6e450ab4c517a8d43b642fcf6b713d75095c878b71a0417e77468"


class TestConstitutionalDoctrine(unittest.TestCase):

    def test_01_doctrine_source_and_hash_fidelity(self):
        """TEST 1: Doctrine Drift — A fonte original existe e possui hash exato."""
        self.assertTrue(RAW_CONSTITUTION_PATH.exists(), "A fonte original da Constituição deve existir.")
        content = RAW_CONSTITUTION_PATH.read_bytes().replace(b"\r\n", b"\n")
        actual_hash = hashlib.sha256(content).hexdigest()
        self.assertEqual(
            actual_hash,
            EXPECTED_CONSTITUTION_SHA256,
            f"O hash da Constituição v1.0 divergiu! Esperado: {EXPECTED_CONSTITUTION_SHA256}, Obtido: {actual_hash}",
        )

        # Verificar se a Operating Doctrine aponta para a fonte com o hash correto
        op_doctrine = (DOCTRINE_DIR / "OPERATING-DOCTRINE.md").read_text(encoding="utf-8")
        self.assertIn(EXPECTED_CONSTITUTION_SHA256, op_doctrine)
        self.assertIn("v1.0", op_doctrine)

    def test_02_foundation_reopen_trap(self):
        """TEST 2: Foundation Reopen Trap — A constituição não autoriza Foundation 04."""
        gate_path = REPO_ROOT / "docs" / "intelligence" / "foundation-readiness.json"
        self.assertTrue(gate_path.exists())
        with open(gate_path, "r", encoding="utf-8") as f:
            gate = json.load(f)
        self.assertTrue(gate.get("foundation_ready", False))

        decisions = (REPO_ROOT / "docs" / "DECISIONS-LEDGER.md").read_text(encoding="utf-8")
        self.assertIn("ADR-012", decisions)
        self.assertIn("Proibição de Missões de Fundação por Inércia", decisions)

    def test_03_fioos_contamination_blocked(self):
        """TEST 3: FioOS Contamination — Mecanismos de kernel FioOS não contaminam o contrato do MVP."""
        matrix_path = DOCTRINE_DIR / "CONSTITUTION-APPLICABILITY-MATRIX.md"
        self.assertTrue(matrix_path.exists())
        matrix = matrix_path.read_text(encoding="utf-8")
        self.assertIn("FIOOS_SPECIFIC", matrix)
        self.assertIn("Isolado no FioOS", matrix)

        mvp_contract = (REPO_ROOT / "docs" / "intelligence" / "MISSION-04-TASK-CONTRACT.md").read_text(encoding="utf-8")
        self.assertNotIn("workload identity", mvp_contract.lower())
        self.assertNotIn("hypervisor", mvp_contract.lower())
        self.assertIn("FioOS", mvp_contract)

    def test_04_no_duplicate_canonical_owners(self):
        """TEST 4: Documentation Duplication — Conceitos possuem uma única casa canônica declarada."""
        op_doctrine = (DOCTRINE_DIR / "OPERATING-DOCTRINE.md").read_text(encoding="utf-8")
        self.assertIn("Pointers > Duplication", op_doctrine)
        self.assertIn("WORK-PROTOCOL.md", op_doctrine)
        self.assertIn("EVIDENCE-POLICY.md", op_doctrine)
        self.assertIn("BASELINE-POLICY.md", op_doctrine)
        self.assertIn("TASK-CONTRACT.md", op_doctrine)

    def test_05_anti_circle_task_contract(self):
        """TEST 5: Anti-Circle Rule — TaskContract exige target_uncertainty e target_decision."""
        contract_spec = (REPO_ROOT / "docs" / "intelligence" / "TASK-CONTRACT.md").read_text(encoding="utf-8")
        self.assertIn("target_uncertainty", contract_spec)
        self.assertIn("target_decision", contract_spec)
        self.assertIn("Anti-Circle Rule", contract_spec)

        mvp_contract = (REPO_ROOT / "docs" / "intelligence" / "MISSION-04-TASK-CONTRACT.md").read_text(encoding="utf-8")
        self.assertIn("target_uncertainty", mvp_contract)
        self.assertIn("target_decision", mvp_contract)

    def test_06_stop_condition_required(self):
        """TEST 6: Stop Condition — Toda missão deve declarar stop_condition inequívoca."""
        contract_spec = (REPO_ROOT / "docs" / "intelligence" / "TASK-CONTRACT.md").read_text(encoding="utf-8")
        self.assertIn("stop_condition", contract_spec)

        mvp_contract = (REPO_ROOT / "docs" / "intelligence" / "MISSION-04-TASK-CONTRACT.md").read_text(encoding="utf-8")
        self.assertIn("Condição de Parada (Stop Condition)", mvp_contract)

    def test_07_research_and_doctrine_not_authority(self):
        """TEST 7: Research != Authority — A Constituição e doadores não conferem autoridade operacional direta."""
        auth_doc = (REPO_ROOT / "docs" / "specs" / "AUTHORITY-MATRIX-v0.1.md").read_text(encoding="utf-8")
        self.assertIn("Capability != Authority", auth_doc)

        op_doctrine = (DOCTRINE_DIR / "OPERATING-DOCTRINE.md").read_text(encoding="utf-8")
        self.assertIn("Capability", op_doctrine)
        self.assertIn("Permission", op_doctrine)
        self.assertIn("Authority", op_doctrine)


if __name__ == "__main__":
    unittest.main(verbosity=2)
