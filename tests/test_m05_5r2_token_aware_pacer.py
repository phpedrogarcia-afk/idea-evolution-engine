"""
tests/test_m05_5r2_token_aware_pacer.py
Testes unitários offline para o token-aware pacer e componentes do runner confirmatório M05.5R2.

Zero chamadas ao modelo.
Zero chamadas de rede.
"""

import time
from pathlib import Path
import pytest

from tools.experiments.execute_m05_5r2_confirmatory import (
    AppendOnlyUsageLedger,
    TokenAwarePacer,
    SAFE_RPM_BUDGET,
    SAFE_TPM_BUDGET,
    run_preflight_verification,
)


def test_token_aware_pacer_cadence_and_window(tmp_path):
    ledger_path = tmp_path / "test-ledger.jsonl"
    ledger = AppendOnlyUsageLedger(ledger_path)

    pacer = TokenAwarePacer(
        ledger=ledger,
        safe_rpm=4,
        safe_tpm=27000,
        min_cadence_seconds=0.1,  # Reduzido para teste rápido
    )

    # 1. Primeiro despacho: imediato
    t0 = time.time()
    pacer.wait_if_needed(reserved_tokens=5000, request_id="req1", cell_id="cell1")
    pacer.record_dispatch(reserved_tokens=5000)
    assert len(pacer.dispatches) == 1

    # 2. Despacho rápido: deve esperar pelo menos min_cadence
    pacer.wait_if_needed(reserved_tokens=5000, request_id="req2", cell_id="cell1")
    pacer.record_dispatch(reserved_tokens=5000)
    assert len(pacer.dispatches) == 2
    assert time.time() - t0 >= 0.1

    # 3. Teste de pruning após 60 segundos
    now = time.time()
    pacer.dispatches.append((now - 65.0, 10000))
    assert len(pacer.dispatches) == 3
    pacer.prune(now)
    assert len(pacer.dispatches) == 2  # A entrada de 65s atrás foi podada


def test_m05_5r2_preflight_verification_passes():
    holdout_map, schedule = run_preflight_verification()
    assert len(holdout_map) == 8
    assert len(schedule) == 24
    assert set(holdout_map.keys()) == {f"H0{i}" for i in range(1, 9)}
