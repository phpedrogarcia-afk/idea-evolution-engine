# docs/context/CURRENT-STATE.md — Snapshot Operacional Dinâmico

> **ESTE DOCUMENTO É A DECLARAÇÃO OPERACIONAL VIVA DO ESTADO DO REPOSITÓRIO.**
> Atualizado em: 2026-09-01 | Checkpoint: CP-20260901-002

---

## 1. Identificação Operacional

- **Projeto:** Idea Evolution Engine (IEE)
- **Fase Ativa:** FASE 1 — SIMPLE IDEA EVOLUTION LOOP MVP
- **Status da Fundação:** `COMPLETE_AND_LOCKED` (`FOUNDATION_READY = TRUE`)
- **Status do Experimento M05.4 (EXP-M05.4-PROSPECTIVE-RERUN-20260829):** `CLOSED_PROSPECTIVE_EXPERIMENT`
  - Efeito de Tratamento Observado: `C_BEST_IN_M05_4`
  - Status do Lean L1: `LEADING_CANDIDATE_PROVISIONAL_DEFAULT`
  - Mecanismo Causal: `UNRESOLVED`
- **Status do Experimento M05.5 (EXP-M05.5-CONTROLLED-REPLICATION-20260831):**
  - Execução: `REAL-EXECUTION-ATTEMPT-001`
  - Papel da evidência: `QUARANTINED_EXECUTION_STRESS_EVIDENCE`
  - Admissibilidade: `INVALID_PRIMARY_REPLICATION`
  - Razão: reutilização de identidade de tentativa, contaminação dos holdouts e interferência de quota/TPD do provedor.
  - Semântica preservada: isto é `EXPERIMENT_EXECUTION_FAILURE`, não `LEAN_L1_REPLICATION_FAILURE`; não é `FAILED`, `REJECTED`, `READY`, `PROVEN` ou `SUPERSEDED`.
  - Evidência: `experiments/EXP-M05.5-CONTROLLED-REPLICATION-20260831/M05.5-ATTEMPT-001-INTEGRITY-AUDIT.md` (commit `26a2a67`).
- **M05.5R1 (EXP-M05.5R1-CONTROLLED-REPLICATION-20260901):** `PLANNED_NOT_EXECUTION_READY`
  - Contrato: `experiments/EXP-M05.5R1-CONTROLLED-REPLICATION-20260901/M05.5R1-PRE-FREEZE-READINESS.md`.
  - Bloqueios: o harness existente não prova imutabilidade, boundary de holdout ou capacidade determinística; execução permanece bloqueada.
- **Último Checkpoint Imutável:** [`CP-20260901-002`](checkpoints/CP-20260901-002.md)
- **Último Estado Seguro (Last Known Good):** `CP-20260901-002`
- **Git Branch:** `main`
- **Worktree no planejamento R2:** `DIRTY_PLANNING_PENDING_COMMIT`

---

## 2. Status do Trabalho

- **Último Trabalho Concluído:**
  - Auditoria forense de `REAL-EXECUTION-ATTEMPT-001`, preservada como evidência quarantinada.
  - `PFI-R0-IDEA-EVOLUTION-ENGINE-READINESS-AUDIT-001`, que confirmou que E10 só prova a fronteira epistêmica/de autoridade, não um bridge de runtime.
  - `PFI-R1-STATE-QUEUE-RECONCILIATION-001`, que substituiu o estado pré-execução obsoleto pela classificação acima.
  - `PFI-R2-M05_5R1-REPLICATION-PLANNING-001`, que congelou o desenho mínimo e identificou os controles determinísticos ainda ausentes.
- **Tarefa Ativa Atual:**
  - M05.5R1 permanece em planejamento; execução autônoma não está autorizada.
- **Próximo Passo Exato:**
  - Decisão humana explícita sobre autorizar ou não uma missão offline para implementar e testar o harness/preflight M05.5R1. Nenhuma chamada semântica, novo holdout, novo cegamento ou bridge pode começar antes dessa decisão.

---

## 3. O Que Explicitamente NÃO Fazer (DO-NOT-DO)

1. ❌ **NÃO** reutilizar `REAL-EXECUTION-ATTEMPT-001`, seus holdouts ou seu mapeamento cego como base confirmatória.
2. ❌ **NÃO** interpretar a quarentena como falha de replicação do Lean L1, rejeição do produto ou evidência positiva.
3. ❌ **NÃO** expor chaves de API (`GROQ_API_KEY`) no console, git ou logs.
4. ❌ **NÃO** implementar bridge FioOS, parser externo, invocação automática ou transferência de autoridade: `IDEA != REQUIREMENT`, `IDEA != TRUTH`, `IDEA != AUTHORITY`.
