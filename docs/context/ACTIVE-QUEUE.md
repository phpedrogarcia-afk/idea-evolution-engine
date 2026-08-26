# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Trabalho Atual — Concluído)
- [x] **TASK-005.1-R5-A:** Criação do módulo determinístico `AuthorityProofValidator` com auditoria de `GroundingRecord`.
- [x] **TASK-005.1-R5-B:** Integração da validação de autoridade no `SynthesizeStage` e `FinalReviewStage` com rebaixamento para `MODEL_HYPOTHESIS` / `CANDIDATE`.
- [x] **TASK-005.1-R5-C:** Implementação de `_evaluate_hard_gates` no `SimpleLoopRunner` como autoridade soberana sobre o status final.
- [x] **TASK-005.1-R5-D:** Criação de 12 testes adversariais em `tests/adversarial/test_adversarial_ontology_provenance.py` (total: 98 testes verdes).
- [ ] **TASK-000:** Gate de Governança: Apresentação do relatório da Missão M05.1-R5 e parada mandatória (*STOP*).

---

## 🟡 NEXT (Próximos Passos — Após autorização e credencial real)
- [ ] **M05-FINAL-REAL-REATTACK:** Execução do canário real com modelo Groq `openai/gpt-oss-120b` sobre a ideia de clarificação de projetos sob as regras de prova de autoridade e gates soberanos.
- [ ] **EXP-M05:** Execução do experimento controlado A/B/C sobre as 3 fixtures.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)
- **EXP-M05:** Bloqueado até validação com sucesso do canário real reparado.
