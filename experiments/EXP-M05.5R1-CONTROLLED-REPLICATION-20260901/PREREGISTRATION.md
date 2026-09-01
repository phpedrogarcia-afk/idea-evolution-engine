# PREREGISTRATION: EXP-M05.5R1-CONTROLLED-REPLICATION

**Status:** DRAFT_PENDING_SUPERVISOR_FREEZE
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
To guarantee uncontaminated provenance, 8 completely new holdouts MUST be defined, maintaining the original conceptual classes. Current draft is rejected because the designer knew treatment results. New independent holdouts are awaited for:

1. SIMPLE_CONSTRAINED_UTILITY
2. FERTILE_INCUBATIVE
3. TWO_PLAUSIBLE_MECHANISMS
4. HARD_LOCAL_PRIVACY_CONSTRAINT
5. PHYSICAL_OPERATIONAL_IDEA
6. NORMATIVE_HUMAN_DECISION
7. SIMPLE_DEVELOPER_TOOL
8. TESTABLE_PRODUCT_HYPOTHESIS

*Note: Holdouts must NOT be REP-01..08. New literal text is required.*

## 4. New Blinding (Revision 1)
An entirely fresh mapping (BLINDING_REVISION = 1) will be created using an OS-backed CSPRNG once new holdouts are frozen. 
- Mapping must NEVER be printed or logged.
- Reveal is stored only in a canonical external sealed directory.
- Only the commitment hash is committed to this repository.

## 5. Execution Integrity Rules

### Attempt Immutability Guard
Once an attempt performs its first semantic provider call, its `ATTEMPT_ID` becomes **IMMUTABLE**.
- Its directory MUST NEVER be deleted, emptied, recreated, or reused.
- If execution fails (e.g., due to rate limits), that attempt is closed as FAILED/INVALID.
- The next execution must become `REAL-EXECUTION-ATTEMPT-002` (or incremented attempt).
- 429 Rate Limits are evidence. Do not erase them or restart the same attempt.

### Provider Quota Readiness Gate
Before the first real holdout call, a deterministic `PROVIDER_QUOTA_READINESS_GATE` will verify adequate same-model quota exists for the complete experiment.
- No holdout text may be sent through this gate. Use a neutral non-holdout synthetic string (recorded as `INFRASTRUCTURE_QUOTA_PROBE`).
- Estimate Required Quota: Since historical exact usage is unproven, the gate requires a freshly reset provider quota window and NO competing workloads.

### Exclusive Provider Window
During primary execution:
- NO diagnostic model calls.
- NO Groq pings.
- NO parallel Groq experiments.
- NO unrelated workloads under the same known quota.
- The primary runner owns the experimental provider window.

## 6. Execution Readiness Contract
Before execution, the following MUST be confirmed:
- [ ] NEW_HOLDOUTS_FROZEN = YES
- [ ] TREATMENT_HASHES_MATCH_REFERENCE = YES
- [ ] RUBRIC_MATCH = YES
- [ ] MODEL_PROVIDER_MATCH = YES
- [ ] BLIND_MAPPING_SEALED = YES
- [ ] MAPPING_PRINTED = NO
- [ ] ATTEMPT_DIRECTORY_FRESH = YES
- [ ] ATTEMPT_IMMUTABILITY_GUARD = ACTIVE
- [ ] PROVIDER_QUOTA_READY = YES
- [ ] COMPETING_PROVIDER_WORKLOADS = NONE_KNOWN
- [ ] WORKTREE_CLEAN = YES
