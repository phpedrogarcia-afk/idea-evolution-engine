# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Trabalho Atual — Concluído)
- [x] **TASK-005.1-R2-A:** Autópsia Causal da falha do RUN-008 (Contaminação Semântica no UNDERSTAND e Erro 400 no Groq Structured Output).
- [x] **TASK-005.1-R2-B:** Atualização dos prompts `UNDERSTAND` e `ATTACK` garantindo que o UNDERSTAND seja puramente descritivo e não generativo.
- [x] **TASK-005.1-R2-C:** Atualização do contrato `UnderstandOutput` e do estágio `understand.py` com isolamento de `inferred_candidates`.
- [x] **TASK-005.1-R2-D:** Implementação do `to_strict_json_schema()` no `NativeModelRunner` (Groq Strict Mode + bounded repair de 1 tentativa + preservação de `failed_generation`).
- [x] **TASK-005.1-R2-E:** Criação de 3 novos testes em `tests/adversarial/test_adversarial_understand_and_groq_boundary.py` (total: 77 testes verdes).
- [ ] **TASK-000:** Gate de Governança: Apresentação do relatório da Missão M05.1-R2 e parada mandatória (*STOP*).

---

## 🟡 NEXT (Próximos Passos — Após autorização e credencial real)
- [ ] **M05-REAL-REATTACK:** Execução do canário real com modelo Groq `openai/gpt-oss-120b` sobre a ideia de clarificação de projetos com os dois reparos em vigor.
- [ ] **EXP-M05:** Execução do experimento controlado A/B/C sobre as 3 fixtures.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)
- **EXP-M05:** Bloqueado até validação com sucesso do canário real reparado.
