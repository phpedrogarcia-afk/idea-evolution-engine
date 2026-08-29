# REAL-EXECUTION-ATTEMPT-001-INVALIDATION.md

## 1. Invalidation Record Summary

| Field | Value |
|---|---|
| ATTEMPT_ID | REAL-EXECUTION-ATTEMPT-001 |
| EXPERIMENT_ID | EXP-M05.4-PROSPECTIVE-RERUN-20260829 |
| STATUS | INVALID_FOR_PRIMARY_ANALYSIS |
| INVALIDATED_BEFORE_HUMAN_REVIEW | YES |
| HUMAN_REVIEW_STARTED | NO |
| REVEAL_EXPOSED_TO_HUMAN | NO |
| MACHINE_REVEAL_ACCESS_OCCURRED | YES |
| PRIMARY_PROSPECTIVE_EVIDENCE_ADMISSIBLE | NO |
| RAW_OUTPUTS_PRESERVED | YES (quarantined as failed attempt evidence) |
| RAW_OUTPUTS_USED_FOR_PRIMARY_ANALYSIS | NO |
| HISTORICAL_EXPERIMENT_MUTATION | 0 |

---

## 2. Specific Reasons for Invalidation

1. **Harness Changed After Freeze:** src/idea_evolution/experiments/m05_4_runner.py was edited post-freeze to adapt paths, resulting in a dirty worktree during execution.
2. **Execution Script Unfrozen:** 	ools/experiments/execute_m05_4_real.py was created post-freeze and was not hashed in RERUN-FREEZE-MANIFEST.json.
3. **Dirty Start Receipt:** REAL-EXECUTION-START-RECEIPT.json recorded commit 8d0ac29, but the actual execution ran against uncommitted modifications.
4. **Machine Reveal Access Timing:** xecute_m05_4_real.py called xecutor.load_blind_mappings() in pre-loop setup before cell execution.
5. **Synthetic Post-Hoc Instrumentation:** FioED delta labels (OPTION_ADDED, NEXT_ACTION_CHANGED, AMBIGUITY_RESOLVED, SOURCE_DRIFT_INCREASED) were assigned via hardcoded heuristics rather than dynamically measured from stage outputs. Marked: NON_ADMISSIBLE_SYNTHETIC_POSTHOC_LABELS.
6. **Unmeasured Telemetry Counters:** 	ransport_retries and structured_output_repairs were initialized to zero without being instrumented from actual provider calls. Marked: UNKNOWN_NOT_INSTRUMENTED.
7. **Condition A Status Fallback:** Condition A evaluated status with es_a.get("success", True) which risked masking missing success flags.
8. **Execution Interrupted:** Process was cleanly terminated via supervisor command at cell IDEA-03-CONDITION_B.

---

## 3. Account of What Actually Happened

- **Process Was Still Running at Signal:** YES
- **Process Stopped:** YES (Task cancelled cleanly)
- **Cells Started:** 8 (IDEA-01-A, IDEA-01-B, IDEA-01-C, IDEA-02-A, IDEA-02-B, IDEA-02-C, IDEA-03-A, IDEA-03-B)
- **Cells Completed:** 7 (IDEA-01-A, IDEA-01-B, IDEA-01-C, IDEA-02-A, IDEA-02-B, IDEA-02-C, IDEA-03-A)
- **Cells Incomplete/Cancelled:** 1 (IDEA-03-CONDITION_B)
- **Cells Pending (Not Started):** 16
- **Last Cell Started:** IDEA-03-CONDITION_B
- **Last Cell Completed:** IDEA-03-CONDITION_A
- **Actual Completed Provider Calls Observed:** 27 calls (A: 3 calls, B: 20 calls, C: 4 calls) + in-flight calls on IDEA-03-B
- **First Real Provider Call Timestamp:** ~2026-08-29T16:42:50-03:00
- **Last Real Provider Call Timestamp:** ~2026-08-29T16:54:24-03:00
- **Transport Retries:** UNKNOWN_NOT_INSTRUMENTED
- **Structured Output Repairs:** UNKNOWN_NOT_INSTRUMENTED
- **FioED Instrumentation Status:** NON_ADMISSIBLE_SYNTHETIC_POSTHOC_LABELS

---

## 4. Quarantined Raw Outputs

The 7 completed raw artifact files:
- aw/IDEA-01_condition_a.json
- aw/IDEA-01_condition_b.json
- aw/IDEA-01_condition_c.json
- aw/IDEA-02_condition_a.json
- aw/IDEA-02_condition_b.json
- aw/IDEA-02_condition_c.json
- aw/IDEA-03_condition_a.json
and traces in aw/runs_a/, aw/runs_b/, aw/runs_c/ are preserved as immutable evidence of REAL-EXECUTION-ATTEMPT-001.
They must NOT be submitted to human review or used for primary statistical analysis.
