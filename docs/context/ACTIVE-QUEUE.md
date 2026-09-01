# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](../DECISIONS-LEDGER.md).

---

## 🟢 NOW (Próxima Decisão Imediata)

- [ ] **HUMAN-DECISION-M05.5R1-CAPACITY-DESIGN-RESOLUTION:** decidir se será autorizada uma missão pré-execução para congelar limites de token e uma política de ordem/pacing neutra entre A/B/C.
  - **Fato de partida:** capacity readiness retornou `STOP_CAPACITY_DESIGN_CONFLICT`; remaining TPD da conta real também não foi comprovado.
  - **Escopo possível:** somente desenho/preflight offline e posterior leitura autenticada de limites/saldos; sem chamada semântica, A/B/C, execução real, reveal, alteração de produto ou integração FioOS.

---

## 🟡 NEXT (Condicionado à Decisão Humana)

1. [ ] **M05.5R1-PROVIDER-CAPACITY-EVIDENCE:** após envelope e schedule congelados, obter limites/saldos autenticados da organização/projeto Groq exatos, inclusive remaining TPD.
2. [ ] **M05.5R1-PREFLIGHT-FREEZE:** somente após capacity readiness aprovada, executar preflight sem chamadas semânticas.
3. [ ] **M05.5R1-EXECUTION-AUTHORIZATION:** decisão humana separada, somente após o preflight retornar pronto e todos os checks determinísticos passarem.
4. [ ] **M05.5R1-REAL-EXECUTION:** somente sob a autorização específica acima; nunca reutilizar `REAL-EXECUTION-ATTEMPT-001`.
5. [ ] **M05.5R1-HUMAN-REVIEW-AND-REVEAL:** somente se uma tentativa futura for admissível e tiver pacote cego válido.
6. [ ] **KNOWLEDGE-TRANSFER-PRESERVATION:** manter E10 como evidência de não elevação de autoridade. O documento não habilita implementação, parser externo, invocação FioOS ou escrita entre projetos.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)

- **M05.5 Attempt 001:** bloqueado como caminho confirmatório; seus artefatos brutos são preservados, mas não são base para revisão humana, reveal ou conclusão de replicação.
- **Bridge IEE ↔ FioOS:** bloqueado até uma missão e autoridade específicas. `READY_TO_TEST != EXECUTION_AUTHORITY`.
