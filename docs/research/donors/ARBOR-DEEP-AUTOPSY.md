---
document_type: DONOR_DEEP_AUTOPSY
schema_version: "1.0"
donor_id: "DONOR-ARBOR"
donor_name: "Arbor"
donor_org: "Renmin University of China / Microsoft Research"
primary_receiver: "Projeto FioIdeias / Idea Evolution Engine (IEE)"
autopsy_status: "DEEP_REVIEW_COMPLETE"
strategy_status: "TRANSPLANT_PLAN_READY_REQUIRES_RECEIVER_EXPERIMENT"
last_verified: "2026-08-27"
donor_snapshot_commit: "531885d9c2c6c409e09230a12b0fa27915ed8d63"
paper_version_reviewed: "arXiv:2606.11926v1 — living technical report"
epistemic_rule: "Donor claims, benchmarks, code comments, issues and LLM-distilled insights are not IEE truth until classified and, where needed, validated in the receiver."
overall_decision: "ADAPT_STRONGLY_SELECTED_MECHANISMS; REJECT_LITERAL_TREE_COPY; REJECT_FULL_RUNTIME_COPY"
iee_relevance: "VERY_HIGH"
implementation_authorized_by_this_document: false
---

# ARBOR — DEEP DONOR AUTOPSY FOR FIOIDEIAS / IEE

> **AUTÓPSIA DE DOADOR — STATUS: ADAPT_STRONGLY_SELECTED_MECHANISMS (Level A / High Value)**
> *Autópsia Profunda de Doador, Ancoragem Epistêmica e Memória Institucional.*

---

## 0. Executive verdict

Arbor is one of the highest-value donors identified so far for the Idea Evolution Engine.

The useful transplant is **not “use Arbor”** and not even “copy its Idea Tree.” The strongest transferable principle is:

> Turn idea evolution from a sequence of rewritten texts into a cumulative, inspectable search state in which hypotheses, evidence, failures, artifacts, interpretations and decisions remain connected across time.

Arbor calls its approach **Hypothesis Tree Refinement (HTR)**. Its architecture combines:

- a long-lived Coordinator that maintains global research strategy;
- short-lived Executors that test one hypothesis at a time;
- a persistent Idea/Hypothesis Tree;
- isolated experiment branches/worktrees;
- factual results and scores;
- distilled insights propagated into future search;
- pruning and retention of failed directions;
- development feedback for iteration;
- held-out evaluation for promotion;
- compact durable state instead of relying on conversation history;
- cross-run experience distillation and recall;
- separate external-knowledge lanes for generating ideas and checking novelty.

This is closely aligned with the direction already emerging in FioIdeias:

```text
HUMAN IDEA
    ↓
PROTECTED INTENT
    ↓
CANDIDATE ALTERNATIVES
    ↓
CRITIQUE / REALITY CHECK
    ↓
EVIDENCE
    ↓
EPISTEMIC UPDATE
    ↓
DECISION
```

However, literal transplantation would import important weaknesses:

1. Arbor's tree is single-parent, while IEE candidates may be legitimate recombinations of several ancestors.
2. Arbor's `insight` is semantic interpretation produced by an LLM; interpretation cannot silently become evidence or causal truth.
3. The Coordinator concentrates proposal, selection, interpretation, pruning and merge decisions.
4. At the reviewed repository snapshot, `merge_threshold` is not mechanically enforced as the documentation implies: an improvement smaller than the threshold produces a warning and can still proceed.
5. When an independent test evaluator is absent, the current merge path can fall back to an LLM-reported `test_score`, explicitly marked unverified.
6. Repeated exposure of held-out scores to the long-lived Coordinator can make the nominal held-out signal part of adaptive search.
7. A historical bug allowed text promising future work to be interpreted as successful completion without a concrete experiment; the reviewed current HEAD contains a fix.
8. A historical incomplete-executor problem motivated stronger `needs_retry`, attempt, stop-reason and resume semantics.
9. Cross-run recurrence is used as a confidence heuristic, but repeated correlated runs are not independent evidence.
10. Arbor's research loop can consume tens of millions of tokens; its lesson is structured spending, not cheapness.

Recommended receiver stance:

- **ADAPT STRONGLY** — evidence-conditioned lineage.
- **ADAPT STRONGLY** — compact persistent research state.
- **ADAPT WITH HARDENING** — insight propagation.
- **ADAPT** — scoped negative knowledge / pruned lessons.
- **ADOPT CONCEPT** — fixed hypothesis during local repair.
- **ADAPT CONCEPT** — global strategy separated from local execution.
- **ADAPT WITH HARDENING** — dev / promotion / sealed evaluation.
- **ADOPT STRONGLY** — independent generation and validation contexts.
- **ADAPT** — cross-run experience memory.
- **ADOPT** — deterministic retrieval before expensive semantic infrastructure.
- **REJECT LITERAL COPY** — universal single-parent tree.
- **REJECT AS AUTHORITY** — LLM-distilled insight as truth.
- **REJECT** — LLM-reported metric as verified held-out evidence.
- **REJECT** — advisory policy disguised as hard gate.
- **REJECT NOW** — full Arbor runtime inside IEE.

The deepest positive Arbor lesson is:

> **The tree is not valuable because it is a tree. It is valuable because accumulated evidence constrains future search.**

The deepest negative lesson is:

> **A policy written in prompts, documentation or tool descriptions is not an invariant until the state transition mechanically enforces it.**

---

# 1. Receiver uncertainties that justify this autopsy

This document is receiver-oriented. It studies Arbor only where Arbor can reduce uncertainty or engineering work in FioIdeias.

## 1.1 How should one human idea evolve into multiple competing candidates without losing history?

An overwrite-only process:

```text
IDEA V1
↓
rewrite
IDEA V2
↓
rewrite
IDEA V3
```

loses:

- ancestry;
- mutations;
- rejected paths;
- what criticism caused each change;
- what evidence justified promotion;
- what was discarded;
- which decision changed.

Arbor has already paid for part of this problem with a persistent hierarchical hypothesis state.

## 1.2 How should failures reduce future search?

IEE already has concepts such as `REJECTED`, `DEFERRED`, contradiction and provenance.

The remaining question is:

> How does a failed candidate become a constraint on future candidates rather than a forgotten paragraph?

Arbor's pruned lessons directly address this.

## 1.3 How should evidence become reusable memory?

Raw evidence is too detailed for every future context.
A free-form summary can create false causal explanations.

Arbor separates experiment result from distilled insight, which is valuable, but IEE must strengthen the epistemic typing.

## 1.4 How can long investigations avoid transcript growth?

Arbor makes the tree the durable state and provides executors concise relevant context.

This directly supports:

> Conversation is cache. Repository is durable project memory.

## 1.5 How should evaluation avoid self-deception?

Arbor's dev/held-out design is useful, and its current implementation scars reveal why we need stronger enforcement.

## 1.6 When is branching search worth its cost?

Arbor demonstrates that cumulative tree refinement can add value under measurable optimization tasks. Its token usage simultaneously warns that branching is expensive.

