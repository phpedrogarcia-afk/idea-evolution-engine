#!/usr/bin/env python3
"""
tools/experiments/execute_m05_5r1.py
Executor do experimento de replicação controlada M05.5R1 com integridade reforçada.

Architectural Invariant:
  EXECUTION_PLANE_HAS_NO_BLIND_KNOWLEDGE = True

Responsabilidades:
  1. Guardião de Imutabilidade da Tentativa (Attempt Immutability Guard).
  2. Portão de Prontidão de Cota do Provedor (Provider Quota Readiness Gate).
  3. Validar conformidade de provedor (groq) e modelo (openai/gpt-oss-120b).
  4. Executar as 24 células sequencialmente.
"""

from __future__ import annotations
import os
import sys
import json
import time
import hashlib
import requests
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Flush stdout immediately
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.idea_evolution.providers.native import NativeModelRunner
from src.idea_evolution.orchestration.baseline import BaselineRunner
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.orchestration.lean_loop import LeanLoopRunner

EXP_DIR = REPO_ROOT / "experiments" / "EXP-M05.5R1-CONTROLLED-REPLICATION-20260901"
ATTEMPT_DIR = EXP_DIR / "REAL-EXECUTION-ATTEMPT-001"
RAW_DIR = ATTEMPT_DIR / "raw"
LOCK_FILE = ATTEMPT_DIR / ".attempt_immutability_lock"

EXPECTED_PROVIDER = "groq"
EXPECTED_MODEL = "openai/gpt-oss-120b"
EXPERIMENT_ID = "EXP-M05.5R1-CONTROLLED-REPLICATION-20260901"
ATTEMPT_ID = "REAL-EXECUTION-ATTEMPT-001"

def enforce_immutability_guard():
    if LOCK_FILE.exists():
        raise RuntimeError("ATTEMPT_IMMUTABILITY_GUARD: Este ATTEMPT_ID já foi iniciado e é imutável. Abortando nova execução.")
    
    if RAW_DIR.exists() and list(RAW_DIR.glob("*.json")):
        raise RuntimeError("ATTEMPT_IMMUTABILITY_GUARD: O diretório contém arquivos brutos, mas não possui lock. Abortando para evitar sobrescrita.")

def create_immutability_lock():
    ATTEMPT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    
    lock_data = {
        "experiment_id": EXPERIMENT_ID,
        "attempt_id": ATTEMPT_ID,
        "start_timestamp": datetime.utcnow().isoformat() + "Z",
        "start_head": os.popen("git rev-parse HEAD").read().strip(),
        "freeze_manifest_sha": "TODO_POST_FREEZE"
    }
    LOCK_FILE.write_text(json.dumps(lock_data, indent=2))

def provider_quota_readiness_gate(api_key: str):
    print("Executando PROVIDER_QUOTA_READINESS_GATE...", flush=True)
    res = requests.post(
        'https://api.groq.com/openai/v1/chat/completions',
        headers={'Authorization': f'Bearer {api_key}'},
        json={'model': EXPECTED_MODEL, 'messages': [{'role': 'user', 'content': 'INFRASTRUCTURE_QUOTA_PROBE'}]}
    )
    if res.status_code != 200:
        raise RuntimeError(f"QUOTA_GATE_FAILED: Falha na sonda. {res.text}")
    
    remaining = res.headers.get('x-ratelimit-remaining-tokens')
    if remaining:
        print(f"QUOTA_GATE_PASS: Sonda confirmada. (Tokens limit: {remaining})")
    else:
        print("QUOTA_GATE_PASS: Sonda confirmada (Headers de limite não disponíveis na resposta).")

def execute_replication(api_key: Optional[str] = None):
    key = api_key or os.environ.get("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY_MISSING")

    enforce_immutability_guard()
    provider_quota_readiness_gate(key)
    create_immutability_lock()
    print("Immutability lock created. Execution stub finished.")

if __name__ == "__main__":
    try:
        # execute_replication() is intentionally skipped during tests to avoid real API calls
        print("M05.5R1 Execute Stub Loaded")
    except Exception as e:
        print(f"FATAL: {e}")
        sys.exit(1)
