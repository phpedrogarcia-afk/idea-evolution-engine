# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](../DECISIONS-LEDGER.md).

---

## 🟢 NOW (Próxima Decisão Imediata)

- [ ] **HUMAN-API-KEY-LOCAL-SETUP-FOR-SACRIFICIAL-PILOT:** criar/selecionar key no console oficial Groq, gravá-la somente na variável de ambiente local `GROQ_API_KEY` e reiniciar a sessão. Não colar a key no chat ou repositório.
  - **Escopo posterior estrito:** um único bloco sacrificial `M05.4-ATTEMPT-004-IDEA-08`, em `CONDITION_C → CONDITION_B → CONDITION_A`, com guard offline aprovado; `H01`–`H08` e reveal continuam negados.

- [ ] **M05.5R1-HIGHER-CAPACITY-EVIDENCE:** obter capacidade autenticada maior, mantendo provedor, modelo e tratamentos congelados.
  - **Fato autenticado:** a conta `Personal` / `Default Project` está no plano `FREE`, sem limite customizado; `openai/gpt-oss-120b` tem `30 RPM`, `1.000 RPD`, `8.000 TPM`, `200.000 TPD`.
  - **Decisão humana congelada:** `FREE_PATH_REJECTED_FOR_CONFIRMATORY_EXECUTION`; `FREE_CONFIRMATORY_RISK_NOT_DEFENSIBLE`, sem alegar falha provada.
  - **Evidência:** `M05.5R1-AUTHENTICATED-CAPACITY-CHECK-R2.json`; nenhuma API call, A/B/C, holdout ou reveal ocorreu.
  - **Evidência empírica adicional:** `PFI-M05_5R1-FREE-EMPIRICAL-CAPACITY-AUDIT-001.md` é `TRACE_INCOMPLETE`: 78 B records exatos ficaram abaixo do TPM por chamada, mas consomem 70,16% do TPD; A/C e duas cadeias de repair não são reconstituíveis. Não iniciar campanha de otimização Free nem apostar os holdouts Free.

---

## 🟡 NEXT (Condicionado à Decisão Humana)

1. [ ] **M05.5R1-PROVIDER-CAPACITY-EVIDENCE:** somente após capacidade autenticada maior no mesmo provedor/modelo; não repetir a evidência atual sem mudança material de conta/projeto/capacidade.
2. [ ] **M05.5R1-PREFLIGHT-FREEZE:** somente após uma decisão humana de capacidade e novo gate autenticado aprovado, executar preflight sem chamadas semânticas.
3. [ ] **M05.5R1-EXECUTION-AUTHORIZATION:** decisão humana separada, somente após o preflight retornar pronto e todos os checks determinísticos passarem.
4. [ ] **M05.5R1-REAL-EXECUTION:** somente sob a autorização específica acima; nunca reutilizar `REAL-EXECUTION-ATTEMPT-001`.
5. [ ] **M05.5R1-HUMAN-REVIEW-AND-REVEAL:** somente se uma tentativa futura for admissível e tiver pacote cego válido.
6. [ ] **KNOWLEDGE-TRANSFER-PRESERVATION:** manter E10 como evidência de não elevação de autoridade. O documento não habilita implementação, parser externo, invocação FioOS ou escrita entre projetos.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)

- **M05.5 Attempt 001:** bloqueado como caminho confirmatório; seus artefatos brutos são preservados, mas não são base para revisão humana, reveal ou conclusão de replicação.
- **Groq Free para M05.5R1 confirmatório:** bloqueado por decisão humana. Não é falha provada; é risco não defensável com holdouts confirmatórios e telemetria histórica incompleta.
- **Bridge IEE ↔ FioOS:** bloqueado até uma missão e autoridade específicas. `READY_TO_TEST != EXECUTION_AUTHORITY`.