---

# 2. What Arbor actually is

Arbor is an open-source autonomous research system introduced in 2026 by researchers from Renmin University of China and Microsoft Research.

The paper frames the problem as **Autonomous Optimization (AO)**:

```text
initial artifact
+
natural-language objective
+
development evaluator
+
held-out evaluator
+
budget
↓
autonomous experimentation
↓
best verified artifact
+
persistent hypothesis tree
```

This fit matters.

Arbor is strongest where:

- there is an artifact that can change;
- experiments can be executed;
- an objective can be evaluated;
- a development signal exists;
- a separate signal can test transfer.

FioIdeias is broader. A vague human idea often begins before executable artifacts, clean metrics or evaluation splits exist.

Therefore:

```text
ARBOR = HIGH-VALUE MECHANISM DONOR
ARBOR != IEE REPLACEMENT
```

---

# 3. Architecture

```text
HUMAN OBJECTIVE
       │
       ▼
LONG-LIVED COORDINATOR
       │
       ├── observe global state
       ├── ideate
       ├── select frontier
       ├── dispatch experiments
       ├── interpret results
       ├── propagate insights
       ├── merge / prune
       └── stop
              │
              ▼
       HYPOTHESIS TREE
              │
       selected hypothesis
              ▼
SHORT-LIVED EXECUTOR
              │
       isolated worktree
              │
       implementation
              │
       development evaluation
              │
       structured evidence
              ▼
       COORDINATOR / TREE
```

The useful architectural separation is:

```text
GLOBAL STRATEGY != LOCAL EXECUTION
```

The Executor should make one local hypothesis real and return evidence, not silently redefine the whole research objective.

---

# 4. Hypothesis Tree Refinement

The paper models research nodes around:

```text
Hypothesis
Insight
Metadata
```

The current open-source implementation is richer:

```text
id
parent_id
children_ids
depth

hypothesis
status

insight
result
score
score_split
test_score
code_ref
related_work
grounding

eval_status
stop_reason
attempt
```

Current operational states include:

```text
pending
running
done
needs_retry
merged
pruned
```

Persistence uses:

```text
JSON = canonical machine state
Markdown = human-readable view
```

This dual representation is a strong donor concept for IEE.

---

# 5. Three roles of Arbor's tree

## 5.1 Search frontier

The tree shows which directions are:

- pending;
- active;
- completed;
- merged;
- pruned.

## 5.2 Long-term memory

It preserves:

- hypotheses;
- success;
- failure;
- score;
- artifact reference;
- related work;
- grounding;
- interpretation.

## 5.3 Audit trail

It allows reconstruction:

```text
why was this tried?
↓
which parent produced it?
↓
what artifact implemented it?
↓
what happened?
↓
what lesson was extracted?
↓
what decision followed?
```

For FioIdeias, this three-role model matters more than the literal tree data structure.

---

# 6. Depth carries semantic meaning

Arbor uses depth as refinement granularity:

```text
near root
=
broad direction

deeper
=
concrete intervention
```

Receiver example:

```text
ROOT — clarify vague ideas
├── structured questioning
│   ├── adaptive questioning
│   └── fixed Socratic sequence
└── visual decomposition
    ├── mind map
    └── dependency canvas
```

This is useful, but IEE must allow recombination across branches.

---

# 7. Arbor cycle

Conceptually:

```text
OBSERVE
↓
IDEATE
↓
SELECT
↓
EXPERIMENT / DISPATCH
↓
BACKPROPAGATE
↓
DECIDE
```

### Observe
Read compact research state, tree shape, global insights, failed paths and validated findings.

### Ideate
Propose candidates grounded in current evidence and known failure classes.

### Select
Balance exploitation of promising branches with exploration of alternatives.

### Experiment
Send one hypothesis to an isolated Executor.

### Backpropagate
Convert results into lessons that influence ancestors/siblings/future nodes.

### Decide
Continue, prune, merge or stop.

---

# 8. Donation 1 — preserve lineage instead of overwriting

IEE should move from:

```text
IDEA → rewritten IDEA → rewritten IDEA
```

toward:

```text
HUMAN ROOT
├── Candidate A
│   ├── A1
│   └── A2
├── Candidate B
└── Candidate C
```

This permits questions such as:

- Which mutation introduced this feature?
- What evidence produced this candidate?
- Which criticism caused the branch?
- Why was a branch rejected?
- What changed when it reopened?
- Which candidate inherited speculation?
- Which human/evidence authority justified promotion?

### Decision
**ADAPT STRONGLY**

But use a lineage graph / multi-parent support rather than literal single-parent tree.

Candidate structure:

```text
IdeaLineageNode
├── node_id
├── parent_ids[]
├── originating_operation
├── proposal
├── ontology_state
├── authority_basis
├── authority_proof_ref
├── evidence_refs[]
├── factual_result
├── interpretation_refs[]
├── decision_delta
├── status
├── reopen_condition
└── cost_record
```

---

# 9. Donation 2 — evidence-conditioned search

The strongest mechanism is:

```text
EXPERIMENT
↓
EVIDENCE
↓
LESSON
↓
FUTURE SEARCH IS DIFFERENT
```

This is much stronger than:

```text
new round
↓
new brainstorm
```

Receiver rule:

> **A new variation should identify what decision-relevant delta from existing evidence justifies exploring it.**

This is how an investigation accumulates intelligence rather than merely accumulating tokens.

---

# 10. Donation 3 — pruned lessons as negative knowledge

Arbor feeds explicit pruned lessons into later ideation and warns against re-proposing a failed mechanism without explaining what changed.

This directly implements part of:

> DO NOT PAY TWICE FOR THE SAME UNCERTAINTY.

But FioIdeias needs richer negative state than simple `pruned`.

Proposed:

```text
NegativeKnowledgeRecord
├── record_id
├── proposition_or_mechanism
├── failure_class
├── evidence_refs
├── scope
├── conditions_at_failure
├── affected_nodes
├── confidence
├── what_not_to_repeat
├── what_remains_unknown
└── reopen_condition
```

A branch may fail because:

- the mechanism is false;
- implementation was bad;
- evidence was inconclusive;
- authority was missing;
- context was wrong;
- dependency was unavailable;
- cost was unjustified.

These should not be collapsed into one permanent ban.

### Decision
**ADAPT WITH EPISTEMIC TYPING**

---

# 11. Donation 4 — fixed hypothesis during local repair

Arbor's executor design keeps the hypothesis fixed while repairing implementation.

This prevents:

```text
test X
↓
X fails
↓
quietly mutate into Y
↓
Y succeeds
↓
claim X succeeded
```

Receiver principle:

> **LOCAL REPAIR MUST NOT SILENTLY MOVE THE HYPOTHESIS.**

If the claim changes, create a new candidate identity.

### Decision
**ADOPT CONCEPT STRONGLY**

---

# 12. Donation 5 — compact state, not transcript memory

Arbor makes persistent research state the durable memory rather than chat history.

This aligns exactly with FioIdeias:

