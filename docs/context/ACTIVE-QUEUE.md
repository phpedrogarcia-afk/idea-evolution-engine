# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Trabalho Atual — Concluído)
- [x] **TASK-005.1-R3-A:** Autópsia Causal da falha do RUN-009 (Promoção sem proveniência, duplicação ontológica e contaminação de testes do Core).
- [x] **TASK-005.1-R3-B:** Implementação do modelo `ProposalRecord` e tipos `AcceptedChangeItem` / `core_mechanism_justification`.
- [x] **TASK-005.1-R3-C:** Isolamento estrito de testes em `candidate_tests` (Core) e `exploratory_candidate_tests` (Exploratório).
- [x] **TASK-005.1-R3-D:** Implementação da verificação determinística de contradições ontológicas no `FinalReviewStage`.
- [x] **TASK-005.1-R3-E:** Criação de 4 novos testes em `tests/adversarial/test_adversarial_ontology_provenance.py` (total: 81 testes verdes).
- [ ] **TASK-000:** Gate de Governança: Apresentação do relatório da Missão M05.1-R3 e parada mandatória (*STOP*).

---

## 🟡 NEXT (Próximos Passos — Após autorização e credencial real)
- [ ] **M05-FINAL-REAL-REATTACK:** Execução do canário real com modelo Groq `openai/gpt-oss-120b` sobre a ideia de clarificação de projetos com a blindagem ontológica completa em vigor.
- [ ] **EXP-M05:** Execução do experimento controlado A/B/C sobre as 3 fixtures.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)
- **EXP-M05:** Bloqueado até validação com sucesso do canário real reparado.
