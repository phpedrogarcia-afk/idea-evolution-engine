# PREREGISTRATION: EXP-M05.5R1-CONTROLLED-REPLICATION

**Status:** FROZEN
**Type:** Controlled Replication (Clean Rerun of M05.5)

## 1. Goal
Repeat the intended M05.5 reliability experiment without carrying forward contaminated holdouts, attempt identity, blind mapping, or provider state.

## 2. Treatments (Unchanged from M05.5)
- **Condition A (Baseline):** The frozen baseline prompt.
- **Condition B (Simple Loop):** The frozen iterative execution loop.
- **Condition C (Lean L1):** The frozen deterministic Lean L1.
- **Provider:** groq
- **Model:** openai/gpt-oss-120b

## 3. New Holdouts (N=8)
To guarantee uncontaminated provenance, 8 completely new holdouts were defined and sealed in M05.5R1-HOLDOUT-SET-REV1, maintaining the original conceptual classes:

1. SIMPLE_CONSTRAINED_UTILITY (H01)
2. FERTILE_INCUBATIVE (H02)
3. TWO_PLAUSIBLE_MECHANISMS (H03)
4. HARD_LOCAL_PRIVACY_CONSTRAINT (H04)
5. PHYSICAL_OPERATIONAL_IDEA (H05)
6. NORMATIVE_HUMAN_DECISION (H06)
7. SIMPLE_DEVELOPER_TOOL (H07)
8. TESTABLE_PRODUCT_HYPOTHESIS (H08)

## 4. New Blinding (Revision 1)
An entirely fresh mapping (BLINDING_REVISION = 1) was created using an OS-backed CSPRNG once new holdouts were frozen.
- Mapping must NEVER be printed or logged.
- Reveal is stored only in canonical external sealed directory.
- Only the commitment hash (d2de9ac1bbcd76c7aaef639b0b61d63dd355f1bea96f9d1c0f41ef7d434eed02) is committed to this repository.

## 5. Execution Integrity Rules

### Attempt Immutability Guard
Once an attempt performs its first semantic provider call, its `ATTEMPT_ID` becomes **IMMUTABLE**.
- Its directory MUST NEVER be deleted, emptied, recreated, or reused.
- If execution fails (e.g., due to rate limits), that attempt is closed as FAILED/INVALID.
- 429 Rate Limits are evidence. Do not erase them or restart the same attempt.

### Provider Quota Readiness Gate
- Pacing guard active: concurrency 1, exact token pre-dispatch guard, TPM reset wait.
- Tested and validated under FREE-SACRIFICIAL-PILOT-006 (CAPACITY_VERDICT = PASS_WITH_PACING).

### Exclusive Provider Window
During primary execution:
- NO diagnostic model calls.
- NO Groq pings.
- NO parallel Groq experiments.
- NO unrelated workloads under the same known quota.
- The primary runner owns the experimental provider window.

## 6. Execution Readiness Contract
- [x] NEW_HOLDOUTS_FROZEN = YES
- [x] TREATMENT_HASHES_MATCH_REFERENCE = YES
- [x] RUBRIC_MATCH = YES
- [x] MODEL_PROVIDER_MATCH = YES
- [x] BLIND_MAPPING_SEALED = YES
- [x] MAPPING_PRINTED = NO
- [x] ATTEMPT_DIRECTORY_FRESH = YES
- [x] ATTEMPT_IMMUTABILITY_GUARD = ACTIVE
- [x] PROVIDER_QUOTA_READY = YES
- [x] COMPETING_PROVIDER_WORKLOADS = NONE_KNOWN
- [x] WORKTREE_CLEAN = YES
