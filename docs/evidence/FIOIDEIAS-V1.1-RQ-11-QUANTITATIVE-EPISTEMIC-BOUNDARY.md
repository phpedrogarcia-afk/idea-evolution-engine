# FioIdeias V1.1 — RQ-11: Quantitative Epistemic Boundary

MISSION_ID = FIOIDEIAS-V1.1-RQ-11-QUANTITATIVE-EPISTEMIC-BOUNDARY
DATE = 2026-09-30
MODE = AUTOPSY → MINIMAL FIX → PROVE → FREEZE → STOP
VERDICT = PASS, within the tested envelope

## 1. Start state and scope

- Isolated checkout: `C:\Users\phped\Documents\FioIdeias_RQ10_Clean`
- `START_HEAD = 96ef97000e0a112083aa41db189e77cad54c0141` (RQ-10 evidence commit)
- Target branch: `fioideias/v1.1-decision-relevance`; this isolated checkout was detached at the expected commit. The primary `ProjetoFioIedeias` checkout had pre-existing dirty state and was not modified.
- Initial isolated worktree was clean. The RQ-07/RQ-09 candidate at `571bcdf97aeea9bdd5cc6ad8a8de92cf443f92a4` was not rewritten.
- Changes were limited to RQ-11 implementation, regression tests, and this evidence record. No release, merge, tag, `main` change, Qwen invocation, new blind input, or V1.2 work occurred.

## 2. RQ-10 Case E autopsy

RQ-10 confirmed the blocker as unsupported quantitative precision that could influence a future continue/abandon judgment. The preserved Case E input contains no numerical criteria. The numbers below were present in the generated Case E artifact at `final.md`, section 4.1, and were not present in the user input, backed by cited evidence, or derived deterministically. RQ-10 did not record a numeric provenance field or supporting source for them.

| Criterion in Case E | Value and unit | Purpose / downstream force | Provenance and status |
|---|---|---|---|
| “Nenhuma correlação estatisticamente significativa … com N≥30 usuários” | N ≥ 30 users | Sample-size condition inside “what would falsify it”; could be read as a validated rejection boundary | Model-generated heuristic; unsupported in the input and evidence record |
| “Estudo de 1–2 semanas com 30 participantes” | 1–2 weeks; 30 participants | Pilot duration and sample-size prescription; supports the proposed experiment | Model-generated heuristic; no derivation or justification recorded |
| “Taxa de consentimento inferior a 30%” | consent < 30% | Explicit condition for rejecting the audio-consent hypothesis | Model-generated kill threshold; no justification recorded |
| “Entrevistas de 10–15 minutos com 20 potenciais usuários” | 10–15 minutes; 20 users | Interview duration and sample size for the consent test; supports the proposed next action | Model-generated heuristic; no derivation or justification recorded |

These numbers were used in falsification/test descriptions, with the low-consent threshold explicitly phrased as what would “derrubar” the hypothesis. The mapped `lowest_cost_discriminating_test` was also reused as next-action support. That gave the values potential decisional force for a human reader. **They did not trigger an automated gate in the recorded RQ-10 run:** Case E returned `RETURN_NOW`, with `EVIDENCE_NEEDED` status. The blocker was unsafe presentation and future decision influence, not an observed automatic abandonment.

### Exact root cause

`FalsificationCriterion` represented hypotheses, kill conditions, and test plans as free-form strings without quantitative provenance. The existing `FalsePrecisionGuard.sanitize_unsupported_precision` covered a narrower metric pattern and was applied to the primary mechanism, not to falsification criteria and action-support text. The renderer then printed those strings verbatim, and `EvolutionArtifactMapper` reused the unqualified lowest-cost test as action support. Thus an unsupported number could survive generation, mapping, and rendering with the appearance of a usable decision boundary. General `MODEL_HYPOTHESIS` / `EVIDENCE_NEEDED` labels did not identify which numeric values were provisional.

## 3. Minimal fix and enforced invariant

The deterministic qualification now runs on first-pass and escalation decision text **before** gate processing, next-action arbitration, persistence, or human-readable rendering. It covers falsification hypotheses, kill criteria, discriminating tests, and proposed/updated next actions.

- Unsupported quantities remain in the text; they are not deleted or rounded.
- They carry a visible `PROVISIONAL_HEURISTIC` notice stating that the quantitative relation is not textually linked to a verified source or derivation and is not a validated continue/abandon cutoff.
- A number appearing somewhere else in the source is insufficient. The decision sentence must match the normalized source sentence; this prevents, for example, reusing an observed `30%` conversion rate as an unrelated consent threshold.
- An explicitly trusted `USER_SUPPLIED`, `DETERMINISTIC_CALCULATION`, `MEASURED`, or `EXTERNAL_EVIDENCE` basis remains usable. The normal model path does not trust model self-attestation as evidence. Explicit provisional heuristics remain allowed.
- `FROZEN_LEAN_CORE_HASH_V1_1` remains unchanged. The changed core receives the separate `FROZEN_LEAN_CORE_HASH_RQ11 = 1d294c2be6b9e52733e2e543b7b921b2f0fb64034ebced95aa08403b6504fa83` identity.

This preserves RQ-07 gate authority and the RQ-09 distinction between verified facts and model hypotheses. It does not grant authority to the model or change human final authority.

## 4. Tests and suite

Added 13 deterministic RQ-11 tests covering:

