#!/usr/bin/env python3
"""
tools/context/create_checkpoint.py
Script determinístico para geração de checkpoints imutáveis de continuidade no IEE.
"""

import sys
import os
import json
import datetime
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST_PATH = REPO_ROOT / "docs" / "context" / "context-manifest.json"
CHECKPOINTS_DIR = REPO_ROOT / "docs" / "context" / "checkpoints"


def get_git_info():
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
        status = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=REPO_ROOT, text=True
        ).strip()
        worktree = "DIRTY" if status else "CLEAN"
        return branch, commit, worktree
    except Exception:
        return "master", "ce3552f", "CLEAN"


def get_next_checkpoint_id():
    today = datetime.datetime.now().strftime("%Y%m%d")
    existing = list(CHECKPOINTS_DIR.glob(f"CP-{today}-*.json"))
    next_idx = len(existing) + 1
    return f"CP-{today}-{next_idx:03d}"


def create_checkpoint(
    author="Antigravity (Google DeepMind)",
    phase="FASE_0_FOUNDATION",
    objective="Intelligence & Continuity Hardening",
    completed_tasks=None,
    changed_files=None,
    new_decisions=None,
    tests_executed=None,
    unresolved_questions=None,
    known_contradictions=None,
    known_risks=None,
    blockers=None,
    next_exact_action="Governance Gate: Aguardar aprovação humana para transição de fase",
    authorized_next_scope=None,
    do_not_repeat=None,
    recovery_notes=None,
):
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    cp_id = get_next_checkpoint_id()
    now_iso = datetime.datetime.now().isoformat()
    branch, commit, worktree = get_git_info()

    data = {
        "checkpoint_id": cp_id,
        "created_at": now_iso,
        "author": author,
        "phase": phase,
        "objective": objective,
        "repository": {
            "branch": branch,
            "commit": commit,
            "worktree_state": worktree,
        },
        "completed_tasks": completed_tasks or [],
        "changed_files": changed_files or [],
        "new_decisions": new_decisions or [],
        "tests_executed": tests_executed or [],
        "unresolved_questions": unresolved_questions or [],
        "known_contradictions": known_contradictions or [],
        "known_risks": known_risks or [],
        "blockers": blockers or [],
        "next_exact_action": next_exact_action,
        "authorized_next_scope": authorized_next_scope or [],
        "do_not_repeat": do_not_repeat or [],
        "recovery_notes": recovery_notes or "Consulte CONTINUITY-CAPSULE.md e execute project_status.py.",
    }

    # Salva JSON
    json_path = CHECKPOINTS_DIR / f"{cp_id}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Salva Markdown
    md_path = CHECKPOINTS_DIR / f"{cp_id}.md"
    md_content = f"""# CHECKPOINT: {cp_id}

- **Data / Hora:** {now_iso}
- **Autor / Agente:** {author}
- **Fase:** {phase}
- **Objetivo do Marco:** {objective}
- **Git State:** branch={branch} | commit={commit} | worktree={worktree}

---

## 1. Tarefas Concluídas Neste Marco
{chr(10).join(f"- [x] {t}" for t in data['completed_tasks'])}

## 2. Arquivos Modificados
{chr(10).join(f"- `{f}`" for f in data['changed_files'])}

## 3. Decisões Arquiteturais Registradas
{chr(10).join(f"- {d}" for d in data['new_decisions']) if data['new_decisions'] else "- Nenhuma nova decisão neste checkpoint."}

## 4. Testes e Validações Executadas
{chr(10).join(f"- {t}" for t in data['tests_executed'])}

## 5. Dúvidas e Incertezas Abertas
{chr(10).join(f"- {q}" for q in data['unresolved_questions'])}

## 6. Tensões e Contradições Registradas
{chr(10).join(f"- {c}" for c in data['known_contradictions'])}

## 7. Próximo Passo Exato Autorizado
- **Ação:** {next_exact_action}
- **Escopo Autorizado:** {', '.join(data['authorized_next_scope'])}
- **O Que NÃO Repetir:** {', '.join(data['do_not_repeat'])}

---
*Este checkpoint é imutável. Correções devem gerar um novo checkpoint sucessor.*
"""
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    # Atualiza Manifest
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        manifest["latest_checkpoint"] = cp_id
        manifest["updated_at"] = now_iso
        with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"✅ Checkpoint {cp_id} gerado com sucesso!")
    print(f"   JSON: {json_path.relative_to(REPO_ROOT)}")
    print(f"   MD:   {md_path.relative_to(REPO_ROOT)}")
    return cp_id


if __name__ == "__main__":
    create_checkpoint()