```text
conversation = working cache

IdeaGenome
Lineage
Evidence
Decisions
Tensions
Rejected knowledge
=
durable memory
```

### Decision
**ADOPT STRONGLY AS PRINCIPLE**

---

# 13. Donation 6 — insight propagation

The Arbor paper reports an important ablation on MLE-Bench Lite:

```text
Full Arbor               81.82% Any Medal
without tree             63.64%
without insight feedback 54.54%
```

All variants reportedly produced valid submissions.

The key lesson is not merely “trees help.”

It is:

> **Hierarchy without evidence-to-learning semantics can become only a filing system.**

The reported `without insight feedback` result suggests the semantic lesson propagated from previous experiments contributed materially inside the donor setting.

Status:

```text
REPORTED_BY_PAPER
NOT IEE PROOF
```

---

# 14. Critical hardening — insight is not evidence

Arbor allows an LLM to explain *why* an experiment succeeded or failed.

Example:

Observed:

```text
score 60 → 64
```

Inferred:

```text
"the gain came from reducing cognitive load"
```

These are not the same epistemic object.

IEE should use:

```text
EvidenceObservation
├── what happened
├── evidence/source
├── measurement
└── artifact_ref
```

and separately:

```text
InsightRecord
├── insight_id
├── statement
├── source_node_ids
├── evidence_refs
├── type
│   ├── OBSERVATION_SUMMARY
│   ├── INFERENCE
│   ├── CAUSAL_HYPOTHESIS
│   ├── CONSTRAINT
│   └── HEURISTIC
├── claim_status
├── confidence
├── counter_explanations
├── scope
├── created_by
└── validation_needed
```

Canonical rule:

> **DISTILLED INSIGHT MAY GUIDE SEARCH. IT MAY NOT SILENTLY BECOME PROVEN CAUSAL TRUTH.**

### Decision
**ADAPT WITH HARDENING**

---

# 15. Donation 7 — strategy and local execution are different scopes

Arbor uses a persistent coordinator and ephemeral/local executors.

IEE does not need to copy the agent count.

The transferable rule is:

```text
GLOBAL EPISTEMIC STRATEGY
!=
LOCAL TASK EXECUTION
```

A local worker may:

```text
search
critique
test
derive
compare
```

but should not automatically:

```text
rewrite human intent
promote candidate to core
erase rejected alternatives
rewrite project memory
```

### Decision
**ADAPT CONCEPT**

---

# 16. Donation 8 — isolated experiment artifacts

Each Arbor experiment can live in an isolated git worktree.

This is valuable because experiments become:

- attributable;
- reversible;
- parallel-safe;
- non-destructive;
- artifact-linked.

IEE does not need this for every cognitive operation today.

It becomes useful later when candidates produce:

```text
prototype
code
prompt
workflow
design
evaluation harness
```

### Decision
**DEFER IMPLEMENTATION / ADOPT PRINCIPLE**

---

# 17. Donation 9 — development vs promotion evidence

Arbor conceptually separates:

```text
DEV SIGNAL
=
allowed to influence search

HELD-OUT SIGNAL
=
used for promotion
```

This is directionally excellent.

But its implementation provides several high-value scars showing why FioIdeias should use a stronger form.

Proposed IEE model:

```text
DEV
=
freely informs evolution

PROMOTION
=
independent + budgeted
used for bounded admission

SEALED
=
revealed only after the relevant search policy stops
```

---

# 18. SCAR-ARBOR-001 — held-out is not truly sealed under repeated adaptive use

The Coordinator can observe successive held-out promotion outcomes and then choose later hypotheses based on the updated trunk/history.

Conceptually:

```text
candidate 1
→ held-out score
→ coordinator learns

candidate 2
→ held-out score
→ coordinator learns

candidate 3
...
```

Executors may not see raw test data, yet the test score gradually participates in optimization.

This risk is explicitly identified in repository issue #58 and is consistent with the reviewed merge workflow.

Epistemic status:

```text
ADAPTIVE_HOLDOUT_RISK = STRONG_INFERENCE
MEASURED_OVERFITTING_CAUSED_BY_THIS = NOT_PROVEN
```

### Receiver adaptation

```text
DEV
PROMOTION
SEALED
```

with:
- query budgets;
- evaluator identity;
- provenance;
- append-only evaluation records;
- one-time or strictly controlled sealed reveal.

---

# 19. SCAR-ARBOR-002 — documented margin gate is not currently a hard gate

This is one of the highest-value findings of the autopsy.

Arbor documentation describes a configurable margin-based merge gate.

But current reviewed `GitMergeBranchTool` logic:

```text
if candidate fails to improve trunk:
    reject

if candidate improves,
but improvement < merge_threshold:
    warn
    proceed
```

Therefore:

```text
DOCUMENTED_GATE != ENFORCED_GATE
```

Receiver rule:

> **Critical policy must be encoded in the state transition and tested adversarially.**

This directly reinforces what FioIdeias learned with R5:

```text
MODEL RECOMMENDATION != FINAL STATUS AUTHORITY
```

### Decision
**ADOPT SCAR AS CANONICAL WARNING**

---

# 20. SCAR-ARBOR-003 — unverified LLM-reported test score fallback

At the reviewed snapshot, if no independent `eval_cmd_test` exists, Arbor can fall back to a model-reported test score and explicitly logs that it is not independently verified.

Transparency is good.
Using the value as held-out proof is not.

Receiver rule:

```text
MODEL_REPORTED_METRIC != VERIFIED_PROMOTION_EVIDENCE
```

If independent evidence is absent:

```text
UNKNOWN
or
HUMAN_REVIEW_REQUIRED
```

not verified promotion.

### Decision
**REJECT DONOR BEHAVIOR**

---

# 21. SCAR-ARBOR-004 — future-work prose was once treated as completion

Repository issue #59 documented a case where a model response like:

```text
"I will test these approaches next."
```

could end the run as `finished` even when:

```text
no Executor ran
no experiment was scored
```

The latest reviewed commit:

```text
531885d9c2c6c409e09230a12b0fa27915ed8d63
```

contains:

```text
fix(agent): continue sentence-final future work
```

Therefore classify this as:

```text
HISTORICAL_SCAR
FIX_PRESENT_AT_REVIEWED_HEAD
```

Receiver rule:

> **PROMISED FUTURE ACTION != COMPLETION**

Completion needs a concrete evidence/state condition.

---

# 22. SCAR-ARBOR-005 — incomplete Executor previously looked terminal

Issue #2 documented max-turn/null-score execution that could lose expensive work and look completed.

Current Arbor code now contains:

```text
needs_retry
eval_status
stop_reason
attempt
```

and the repository contains resume-related tests.

We should not overclaim that every recovery edge is solved, but the hardening direction is valuable.

Receiver statuses should distinguish:

```text
COMPLETED
FAILED
SKIPPED
INTERRUPTED
NEEDS_RETRY
INCONCLUSIVE
```

Never:

```text
NO RESULT → DONE
```

### Decision
**ADOPT STRONGLY**