1. Unsupported kill threshold, continue threshold, and percentage qualification.
2. Exact user-explicit threshold preservation, trusted evidence-backed values, and trusted deterministic arithmetic.
3. Provisional heuristic allowance and a negative control where the same numeric value appears in an unrelated source claim.
4. The structural RQ-10 Case E response shape, including a model self-attestation that must not bypass qualification, and no gate/automatic abandonment from a provisional threshold.
5. RQ-09 unverified-claim rendering and RQ-11 core identity separation from historical V1.1.

Existing exact next-action assertions were updated only to preserve the action text while requiring the new provisional marker for unsupported quantities.

`FULL_SUITE = 542 passed, 0 failed, 1 known PytestCollectionWarning, exit 0 (14.42s).` The warning is the existing `TestabilityBinding` collection warning. A prior full run found four legacy assertions expecting unqualified exact action strings; those assertions were updated to require both the preserved recommendation and its provisional marker. The final full suite ran after the negative control and marker wording were finalized. Python bytecode writing was disabled; no tracked `.pyc` changes remained.

Test-generated run artifacts were moved outside the checkout and hash-verified before removal from `runs/`:

- `C:\Users\phped\Documents\FioIdeias_RQ11_TestArtifacts_20260930`: 10 directories, 102 files.
- `C:\Users\phped\Documents\FioIdeias_RQ11_FinalSuiteArtifacts_20260930`: 5 directories, 51 files.
- `C:\Users\phped\Documents\FioIdeias_RQ11_FinalSuiteArtifacts2_20260930`: 5 directories, 51 files.

No pre-existing run directory was removed.

## 5. Known regression set D/E/F

The preserved RQ-10 inputs were run once each, D → E → F, with the same `LEAN_IEE_L1` topology, Cerebras route, and configured `openai/gpt-oss-120b` model. These are now `KNOWN_REGRESSION_SET = YES`, not blind or generalization evidence. Each invocation completed with one model call, `COMPLETED_DIRECT_ONE_PASS`, `RETURN_NOW`, and empty stderr.

| Case | Frozen input JSON SHA-256 | New run | Stdout SHA-256 | Provisional numeric lines |
|---|---|---|---|---:|
| D | `DFD77C6EC2A31F218262E79B274957D060D4085E47E970AC258B6AF0966DCFAB` | `RUN-20260930_194338` | `E1E2CB5A06C7CEA137FBD45C5FABDF1C4F4FA4046A17DBD79F54D9DB4AB787A4` | 1 |
| E | `8391F59CC78B55BF9309D25190D29DD1B0C4323D440B0411563FEED82679EE13` | `RUN-20260930_194353` | `36E529A206EE85F5AE32AF97F6C4F4ED5E0A7CD37EE3ADD2D685207DDC8CEB29` | 3 |
| F | `43856824768FB31137EE17B11C1A580BC5FC8CAE63371DC21170F08F2A9833D3` | `RUN-20260930_194423` | `59A34F60B514FA6296BF8B8CACDC06177860E9FC3F88B437FCECD278FE41831E` | 4 |

For all three frozen user inputs, the original idea text contains no numeric characters. Every numeric line found in the decision-relevant false-falsification and next-action sections of the recorded outputs has a visible provisional marker. The final sentence-level source-anchor tightening was added after these one-time calls; because none of these input texts contains a number, it cannot convert any of their previously unsupported output values into a supported value. D/E/F were not rerun.

### Case E result

`RQ10_NUMERIC_BLOCKER_REPRODUCED_AFTER_FIX = NO` within this regression run. The new Case E output proposes 5 minutes and 10 seconds as experimental-test durations and 1 second in the next-action support; all three values are visibly labeled `PROVISIONAL_HEURISTIC`. No numerical kill/abandon criterion is stated in the “what would falsify it” lines. The gate remains `RETURN_NOW`; the numeric heuristics do not cause continue, stop, or abandonment. `MODEL_HYPOTHESIS` remains the next-action basis and the unverified competitor statements remain model hypotheses.

The structured output still reports `human_decision_required = false`, which remains underexplained in the RQ-10 evidence and is not treated as execution or decision authority. No decision or external action was executed. The earlier Case F `SPOOFING_DETECTED` false-positive remains `KNOWN_NON_BLOCKING_DEBT`; it was not changed. Related ambiguity in Case E was also left untouched.

## 6. Claim boundary and limitations

- `RQ10_BLOCKER_CONFIRMED = YES`; `UNSUPPORTED_MODEL_NUMBER_CAN_ACT_AS_VALIDATED_THRESHOLD = NO` within the deterministic guard and evaluated paths.
- `PROVISIONAL_NUMERIC_HEURISTICS_ALLOWED = YES`.
- Explicit user values, trusted evidence-backed values, and trusted deterministic arithmetic remain usable under their corresponding basis; the normal path does not accept model-declared provenance as proof.
- `RQ09_INVARIANT_PRESERVED = YES`; `RQ07_GATE_INVARIANTS_PRESERVED = YES` (the existing RQ-07 suite and full suite passed; Case E remained `RETURN_NOW`).
- No automatic threshold-to-gate or threshold-to-abandon path was introduced.
- `HUMAN_AUTHORITY_PRESERVED = YES`: the system returned suggestions and did not execute a decision. The underexplained `human_decision_required = false` output remains explicit debt.
- Raw HTTP transcripts/provider response metadata were not available in the original RQ-10 evidence and were not fabricated here. D/E/F executions are a fixed regression set only: `BLIND_EVIDENCE = NO`; `GENERALIZATION_EVIDENCE = NO`.
- A **new prospective blind release gate is required before any release**. It is not authorized or started by RQ-11.

NEXT_ALLOWED_STEP = stop after preserving RQ-11 evidence; await a separate human-authorized prospective blind release gate.
