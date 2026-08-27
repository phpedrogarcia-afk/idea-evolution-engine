# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Próxima Missão Imediata)
- [ ] **MISSION-M05.3-CALIBRATION:** **M05.3 FioED / Lean IEE Offline Replay & Adversarial Calibration**
  - **Objetivo:** Replay offline de dados históricos de execuções do IEE aplicando o modelo FioED congelado (`IntermediaryDepth`, `EvidenceFreePersistence`, `DriftRiskVector`, `DecisionDeltaRecord`, `U_f`/`U_g`, $Q^*$, `PressureReadiness`, `EvidenceAdmissionGate`) para calibrar empiricamente os limiares de falso positivo/falso negativo de escalação do `EarlyEpistemicGate`.
  - **Diretriz Mandatória:** Execução 100% offline (0 chamadas reais). Preservar o Simple Loop como controle. Manter definições do FioED congeladas durante o replay.

---

## 🟡 NEXT (Próximos Passos na Fila)
1. [ ] **EXP-M05.4-REAL-REPLICATION:** Execução da replicação multicaso (IDEA-01 a IDEA-05) contra provedores reais com blinding 1-to-1.
2. [ ] **EXP-HTR-LITE-REPLAY:** Replay de linhagem de ideias sob `IdeaLineageNode`.
3. [ ] **DONOR-DEEP-AUTOPSIES:** Continuidade das autópsias de doadores no arsenal.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)
- *Nenhuma tarefa bloqueada no momento.*
