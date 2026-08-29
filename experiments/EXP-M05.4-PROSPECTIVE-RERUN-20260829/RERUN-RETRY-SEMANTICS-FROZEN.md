# RERUN-RETRY-SEMANTICS-FROZEN.md

Experiment: EXP-M05.4-PROSPECTIVE-RERUN-20260829
Frozen: 2026-08-29

## Retry Taxonomy

| Class | Definition | Allowed |
|-------|-----------|---------|
| TRANSPORT_RETRY | Network/HTTP failure before provider processes the request. Logged as infrastructure event. Does not count as a model call. | YES |
| STRUCTURED_OUTPUT_REPAIR | Provider returned text that fails schema validation. NativeModelRunner attempts JSON repair up to max_repairs=1. Part of frozen A/B/C semantics. | YES |
| SEMANTIC_RETRY | Re-running a stage because the semantic output appears weak, incomplete, or unsatisfactory. | NO - strictly prohibited |
| RECONSTRUCTION | SimpleLoopRunner Stage 6 (FINAL_REVIEW) returns recommendation=RECONSTRUCT. Pipeline runs one additional 4-stage cycle (ALTERNATIVES, SYNTHESIZE, REALITY_CHECK, FINAL_REVIEW). Max 1 cycle. | YES - Condition B only, governed by frozen FinalReviewOutput |

## Policy

- Infrastructure retries (TRANSPORT) must be recorded in the run trace.
- STRUCTURED_OUTPUT_REPAIR is bounded by max_repairs=1 per stage call.
- No quality-based regeneration.
- No manual re-runs because output appears weak.
- RECONSTRUCTION is governed solely by the frozen FinalReviewOutput.recommendation field.
- Any deviation from this taxonomy during execution must be recorded as a
  protocol violation before the blind review.

## Condition Retry Bounds

| Condition | Min Calls | Max Calls | Reconstruction |
|-----------|-----------|-----------|----------------|
| A (Baseline) | 1 | 1 | N/A |
| B (Simple Loop) | 6 | 10 | Max 1 reconstruction cycle |
| C (Lean L1) | 1 | 2 | N/A - gate-governed |
