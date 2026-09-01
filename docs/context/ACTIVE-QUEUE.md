# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](../DECISIONS-LEDGER.md).

---

## 🟢 NOW (Próxima Decisão Imediata)

- [ ] **HUMAN-DECISION-M05.5R1:** decidir se uma nova replicação controlada deve ser planejada após a invalidação de `REAL-EXECUTION-ATTEMPT-001`.
  - **Fato de partida:** `M05.5_ATTEMPT_001 = QUARANTINED_EXECUTION_STRESS_EVIDENCE / INVALID_PRIMARY_REPLICATION`.
  - **Escopo desta decisão:** autorizar ou negar apenas o planejamento/preflight de M05.5R1.
  - **Não autorizado agora:** chamadas semânticas, uso de novos holdouts, geração de novo mapeamento cego, execução real, alteração de produto ou integração FioOS.

---

## 🟡 NEXT (Condicionado à Decisão Humana)

1. [ ] **M05.5R1-PREFLIGHT-FREEZE:** se autorizado, congelar uma nova replicação com 8 holdouts inéditos, novo mapeamento cego, novo namespace de tentativa e prova de quota adequada — sem executar chamadas semânticas.
2. [ ] **M05.5R1-REAL-EXECUTION:** somente após o preflight congelado e uma autorização de execução específica; nunca reutilizar `REAL-EXECUTION-ATTEMPT-001`.
3. [ ] **M05.5R1-HUMAN-REVIEW-AND-REVEAL:** somente se uma tentativa futura for admissível e tiver pacote cego válido.
4. [ ] **KNOWLEDGE-TRANSFER-PRESERVATION:** manter E10 como evidência de não elevação de autoridade. O documento não habilita implementação, parser externo, invocação FioOS ou escrita entre projetos.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)

- **M05.5 Attempt 001:** bloqueado como caminho confirmatório; seus artefatos brutos são preservados, mas não são base para revisão humana, reveal ou conclusão de replicação.
- **Bridge IEE ↔ FioOS:** bloqueado até uma missão e autoridade específicas. `READY_TO_TEST != EXECUTION_AUTHORITY`.
