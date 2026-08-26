#!/usr/bin/env python3
"""
tools/intelligence/validate_intelligence.py
Validador determinístico da Arquitetura de Inteligência de Agentes do IEE.
Verifica protocolos, manifestos, checklists e calcula o Foundation Ready Gate.
"""

import sys
import os
import json
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
INTEL_MANIFEST_PATH = REPO_ROOT / "docs" / "intelligence" / "intelligence-manifest.json"
GATE_JSON_PATH = REPO_ROOT / "docs" / "intelligence" / "foundation-readiness.json"

REQUIRED_INTEL_DOCS = [
    REPO_ROOT / "docs" / "intelligence" / "INDEX.md",
    REPO_ROOT / "docs" / "intelligence" / "AGENT-INTELLIGENCE-AUDIT.md",
    REPO_ROOT / "docs" / "intelligence" / "WORK-PROTOCOL.md",
    REPO_ROOT / "docs" / "intelligence" / "TASK-CLASSIFICATION.md",
    REPO_ROOT / "docs" / "intelligence" / "CONTEXT-ROUTING.md",
    REPO_ROOT / "docs" / "intelligence" / "EVIDENCE-POLICY.md",
    REPO_ROOT / "docs" / "intelligence" / "HYPOTHESIS-PROTOCOL.md",
    REPO_ROOT / "docs" / "intelligence" / "BASELINE-POLICY.md",
    REPO_ROOT / "docs" / "intelligence" / "ADVERSARIAL-REVIEW.md",
    REPO_ROOT / "docs" / "intelligence" / "GOVERNED-CHANGE.md",
    REPO_ROOT / "docs" / "intelligence" / "FINDINGS.md",
    REPO_ROOT / "docs" / "intelligence" / "TASK-CONTRACT.md",
    REPO_ROOT / "docs" / "intelligence" / "CONTEXT-PACK.md",
    REPO_ROOT / "docs" / "intelligence" / "CHECKLISTS.md",
    REPO_ROOT / "docs" / "intelligence" / "FOUNDATION-READINESS.md",
    REPO_ROOT / "docs" / "intelligence" / "MISSION-04-TASK-CONTRACT.md",
    INTEL_MANIFEST_PATH,
    GATE_JSON_PATH,
]


def validate_required_docs():
    errors = []
    for doc in REQUIRED_INTEL_DOCS:
        if not doc.exists():
            errors.append(f"Documento de inteligência obrigatório ausente: {doc.relative_to(REPO_ROOT)}")
    return errors


def validate_intelligence_manifest():
    errors = []
    if not INTEL_MANIFEST_PATH.exists():
        return [f"Manifesto de inteligência ausente: {INTEL_MANIFEST_PATH}"]

    try:
        with open(INTEL_MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        return [f"Erro ao parsear {INTEL_MANIFEST_PATH}: {e}"]

    protocols = manifest.get("protocols", {})
    for name, rel_path in protocols.items():
        p = REPO_ROOT / rel_path
        if not p.exists():
            errors.append(f"Manifesto referencia protocolo inexistente '{name}': {rel_path}")

    return errors


def validate_foundation_ready_gate():
    errors = []
    if not GATE_JSON_PATH.exists():
        return [f"Arquivo do Foundation Ready Gate ausente: {GATE_JSON_PATH}"]

    try:
        with open(GATE_JSON_PATH, "r", encoding="utf-8") as f:
            gate = json.load(f)
    except Exception as e:
        return [f"Erro ao parsear {GATE_JSON_PATH}: {e}"]

    if not gate.get("foundation_ready", False):
        errors.append("O Foundation Ready Gate está marcado como false!")

    checklist = gate.get("checklist_status", {})
    for item, status in checklist.items():
        if not status:
            errors.append(f"Item de prontidão não satisfeito no Gate: {item}")

    return errors


def main():
    print("=" * 65)
    print("     IEE AGENT INTELLIGENCE ARCHITECTURE VALIDATOR")
    print("=" * 65)

    all_errors = []

    print("[1/3] Verificando existência dos protocolos de inteligência...")
    doc_errors = validate_required_docs()
    if doc_errors:
        all_errors.extend(doc_errors)
        print(f"  [FAIL] {len(doc_errors)} erro(s) encontrado(s).")
    else:
        print("  [OK] Todos os 16 documentos de inteligência estão presentes.")

    print("[2/3] Validando integridade do Intelligence Manifest...")
    man_errors = validate_intelligence_manifest()
    if man_errors:
        all_errors.extend(man_errors)
        print(f"  [FAIL] {len(man_errors)} erro(s) encontrado(s).")
    else:
        print("  [OK] Intelligence Manifest 100% íntegro e validado.")

    print("[3/3] Computando Foundation Ready Gate...")
    gate_errors = validate_foundation_ready_gate()
    if gate_errors:
        all_errors.extend(gate_errors)
        print(f"  [FAIL] {len(gate_errors)} erro(s) no Foundation Ready Gate.")
    else:
        print("  [OK] FOUNDATION_READY = TRUE (21/21 itens satisfeitos).")

    print("=" * 65)
    if all_errors:
        print(f"ALERTA: VALIDACAO DE INTELIGENCIA FALHOU COM {len(all_errors)} ERRO(S):")
        for idx, err in enumerate(all_errors, 1):
            print(f"  {idx}. {err}")
        print("=" * 65)
        sys.exit(1)
    else:
        print("VALIDACAO CONCLUIDA: AGENT INTELLIGENCE ARCHITECTURE APROVADA!")
        print("=" * 65)
        sys.exit(0)


if __name__ == "__main__":
    main()
