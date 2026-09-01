# PFI-R0 — Idea Evolution Engine Readiness Audit

**MISSION_ID:** `PFI-R0-IDEA-EVOLUTION-ENGINE-READINESS-AUDIT-001`  
**MISSION_CLASS:** `RECEIVER_READINESS_AUDIT`  
**MODE:** `READ_ONLY_ANALYSIS`  
**AUDITED_REPOSITORY:** `ProjetoFioIedeias` at `26a2a67f812bedacf0f1b43cf2700b7ae3accf63` (`main`)  
**DATE:** 2026-09-01  
**DECISION_DELTA:** `FOUND_CURRENT_STATE_DRIFT_AND_BRIDGE_BOUNDARY_GAPS`

## Executive verdict

**VERDICT: `NEEDS_REFINEMENT`**

The IEE is a materially implemented, evidence-oriented idea-evolution receiver. It already has a useful Simple Loop, a Lean L1 path, typed stage outputs, source anchoring, candidate isolation, provenance-aware experiment artifacts, deterministic evidence-admission primitives, donor/scar memory, and typed IEE/FioOS boundary contracts.

It is **not** ready to integrate with FioOS at runtime. The existing protocol is a protected specification and a set of offline contracts, not a bridge. In particular, it has no external-input ingress boundary, no bridge executor, no durable integration of `EvidenceEnvelope` into the live idea state, and no proof that a FioOS-originated payload can be admitted without changing IEE state or authority incorrectly.

The smallest useful outcome of this audit is therefore preservation of the readiness map and a correction to the next decision: **do not implement the bridge; reconcile the M05.5 quarantine in the IEE's live operational state first.**

## Scope and evidence discipline

This audit inspected the repository's current Git state, Python source, tests, prompts, experiment records, contracts, and canonical documents. It did not modify code, prompts, experiments, FioOS, authority, or runtime configuration.

### External E10 package

The E10 evidence package was read as a **source-bound external claim**. Its narrow result is useful:

> A foreign `PROPOSAL_ONLY` idea, including nested authority-looking declarations, did not change the tested FioOS receiver decision in the E10 controls.

For this IEE audit, its status is `OBSERVED_EXTERNAL_EVIDENCE_PACKAGE`, not an IEE proof of a runtime bridge. E10 itself explicitly excludes proof of bridge runtime, external-input parsing, schema compatibility, or integration authorization. Therefore the field `BRIDGE_PROVEN=YES` must be read only as the narrow idea-to-evidence boundary claim, never as `IEE_FIOOS_RUNTIME_BRIDGE_PROVEN`.

### Source binding result

| Artifact | Observed SHA-256 | Status |
|---|---|---|
| Repository source `docs/intelligence/FIOOS-TO-FIOIDEIAS-KNOWLEDGE-TRANSFER.md` | `b493cd30883f952ff1503b771194aa552a1d11c813855893318ad3fb67b6d4fb` | `CONFIRMED_SOURCE_MATCH` |
| Attached Downloads copy | `b57578b25a3b5554df31c2e05b5d08e41f08c581569482a2111a25dff6401e0b` | `SOURCE_MISMATCH`; not used as the declared exact source |
| FioOS E10 evidence artifact | `5a094f3cff00d441c8f2da58f839a780dd433f136f238614ec233df50cf4a323` | Read as external evidence package |

This follows the receiver's own rule: a useful document is not silently elevated into canonical source, requirement, truth, or authority.

## Repository state

| Item | Observed state | Evidence status |
|---|---|---|
| Branch / HEAD | `main` / `26a2a67…` | `OBSERVED` |
| Context validator | pass | `PROVEN` |
| Intelligence validator | pass; `FOUNDATION_READY = TRUE` | `PROVEN` |
| Test suite | `198 passed`, one Pytest collection warning | `PROVEN` |
| M05.4 | closed; C remains `LEADING_CANDIDATE_PROVISIONAL_DEFAULT` | `OBSERVED` |
| M05.5 Attempt 001 | quarantined and `INVALID_PRIMARY_REPLICATION` | `OBSERVED` |
| Current-state / queue text | still describes M05.5 as pre-execution / M05.4 as next work | `CONTRADICTION_FOUND` |

The M05.5 quarantine is correct: its audit found pre-primary semantic calls, reuse of the attempt identity, holdout contamination, and provider quota interference. This is an **experiment-execution failure**, not evidence that Lean L1 failed to replicate. It must not be interpreted as an outcome of the product hypothesis.

