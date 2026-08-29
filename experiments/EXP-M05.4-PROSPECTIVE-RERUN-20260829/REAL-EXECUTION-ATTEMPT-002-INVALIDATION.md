# REAL-EXECUTION-ATTEMPT-002-INVALIDATION.md

## 1. Invalidation Record Summary

| Field | Value |
|---|---|
| ATTEMPT_ID | REAL-EXECUTION-ATTEMPT-002 |
| EXPERIMENT_ID | EXP-M05.4-PROSPECTIVE-RERUN-20260829 |
| STATUS | INVALID_FOR_PRIMARY_ANALYSIS |
| INVALIDATION_CLASS | MID_EXECUTION_RUNTIME_EXCEPTION |
| START_HEAD | e2d6f0725b59d0a4f094c78fb04067dd96cdef47 |
| CELLS_FROZEN | 24 |
| CELLS_STARTED | 12 |
| CELLS_COMPLETED | 11 |
| CELLS_INCOMPLETE | 1 (IDEA-04-CONDITION_C) |
| LAST_CELL_STARTED | IDEA-04-CONDITION_C |
| COMPLETED_CELL_SEMANTIC_CALLS | 34 |
| IDEA_04_C_PROVIDER_CALLS_OBSERVED | 1 |
| ACTUAL_PROVIDER_CALLS_TOTAL | 35 |
| HUMAN_REVIEW_STARTED | NO |
| MACHINE_REVEAL_ACCESS_OCCURRED | NO |
| REVEAL_EXPOSED_TO_HUMAN | NO |
| ATTEMPT_001_OUTPUTS_REUSED | NO |
| PRIMARY_EVIDENCE_ADMISSIBLE | NO |
| HISTORICAL_EXPERIMENT_MUTATION | 0 |
| ATTEMPT_001_MUTATION | 0 |

---

## 2. Autopsy of Failure at Cell 12 (IDEA-04-CONDITION_C)

### Causal Chain
1. xecute_m05_4_cell invoked LeanLoopRunner.run(original_idea=raw_idea) for IDEA-04-CONDITION_C.
2. LeanLoopRunner executed Chamada 1 (self.runner.generate(..., output_schema=LeanFirstPassOutput)).
3. The provider generation returned parsed = None (failed structured output or provider error).
4. irst_pass_output became None.
5. LeanLoopRunner passed irst_pass_output=None into EarlyEpistemicGate.evaluate(source_anchor=..., first_pass=None, ...).
6. EarlyEpistemicGate.evaluate line 226 attempted to dereference irst_pass.primary_mechanism.
7. Python raised an unhandled AttributeError: 'NoneType' object has no attribute 'primary_mechanism'.
8. The unhandled exception crashed the runner process at cell 12 of 24.

### Defect Classification
- **Classification:** LEAN_ORCHESTRATION_NULL_UNHANDLED (infrastructure/orchestration defect).
- **Root Cause File:** src/idea_evolution/orchestration/lean_loop.py & src/idea_evolution/domain/early_epistemic_gate.py.
- **Root Cause Function:** LeanLoopRunner.run (missing null check on irst_pass_output) and EarlyEpistemicGate.evaluate (missing precondition guard).
- **Core Principle:** An admissible cell-level model generation failure must be captured as a typed fail-closed cell result (FIRST_PASS_FAILED) rather than an unhandled Python process crash.

---

## 3. Condition B Failure Classification

All 4 completed Condition B cells (IDEA-01-B, IDEA-02-B, IDEA-03-B, IDEA-04-B) were classified as VALID_FROZEN_SEMANTIC_OUTCOME under frozen fail-closed semantics:
- IDEA-01-B: 10 stages executed, reconstruction limit reached -> REFINEMENT_INCOMPLETE (VALID_FROZEN_SEMANTIC_OUTCOME).
- IDEA-02-B: 1 stage executed, understand stage failed -> FAILED (VALID_FROZEN_SEMANTIC_OUTCOME).
- IDEA-03-B: 10 stages executed, reconstruction limit reached -> REFINEMENT_INCOMPLETE (VALID_FROZEN_SEMANTIC_OUTCOME).
- IDEA-04-B: 5 stages executed, reality check stage failed -> FAILED (VALID_FROZEN_SEMANTIC_OUTCOME).

No shared infrastructure defect was found in Condition B.

---

## 4. Preservation of Attempt-002 Evidence

All 11 completed raw artifact files and traces under xperiments/EXP-M05.4-PROSPECTIVE-RERUN-20260829/REAL-EXECUTION-ATTEMPT-002/ are preserved as immutable historical failure evidence. They will not be reused or submitted to human review.
