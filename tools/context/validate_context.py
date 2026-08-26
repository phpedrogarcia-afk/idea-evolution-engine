#!/usr/bin/env python3
"""
tools/context/validate_context.py
Validador determinístico da arquitetura de contexto e continuidade do IEE.
Executa verificações mecânicas sem uso de LLM.
"""

import sys
import os
import json
import hashlib
from pathlib import Path

# Force UTF-8 on Windows stdout if possible
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST_PATH = REPO_ROOT / "docs" / "context" / "context-manifest.json"

REQUIRED_FILES = [
    REPO_ROOT / "AI-START-HERE.md",
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "README.md",
    REPO_ROOT / "docs" / "INDEX.md",
    REPO_ROOT / "docs" / "SOURCE-OF-TRUTH.md",
    REPO_ROOT / "docs" / "CURRENT-STATE.md",
    REPO_ROOT / "docs" / "GOVERNANCE-INVARIANTS.md",
    REPO_ROOT / "docs" / "DECISIONS-LEDGER.md",
    REPO_ROOT / "docs" / "ACTIVE-QUEUE.md",
    REPO_ROOT / "docs" / "TERMINOLOGY.md",
    REPO_ROOT / "docs" / "TARGET-ARCHITECTURE.md",
    REPO_ROOT / "docs" / "context" / "INDEX.md",
    REPO_ROOT / "docs" / "context" / "CURRENT-STATE.md",
    REPO_ROOT / "docs" / "context" / "CONTINUITY-CAPSULE.md",
    REPO_ROOT / "docs" / "context" / "IMPLEMENTATION-HISTORY.md",
    REPO_ROOT / "docs" / "context" / "ACTIVE-QUEUE.md",
    REPO_ROOT / "docs" / "context" / "DECISIONS-SUMMARY.md",
    REPO_ROOT / "docs" / "context" / "OPEN-QUESTIONS.md",
    REPO_ROOT / "docs" / "context" / "CONTRADICTIONS.md",
    REPO_ROOT / "docs" / "context" / "RESEARCH-BACKLOG.md",
    REPO_ROOT / "docs" / "context" / "REPOSITORY-MAP.md",
    REPO_ROOT / "docs" / "context" / "CONTEXT-PROTOCOL.md",
    REPO_ROOT / "docs" / "context" / "CHECKPOINT-PROTOCOL.md",
    MANIFEST_PATH,
]

CHECKPOINT_REQUIRED_FIELDS = [
    "checkpoint_id",
    "created_at",
    "author",
    "phase",
    "objective",
    "repository",
    "completed_tasks",
    "changed_files",
    "new_decisions",
    "tests_executed",
    "unresolved_questions",
    "known_contradictions",
    "known_risks",
    "blockers",
    "next_exact_action",
    "authorized_next_scope",
    "do_not_repeat",
    "recovery_notes",
]


def calculate_sha256(filepath: Path) -> str:
    """Calcula hash SHA-256 normalizado (tratando CRLF/LF consistentemente)."""
    with open(filepath, "rb") as f:
        content = f.read()
    # Normalize CRLF to LF for deterministic hash computation across platforms
    normalized = content.replace(b"\r\n", b"\n")
    return hashlib.sha256(normalized).hexdigest()


def validate_required_files():
    errors = []
    for req in REQUIRED_FILES:
        if not req.exists():
            errors.append(f"Arquivo obrigatório ausente: {req.relative_to(REPO_ROOT)}")
    return errors


def validate_manifest():
    errors = []
    if not MANIFEST_PATH.exists():
        return [f"Manifesto ausente em {MANIFEST_PATH}"]

    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        return [f"Erro ao parsear {MANIFEST_PATH}: {e}"]

    # Verificar listas de documentos
    for category in ["canonical_documents", "research_documents", "active_specs"]:
        docs = manifest.get(category, [])
        for doc in docs:
            doc_path = REPO_ROOT / doc
            if not doc_path.exists():
                errors.append(f"Manifesto referencia arquivo inexistente em '{category}': {doc}")

    # Verificar hashes
    critical_hashes = manifest.get("critical_file_hashes", {})
    for rel_path, expected_hash in critical_hashes.items():
        doc_path = REPO_ROOT / rel_path
        if not doc_path.exists():
            errors.append(f"Arquivo de hash crítico ausente: {rel_path}")
        else:
            actual_hash = calculate_sha256(doc_path)
            if actual_hash != expected_hash:
                errors.append(
                    f"Hash divergente para {rel_path}! Esperado: {expected_hash}, Atual: {actual_hash}"
                )

    # Verificar latest checkpoint
    latest_cp = manifest.get("latest_checkpoint")
    if latest_cp:
        cp_json = REPO_ROOT / "docs" / "context" / "checkpoints" / f"{latest_cp}.json"
        cp_md = REPO_ROOT / "docs" / "context" / "checkpoints" / f"{latest_cp}.md"
        if not cp_json.exists():
            errors.append(f"Latest checkpoint JSON ausente: {cp_json.relative_to(REPO_ROOT)}")
        if not cp_md.exists():
            errors.append(f"Latest checkpoint MD ausente: {cp_md.relative_to(REPO_ROOT)}")

    return errors


