#!/usr/bin/env python3
"""
tests/intelligence/test_intelligence.py
Suíte de testes adversariais da Arquitetura de Inteligência de Agentes do IEE.
Verifica se as armadilhas cognitivas comuns de LLMs são devidamente bloqueadas pelas regras e protocolos.
"""

import sys
import os
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
INTEL_DIR = REPO_ROOT / "docs" / "intelligence"


class TestAgentIntelligenceArchitecture(unittest.TestCase):

    def test_01_build_trap_blocked(self):
        """TEST 1: Build Trap — O protocolo proíbe código prematuro antes de orientação e enquadramento."""
        work_proto = (INTEL_DIR / "WORK-PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn("ORIENT", work_proto)
        self.assertIn("CLASSIFY", work_proto)
        self.assertIn("HYPOTHESIZE", work_proto)
        # Verifica se a etapa ACT ocorre apenas após ORIENT, CLASSIFY, FRAME, RECON, HYPOTHESIZE, ATTACK, PLAN
        orient_idx = work_proto.find("[1. ORIENT]")
        act_idx = work_proto.find("[8. ACT]")
        self.assertLess(orient_idx, act_idx, "ACT deve ocorrer estritamente após etapas de orientação e ataque de hipóteses.")

    def test_02_donor_trap_blocked(self):
        """TEST 2: Donor Trap — Proíbe adoção de doador externo sem gap receptor explícito."""
        donor_method = (REPO_ROOT / "docs" / "research" / "DONOR-AUTOPSY-METHOD.md").read_text(encoding="utf-8")
        self.assertIn("GAP RECEPTOR NOSSO", donor_method)
        self.assertIn("turismo tecnológico", donor_method)

    def test_03_evidence_trap_blocked(self):
        """TEST 3: Evidence Trap — Modelos não são fontes independentes; repetição de IA != mais evidência."""
        evidence_policy = (INTEL_DIR / "EVIDENCE-POLICY.md").read_text(encoding="utf-8")
        self.assertIn("Modelo Não É Fonte Independente", evidence_policy)
        self.assertIn("Três modelos de IA concordando", evidence_policy)

    def test_04_baseline_trap_blocked(self):
        """TEST 4: Baseline Trap — Nenhuma alegação de melhoria é aceita sem baseline de medição anterior."""
        baseline_policy = (INTEL_DIR / "BASELINE-POLICY.md").read_text(encoding="utf-8")
        self.assertIn("BASELINE_REQUIRED", baseline_policy)
        self.assertIn("Sem medição anterior", baseline_policy)

    def test_05_authority_trap_blocked(self):
        """TEST 5: Authority Trap — Declaração 'actor: human' em payload não confere autoridade sem ExecutionContext."""
        auth_doc = (REPO_ROOT / "docs" / "specs" / "AUTHORITY-MATRIX-v0.1.md").read_text(encoding="utf-8")
        self.assertIn("Capability != Authority", auth_doc)
        self.assertIn("ExecutionContext", auth_doc)

    def test_06_research_trap_blocked(self):
        """TEST 6: Research Trap — Papers ou pesquisas teóricas não viram fatos estabelecidos por repetição."""
        evidence_policy = (INTEL_DIR / "EVIDENCE-POLICY.md").read_text(encoding="utf-8")
        self.assertIn("SOURCE_CLAIM", evidence_policy)
        self.assertIn("MODEL_INFERENCE", evidence_policy)
        self.assertIn("SPECULATION", evidence_policy)

    def test_07_failure_trap_blocked(self):
        """TEST 7: Failure Trap — Falhas devem gerar reprodução e testes de regressão antes de virar memória."""
        hyp_doc = (INTEL_DIR / "HYPOTHESIS-PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn("REPRODUCTION", hyp_doc)
        self.assertIn("FAILING TEST", hyp_doc)
        self.assertIn("REGRESSION TEST", hyp_doc)

    def test_08_complexity_trap_blocked(self):
        """TEST 8: Complexity Trap — Exige Simplicity Challenge para vetar arquiteturas ornamentais."""
        work_proto = (INTEL_DIR / "WORK-PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn("Simplicity Challenge", work_proto)

    def test_09_repetition_trap_blocked(self):
        """TEST 9: Repetition Trap — Exige verificação no repositório antes de propor novos componentes."""
        work_proto = (INTEL_DIR / "WORK-PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn("Don't Reinvent Check", work_proto)

    def test_10_stop_trap_blocked(self):
        """TEST 10: Stop Trap — Permite encerramento válido com NO_USEFUL_WORK_FOUND se nada for descoberto."""
        work_proto = (INTEL_DIR / "WORK-PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn("NO_USEFUL_WORK_FOUND", work_proto)


if __name__ == "__main__":
    unittest.main(verbosity=2)
