# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Trabalho Atual — Concluído)
- [x] **TASK-005.1-R4-A:** Reordenação Topológica Canônica: `SYNTHESIZE` $\to$ `REALITY_CHECK` $\to$ `FINAL_REVIEW`.
- [x] **TASK-005.1-R4-B:** Formalização da Base de Autoridade (`PromotionAuthorityBasis`) e veto a promoção circular via `MODEL_HYPOTHESIS`.
- [x] **TASK-005.1-R4-C:** Implementação de 6 Invariantes Cross-State no `FinalReviewStage`.
- [x] **TASK-005.1-R4-D:** Implementação da política de Run ID imutável `RUN-<UTC>-<UUID>` e rastreabilidade de git commit / environment.
- [x] **TASK-005.1-R4-E:** Criação de 9 testes adversariais em `tests/adversarial/test_adversarial_ontology_provenance.py` (total: 86 testes verdes).
- [ ] **TASK-000:** Gate de Governança: Apresentação do relatório da Missão M05.1-R4 e parada mandatória (*STOP*).

---

## 🟡 NEXT (Próximos Passos — Após autorização e credencial real)
- [ ] **M05-FINAL-REAL-REATTACK:** Execução do canário real com modelo Groq `openai/gpt-oss-120b` sobre a ideia de clarificação de projetos com a blindagem ontológica, topológica e de identidade em vigor.
- [ ] **EXP-M05:** Execução do experimento controlado A/B/C sobre as 3 fixtures.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)
- **EXP-M05:** Bloqueado até validação com sucesso do canário real reparado.