The test command required explicit exclusion of six inaccessible `pytest-cache-files-*` directories. No directory was deleted. This is a local test-collection hygiene issue, not a product finding.

## Current engine summary

The implemented engine operates in three practical layers:

1. **Simple Loop:** typed `UNDERSTAND → ATTACK/CRITIQUE → ALTERNATIVES → SYNTHESIZE → REALITY_CHECK → FINAL_REVIEW`, persisted per run with traceable stage artifacts.
2. **Lean L1 / FioED:** source-anchored first pass, deterministic Early Epistemic Gate, bounded focused escalation, decision-delta and epistemic-rent records, incubation and reality-boundary primitives.
3. **Governance perimeter:** Pydantic contracts, model-routing/cost controls, explicit candidate versus core separation, experiment manifests, blind human-review packets, donor catalog, and an IEE/FioOS protocol specification.

The engine is therefore more than documentation and more than a chat pipeline. Its gap is not lack of concepts; it is that some of the strongest concepts exist as offline contracts or isolated components rather than one durable, end-to-end `IdeaGenome` runtime.

## Material findings

| ID | Finding | Disposition | Scope | Evidence |
|---|---|---|---|---|
| F-01 | Typed stage contracts, deterministic final gates, and persisted run traces provide a real minimal evolution loop. | `KEEP` | `NEEDED_FOR_FIOIDEIAS_ITSELF` | `PROVEN` |
| F-02 | `CORE`, `DERIVED`, `CANDIDATE`, `DEFERRED`, and `REJECTED` are explicit in state/contracts; candidate extensions are rendered separately from the core. | `KEEP` | `NEEDED_FOR_FIOIDEIAS_ITSELF` | `PROVEN` |
| F-03 | `SourceAnchor`, grounding checks, and anti-accretion controls prevent models from silently claiming human authority. | `KEEP` | `NEEDED_FOR_FIOIDEIAS_ITSELF` | `PROVEN` |
| F-04 | Lean L1's early gate makes extra inference conditional on a typed reason and preserves normative choices for humans. | `KEEP` | `NEEDED_FOR_FIOIDEIAS_ITSELF` | `PROVEN` |
| F-05 | `EvidencePassport`, frozen `TestabilityBinding`, and `EvidenceAdmissionGate` are strong receiver-native reality-boundary mechanisms. | `KEEP` | `NEEDED_FOR_FIOIDEIAS_ITSELF` | `PROVEN_OFFLINE` |
| F-06 | Donor Arsenal, donor manifest, negative knowledge, and reopen conditions preserve paid uncertainty without treating donors as authority. | `KEEP` | `NEEDED_FOR_FIOIDEIAS_ITSELF` | `PROVEN_STRUCTURALLY` |
| F-07 | Controlled A/B/C experiments, raw manifests, blind packets, and human-review freeze are valuable producer/evaluator separation mechanisms. | `KEEP` | `NEEDED_FOR_FIOIDEIAS_ITSELF` | `PROVEN`, with M05.5 attempt quarantined |
| F-08 | The model catalog, routing hash, bounded repair, and no-silent-fallback behavior appropriately govern inference cost and provenance. | `KEEP` | `NEEDED_FOR_FIOIDEIAS_ITSELF` | `PROVEN` |
| F-09 | `InvestigationIntent`, `FioOSMissionPlan`, `ExecutionIdentityBinding`, `EvidenceEnvelope`, and `EpistemicUpdate` enforce the intended conceptual split. | `KEEP` | `NEEDED_FOR_FIOOS_BRIDGE` | `PROVEN_OFFLINE` |
| F-10 | Current-state and queue documents have not incorporated the M05.5 quarantine now committed on `main`. | `MISSING` | `NEEDED_FOR_FIOIDEIAS_ITSELF` | `OBSERVED` |
| F-11 | The runnable product state is `SimpleIdeaState`; no executable `IdeaGenome` plus all-or-nothing `GenomeValidator` is wired into the loop. | `MISSING` | `NEEDED_FOR_FIOIDEIAS_ITSELF` | `OBSERVED` |
| F-12 | Tension preservation is doctrinal and partially represented as strings/ambiguities, but no first-class runtime `TensionRecord` was found. | `MISSING` | `NEEDED_FOR_FIOIDEIAS_ITSELF` | `OBSERVED` |
| F-13 | `Requirement` and `Decision` do not yet have first-class runtime records; separation from ideas is mainly enforced by ontology/provenance and policy. | `MISSING` | `NEEDED_FOR_FIOIDEIAS_ITSELF` | `OBSERVED` |
| F-14 | Lineage and negative knowledge have typed records, but there is no demonstrated durable store/retrieval path shared by every production loop. | `ADAPT` | `NEEDED_FOR_FIOIDEIAS_ITSELF` | `OBSERVED` |
| F-15 | `EvidenceEnvelope` and `EpistemicUpdate` are typed, but no ingress, authenticity verification, admission-to-state flow, or bridge runner connects them to the live loop. | `MISSING` | `NEEDED_FOR_FIOOS_BRIDGE` | `OBSERVED` |
| F-16 | The E10 package demonstrates FioOS-side non-escalation for its tested controls; it does not establish IEE-side external-payload parsing or bridge safety. | `DEFER` | `NEEDED_FOR_FIOOS_BRIDGE` | `OBSERVED_EXTERNAL_EVIDENCE_PACKAGE` |
| F-17 | FioOS runtime gateway, leases, secret retrieval, provider selection, budgets, and sandbox enforcement belong to FioOS and must not be copied into IEE. | `REJECT` | `FIOOS_SPECIFIC_DO_NOT_IMPORT` | `PROVEN_BY_BOUNDARY_SPEC` |
| F-18 | A direct FioOS write path into IEE would violate `EvidenceEnvelope != Truth` and `ProposedGenomePatch != AppliedGenomePatch`. | `REJECT` | `FIOOS_SPECIFIC_DO_NOT_IMPORT` | `PROVEN_BY_BOUNDARY_SPEC` |
| F-19 | Multi-agent orchestration, graph runtimes, and broad donor retrieval are not justified as defaults by the current receiver. | `DEFER` | `USEFUL_LATER` | `OBSERVED` |
| F-20 | Restarting a new replication with contaminated M05.5 holdouts would pay twice for the same failure. A future rerun needs new holdouts and a new namespace. | `KEEP` | `NEEDED_FOR_FIOIDEIAS_ITSELF` | `PROVEN_BY_EXECUTION_AUDIT` |

