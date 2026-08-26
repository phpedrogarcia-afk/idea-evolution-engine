# docs/doctrine/CONSTITUTIONAL-MATURITY-MAP.md — Mapa de Maturidade Constitucional

> **RASTREAMENTO DO ESTÁGIO DE MATURIDADE OPERACIONAL DE CADA REGRA CENTRAL.**
> *Evita declarar que uma regra "existe" quando ela é apenas uma discussão teórica.*

---

## 1. O Ciclo de Vida da Maturidade Constitucional

$$\text{IDEA} \longrightarrow \text{DECISION} \longrightarrow \text{INSTITUTIONALIZED} \longrightarrow \text{ENFORCED} \longrightarrow \text{TESTED} \longrightarrow \text{PROVEN} \longrightarrow \text{FROZEN}$$

- **`IDEA`:** Conceito discutido ou sugerido.
- **`DECISION`:** Aprovado formalmente como ADR no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).
- **`INSTITUTIONALIZED`:** Integrado à documentação canônica e políticas ativas.
- **`ENFORCED`:** Implementado em scripts determinísticos, schemas ou verificadores mecânicos.
- **`TESTED`:** Coberto por testes unitários ou suítes adversariais automatizadas.
- **`PROVEN`:** Validado contra execuções reais e repetíveis no repositório.
- **`FROZEN`:** Estabilizado e trancado (*Do not pay twice for the same uncertainty*).

---

## 2. Matriz de Maturidade dos Princípios Críticos

| Princípio Constitucional | Fonte Principal | Status Decisório | Institucionalizado? | Política? | Código / Script? | Teste Automatizado? | Cold-Start Pointer? | Maturidade Atual |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Truth Over Agreement** | Constituição §2 | `ACCEPTED` (ADR-004) | SIM (`OPERATING-DOCTRINE`) | SIM | SIM (`CONTRADICTIONS.md`) | SIM (`test_continuity.py`) | SIM (`AI-START-HERE`) | **`PROVEN / FROZEN`** |
| **Progress Over Appearance** | Constituição §3 | `ACCEPTED` (ADR-014) | SIM (`OPERATING-DOCTRINE`) | SIM (`TASK-CONTRACT`) | SIM (`validate_intelligence.py`) | SIM (`test_constitutional_doctrine.py`) | SIM (`AI-START-HERE`) | **`TESTED`** |
| **Aggressive in Investigation, Governed in Effects** | Constituição §4 | `ACCEPTED` (ADR-013) | SIM (`OPERATING-DOCTRINE`) | SIM (`GOVERNED-CHANGE`) | SIM (`AUTHORITY-MATRIX`) | SIM (`test_intelligence.py`) | SIM (`AGENTS.md`) | **`TESTED / FROZEN`** |
| **Proven Enough $\to$ Freeze and Use (No Foundation 04)** | Constituição §6 | `ACCEPTED` (ADR-012) | SIM (`FOUNDATION-READINESS`) | SIM | SIM (`validate_intelligence.py`) | SIM (`test_constitutional_doctrine.py`) | SIM (`CURRENT-STATE`) | **`PROVEN / FROZEN`** |
| **Failure is Data (Test Before Memory)** | Constituição §9 | `ACCEPTED` (ADR-011) | SIM (`HYPOTHESIS-PROTOCOL`) | SIM | SIM (`tests/`) | SIM (`test_intelligence.py`) | SIM (`AI-START-HERE`) | **`TESTED`** |
| **Hierarchy of Evidence & Memory $\neq$ Evidence** | Constituição §11–12 | `ACCEPTED` (ADR-002) | SIM (`EVIDENCE-POLICY`) | SIM | SIM (`context-manifest.json`) | SIM (`test_continuity.py`) | SIM (`AI-START-HERE`) | **`PROVEN / FROZEN`** |
| **Conversation is Cache, Repo is Durable Memory** | Constituição §17 | `ACCEPTED` (ADR-011) | SIM (`CONTINUITY-CAPSULE`) | SIM | SIM (`validate_context.py`) | SIM (`test_continuity.py`) | SIM (`AI-START-HERE`) | **`PROVEN / FROZEN`** |
| **Deterministic First** | Constituição §21 | `ACCEPTED` (ADR-003) | SIM (`TASK-CLASSIFICATION`) | SIM | SIM (`tools/`) | SIM (`test_continuity.py`) | SIM (`AGENTS.md`) | **`PROVEN / FROZEN`** |
| **Baseline Required Before Improvement Claim** | Constituição §25 | `ACCEPTED` (ADR-011) | SIM (`BASELINE-POLICY`) | SIM | SIM (`validate_intelligence.py`) | SIM (`test_intelligence.py`) | SIM (`AI-START-HERE`) | **`TESTED`** |
| **Capability $\neq$ Permission $\neq$ Authority** | Constituição §30 | `ACCEPTED` (ADR-004) | SIM (`GOVERNANCE-INVARIANTS`) | SIM (`AUTHORITY-MATRIX`) | SIM (`validate_context.py`) | SIM (`test_continuity.py`) | SIM (`AGENTS.md`) | **`PROVEN / FROZEN`** |
| **Producer $\neq$ Sole Approver (Adversarial Review)** | Constituição §40–41 | `ACCEPTED` (ADR-011) | SIM (`ADVERSARIAL-REVIEW`) | SIM | SIM (`validate_intelligence.py`) | SIM (`test_intelligence.py`) | SIM (`AGENTS.md`) | **`TESTED`** |
| **Before Inventing, Harvest (Gap-First Scar Research)** | Constituição §44–46 | `ACCEPTED` (ADR-008) | SIM (`DONOR-AUTOPSY-METHOD`) | SIM | SIM (`DONOR-INDEX.md`) | SIM (`test_intelligence.py`) | SIM (`AI-START-HERE`) | **`PROVEN / FROZEN`** |
| **Simple Before Platform (Simple Loop MVP First)** | Constituição §50 | `ACCEPTED` (ADR-012) | SIM (`MISSION-04-TASK-CONTRACT`) | SIM | SIM (`validate_context.py`) | SIM (`test_continuity.py`) | SIM (`CURRENT-STATE`) | **`PROVEN / FROZEN`** |
| **Every Mission Needs Stop Condition & Target Uncertainty** | Constituição §66, 148 | `ACCEPTED` (ADR-014) | SIM (`TASK-CONTRACT`) | SIM | SIM (`validate_intelligence.py`) | SIM (`test_constitutional_doctrine.py`) | SIM (`AGENTS.md`) | **`TESTED`** |
| **No Cash Spend Default (`NO_CASH_SPEND=TRUE`)** | Constituição §58 | `ACCEPTED` (ADR-001) | SIM (`GOVERNANCE-INVARIANTS`) | SIM | SIM (`tools/`) | SIM (`test_constitutional_doctrine.py`) | SIM (`AGENTS.md`) | **`PROVEN / FROZEN`** |