---

# 23. SCAR-ARBOR-006 — strict single-parent lineage loses recombination

A human idea can combine two legitimate branches:

```text
A = Socratic questioning
B = visual decomposition

C = Socratic + visual decomposition
```

C derives materially from both A and B.

A strict tree must choose one parent and loses provenance.

### Receiver adaptation

Use:

```text
parent_ids[]
```

or explicit:

```text
derived_from[]
```

This creates DAG-like lineage where needed.

Status:

```text
STRONG RECEIVER INFERENCE
REQUIRES EXPERIMENT
```

---

# 24. SCAR-ARBOR-007 — pruning can overgeneralize

Arbor recursively prunes a subtree.

For IEE, failure must preserve scope.

A branch may fail because:

- idea false;
- implementation weak;
- dependency missing;
- evidence insufficient;
- context changed;
- budget too low;
- human rejected it for preference reasons.

Canonical rule:

> **NEGATIVE KNOWLEDGE REQUIRES SCOPE + REOPEN CONDITIONS.**

### Decision
**ADAPT, DO NOT COPY**

---

# 25. SCAR-ARBOR-008 — recurrence is not independence

Arbor cross-run recall ranks findings seen in several sessions more highly.

This is a useful attention heuristic.

But:

```text
same model
same prompt
same evaluator
same data
same bias
```

can reproduce the same false claim many times.

Therefore:

```text
RECURRENCE != INDEPENDENT CONFIRMATION
```

IEE should track:
- model/provider independence;
- evidence independence;
- dataset independence;
- evaluator independence;
- shared ancestry.

### Decision
**ADAPT WITH PROVENANCE DIVERSITY**

---

# 26. SCAR-ARBOR-009 — Coordinator concentration

The Arbor Coordinator can:

- observe;
- ideate;
- select;
- interpret;
- prune;
- merge;
- stop.

This simplifies orchestration but concentrates semantic power.

IEE already has a stronger constitutional rule:

> **PRODUCER != SOLE APPROVER**

The strategic model may propose state changes, but critical transitions require:
- deterministic invariants;
- admissible evidence;
- authority proof;
- human decision where normative authority is required;
- independent review where useful.

### Decision
**REJECT COORDINATOR AS SEMANTIC GOD OBJECT**

---

# 27. SCAR-ARBOR-010 — human timeout cannot create protected authority

Arbor interaction modes may allow the agent to proceed on its best assumption if a user does not respond.

That may be practical for benchmark autonomy.

In IEE:

```text
optional direction timeout
→ perhaps default

protected core decision timeout
→ MUST NOT manufacture USER authority
```

Canonical rule:

> **TIMEOUT MAY STOP PROGRESS. IT MUST NOT CREATE HUMAN AUTHORITY THAT NEVER EXISTED.**

---

# 28. Donation 10 — two independent external-knowledge lanes

This is one of Arbor's most elegant ideas.

Current Arbor documentation separates:

```text
GROUNDED IDEATION
=
external knowledge used to shape a new candidate

NOVELTY AUDIT
=
fresh independent search used to assess prior art
```

The two lanes intentionally do not share the same fetched text.

The purpose is to prevent:

```text
same source inspires idea
AND
same source certifies novelty
```

Receiver principle:

> **SOURCE_USED_TO_GENERATE_CANDIDATE != SOLE_SOURCE_ALLOWED_TO_VALIDATE_CANDIDATE**

This is structurally similar to IEE's authority rule:

```text
MODEL CLAIMING USER_EXPLICIT
!=
PROOF OF USER_EXPLICIT
```

### Decision
**ADOPT STRONGLY AS PRINCIPLE**

---

# 29. Donation 11 — deterministic retrieval before expensive semantic machinery

Arbor experience recall initially uses cheap deterministic keyword overlap and explicitly leaves embedding/LLM retrieval for later if needed.

This fits FioIdeias Donor Intelligence:

```text
tags / IDs / exact mechanisms
↓
measure misses
↓
semantic retrieval only if deterministic lookup proves insufficient
```

This avoids prematurely building:
- vector DB;
- embeddings pipeline;
- RAG agent;
- semantic router.

### Decision
**ADOPT PRINCIPLE**

---

# 30. Donation 12 — cross-run experience distillation

Current Arbor can create:

```text
EXPERIENCE.md
```

after a run, separating:
- domain-level findings;
- process/meta findings;
- concrete leverage;
- concrete pitfalls.

Future runs may retrieve relevant prior experience.

This independently validates our FioIdeias doctrine:

```text
KNOWN SCARS
PAID UNCERTAINTIES
REUSABLE ENGINEERING MEMORY
```

But IEE must retain:

```text
EXPERIENCE = CANDIDATE PRIOR
EXPERIENCE != INSTITUTIONAL TRUTH
```

### Decision
**ADAPT STRONGLY**

---

# 31. Empirical evidence harvested

Treat every number here as donor evidence, not receiver proof.

## 31.1 Six Autonomous Optimization tasks

The paper reports the best held-out outcome on all six evaluated tasks, spanning:
- model training;
- harness engineering;
- data synthesis.

It reports more than **2.5× average relative held-out gain** versus Codex/Claude Code baselines under matched task interface/resource budget.

Status:

```text
REPORTED_BY_PAPER
```

## 31.2 MLE-Bench Lite

Reported with GPT-5.5:

```text
86.36% Any Medal
```

Status:

```text
REPORTED_BY_PAPER
```

## 31.3 Ablation

Reported:

```text
Full Arbor                  81.82%
without tree                63.64%
without insight feedback    54.54%
```

Status:

```text
REPORTED_BY_PAPER
```

## 31.4 Cross-task transfer

Reported examples:

```text
BrowseComp    45.33 → 67.67
HLE           25.50 → 31.50
DeepSearchQA  61.00 → 69.00
```

Status:

```text
REPORTED_BY_PAPER
```

## 31.5 Token use

The paper reports roughly:

```text
20.12M–43.19M tokens
```

across six completed cost logs.

Interpretation:

```text
NOT:
Arbor is cheap

BUT:
structured cumulative search produced stronger donor outcomes at high but controlled cost
```

---

# 32. What the ablation actually teaches

Weak conclusion:

> trees are good.

Stronger conclusion:

> **A tree without meaningful evidence-to-learning flow may be mostly organization.**

The poor `without insight feedback` result matters because it suggests the real donor value lies in:

```text
EXPERIMENT
↓
LESSON
↓
BETTER NEXT SEARCH
```

not in hierarchy alone.

Canonical IEE reminder:

> **STRUCTURE WITHOUT LEARNING IS FILING.**

---

# 33. Cost lesson — branching must pay epistemic rent

Arbor is not a justification to branch every human idea.

IEE policy candidate:

```text
LOW UNCERTAINTY
+
CLEAR PATH
→ SIMPLE LOOP

MULTIPLE LIVE MECHANISMS
+
DECISION-RELEVANT UNCERTAINTY
+
DISCRIMINATING EVIDENCE POSSIBLE
→ BRANCHING MODE

NO DISCRIMINATING EVIDENCE
→ DO NOT EXPLODE BRANCHES
```

