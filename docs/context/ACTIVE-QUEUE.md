# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Próxima Missão Imediata)
- [ ] **MISSION-M05.4-P1R-CLEAN-RERUN:** **M05.4-P1R Prospective Multi-Idea Clean Rerun**
  - **Objetivo:** Corrigir a injeção do modelo `openai/gpt-oss-120b` no construtor de `SimpleLoopRunner` no executor experimental, gerar novo ID de execução (`EXP-M05.4-PROSPECTIVE-RERUN-20260827`), executar as 24 células com a topologia multistage real da Condição B, gerar o novo pacote cego desidentificado e congelar os artefatos antes da avaliação humana.

---

## 🟡 NEXT (Próximos Passos na Fila)
1. [ ] **HUMAN-REVIEW-M05.4:** Avaliação humana cega sobre o pacote gerado em M05.4-P1R.
2. [ ] **MISSION-M05.4-P2-REVEAL-ANALYSIS:** Congelamento do review humano, abertura de `BLIND-REVEAL.json`, cálculo de eficiência e predições FioED.
3. [ ] **EXP-HTR-LITE-REPLAY:** Replay de linhagem de ideias sob `IdeaLineageNode`.
4. [ ] **DONOR-DEEP-AUTOPSIES:** Continuidade das autópsias de doadores no arsenal.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)
- *Avaliação humana de `EXP-M05.4-PROSPECTIVE-20260827` bloqueada (experimento invalidado por falha na Condição B).*
