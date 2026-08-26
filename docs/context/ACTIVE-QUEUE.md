# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Trabalho Atual — Concluído)
- [x] **TASK-006.1:** Criação da Especificação de Roteamento (`docs/specs/MODEL-ROUTING.md`).
- [x] **TASK-006.2:** Implementação de `ModelRoutingConfig` e `RunnerRouter` com proveniência e hash determinístico.
- [x] **TASK-006.3:** Reconciliação do Anthropic e sanitização de carregamento de `.env` (exclusão de `~/.env`).
- [x] **TASK-006.4:** Implementação dos comandos `iee providers doctor`, `iee routes show` e `--dry-run`.
- [x] **TASK-006.1-A:** Criação do Catálogo Vivo de Modelos (`src/idea_evolution/config/catalog.py` e `config/model_catalog.json`).
- [x] **TASK-006.1-B:** Institucionalização da política `FREE_ONLY` e regras estritas de fallback (`EXPERIMENTAL_PINNED` vs `FREE_POOL_OPERATIONAL`).
- [x] **TASK-006.1-C:** Resolução de model drift (Groq `openai/gpt-oss-120b`, Gemini `gemini-3.7-flash`).
- [x] **TASK-006.1-D:** 12 novos testes automatizados (total: 61 testes verdes).
- [ ] **TASK-000:** Gate de Governança: Apresentação do relatório da Missão 06.1 e parada mandatória (*STOP*).

---

## 🟡 NEXT (Próximos Passos — Após configuração de credenciais reais)
- [ ] **M05-B:** Execução do primeiro canário real de modelo único (Groq `openai/gpt-oss-120b`) sobre 1 ideia crua sob custo zero.
- [ ] **EXP-M05:** Execução do experimento controlado A/B/C sobre as 3 fixtures com inferência real.
- [ ] **M07:** Primeira deliberação real multi-modelo com roteamento por estágio sob `FREE_ONLY`.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)
- **M05-B & M07:** Bloqueados por ausência de chaves de API configuradas no ambiente local.