Canonical rule:

> **BRANCHING MUST PAY EPISTEMIC RENT.**

---

# 34. Proposed transplant — HTR-Lite, not Arbor

Do not embed Arbor.

Prototype an IEE-native mechanism tentatively described as:

> **Evidence-Conditioned Idea Lineage**

Potential state:

```text
IdeaLineageGraph
│
├── HUMAN_ROOT
│
├── CandidateNode(s)
│   ├── proposal
│   ├── parent_ids[]
│   ├── ontology_state
│   ├── authority_basis
│   ├── authority_proof_ref
│   ├── claim_status
│   ├── evidence_refs[]
│   ├── factual_result
│   ├── insight_refs[]
│   ├── decision_delta
│   ├── status
│   ├── reopen_condition
│   └── cost
│
├── InsightRecord(s)
├── NegativeKnowledgeRecord(s)
└── EvaluationRecord(s)
```

---

# 35. Proposed IEE node ontology

Arbor states are operational.
IEE states should preserve epistemic meaning.

Candidate states:

```text
PROPOSED
ACTIVE_CANDIDATE
TESTED_SUPPORTED
TESTED_REFUTED
TESTED_INCONCLUSIVE
DEFERRED
REJECTED
SUPERSEDED
PROMOTED_DERIVED
PROMOTED_CORE
```

Important:

```text
TESTED_SUPPORTED
!=
PROMOTED_CORE
```

because:

```text
EVIDENCE != AUTHORITY
```

---

# 36. Proposed `InsightRecord`

```text
InsightRecord
├── insight_id
├── statement
├── source_node_ids[]
├── evidence_refs[]
├── type
├── claim_status
├── confidence
├── counter_explanations[]
├── scope
├── created_by
└── validation_needed
```

Allowed types:

```text
OBSERVATION_SUMMARY
INFERENCE
CAUSAL_HYPOTHESIS
CONSTRAINT
HEURISTIC
```

This is the minimum hardening required before importing Arbor-style backpropagated insights.

---

# 37. Proposed `NegativeKnowledgeRecord`

```text
NegativeKnowledgeRecord
├── record_id
├── mechanism_or_claim
├── failure_class
├── evidence_refs[]
├── scope
├── conditions_at_failure
├── affected_nodes[]
├── what_not_to_repeat
├── what_remains_unknown
└── reopen_condition
```

This is a better IEE transplant than raw `pruned`.

---

# 38. Proposed evaluation architecture

```text
EVALUATION_ROLE = DEV
free to influence iteration

EVALUATION_ROLE = PROMOTION
bounded + independently verified

EVALUATION_ROLE = SEALED
revealed only at the correct final/generalization gate
```

Every evaluation should record:

```text
evaluation_id
candidate_id
role
evaluator_identity
evaluator_version
artifact_hash
score_or_verdict
provenance
independence_status
timestamp
sequence
```

No provenance:

```text
cannot satisfy strong promotion
```

---

# 39. Proposed external-knowledge architecture

## Lane A — Grounding / inspiration

```text
Donor Intelligence
papers
repos
external evidence
↓
candidate generation
```

Record `grounding_refs`.

## Lane B — Independent challenge / validation

Fresh context checks:
- prior art;
- contradictions;
- overlap;
- unsupported claims;
- external evidence.

Canonical rule:

> **GENERATION CONTEXT AND VALIDATION CONTEXT SHOULD NOT BE IDENTICAL WHEN INDEPENDENCE MATTERS.**

---

# 40. Arbor strengthens BEFORE INVENTING, HARVEST

Arbor itself demonstrates several forms of institutional reuse:

```text
external search before/during ideation
+
separate prior-art checking
+
experience distillation
+
cross-run recall
```

This strongly supports our FioIdeias model:

```text
RECEIVER UNCERTAINTY
↓
DONOR LOOKUP
↓
KNOWN MECHANISMS / SCARS / PAID UNCERTAINTIES
↓
ONLY THE REMAINING UNKNOWN BECOMES NEW WORK
```

Closed loop:

```text
EXTERNAL KNOWLEDGE
→ IDEA
→ TEST
→ EXPERIENCE
→ INSTITUTIONAL MEMORY
→ BETTER NEXT IDEA
```

---

# 41. What NOT to copy

1. Full Arbor runtime.
2. Strict single-parent Idea Tree as universal IEE lineage.
3. Tens-of-millions-token search as default behavior.
4. Coordinator as proposer + judge + prune authority + merge authority.
5. LLM-generated causal insight as truth.
6. Recursive `pruned` as permanent universal rejection.
7. Repeated held-out exposure as clean sealed evaluation.
8. Advisory `merge_threshold` described as hard policy.
9. LLM-reported test score as verified evidence.
10. Recurrence count as proof.
11. Timeout as substitute for protected human authority.
12. Worktree machinery before empirical artifact testing exists.
13. Arbor's exact node statuses.
14. Scalar optimization as universal human idea quality.
15. Novelty pressure as a universal objective.

---

# 42. Highest-value mechanisms

| Mechanism | IEE decision |
|---|---|
| Evidence-conditioned lineage | ADAPT_STRONGLY |
| Persistent compact state | ADOPT_STRONGLY |
| Insight propagation | ADAPT_WITH_HARDENING |
| Result vs insight distinction | ADOPT_CONCEPT |
| Negative/pruned knowledge | ADAPT_WITH_SCOPE |
| Fixed hypothesis during repair | ADOPT_CONCEPT |
| Strategy/local execution split | ADAPT_CONCEPT |
| Isolated experiment artifacts | DEFER |
| Dev/promotion/sealed evaluation | ADAPT_WITH_HARDENING |
| Independent grounding/novelty lanes | ADOPT_STRONGLY |
| Cross-run experience | ADAPT |
| Deterministic recall first | ADOPT |
| Recurrence-as-confidence | ADAPT_WITH_INDEPENDENCE |
| Full Arbor runtime | REJECT |

---

# 43. Paid uncertainties harvested

## PU-ARBOR-001
**Question:** Is flat experiment history necessarily sufficient?

**Donor evidence:** no-tree ablation performed worse than full Arbor.

**Status:** REPORTED_BY_PAPER.

**Receiver implication:** do not assume flat history is sufficient for long-horizon branching investigation.

**Remaining IEE uncertainty:** does lineage improve general human idea evolution enough to justify complexity?

## PU-ARBOR-002
**Question:** Is hierarchy alone sufficient?

**Donor evidence:** no-insight-feedback ablation substantially worse than full Arbor.

**Status:** REPORTED_BY_PAPER.

**Receiver implication:** do not build lineage without evidence-to-learning semantics.

## PU-ARBOR-003
**Question:** Can failed experiments become useful future constraints?

**Donor evidence:** pruned lessons are persisted and reinjected into later ideation.

**Status:** PROVEN_AS_DONOR_MECHANISM.

**Receiver implication:** preserve scoped negative knowledge.