def validate_checkpoints():
    errors = []
    cp_dir = REPO_ROOT / "docs" / "context" / "checkpoints"
    if not cp_dir.exists():
        return [f"Diretório de checkpoints ausente: {cp_dir}"]

    json_files = list(cp_dir.glob("*.json"))
    if not json_files:
        errors.append("Nenhum checkpoint JSON encontrado no diretório de checkpoints.")

    for cp_file in json_files:
        try:
            with open(cp_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for field in CHECKPOINT_REQUIRED_FIELDS:
                if field not in data:
                    errors.append(f"Campo obrigatório '{field}' ausente no checkpoint {cp_file.name}")
        except Exception as e:
            errors.append(f"Erro ao ler checkpoint {cp_file.name}: {e}")

    return errors


def validate_phase_consistency():
    errors = []
    if not MANIFEST_PATH.exists():
        return []

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    manifest_phase = manifest.get("current_phase")

    # Checar AI-START-HERE
    start_path = REPO_ROOT / "AI-START-HERE.md"
    if start_path.exists():
        content = start_path.read_text(encoding="utf-8")
        if "FASE 0" not in content and manifest_phase == "FASE_0_FOUNDATION":
            errors.append("AI-START-HERE.md inconsistente com a Fase 0 declarada no manifest.")

    # Checar CURRENT-STATE
    curr_path = REPO_ROOT / "docs" / "context" / "CURRENT-STATE.md"
    if curr_path.exists():
        content = curr_path.read_text(encoding="utf-8")
        if "FASE 0" not in content and manifest_phase == "FASE_0_FOUNDATION":
            errors.append("docs/context/CURRENT-STATE.md inconsistente com a Fase 0 declarada no manifest.")
        if "SIMPLE IDEA EVOLUTION LOOP" not in content:
            errors.append("docs/context/CURRENT-STATE.md não declara o Simple Idea Evolution Loop como próximo produto.")

    return errors


def main():
    print("=" * 60)
    print("   IEE DETERMINISTIC CONTEXT VALIDATOR")
    print("=" * 60)

    all_errors = []
    
    print("[1/4] Verificando existencia de arquivos obrigatorios...")
    req_errors = validate_required_files()
    if req_errors:
        all_errors.extend(req_errors)
        print(f"  [FAIL] {len(req_errors)} erro(s) encontrado(s).")
    else:
        print("  [OK] Todos os arquivos obrigatorios estao presentes.")

    print("[2/4] Validando integridade do Manifesto de Contexto e Hashes...")
    man_errors = validate_manifest()
    if man_errors:
        all_errors.extend(man_errors)
        print(f"  [FAIL] {len(man_errors)} erro(s) encontrado(s).")
    else:
        print("  [OK] Manifesto e hashes de arquivos criticos validos.")

    print("[3/4] Validando conformidade estrutural de Checkpoints...")
    cp_errors = validate_checkpoints()
    if cp_errors:
        all_errors.extend(cp_errors)
        print(f"  [FAIL] {len(cp_errors)} erro(s) encontrado(s).")
    else:
        print("  [OK] Todos os checkpoints estao integros e em conformidade.")

    print("[4/4] Validando consistencia de fases e alvos de produto...")
    phase_errors = validate_phase_consistency()
    if phase_errors:
        all_errors.extend(phase_errors)
        print(f"  [FAIL] {len(phase_errors)} erro(s) encontrado(s).")
    else:
        print("  [OK] Consistencia de fases e alvos verificada com sucesso.")

    print("=" * 60)
    if all_errors:
        print(f"ALERTA: VALIDACAO FALHOU COM {len(all_errors)} ERRO(S):")
        for idx, err in enumerate(all_errors, 1):
            print(f"  {idx}. {err}")
        print("=" * 60)
        sys.exit(1)
    else:
        print("VALIDACAO CONCLUIDA COM SUCESSO: REPOSITORIO 100% INTEGRO!")
        print("=" * 60)
        sys.exit(0)


if __name__ == "__main__":
    main()
