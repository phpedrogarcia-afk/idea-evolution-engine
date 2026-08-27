# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Trabalho Atual — Aguardando Avaliação Humana)
- [x] **TASK-M05.2-REAL-EXEC:** Execução real online das 3 condições A/B/C contra Groq `openai/gpt-oss-120b` (15 chamadas executadas com sucesso).
- [x] **TASK-M05.2-BLIND-GEN:** Geração do pacote cego `BLIND-REVIEW-PACKET.md` e revelação isolada em `BLIND-REVEAL.json`.
- [x] **TASK-M05.2-DET-COMP:** Geração de `DETERMINISTIC-COMPARISON.md` e `DETERMINISTIC-COMPARISON.json`.
- [ ] **TASK-000 (HUMAN):** Avaliação Cega Humana — Preenchimento da rubrica no `BLIND-REVIEW-PACKET.md`.

---

## 🟡 NEXT (Próximos Passos — Após Avaliação e Revelação Humana)
1. [ ] **M05.2-REVEAL-ANALYSIS:** Leitura de `BLIND-REVEAL.json` e síntese da resposta à pergunta científica central.
2. [ ] **EXP-HTR-LITE-REPLAY:** Replay offline de runs históricos do IEE sob o modelo de linhagem `IdeaLineageNode`.
3. [ ] **EXP-FLAT-VS-LINEAGE:** Experimento controlado comparando Simple Loop plano vs Simple Loop com contexto de linhagem/memória negativa.
4. [ ] **DONOR-DEEP-AUTOPSIES:** Continuidade das autópsias profundas de doadores (um doador por vez).

---

## 🔴 BLOCKED (Tarefas Bloqueadas)
- *Nenhuma tarefa bloqueada no momento.*
