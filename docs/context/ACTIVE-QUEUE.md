# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Próxima Missão Imediata)
- [ ] **MISSION-M05.3-CALIBRATION:** **M05.3 Lean IEE Offline Replay & Adversarial Calibration**
  - **Objetivo:** Usar dados de runs históricas do IEE e cenários sintéticos adicionais para calibrar os limiares de falso positivo/falso negativo do `EarlyEpistemicGate`, refinar a representação de `DecisionDeltaRecord` e testar a interação com `NegativeKnowledgeRecord` offline.
  - **Diretriz Mandatória:** NÃO executar inferência real nesta etapa; calibração 100% offline. Preservar o `SimpleLoopRunner` como grupo de controle.

---

## 🟡 NEXT (Próximos Passos na Fila)
1. [ ] **EXP-M05.4-REAL-REPLICATION:** Execução do experimento de replicação multicaso (IDEA-01 a IDEA-05) contra provedores reais com blinding 1-to-1.
2. [ ] **EXP-HTR-LITE-REPLAY:** Replay offline de runs históricas sob o modelo de linhagem `IdeaLineageNode`.
3. [ ] **DONOR-DEEP-AUTOPSIES:** Continuidade das autópsias profundas de doadores secundários no arsenal.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)
- *Nenhuma tarefa bloqueada no momento.*
