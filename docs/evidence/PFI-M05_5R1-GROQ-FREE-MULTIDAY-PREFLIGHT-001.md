# PFI-M05_5R1-GROQ-FREE-MULTIDAY-PREFLIGHT-001

## Result

`HUMAN_API_KEY_LOCAL_SETUP_REQUIRED`.

The authorized local environment has no `GROQ_API_KEY`. The sacrificial pilot was not started: no provider request, source-content read, confirmatory holdout access or reveal access occurred.

## Implemented offline guard

- Exact `HarmonyGptOss` / `o200k_harmony` chat-token count before every dispatch.
- `max_completion_tokens=2048` reserved with `cached_tokens=0` before dispatch.
- Free request/RPM/TPM/block-TDP checks fail closed and emit a pre-dispatch record before transport.
- Hash-chained append-only JSONL ledger with duplicate request identities denied.
- Post-response-only cache/usage capture, system-fingerprint capture and within-block fingerprint-drift stop.
- No transport retry. A 429 is `ABORTED_CAPACITY`, never a treatment/product result.
- Restart-safe block-window state with `NEXT_BLOCK_NOT_BEFORE = last request + 24h + 5m`.
- Pilot entrypoint has no holdout/reveal argument and denies `H01`–`H08` selection.

## Offline verification

`47 passed` across the multiday-guard suite and the existing M05.5R1 capacity, tokenizer and harness suites. Negative controls cover TPM, cache, duplicate/tampered ledger, schedule mutation, 429, retry, backend drift, premature block start and confirmatory/reveal exclusion.

## Sacrificial pilot definition

- Source identifier: `M05.4-ATTEMPT-004-IDEA-08`.
- Classification: `SACRIFICIAL_M05_4_HISTORICAL_NON_CONFIRMATORY`.
- Frozen treatment permutation: `CONDITION_C → CONDITION_B → CONDITION_A`.
- `CONFIRMATORY_VALUE=NO`.

Provider/model/treatments/holdouts/blinding are unchanged. `EXECUTION_TEMPORAL_SCHEDULE_CHANGED=YES` solely for `FREE_TIER_CAPACITY_ISOLATION`; it does not authorize a confirmatory block.

## Minimal human action

Create or select a key for the intended Groq project in the official Groq console, add a Windows user environment variable named `GROQ_API_KEY`, and restart the local Codex/terminal session. Do not place the key in this repository or chat.