## PU-ARBOR-004
**Question:** Should long transcript be primary durable memory?

**Donor design:** no; research state is externalized.

**Status:** PROVEN_AS_DONOR_ARCHITECTURE.

**Receiver implication:** canonical state > conversation.

## PU-ARBOR-005
**Question:** Is a nominal held-out gate automatically safe?

**Answer:** no.

**Evidence:** current protocol allows repeated promotion-score exposure; adaptive reuse risk exists.

**Status:** STRONG_INFERENCE.

**Receiver implication:** introduce promotion budget + sealed evaluation lifecycle.

## PU-ARBOR-006
**Question:** Does documentation equal enforcement?

**Answer:** no.

**Evidence:** current merge path warns below threshold and continues.

**Status:** PROVEN_BY_CURRENT_CODE.

## PU-ARBOR-007
**Question:** Is a model-reported metric independent proof?

**Answer:** no.

**Evidence:** current donor code allows such fallback when independent eval command is absent.

**Status:** PROVEN_BY_CURRENT_CODE.

## PU-ARBOR-008
**Question:** Can promised future work count as completion?

**Answer:** historical bug says yes; current reviewed HEAD contains fix.

**Status:** HISTORICAL_ISSUE + FIX_PRESENT.

## PU-ARBOR-009
**Question:** Does repeated similar experience equal independent confirmation?

**Answer:** not proven.

**Donor mechanism:** recurrence heuristic.

**Receiver implication:** track evidence independence.

## PU-ARBOR-010
**Question:** Is cumulative branching cheap?

**Answer:** no.

**Evidence:** paper cost logs in tens of millions of tokens.

**Status:** REPORTED_BY_PAPER.

---

# 44. Candidate canonical rules harvested

### RULE-ARBOR-01 — EVOLUTION MUST PRESERVE LINEAGE
Meaning-changing refinement creates a new lineage state rather than erasing the parent.

### RULE-ARBOR-02 — LOCAL REPAIR MUST NOT MOVE THE HYPOTHESIS
If the claim changes, create a new candidate identity.

### RULE-ARBOR-03 — INSIGHT IS AN INTERPRETATION LAYER
Observation, result and causal explanation must remain separable.

### RULE-ARBOR-04 — NEGATIVE RESULTS MUST REDUCE FUTURE SEARCH
Failures remain scoped reusable knowledge with reopen conditions.

### RULE-ARBOR-05 — STRUCTURE WITHOUT LEARNING IS FILING
A lineage structure is useful only if evidence improves later decisions.

### RULE-ARBOR-06 — GENERATION EVIDENCE MUST NOT SELF-CERTIFY
The same source/context that shaped a candidate cannot be its sole independent validator.

### RULE-ARBOR-07 — HELD-OUT MUST BE OPERATIONALLY SEALED
A label saying “test” is insufficient if adaptive repeated exposure is permitted.

### RULE-ARBOR-08 — DOCUMENTED GATE != ENFORCED GATE
Critical policy must live in executable transition logic plus tests.

### RULE-ARBOR-09 — MODEL-REPORTED SCORE != VERIFIED SCORE
Unverified metrics cannot satisfy strong promotion evidence.

### RULE-ARBOR-10 — PROMISED ACTION != COMPLETION
Future-work prose does not prove work happened.

### RULE-ARBOR-11 — RECURRENCE != INDEPENDENCE
Repeated conclusions raise attention, not automatic truth status.

### RULE-ARBOR-12 — BRANCHING MUST PAY EPISTEMIC RENT
Use branching only when competing hypotheses and discriminating evidence justify cost.

### RULE-ARBOR-13 — COMPACT STATE BEFORE MORE CONTEXT
Prefer durable typed state over transcript accumulation.

---

# 45. Strategic integration plan for FioIdeias

Do not implement everything now.

The current IEE must first complete its controlled value experiment.

## Phase A — Persist donor knowledge now

Safe immediately:

```text
docs/research/donors/ARBOR-DEEP-AUTOPSY.md
DONOR-ARSENAL.md entry
donor-manifest.json entry
```

No runtime change.

## Phase B — Offline HTR-Lite prototype

After current A/B/C evidence:

Create schemas only:

```text
IdeaLineageNode
InsightRecord
NegativeKnowledgeRecord
EvaluationRecord
```

Use existing historical IEE runs.
No new provider calls required.

Question:

> Can typed lineage reconstruct idea evolution better than the current flat state?

## Phase C — Flat vs lineage experiment

Compare:

```text
A = current Simple Loop
B = Simple Loop + lineage / negative-memory context
```

Same:
- model;
- provider;
- ideas;
- budget.

Measure:
- intent preservation;
- repeated rejected proposals;
- unsupported assumptions;
- speculative accretion;
- useful novelty;
- contradiction rate;
- DecisionDelta;
- tokens;
- human blind preference;
- provenance explainability.

Do not claim benefit before evidence.

## Phase D — Insight typing experiment

Compare:

```text
A = raw result only
B = free-form distilled insight
C = typed evidence-conditioned insight
```

Measure:
- false causal claims;
- useful constraint transfer;
- repeated mistakes;
- later decision quality.

## Phase E — Branching mode admission

Only if evidence supports it:

```text
SimpleLoop = DEFAULT

BranchingResearchMode = CONDITIONAL
```

Admission requires:
- multiple live mechanisms;
- decision-relevant uncertainty;
- meaningful discriminating evidence;
- expected gain exceeding complexity cost.

## Phase F — real artifact testing

Later:

```text
candidate
↓
TestContract
↓
real evidence
↓
typed EpistemicUpdate
↓
lineage transition
```

Only here should Arbor's worktree-style artifact isolation become a serious implementation candidate.

---

# 46. HTR-Lite acceptance criteria

A successful transplant must demonstrate that it:

1. preserves parent/child provenance;
2. supports multi-parent synthesis where needed;
3. keeps original human intent immutable;
4. prevents `MODEL_HYPOTHESIS` from silently becoming core;
5. preserves rejected/deferred alternatives;
6. records evidence/reason for promotion;
7. separates observation from interpretation;
8. carries reopen conditions for negative knowledge;
9. reduces repeated rejected proposals;
10. improves decision-relevant context per token;
11. does not force branching on simple ideas;
12. survives context reset without reconstructing from chat history.

---

# 47. Adversarial tests inspired by Arbor scars

## T1 — False causal insight
Evidence: score improved.
Model says privacy caused it.
Expected: `CAUSAL_HYPOTHESIS`, not `PROVEN`.

## T2 — Rejected branch reappears
Same mechanism, unchanged conditions.
Expected: blocked or explicit counter required.

## T3 — Legitimate reopen
Old branch failed because dependency was absent.
Dependency now exists.
Expected: reopen with changed-condition record.

## T4 — Hidden hypothesis mutation
Worker starts X and finishes Y.
Expected: attribution failure/new candidate.

## T5 — Unverified promotion metric
Model says score=92 without independent evaluator.
Expected: cannot satisfy promotion.

