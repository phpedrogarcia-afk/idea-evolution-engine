# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](../DECISIONS-LEDGER.md).

---

## 🟢 NOW (Próxima Decisão Imediata)

- [ ] **HUMAN-DECISION-M05.5R1-PREFLIGHT-FREEZE:** autorizar receipts reais de holdout selado, cegamento e capacidade, seguidos de preflight sem chamadas semânticas.
  - **Fato de partida:** o harness offline R3 está validado por 12 testes sintéticos; ele não consulta provedor nem autoriza execução.
  - **Escopo possível:** receipts e verificações pré-execução; sem chamada semântica, execução real, alteração de produto ou integração FioOS.

---

## 🟡 NEXT (Condicionado à Decisão Humana)

1. [ ] **M05.5R1-PREFLIGHT-FREEZE:** o humano sela 8 holdouts inéditos, novo mapeamento cego e receipt de capacidade; o freeze é feito sem chamadas semânticas.
2. [ ] **M05.5R1-EXECUTION-AUTHORIZATION:** decisão humana separada, somente após o preflight retornar pronto e todos os checks determinísticos passarem.
3. [ ] **M05.5R1-REAL-EXECUTION:** somente sob a autorização específica acima; nunca reutilizar `REAL-EXECUTION-ATTEMPT-001`.
4. [ ] **M05.5R1-HUMAN-REVIEW-AND-REVEAL:** somente se uma tentativa futura for admissível e tiver pacote cego válido.
5. [ ] **KNOWLEDGE-TRANSFER-PRESERVATION:** manter E10 como evidência de não elevação de autoridade. O documento não habilita implementação, parser externo, invocação FioOS ou escrita entre projetos.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)

- **M05.5 Attempt 001:** bloqueado como caminho confirmatório; seus artefatos brutos são preservados, mas não são base para revisão humana, reveal ou conclusão de replicação.
- **Bridge IEE ↔ FioOS:** bloqueado até uma missão e autoridade específicas. `READY_TO_TEST != EXECUTION_AUTHORITY`.
