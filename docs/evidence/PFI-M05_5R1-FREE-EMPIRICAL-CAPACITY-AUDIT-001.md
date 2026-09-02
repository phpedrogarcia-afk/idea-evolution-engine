# PFI-M05_5R1-FREE-EMPIRICAL-CAPACITY-AUDIT-001

## Scope and invariants

- Execution authority: `OFFLINE_ANALYSIS_ONLY`.
- Tokenizer: `openai-harmony==0.0.8`, `HarmonyGptOss` / `o200k_harmony`, artifact SHA-256 `45c75e9070327773c24c9c7a345f18cf11afb17eba36108667bffc35f84f7e39`.
- Provider calls, network inference calls, A/B/C cells executed, real replication started and reveal accessed: `0`, `0`, `0`, `0`, `NO`.
- The sealed R1 boundary returned token counts only. No raw holdout content was emitted to this coordinating analysis or recorded here.

## Trace completeness: `TRACE_INCOMPLETE`

Attempt-004 stores 98 stage records: A=8, B=80 and C=10. It does not retain provider request payloads or provider usage fields. A has 8 absent raw-response payloads; C has 10 absent raw-response payloads. Two B records have `retry_count=1` (`IDEA-01` position 5 and `IDEA-04` position 1); their original rejected generation and repair request are not stored. Transport retry instrumentation is `UNKNOWN_NOT_INSTRUMENTED`.

Consequently, exact M05.4 A+B+C input, output, total, request count, per-holdout totals and whole-attempt maximum are all `UNKNOWN`. No missing quantity is estimated. The stored trace contradicts a zero-semantic-repair characterization: its own execution manifest classifies structured repairs as `UNKNOWN_NOT_INSTRUMENTED`, and the two B retry markers require at least a repair chain to have occurred.

## Exact reconstructable B subset

For 78 B stage records with no repair chain, the frozen source/prompt construction and stored raw response support an exact local token reconstruction. All counts below are content-token counts using the frozen tokenizer; they are a lower-bound subset, not whole-attempt totals.

| Measure | Input | Output | Total |
| --- | ---: | ---: | ---: |
| Records | 78 | 78 | 78 |
| Minimum | 701 | 93 | 1,086 |
| Median | 1,263.5 | 483 | 1,669 |
| P95 | 2,198 | 671 | 2,814 |
| Maximum | 2,406 | 770 | 3,008 |
| Sum | 105,687 | 34,634 | 140,321 |

The maximum observed exact B request was `3,008` tokens, far below the theoretical 131,072-token state bound. This is empirical behavior only; it does not narrow the frozen structural bound.

| B call position | Stage | Exact records | Max input | Max output | Max total |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | UNDERSTAND | 7 | 1,035 | 524 | 1,558 |
| 2 | ATTACK | 8 | 1,350 | 556 | 1,906 |
| 3 | ALTERNATIVES | 8 | 903 | 588 | 1,491 |
| 4 | SYNTHESIZE | 8 | 2,381 | 697 | 2,933 |
| 5 | REALITY_CHECK | 7 | 1,293 | 770 | 1,950 |
| 6 | FINAL_REVIEW | 8 | 1,531 | 161 | 1,635 |
| 7 | ALTERNATIVES | 8 | 891 | 594 | 1,470 |
| 8 | SYNTHESIZE | 8 | 2,406 | 644 | 3,008 |
| 9 | REALITY_CHECK | 8 | 1,316 | 671 | 1,987 |
| 10 | FINAL_REVIEW | 8 | 1,592 | 231 | 1,766 |

Exact B subtotals by holdout: `IDEA-01=16,634` (incomplete repair chain), `IDEA-02=17,005`, `IDEA-03=17,893`, `IDEA-04=15,068` (incomplete repair chain), `IDEA-05=18,739`, `IDEA-06=17,213`, `IDEA-07=18,288`, `IDEA-08=19,481`.

## Free-account descriptive comparison

Authenticated Free limits: TPM=8,000, TPD=200,000, RPD=1,000, RPM=30.

- Exact B-subset maximum request: `3,008` = `37.60%` of Free TPM; descriptive headroom `4,992`.
- Exact B-subset total: `140,321` = `70.16%` of Free TPD; descriptive headroom `59,679`.
- Exact B-subset request count: `78` = `7.80%` of Free RPD; descriptive headroom `922`.
- `WOULD_M05_4_HAVE_FIT_CURRENT_FREE_LIMITS=UNKNOWN_TRACE_INCOMPLETE`.
- `LIMIT_THAT_WOULD_HAVE_FAILED=UNKNOWN`.

These values show that the recovered B records were not close to the per-request TPM limit, while B alone consumes most of daily Free TPD. They neither establish whole-attempt fit nor predict M05.5R1.

## Input-size-only comparison

M05.4 source input token counts: `IDEA-01=31`, `IDEA-02=26`, `IDEA-03=43`, `IDEA-04=32`, `IDEA-05=34`, `IDEA-06=43`, `IDEA-07=23`, `IDEA-08=42` (range 23–43).

Sealed R1 raw-input token counts: `H01=49`, `H02=53`, `H03=56`, `H04=43`, `H05=51`, `H06=49`, `H07=42`, `H08=51`.

`R1_INPUTS_WITHIN_M05_4_RANGE=MIXED`. This is only a length comparison; it makes no claim about semantic difficulty or output length.

## Future guard assessment

`CURRENT_PRE_REQUEST_CAPACITY_GUARD_SUFFICIENT=NO` and `GUARD_CHANGE_REQUIRED=YES`.

The capacity-design document specifies a desired per-request policy, but the available harness has a broad initial-envelope gate only. It does not contain executable enforcement that serializes each next request, locally counts its exact tokens, checks per-request Free admissibility, maintains an exact cumulative daily ledger, and aborts before dispatch as `ABORTED_CAPACITY`. No change was made in this analysis mission.

## Invariants and conclusion

- `FAILED_FREE_ATTEMPT_MAY_REQUIRE_NEW_HOLDOUT_SET=YES`.
- `HARD_BOUND_STILL_VALID=YES`.
- `EMPIRICAL_HISTORY_IS_GUARANTEE=NO`.
- `VERDICT=TRACE_INCOMPLETE`.

The evidence is enough to reject an assertion that Free fit is proven or obviously safe. It is not enough to claim historical Free incompatibility either. The missing A/C payloads, unrecorded repair-chain inputs and absent transport instrumentation leave the counterfactual undecidable without inventing data.