## T6 — Adaptive hold-out exhaustion
Promotion evaluator exceeds query budget.
Expected: further queries blocked; sealed evaluation preserved.

## T7 — Human authority timeout
Protected-core decision awaits human.
Timeout.
Expected: `HUMAN_DECISION_REQUIRED`.

## T8 — Correlated repetition
Same model/evaluator repeats claim five times.
Expected: recurrence increases, independence remains low.

## T9 — Multi-parent synthesis
Candidate combines A+B.
Expected: both ancestors preserved.

## T10 — Future-work completion
Model says “I will validate this next.”
Expected: incomplete.

---

# 48. Donor overlap — why Arbor is not redundant

## IDEAgent
Overlap:
- lineage;
- rejected-history value;
- cumulative refinement.

Arbor adds:
- executable artifact/evidence binding;
- insight backpropagation;
- held-out promotion;
- worktree experiments;
- cross-run experience.

## Magentic-One
Overlap:
- durable progress state;
- failure learning;
- compact memory.

Magentic-One is stronger on:
- stalls;
- replanning;
- progress control.

Arbor is stronger on:
- branching hypothesis structure;
- experiment attribution;
- evidence-conditioned branch refinement.

## Google Co-Scientist
Overlap:
- hypothesis evolution;
- selection;
- iterative refinement.

Arbor adds:
- artifact execution;
- git/evidence links;
- promotion evaluation.

## DCI
DCI provides the hardening Arbor needs:

```text
selected/pruned
!=
all disagreement erased
```

IEE should preserve:
- minority objection;
- residual uncertainty;
- reopen condition.

---

# 49. Arbor + Donor Intelligence

Proposed FioIdeias knowledge cycle:

```text
BEFORE INVENTING, HARVEST
        ↓
grounded donor/external context
        ↓
candidate mechanisms
        ↓
independent challenge / prior-art lane
        ↓
candidate maturation
        ↓
real test
        ↓
typed lesson
        ↓
paid uncertainty / scar memory
        ↓
future receiver-gap lookup
```

Result:

```text
EXTERNAL KNOWLEDGE
→ IDEA
→ TEST
→ EXPERIENCE
→ INSTITUTIONAL MEMORY
→ BETTER NEXT IDEA
```

---

# 50. Why FioIdeias should not depend on Arbor now

Direct dependency would bring:
- provider/runtime complexity;
- git/worktree assumptions;
- high-compute search;
- optimization-specific semantics;
- current evaluation weaknesses;
- single-parent tree;
- coordinator authority concentration.

IEE already has valuable receiver-specific machinery:
- ontology;
- authority proof;
- core/candidate separation;
- Simple Loop;
- Reality Check;
- reconstruction;
- provider routing.

Replacing it with Arbor would discard our own learned constraints.

Decision:

```text
DEPEND_ON_ARBOR = NO
HARVEST_ARBOR = YES
```

---

# 51. Claim-status matrix

| Claim | Status |
|---|---|
| Coordinator + short-lived Executors | PROVEN_BY_PRIMARY_SOURCE_AND_CODE |
| Persistent hypothesis tree | PROVEN_BY_PRIMARY_SOURCE_AND_CODE |
| Tree outside conversation history | PROVEN_BY_CURRENT_CODE |
| Pruned/validated lessons enter later context | PROVEN_BY_CURRENT_CODE |
| Full Arbor outperforms no-tree donor ablation | REPORTED_BY_PAPER |
| Insight feedback materially contributes in donor ablation | REPORTED_BY_PAPER |
| >2.5× average relative held-out gain vs baselines | REPORTED_BY_PAPER |
| Same gain applies to IEE | NOT_PROVEN |
| 20.12M–43.19M token range | REPORTED_BY_PAPER |
| `merge_threshold` fully enforced | FALSE_IN_REVIEWED_CODE |
| Below-threshold improvement may proceed | PROVEN_BY_CURRENT_CODE |
| LLM-reported test score fallback exists | PROVEN_BY_CURRENT_CODE |
| Repeated held-out exposure caused measured donor overfit | NOT_PROVEN |
| Repeated exposure creates adaptive-holdout risk | STRONG_INFERENCE |
| Future-work false-completion bug existed | REPORTED_BY_ISSUE |
| Reviewed HEAD contains fix | PROVEN_BY_COMMIT_HISTORY |
| Incomplete executor issue prompted hardening | ISSUE + CURRENT_CODE_SUPPORT |
| Distilled LLM insight is causal truth | NOT_PROVEN / REJECT_AS_AUTHORITY |
| Recurrence equals independent confirmation | NOT_PROVEN |
| Literal tree is correct universal IEE lineage | NOT_PROVEN |
| Arbor mechanisms are promising IEE donor candidates | STRONG_RECEIVER_INFERENCE / REQUIRES_EXPERIMENT |

---

# 52. Final transplant table

| Arbor mechanism | IEE decision |
|---|---|
| Persistent hypothesis lineage | ADAPT_STRONGLY |
| Single-parent tree | REJECT_LITERAL / EXPERIMENT MULTI-PARENT |
| Depth as granularity | ADAPT |
| Insight backpropagation | ADAPT_WITH_HARDENING |
| Result/insight distinction | ADOPT_CONCEPT |
| Pruned lessons | ADAPT_WITH_SCOPE |
| Fixed hypothesis during repair | ADOPT_CONCEPT |
| Compact state | ADOPT_STRONGLY |
| Coordinator/Executor separation | ADAPT_CONCEPT |
| Git worktrees | DEFER |
| Dev/held-out split | ADAPT_WITH_HARDENING |
| Current merge-threshold behavior | REJECT |
| LLM test-score fallback | REJECT |
| Repeated held-out promotion queries | REPLACE |
| Grounded ideation | ADAPT |
| Independent novelty lane | ADOPT_CONCEPT |
| Cross-run experience | ADAPT |
| Deterministic recall first | ADOPT |
| Recurrence confidence | ADAPT_WITH_INDEPENDENCE |
| Full runtime | REJECT |

---

# 53. Receiver architecture

```text
                    HUMAN IDEA
                        │
                immutable intent
                        │
                        ▼
                   SIMPLE LOOP
                        │
             ┌──────────┴──────────┐
             │                     │
       low uncertainty       branching justified?
             │                     │
             ▼                     ▼
          continue          LINEAGE MODE
                                  │
                       ┌──────────┼──────────┐
                       │          │          │
                    Cand A     Cand B     Cand C
                       │          │          │
                       └──── evidence ───────┘
                                  │
                                  ▼
                         EVIDENCE RECORDS
                                  │
                                  ▼
                          TYPED INSIGHTS
                                  │
                       ┌──────────┴──────────┐
                       │                     │
                negative knowledge    supported lesson
                       │                     │
                       └──────────┬──────────┘
                                  ▼
                        FUTURE SEARCH SPACE
                                  │
                                  ▼
                         promotion candidate
                                  │
                        independent evidence
                                  │
                                  ▼
                           state transition
```

---

