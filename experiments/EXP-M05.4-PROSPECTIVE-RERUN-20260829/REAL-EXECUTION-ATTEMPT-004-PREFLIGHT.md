# REAL-EXECUTION-ATTEMPT-004-PREFLIGHT.md

## 1. Attempt Identity & Status

| Field | Value |
|---|---|
| EXPERIMENT_ID | EXP-M05.4-PROSPECTIVE-RERUN-20260829 |
| ATTEMPT_ID | REAL-EXECUTION-ATTEMPT-004 |
| STATUS | FROZEN_NOT_EXECUTED |
| REAL_PROVIDER_CALLS | 0 |
| STRUCTURED_OUTPUT_ADAPTER | PROVEN_ENOUGH |
| TREATMENT_DELIVERY_PILOT | PASS |
| B_REFINEMENT_INCOMPLETE_REVIEWABILITY | ADMISSIBLE_IF_SUBSTANTIVE_CANDIDATE_PRESENT |
| HUMAN_REVIEW_STARTED | NO |
| ATTEMPT_001_OUTPUTS_REUSED | NO |
| ATTEMPT_002_OUTPUTS_REUSED | NO |
| ATTEMPT_003_OUTPUTS_REUSED | NO |
| PILOT_OUTPUTS_REUSED | NO |
| BLINDING_REVISION | 3 |
| BLINDING_REVISION_3_STATUS | ACTIVE |
| BLIND_COMMITMENT_SHA256 | b2e271ff9dd35a8215c067d1e545f84dfa8add7f33335a69845ebd8d5ed82cf3 |
| BLIND_STATUS | SEALED_OUTSIDE_REPOSITORY |
| SEALED_REVEAL_LOCATION | C:\Users\phped\.fioideias\sealed\EXP-M05.4-PROSPECTIVE-RERUN-20260829\BLIND-REVEAL-REV3.json |
| PRIMARY_OUTPUT_NAMESPACE | REAL-EXECUTION-ATTEMPT-004 |

---

## 2. Scientific & Engineering Context

1. **Attempt-003 Structured Output Autopsy Findings:**
   - Established that IEE correctly targets Groq Chat Completions with strict JSON schema mode.
   - Identified that `NativeModelRunner._call_provider` collapsed generic provider exceptions into `failed_generation`, causing unwarranted semantic repair loops.
   - Corrected in `src/idea_evolution/providers/native.py`: added typed error classification (`ProviderErrorDetails`), credential sanitization (`sanitize_error_message`), and bounded transport retries for transient errors (429/5xx). Semantic repair is only invoked when the provider genuinely returns `failed_generation`.

2. **Micro-Probe & Calibration Pilot Validation:**
   - Micro-probe 001: 3/3 representative schemas admitted cleanly (Condition A: 1.65s, Condition B: 2.91s, Condition C: PASS).
   - Treatment Delivery Pilot 01 (`CAL-01`, `CAL-02`): 6/6 cells completed.
     - Condition A: 2/2 DELIVERED (`SUCCESS`, 1 call each)
     - Condition B: 2/2 PARTIALLY_DELIVERED (`REFINEMENT_INCOMPLETE` with substantive candidate, 10 calls each)
     - Condition C: 2/2 DELIVERED (`HUMAN_DECISION_REQUIRED`, 1 call each)
   - Supervisor Decision: `CONDITION_B_REFINEMENT_INCOMPLETE_WITH_SUBSTANTIVE_CANDIDATE = ADMISSIBLE_TREATMENT_OUTPUT`. The 10-stage ceiling is part of the frozen treatment definition.

3. **Reviewability Contract:**
   - `REVIEWABLE_OUTPUT != TERMINAL_SUCCESS`
   - A cell is `HUMAN_REVIEWABLE` if a substantive candidate/evolution artifact exists and can be rendered without exposing condition identity.
   - For Condition B: `REFINEMENT_INCOMPLETE` + substantive candidate present = `HUMAN_REVIEWABLE`.
   - Provider failure before candidate / structured output failure before candidate / orchestration crash = `NOT_REVIEWABLE`.

4. **Mechanical Start Gates:**
   - Gate 1: Git worktree clean check (`git status --porcelain`) + 22 critical file hash checks against `RERUN-FREEZE-MANIFEST.json` + Revision 3 blind commitment check.
   - Gate 2: Single-use attempt namespace verification.
   - Gate 3: Manifest cells verification (24 cells: 8 A / 8 B / 8 C, groq / openai/gpt-oss-120b).
   - Gate 4: Runner provider & model validation.
   - Gate 5: Start receipt created only after all gates pass.

---

## 3. Offline Verification Summary

- Canonical unittests: 198/198 PASS
- Deterministic Context Validator: PASS
- Agent Intelligence Architecture Validator: PASS
- `SELF_ENFORCING_FREEZE_GATE` = PROVEN_OFFLINE
- Historical experiment mutation: 0
- Attempt-001 mutation: 0
- Attempt-002 mutation: 0
- Attempt-003 mutation: 0
- Pilot-01 mutation: 0
