#!/usr/bin/env python3
"""
tools/context/project_status.py
CLI de inspeção instantânea do estado do projeto e da integridade de contexto do IEE.
"""

import sys
import os
import json
import subprocess
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST_PATH = REPO_ROOT / "docs" / "context" / "context-manifest.json"


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
        return "UNKNOWN", "UNKNOWN", "UNKNOWN"


def main():
    if not MANIFEST_PATH.exists():
        print("[FAIL] Erro: Manifesto nao encontrado em docs/context/context-manifest.json")
        sys.exit(1)

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    branch, commit, worktree = get_git_info()

    print("=" * 65)
    print("        IDEA EVOLUTION ENGINE — OPERATIONAL STATUS")
    print("=" * 65)
    print(f"  Project:           {manifest.get('project', 'IEE')}")
    print(f"  Current Phase:     {manifest.get('current_phase', 'UNKNOWN')}")
    print(f"  Next Product:      {manifest.get('next_product_target', 'UNKNOWN')}")
    print(f"  Git State:         branch={branch} | commit={commit} | worktree={worktree}")
    print(f"  Latest Checkpoint: {manifest.get('latest_checkpoint', 'NONE')}")
    print(f"  Active Task:       {manifest.get('current_active_task', 'NONE')}")
    print(f"  Next Action:       {manifest.get('next_authorized_work', 'NONE')}")
    print("=" * 65)

    # Executa validação de integridade
    val_script = REPO_ROOT / "tools" / "context" / "validate_context.py"
    if val_script.exists():
        res = subprocess.run([sys.executable, str(val_script)], capture_output=True, text=True)
        if res.returncode == 0:
            print("  Context Integrity: [OK] 100% VALIDATED (Zero Drift)")
        else:
            print("  Context Integrity: [FAIL] DRIFT / ERRORS DETECTED!")
            print(res.stdout)
    print("=" * 65)


if __name__ == "__main__":
    main()