# 54. Minimal implementation sequence if receiver evidence earns it

```text
M-ARBOR-1
Persist autopsy + Donor Arsenal entry.

M-ARBOR-2
Schemas only:
IdeaLineageNode
InsightRecord
NegativeKnowledgeRecord

M-ARBOR-3
Replay historical IEE runs into lineage.
No new model calls.

M-ARBOR-4
Measure whether lineage reveals history/contradictions better.

M-ARBOR-5
Controlled flat-vs-lineage experiment.

M-ARBOR-6
Only if value appears:
optional BranchingResearchMode.

M-ARBOR-7
Only when empirical artifact testing exists:
promotion/sealed evaluation.
```

---

# 55. Stop conditions

Stop adding Arbor mechanisms if:

1. Simple Loop itself fails the current value experiment.
2. Lineage increases speculative accretion.
3. Branching does not reduce rediscovery.
4. Token cost increases without DecisionDelta.
5. Humans find lineage harder to understand than flat output.
6. typed insight does not outperform simpler evidence summaries.
7. negative memory suppresses legitimate alternatives.
8. most real usage remains single-path/simple.
9. donor lookup already solves the gap more cheaply.
10. a stronger donor provides better evidence.

---

# 56. Reopen conditions

Revisit Arbor if:

1. a newer paper version changes evaluation design;
2. repository issue #58 is resolved with deterministic promotion/sealed evaluation;
3. `merge_threshold` becomes truly enforced;
4. Arbor publishes stronger tree-policy/cost ablations;
5. IEE begins repeated real artifact experimentation;
6. IEE accumulates enough runs for cross-run memory evaluation;
7. multi-parent candidate synthesis becomes a real need;
8. another donor isolates insight propagation better;
9. Arbor adds explicit epistemic provenance for insights;
10. external replication appears.

---

# 57. Source provenance

## S1 — Primary paper
Jiajie Jin et al.
**Toward Generalist Autonomous Research via Hypothesis-Tree Refinement**
arXiv:2606.11926v1, 2026.

https://arxiv.org/abs/2606.11926

Used for:
- HTR;
- AO formulation;
- algorithm;
- architecture;
- results;
- ablations;
- token costs;
- transfer;
- limitations.

Status:
`PRIMARY RESEARCH SOURCE / LIVING TECHNICAL REPORT`

## S2 — Microsoft Research publication
https://www.microsoft.com/en-us/research/publication/toward-generalist-autonomous-research-via-hypothesis-tree-refinement/

## S3 — Official repository
https://github.com/RUC-NLPIR/Arbor

Reviewed commit:
`531885d9c2c6c409e09230a12b0fa27915ed8d63`

## S4 — Idea Tree
https://github.com/RUC-NLPIR/Arbor/blob/main/src/coordinator/idea_tree.py

## S5 — How It Works
https://github.com/RUC-NLPIR/Arbor/blob/main/docs/how-it-works.md

## S6 — Coordinator prompts
https://github.com/RUC-NLPIR/Arbor/blob/main/src/coordinator/prompts.py

## S7 — Search & External Knowledge
https://github.com/RUC-NLPIR/Arbor/blob/main/docs/search.md

## S8 — Experience distillation
https://github.com/RUC-NLPIR/Arbor/blob/main/src/distill.py

## S9 — Experience recall
https://github.com/RUC-NLPIR/Arbor/blob/main/src/recall.py

## S10 — Git merge/evaluation path
https://github.com/RUC-NLPIR/Arbor/blob/main/src/coordinator/tools/git_ops.py

## S11 — Issue #58
**Proposal: sealed evaluation and enforceable branch-promotion policy**
https://github.com/RUC-NLPIR/Arbor/issues/58

Status:
`ISSUE / DESIGN ANALYSIS`
Claims about current threshold/fallback behavior were cross-checked against code.

## S12 — Issue #59
**Autonomous Agent exits after future-work text without tool call**
https://github.com/RUC-NLPIR/Arbor/issues/59

Status:
`HISTORICAL SCAR`

Reviewed HEAD includes a merged fix.

## S13 — Issue #2
**Resume executor runs after max-turn/null-score exits instead of marking node done**
https://github.com/RUC-NLPIR/Arbor/issues/2

Status:
`HISTORICAL OPERATIONAL SCAR`

---

# 58. Final receiver verdict

Arbor should be remembered inside FioIdeias as:

> **a primary donor for cumulative idea/hypothesis lineage, evidence-conditioned search, semantic learning from failed and successful branches, compact persistent research state and evaluation separation — plus a major warning that even a well-designed “held-out gate” can be weakened by adaptive reuse, advisory enforcement and unverified metric fallbacks.**

Its greatest positive mechanism:

```text
LOCAL EXPERIMENT
↓
EVIDENCE
↓
TYPED LESSON
↓
FUTURE SEARCH CONSTRAINT
```

Its greatest negative lesson:

```text
DESIGN CLAIM != ENFORCED INVARIANT
```

The most promising FioIdeias transplant is not `IdeaTree`.

It is:

> **EVIDENCE-CONDITIONED IDEA LINEAGE**

with:
- multi-parent provenance;
- typed insights;
- scoped negative knowledge;
- reopen conditions;
- authority proof;
- evaluation independence;
- bounded branching.

---

# 59. Overall decision

```yaml
overall_decision: ADAPT_STRONGLY_SELECTED_MECHANISMS

high_priority:
  - evidence_conditioned_idea_lineage
  - compact_persistent_research_state
  - typed_insight_propagation
  - scoped_negative_knowledge
  - fixed_hypothesis_during_local_repair
  - independent_generation_and_validation_contexts
  - deterministic_retrieval_first
  - cross_run_paid_uncertainty_memory

adapt_with_hardening:
  - hypothesis_tree
  - pruning
  - insight_backpropagation
  - dev_test_evaluation
  - cross_run_experience_confidence
  - coordinator_executor_split

replace:
  - single_parent_tree_with_multi_parent_lineage_when_needed
  - repeated_heldout_checks_with_dev_promotion_sealed_roles
  - untyped_insight_with_evidence_conditioned_insight_record
  - recurrence_confidence_with_independence_aware_provenance

reject:
  - full_arbor_runtime_as_iee_core
  - llm_insight_as_truth
  - llm_reported_test_score_as_verified_evidence
  - advisory_hard_gate
  - unlimited_branching
  - scalar_metric_as_universal_idea_quality
  - coordinator_as_single_semantic_authority
  - timeout_as_substitute_for_protected_human_authority

implementation_authorized_by_this_document: false

next_receiver_action:
  - persist_autopsy
  - index_in_donor_arsenal
  - finish_current_iee_value_experiment
  - run_htr_lite_receiver_experiments_before_integration
```

---

# 60. Canonical one-sentence memory

> **ARBOR DONOR MEMORY:** Use persistent evidence-conditioned lineage so each experiment reduces future search; preserve failures as scoped knowledge; keep observations separate from LLM interpretations; and never trust a “held-out” or policy gate unless its independence and enforcement are mechanically real.
