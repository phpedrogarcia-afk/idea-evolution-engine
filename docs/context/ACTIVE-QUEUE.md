# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Trabalho Atual — Concluído)
- [x] **TASK-M05.2-A:** Congelamento da especificação experimental (`docs/experiments/EXPERIMENT-SPEC-M05.2.md`).
- [x] **TASK-M05.2-B:** Inventário e auditoria de trabalho pago prévio (`docs/experiments/PAID-WORK-INVENTORY.md`).
- [x] **TASK-M05.2-C:** Implementação do harness `ABCExperimentRunner` com cegueira e accounting (`src/idea_evolution/experiments/abc_experiment.py`).
- [x] **TASK-M05.2-D:** 5 Testes de controle experimental em `tests/experiment/test_abc_controlled_experiment.py` (total: 114 testes verdes).
- [ ] **TASK-000:** Gate de Governança: Apresentação do relatório da Missão M05.2 e parada mandatória (*STOP*) por falta de credencial Groq no ambiente.

---

## 🟡 NEXT (Próximos Passos — Após export de GROQ_API_KEY pelo operador humano)
1. [ ] **M05.2-REAL-RUN:** Disparo da execução real das condições A, B e C com Groq `openai/gpt-oss-120b`.
2. [ ] **M05.2-BLIND-EVAL:** Geração de `BLIND-REVIEW-PACKET.md` e `BLIND-REVEAL.json` para avaliação humana independente.
3. [ ] **M05.2-HUMAN-SCORING:** Coleta de notas da rubrica pelo operador humano e revelação do mapeamento.
4. [ ] **EXP-HTR-LITE-REPLAY:** Replay offline de runs históricos do IEE sob o modelo de linhagem `IdeaLineageNode`.
5. [ ] **EXP-FLAT-VS-LINEAGE:** Experimento controlado comparando Simple Loop plano vs Simple Loop com contexto de linhagem/memória negativa.
6. [ ] **DONOR-DEEP-AUTOPSIES:** Continuidade das autópsias profundas de doadores (um doador por vez).

---

## 🔴 BLOCKED (Tarefas Bloqueadas)
- **M05.2-REAL-RUN:** Bloqueado até configuração de `GROQ_API_KEY` no ambiente pelo operador humano (`REAL_EXECUTION_BLOCKED = MISSING_GROQ_CREDENTIAL_OR_PROVIDER`).
