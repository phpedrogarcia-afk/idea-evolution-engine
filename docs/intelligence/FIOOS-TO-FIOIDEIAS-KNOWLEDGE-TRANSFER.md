# FIOOS-TO-FIOIDEIAS-KNOWLEDGE-TRANSFER.md

## Status: PRESERVED / NOT ACTIVATED DURING M05.4

Reason: These principles improve the receiver environment. Activating them
during M05.4 prospective evaluation would constitute changing the receiver
under evaluation -- a protocol violation. They are preserved here for
activation after M05.4 human review and reveal are complete.

---

## Pending Knowledge Transfer Items

### From FioOS Architecture

**Source:** FioOS kernel / architectural cross-pollination
**Preserved at:** 2026-08-29
**Activation target:** POST-M05.4

These structural invariants from FioOS should be formally transplanted into
the IEE doctrine after M05.4 closes:

1. Authority leases must be temporal and auditable
2. Sandboxed budget enforcement per execution unit
3. Tool invocation must leave an auditable trace
4. Human override must always be reachable

### From Video-Derived Agent-Environment Principles

**Source:** Video/external material reviewed 2026-08-29
**Preserved at:** 2026-08-29
**Activation target:** POST-M05.4

These design principles were identified but intentionally NOT operationalized:

| Principle | Description |
|-----------|-------------|
| GOOD IDEA != IMPLEMENT NOW | Recognizing a good idea does not constitute authorization to implement it. Timing matters. |
| MAKE THE CORRECT PATH THE EASY PATH | Environment design should make correct behavior the path of least resistance, not just the permitted path. |
| DON'T ASK THE AGENT TO REMEMBER A RULE THE ENVIRONMENT CAN ENFORCE | Structural enforcement is more reliable than instruction-based compliance. Convert rules to invariants where possible. |
| VERIFY THE VERIFIER | Any verification system must itself be verified. Negative-control checks must accompany positive-control proofs. |
| AGENT CAPABILITY != MODEL CAPABILITY | What an agent can do is a function of model + environment + tools + protocol. Model capability alone is insufficient. |
| ENVIRONMENT CONTRIBUTES TO EFFECTIVE AGENT CAPABILITY | The scaffolding, constraints, and affordances of the environment materially determine what an agent can reliably accomplish. |

---

## Activation Condition

These items may be activated in the first mission AFTER:

- M05.4 human review is complete
- Blind reveal is opened
- Winner is formally declared
- Checkpoint post-M05.4-review is emitted

DO NOT activate before those conditions are met.
