# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Próxima Missão Imediata)
- [ ] **MISSION-M05.4-REAL-EXECUTION:** **M05.4 REAL 24-CELL EXECUTION**
  - **Objetivo:** Executar as 24 células (8 ideias x 3 condições) contra Groq `openai/gpt-oss-120b` sob `EXP-M05.4-PROSPECTIVE-RERUN-20260829`. Salvar artefatos brutos, computar instrumentação FioED, gerar novo pacote cego desidentificado e congelar para avaliação humana.
  - **Pré-condição:** GROQ_API_KEY válida fornecida pelo operador humano.
  - **Protocolo:** Seguir `RERUN-EXECUTION-MANIFEST.json` e `RERUN-RETRY-SEMANTICS-FROZEN.md`.

---

## 🟡 NEXT (Próximos Passos na Fila)
1. [ ] **HUMAN-REVIEW-M05.4:** Avaliação humana cega sobre o pacote gerado na execução real.
2. [ ] **MISSION-M05.4-REVEAL-ANALYSIS:** Congelamento do review humano, abertura de `BLIND-REVEAL.json`, cálculo de eficiência e predições FioED.
3. [ ] **KNOWLEDGE-TRANSFER-ACTIVATION:** Ativar `FIOOS-TO-FIOIDEIAS-KNOWLEDGE-TRANSFER.md` após M05.4 fechar.
4. [ ] **EXP-HTR-LITE-REPLAY:** Replay de linhagem de ideias sob `IdeaLineageNode`.
5. [ ] **DONOR-DEEP-AUTOPSIES:** Continuidade das autópsias de doadores no arsenal.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)
- *Avaliação humana bloqueada até execução real concluída.*
- *Ativação de knowledge transfer bloqueada até M05.4 fechar.*