**Counts:** `KEEP=10`, `ADAPT=1`, `MISSING=5`, `DEFER=2`, `REJECT=2`.

## Separation audit

| Separation | Status | Basis |
|---|---|---|
| `IDEA != TRUTH` | `PASS` | claims/evidence classes, source anchors, evidence admission, and explicit model-hypothesis treatment |
| `IDEA != REQUIREMENT` | `PARTIAL` | ontology and false-requirement events exist; first-class requirement record does not |
| `IDEA != AUTHORITY` | `PASS_FOR_CONTRACTS` | `InvestigationIntent` rejects secrets, tool requests, operational authority language; E10 is consistent with this boundary |
| Evidence provenance | `PASS_OFFLINE` | passport, channel, hash, independence, frozen testability binding |
| Negative knowledge | `PARTIAL` | typed records and gate input exist; durable shared retrieval is not established |
| Contradiction support | `PARTIAL` | doctrine and ambiguities exist; no runtime `TensionRecord` object |
| Activation/reopen support | `PARTIAL` | donor and negative-knowledge reopen conditions plus ontology validator; not one durable lifecycle across loops |
| Donor memory | `PASS_STRUCTURALLY` | donor index, manifest, donor intelligence catalog, and scars |
| Duplicate-uncertainty prevention | `PARTIAL` | epistemic rent, stop conditions, and scar rules exist; cross-run retrieval is incomplete |
| Producer/evaluator separation | `PARTIAL` | blind review separates evaluator from condition identity; no general enforced evaluator-role protocol |
| Falsification support | `PASS_OFFLINE` | adversarial tests, negative controls, baseline experiments, and E10's bounded control design |

## Evolution-loop readiness

The conceptual flow is supported:

```text
idea → uncertainty → hypothesis/candidate → investigation request
     → evidence boundary → epistemic interpretation → preserve/reject/evolve
```

It does **not** yet run as one persistent graph with all transitions enforced across sessions. The present runtime is strongest for a bounded single-idea loop and controlled experiments. The full `IdeaGenome` lifecycle remains a target architecture, not a demonstrated runtime capability.

## FioOS bridge readiness

