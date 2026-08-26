# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Trabalho Atual — Concluído)
- [x] **TASK-005.1-A:** Autópsia Causal de Proliferação de Features e Linhagem de Conceitos.
- [x] **TASK-005.1-B:** Formalização das 3 camadas de estado (`CORE`, `DERIVED`, `CANDIDATE`).
- [x] **TASK-005.1-C:** Atualização dos contratos `SynthesizeOutput` e `FinalReviewOutput` com `candidate_possibilities` e `speculative_accretion_detected`.
- [x] **TASK-005.1-D:** Atualização dos prompts `SYNTHESIZE` e `FINAL_REVIEW`.
- [x] **TASK-005.1-E:** Criação de testes adversariais em `tests/adversarial/test_adversarial_essence_drift.py` (total: 63 testes verdes).
- [ ] **TASK-000:** Gate de Governança: Apresentação do relatório da Missão 05.1 e parada mandatória (*STOP*).

---

## 🟡 NEXT (Próximos Passos — Após configuração de credenciais reais)
- [ ] **M05-B:** Execução do canário real de modelo único (Groq `openai/gpt-oss-120b`) sobre 1 ideia crua com proteção contra inchaço especulativo.
- [ ] **EXP-M05:** Execução do experimento controlado A/B/C sobre as 3 fixtures.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)
- **M05-B:** Bloqueado por ausência de chaves de API configuradas no ambiente local.
