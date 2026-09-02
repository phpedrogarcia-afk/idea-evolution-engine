# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](../DECISIONS-LEDGER.md).

---

## 🟢 NOW (Próxima Decisão Imediata)

- [ ] **HUMAN-DECISION-M05.5R1-CAPACITY-STRATEGY:** decidir entre capacidade de provedor maior, recalibração científica separada ou adiamento de M05.5R1.
  - **Fato autenticado:** a conta `Personal` / `Default Project` está no plano `FREE`, sem limite customizado; `openai/gpt-oss-120b` tem `30 RPM`, `1.000 RPD`, `8.000 TPM`, `200.000 TPD`.
  - **Gate determinado:** `131.072 > 8.000` torna a solicitação máxima inadmissível; `11.226.334 > 200.000` impede a garantia diária (gap `11.026.334`). `M05.5R1` não pode executar nesta conta.
  - **Evidência:** `M05.5R1-AUTHENTICATED-CAPACITY-CHECK-R2.json`; nenhuma API call, A/B/C, holdout ou reveal ocorreu.

---

## 🟡 NEXT (Condicionado à Decisão Humana)

1. [ ] **M05.5R1-PROVIDER-CAPACITY-EVIDENCE:** somente após uma mudança humana material de conta/projeto/capacidade; não repetir a evidência autenticada atual sem mudança de estado.
2. [ ] **M05.5R1-PREFLIGHT-FREEZE:** somente após uma decisão humana de capacidade e novo gate autenticado aprovado, executar preflight sem chamadas semânticas.
3. [ ] **M05.5R1-EXECUTION-AUTHORIZATION:** decisão humana separada, somente após o preflight retornar pronto e todos os checks determinísticos passarem.
4. [ ] **M05.5R1-REAL-EXECUTION:** somente sob a autorização específica acima; nunca reutilizar `REAL-EXECUTION-ATTEMPT-001`.
5. [ ] **M05.5R1-HUMAN-REVIEW-AND-REVEAL:** somente se uma tentativa futura for admissível e tiver pacote cego válido.
6. [ ] **KNOWLEDGE-TRANSFER-PRESERVATION:** manter E10 como evidência de não elevação de autoridade. O documento não habilita implementação, parser externo, invocação FioOS ou escrita entre projetos.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)

- **M05.5 Attempt 001:** bloqueado como caminho confirmatório; seus artefatos brutos são preservados, mas não são base para revisão humana, reveal ou conclusão de replicação.
- **Bridge IEE ↔ FioOS:** bloqueado até uma missão e autoridade específicas. `READY_TO_TEST != EXECUTION_AUTHORITY`.
