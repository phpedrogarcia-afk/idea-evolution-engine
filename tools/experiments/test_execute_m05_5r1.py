#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
EXP_DIR = REPO_ROOT / "experiments" / "EXP-M05.5R1-CONTROLLED-REPLICATION-20260901"
ATTEMPT_DIR = EXP_DIR / "REAL-EXECUTION-ATTEMPT-001"
RAW_DIR = ATTEMPT_DIR / "raw"
LOCK_FILE = ATTEMPT_DIR / ".attempt_immutability_lock"

sys.path.insert(0, str(REPO_ROOT))
from tools.experiments.execute_m05_5r1 import enforce_immutability_guard, create_immutability_lock

def test_immutability_guard():
    print("Running attempt immutability tests...")
    
    # 1. Clean state
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
    if RAW_DIR.exists():
        for f in RAW_DIR.glob("*.json"):
            f.unlink()
            
    # Should pass
    enforce_immutability_guard()
    print("PASS: Clean state")
    
    # 2. Lock exists
    create_immutability_lock()
    try:
        enforce_immutability_guard()
        print("FAIL: Did not block when lock exists")
        sys.exit(1)
    except RuntimeError as e:
        if "já foi iniciado e é imutável" in str(e):
            print("PASS: Blocks when lock exists")
        else:
            print(f"FAIL: Wrong error message: {e}")
            sys.exit(1)
            
    # 3. No lock but raw files exist
    LOCK_FILE.unlink()
    (RAW_DIR / "test.json").write_text("{}")
    try:
        enforce_immutability_guard()
        print("FAIL: Did not block when raw files exist without lock")
        sys.exit(1)
    except RuntimeError as e:
        if "contém arquivos brutos, mas não possui lock" in str(e):
            print("PASS: Blocks when raw files exist without lock")
        else:
            print(f"FAIL: Wrong error message: {e}")
            sys.exit(1)
            
    # Cleanup
    (RAW_DIR / "test.json").unlink()
    print("All tests passed.")

if __name__ == "__main__":
    test_immutability_guard()