| Capability | Readiness | Reason |
|---|---|---|
| `InvestigationIntent` emission | `READY_AS_TYPED_PROPOSAL` | typed, validated against operational contamination, and covered by boundary tests |
| `EvidencePackage` / `EvidenceEnvelope` receipt | `STRUCTURAL_ONLY` | typed envelope exists, but no authenticated ingress or live admission-to-state flow |
| No FioOS write authority over IEE | `READY_AS_DESIGN_CONSTRAINT` | protocol explicitly prohibits it; no runtime path currently exists |
| Runtime bridge | `NOT_READY` | explicitly not implemented and not earned by E10 |
| Production integration authorization | `NOT_GRANTED` | outside this audit and requires a separate mission and human authority |

The correct eventual topology is one-way data exchange at each step, not shared mutable state:

```text
IEE proposal (no tools, no secrets, no authority)
  → FioOS planning/authorization/execution
  → provenance-bound evidence observation
  → IEE admission and proposed epistemic update
  → deterministic IEE validation and separate human authority where required
```

## Top 10 highest-value gaps

1. Reconcile `CURRENT-STATE.md`, active queue, and context manifest with the committed M05.5 quarantine.
2. Define the decision gate after the quarantined M05.5 attempt before any product or bridge work.
3. Make the `IdeaGenome`/validator boundary real only when the simple-loop receiver has a concrete persistent-state need.
4. Add first-class `TensionRecord` only with a demonstrated receiver case that needs durable disagreement rather than strings.
5. Add first-class requirement and decision records if they are needed to prevent observed lifecycle collapse.
6. Connect negative knowledge and lineage to durable retrieval across runs before adding more reasoning layers.
7. Define a typed, source-bound external evidence ingress boundary before accepting any FioOS envelope.
8. Bind admitted external evidence to one frozen `TestabilityBinding` and a proposed, never automatic, update.
9. Define an independent evaluator policy for material claims beyond experiment blind review.
10. Resolve test-collection hygiene by excluding or relocating inaccessible cache artifacts without deleting user data.

## Good ideas preserved for later

| Idea | Why valuable | Activation condition | Dependencies |
|---|---|---|---|
| Runtime `IdeaGenome` and deterministic patch validator | makes cross-session evolution auditable and atomic | a real persistent lifecycle cannot be represented safely by `SimpleIdeaState` | receiver-specific state transition contract |
| First-class `TensionRecord` | preserves material disagreement without forced synthesis | an actual decision requires competing positions across runs | tension schema and consumer workflow |
| Source-bound external evidence ingress | permits a future FioOS observation without authority leakage | separately authorized bridge-design mission | schema versioning, authentication/provenance, admission gate |
| Durable negative-knowledge retrieval | prevents re-paying known failed uncertainty | multiple runs demonstrably rediscover the same rejected mechanism | scoped index and reopen evaluator |
| Independent evaluator role | makes non-experimental material claims less producer-dependent | a material claim affects a human decision | reviewer evidence contract |

## What must not be copied from FioOS

- Runtime Gateway, operational authority, leases, identity binding, tool dispatch, provider credential access, budgets, and sandbox enforcement.
- The assumption that planning, registration, model access, or a nested payload grants authority.
- Operational retry, scheduling, or remote-execution machinery as a substitute for IEE epistemic state.
- FioOS governance terminology where the IEE already has a smaller native concept.
- Multi-agent topology as a default.

## Recommendation

**IMPLEMENTATION_RECOMMENDED_NOW: `NO`**

**WHY:** The receiver has a valid current product/experiment decision to close first: M05.5 Attempt 001 is quarantined but the operational documents still say pre-execution. A bridge would add a second moving boundary while the current evidence program needs reconciliation. The E10 evidence usefully proves a narrow FioOS-side non-escalation property; it does not reduce the IEE-side bridge gap enough to justify code.

**NEXT_SMALLEST_STEP:** A separately authorized, metadata-only reconciliation of the IEE operational state and queue to record `M05.5_ATTEMPT_001 = INVALID_PRIMARY_REPLICATION / QUARANTINED`, preserving the raw evidence and requiring a fresh holdout set for any future replication. Stop there; do not start M05.5R1 or a bridge-design implementation without a new mission.

## Claim envelope

This audit supports the bounded conclusion that the IEE can already express a source-bound, non-authoritative `InvestigationIntent` and can conceptually receive provenance-carrying evidence. It does not support the claim that IEE and FioOS are runtime integrated, that either can write the other's state, or that E10 authorizes integration.
