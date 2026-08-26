# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Trabalho Atual — Máximo 1–2 tarefas)
- [x] **TASK-005.1:** Reconciliação do Repositório (`main` branch, remote GitHub origin, `.gitignore` hardening).
- [x] **TASK-005.2:** Execução de Varredura de Segurança (`SECRET_SCAN: PASS`).
- [x] **TASK-005.3:** Preflight de Provedores e atualização do `NativeModelRunner` (suporte a `.env` seguro para Groq/OpenAI/Gemini).
- [ ] **TASK-000:** Gate de Governança: Apresentação do relatório da Missão 05, registro do blocker honesto de credencial (`BLOCKED_PROVIDER_CREDENTIAL_OR_COST`) e parada mandatória (*STOP*).

---

## 🟡 NEXT (Próximos Passos Imediatos — Desbloqueados após configuração de credencial)
- [ ] **REAL-CANARY-001:** Execução do primeiro canário real de ponta a ponta sobre 1 ideia (Condição B: Standard Simple Loop) com provedor único (Groq `llama-3.3-70b-versatile` ou OpenAI/Gemini).
- [ ] **EXP-M05-REAL:** Execução do experimento controlado 3x3 com inferência real (3 fixtures x 3 condições = 9 runs reais) e geração do pacote de comparação cega real.

---

## 🔵 LATER (Trabalhos Futuros Planejados)
- **HUMAN-EVAL:** Avaliação humana cega das saídas reais do experimento.
- **Fase 4:** Deliberação Multi-Agent Heurística com topologias fixas.
- **Fase 5:** Experimentos de valor de coordenação (EXP-002 e EXP-003).
- **Fase 6:** Deliberation Control Engine Adaptativo.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)
- **REAL-CANARY-001 & EXP-M05-REAL:** Bloqueados por ausência de chave de API configurada no ambiente local (`GROQ_API_KEY`, `OPENAI_API_KEY` ou `GEMINI_API_KEY`).
