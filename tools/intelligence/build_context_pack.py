#!/usr/bin/env python3
"""
tools/intelligence/build_context_pack.py
Montador determinístico de ContextPacks por perfil de tarefa.
Gera contexto mínimo suficiente sem uso de IA.
"""

import sys
import os
import json
import argparse
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

PROFILES = {
    "fast": [
        "AI-START-HERE.md",
        "docs/context/CURRENT-STATE.md",
        "docs/context/ACTIVE-QUEUE.md",
    ],
    "deep": [
        "AI-START-HERE.md",
        "docs/context/CURRENT-STATE.md",
        "docs/context/ACTIVE-QUEUE.md",
        "docs/GOVERNANCE-INVARIANTS.md",
        "docs/context/CONTINUITY-CAPSULE.md",
        "docs/TARGET-ARCHITECTURE.md",
    ],
    "research": [
        "AI-START-HERE.md",
        "docs/context/CURRENT-STATE.md",
        "docs/context/ACTIVE-QUEUE.md",
        "docs/research/DONOR-INDEX.md",
        "docs/research/DONOR-AUTOPSY-METHOD.md",
        "docs/context/RESEARCH-BACKLOG.md",
    ],
    "implementation": [
        "AI-START-HERE.md",
        "docs/context/CURRENT-STATE.md",
        "docs/context/ACTIVE-QUEUE.md",
        "docs/context/CONTINUITY-CAPSULE.md",
        "docs/intelligence/WORK-PROTOCOL.md",
    ],
}


def build_pack(profile_name: str, task_id: str = "TASK-AUTO"):
    profile_name = profile_name.lower()
    if profile_name not in PROFILES:
        print(f"[FAIL] Perfil desconhecido '{profile_name}'. Opções: {list(PROFILES.keys())}")
        sys.exit(1)

    files = PROFILES[profile_name]
    pack = {
        "pack_id": f"CPACK-{task_id}",
        "profile": profile_name,
        "document_count": len(files),
        "documents": {},
    }

    for rel_path in files:
        p = REPO_ROOT / rel_path
        if p.exists():
            pack["documents"][rel_path] = p.read_text(encoding="utf-8")
        else:
            pack["documents"][rel_path] = f"[ERROR: File not found {rel_path}]"

    return pack


def main():
    parser = argparse.ArgumentParser(description="IEE Context Pack Builder")
    parser.add_argument(
        "--profile",
        choices=["fast", "deep", "research", "implementation"],
        default="fast",
        help="Perfil de contexto desejado",
    )
    parser.add_argument("--task-id", default="TASK-AUTO", help="ID da tarefa")
    parser.add_argument("--format", choices=["json", "summary"], default="summary")

    args = parser.parse_args()
    pack = build_pack(args.profile, args.task_id)

    if args.format == "json":
        print(json.dumps(pack, indent=2, ensure_ascii=False))
    else:
        print("=" * 60)
        print(f"   CONTEXT PACK: {pack['pack_id']} (Profile: {pack['profile'].upper()})")
        print("=" * 60)
        print(f"Documentos Incluídos ({pack['document_count']}):")
        for doc in pack["documents"].keys():
            print(f"  - {doc}")
        print("=" * 60)


if __name__ == "__main__":
    main()
