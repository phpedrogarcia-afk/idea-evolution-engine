# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](../DECISIONS-LEDGER.md).

---

## 🟢 NOW (Próxima Decisão Imediata)

- [ ] **HUMAN-DECISION-M05.5R1-AUTHENTICATED-CAPACITY-CHECK:** autorizar obtenção/verificação dos limites e saldos reais da organização/projeto Groq para o envelope M05.5R1 calibrado.
  - **Fato de partida:** `max_completion_tokens=2048`, envelope máximo `11,226,334`, schedule e pacing estão congelados; remaining TPD da conta real continua não comprovado.
  - **Escopo possível:** somente evidência autenticada de capacidade, sem chamada semântica, A/B/C, execução real, reveal, alteração de produto ou integração FioOS.

---

## 🟡 NEXT (Condicionado à Decisão Humana)

1. [ ] **M05.5R1-PROVIDER-CAPACITY-EVIDENCE:** obter limites/saldos autenticados da organização/projeto Groq exatos, inclusive remaining TPD, para o envelope congelado.
2. [ ] **M05.5R1-PREFLIGHT-FREEZE:** somente após capacity readiness aprovada, executar preflight sem chamadas semânticas.
3. [ ] **M05.5R1-EXECUTION-AUTHORIZATION:** decisão humana separada, somente após o preflight retornar pronto e todos os checks determinísticos passarem.
4. [ ] **M05.5R1-REAL-EXECUTION:** somente sob a autorização específica acima; nunca reutilizar `REAL-EXECUTION-ATTEMPT-001`.
5. [ ] **M05.5R1-HUMAN-REVIEW-AND-REVEAL:** somente se uma tentativa futura for admissível e tiver pacote cego válido.
6. [ ] **KNOWLEDGE-TRANSFER-PRESERVATION:** manter E10 como evidência de não elevação de autoridade. O documento não habilita implementação, parser externo, invocação FioOS ou escrita entre projetos.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)

- **M05.5 Attempt 001:** bloqueado como caminho confirmatório; seus artefatos brutos são preservados, mas não são base para revisão humana, reveal ou conclusão de replicação.
- **Bridge IEE ↔ FioOS:** bloqueado até uma missão e autoridade específicas. `READY_TO_TEST != EXECUTION_AUTHORITY`.
