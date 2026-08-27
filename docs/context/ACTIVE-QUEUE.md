# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Próxima Missão Imediata)
- [ ] **MISSION-M05.4-P1-REAL-EXECUTION:** **M05.4-P1 Prospective Multi-Idea Real Execution**
  - **Objetivo:** Executar as três condições congeladas (A = Baseline 1 chamada, B = Simple Loop 10 chamadas, C = Lean L1 máx 2 chamadas) sobre as 8 ideias da suíte holdout (`HOLDOUT-IDEAS.json`) utilizando Groq / `openai/gpt-oss-120b`, renderizar os pacotes cegos desidentificados via `BlindRenderer` e congelar a avaliação humana antes da revelação.
  - **Diretriz Mandatória:** Zero alterações de prompt, zero alterações de código ou regras durante a execução.

---

## 🟡 NEXT (Próximos Passos na Fila)
1. [ ] **M05.4-P2-HUMAN-REVIEW-AND-REVEAL:** Avaliação humana cega, congelamento do review e abertura de `BLIND-REVEAL.json`.
2. [ ] **EXP-HTR-LITE-REPLAY:** Replay de linhagem de ideias sob `IdeaLineageNode`.
3. [ ] **DONOR-DEEP-AUTOPSIES:** Continuidade das autópsias de doadores no arsenal.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)
- *Nenhuma tarefa bloqueada no momento.*
