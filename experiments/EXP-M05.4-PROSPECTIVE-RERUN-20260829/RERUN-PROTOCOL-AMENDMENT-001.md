# RERUN-PROTOCOL-AMENDMENT-001.md

## Experiment Lineage Record

| Field | Value |
|-------|-------|
| ORIGINAL_EXPERIMENT_ID | EXP-M05.4-PROSPECTIVE-20260827 |
| ORIGINAL_STATUS | INVALIDATED_BEFORE_HUMAN_REVIEW |
| RERUN_EXPERIMENT_ID | EXP-M05.4-PROSPECTIVE-RERUN-20260829 |
| AMENDMENT_CLASS | EXECUTION_INFRASTRUCTURE_CORRECTION |
| AMENDMENT_DATE | 2026-08-29 |
| ACCEPTED_PATCH_HEAD | 67f4adb |
| ACCEPTED_PATCH_BRANCH | deepseek/m05.4-preflight-hardening-20260827 |

## Root Cause of Original Invalidation

Condition B (CURRENT_SIMPLE_LOOP_CONTROL) was instantiated via
SimpleLoopRunner(runner=self.runner) without passing an explicit
ModelRoutingConfig. This caused SimpleLoopRunner to construct RunnerRouter
with ModelRoutingConfig.default_single_model(), which assigned model="default-model".
The Groq API rejected "default-model" on the first call (UNDERSTAND stage),
causing all 8 Condition B ideas to abort after exactly 1 call with
PROVIDER_STRUCTURED_OUTPUT_REPAIR_FAILED. Conditions A and C executed
correctly with openai/gpt-oss-120b.

## Correction Applied

Receiver-scoped M05.4 routing and preflight hardening (commit 67f4adb):

- _validate_model_routing() now verifies self.runner.provider == "groq" and
  self.runner.default_model == "openai/gpt-oss-120b" BEFORE any condition
  execution. Uses RuntimeError (not assert) -- survives python -O.
- run_condition_b() explicitly constructs ModelRoutingConfig routing all
  Simple Loop stages to the frozen provider/model.
- Duplicate helper methods removed.
- 5 regression tests added (tests/test_m05_4_provider_guard.py) with
  negative-control verification.
- Negative control confirmed: old guard silently passed wrong-provider.

## Integrity Assertions

| Property | Value |
|----------|-------|
| HUMAN_REVIEW_STARTED | NO |
| HUMAN_SEMANTIC_EXPOSURE | NONE |
| BLIND_REVEAL_OPENED | NO |
| OLD_OUTPUTS_REUSED | NO |
| HOLDOUT_CHANGED | NO |
| IDEAS_CHANGED | NO |
| PROMPTS_CHANGED | NO |
| FIOED_CHANGED | NO |
| CONDITION_SEMANTICS_CHANGED | NO |
| RUBRIC_CHANGED | NO |
| PREDICTIONS_CHANGED | NO |
| RERUN_SCOPE | ALL 24 CELLS (8 ideas x 3 conditions) |

## Historical Experiment Scar

HISTORICAL_EXPERIMENT_PREVIOUSLY_MUTATED_BY_TEST_PATH

During the M05.4 P1 audit mission (pre-patch), tracked artifacts under
experiments/EXP-M05.4-PROSPECTIVE/raw/ were found dirty, containing fake
data from an earlier test execution. They were restored from HEAD via
git checkout HEAD -- experiments/EXP-M05.4-PROSPECTIVE/raw/ before the
accepted patch was produced.

Current status: RESTORED. Not a current blocker.
Reopen only if canonical dry-run again mutates historical evidence.

## Scientific Continuity

The original invalidated experiment remains preserved as scientific evidence
of the infrastructure defect. It must not be edited, normalized or reused.
All preregistration documents (theory, predictions, rubric, holdout ideas,
analysis plan) remain unchanged. This rerun uses identical scientific content
with corrected execution infrastructure.
