# REAL-EXECUTION-ATTEMPT-002-PREFLIGHT.md

## 1. Attempt Identity & Status

| Field | Value |
|---|---|
| EXPERIMENT_ID | EXP-M05.4-PROSPECTIVE-RERUN-20260829 |
| ATTEMPT_ID | REAL-EXECUTION-ATTEMPT-002 |
| STATUS | FROZEN_NOT_EXECUTED |
| REAL_PROVIDER_CALLS | 0 |
| HUMAN_REVIEW_STARTED | NO |
| ATTEMPT_001_OUTPUTS_REUSED | NO |
| BLINDING_REVISION | 3 |
| BLIND_COMMITMENT_SHA256 | b2e271ff9dd35a8215c067d1e545f84dfa8add7f33335a69845ebd8d5ed82cf3 |
| BLIND_STATUS | SEALED_OUTSIDE_REPOSITORY |
| SEALED_REVEAL_LOCATION | C:\Users\phped\.fioideias\sealed\EXP-M05.4-PROSPECTIVE-RERUN-20260829\BLIND-REVEAL-REV3.json |

---

## 2. Mechanical Start Gates (Self-Enforcing)

1. **Gate 1 — Self-Enforcing Freeze Validation:**
   - Git worktree clean verification (git status --porcelain). Dirty worktree raises DIRTY_WORKTREE_EXECUTION_FORBIDDEN.
   - Freeze manifest (RERUN-FREEZE-MANIFEST.json) hash verification across 21 execution-critical files.
   - Blind commitment verification (BLIND-REVEAL.sha256 == Rev 3 commitment).

2. **Gate 2 — Single-Use Attempt Namespace:**
   - Attempt directory cannot contain existing receipts, manifests, or raw outputs (ATTEMPT_ALREADY_STARTED).

3. **Gate 3 — Frozen Manifest Cells Validation:**
   - Exactly 24 cells (8 A / 8 B / 8 C), unique cell IDs, unique (idea, condition) pairs.
   - All ideas exist in frozen holdout, all providers == groq, all models == openai/gpt-oss-120b.

4. **Gate 4 — Provider & Model Guards:**
   - NativeModelRunner validated preflight against groq / openai/gpt-oss-120b.

5. **Gate 5 — Start Receipt Created ONLY After Gates Pass:**
   - REAL-EXECUTION-START-RECEIPT.json generated post-validation, pre-loop.

---

## 3. Architectural Separation Invariants

1. **Execution Plane Isolation (xecute_m05_4_frozen.py):**
   - EXECUTION_PLANE_HAS_NO_BLIND_KNOWLEDGE = True (PROVEN_OFFLINE)
   - Zero BlindRenderer imports or references.
   - Zero blind mapping or reveal file access.
   - Manifest-driven execution order (24 cells: 8 ideas x 3 conditions).
   - Status evaluation is strictly FAIL-CLOSED.
   - Uninstrumented telemetry is explicitly classified as UNKNOWN_NOT_INSTRUMENTED.
   - Zero synthetic post-hoc FioED delta labels.

2. **Blind Rendering Plane Isolation (ender_m05_4_blind_review.py):**
   - BLIND_RENDERING_PLANE_HAS_NO_MODEL_EXECUTION = True (PROVEN_OFFLINE)
   - Zero ModelRunner or NativeModelRunner imports or references.
   - Standalone post-execution tool that reads frozen attempt-002 raw outputs and external sealed reveal.
   - Audits and guarantees zero metadata leaks.

---

## 4. Offline Verification Summary

- Canonical suite: 	ests/test_m05_4_clean_harness.py (9/9 PASS)
  - CASE 1: Dirty worktree blocked -> PASS
  - CASE 2: Hash mismatch blocked -> PASS
  - CASE 3: Wrong provider cell blocked -> PASS
  - CASE 4: Wrong model cell blocked -> PASS
  - CASE 5: Duplicate cell blocked -> PASS
  - CASE 6: Attempt already started blocked -> PASS
  - CASE 7: Valid frozen execution (24 cells) -> PASS
  - Negative control (blind isolation): PASS
  - Renderer isolation & leak audit: PASS
- SELF_ENFORCING_FREEZE_GATE = PROVEN_OFFLINE
- Historical experiment mutation: 0
