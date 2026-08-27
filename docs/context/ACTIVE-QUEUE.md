# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Trabalho Atual — Concluído)
- [x] **TASK-EPISTEMIC-01-A:** Institucionalização de `docs/epistemology/OBSERVATION-REPRESENTATION-INVARIANTS.md`.
- [x] **TASK-EPISTEMIC-01-B:** Criação dos contratos epistêmicos offline (`SourceAnchor`, `RepresentationRecord`, `InsightRecord`, `NegativeKnowledgeRecord`, `IdeaLineageNode`).
- [x] **TASK-EPISTEMIC-01-C:** Criação do visualizador e catálogo determinístico `DonorIntelligenceCatalog`.
- [x] **TASK-EPISTEMIC-01-D:** Persistência integral da autópsia canônica em `docs/research/donors/ARBOR-DEEP-AUTOPSY.md` e indexação no `DONOR-ARSENAL.md` e `donor-manifest.json`.
- [x] **TASK-EPISTEMIC-01-E:** 11 Testes determinísticos em `tests/adversarial/test_adversarial_epistemic_donor_foundation.py` (total: 109 testes verdes).
- [ ] **TASK-000:** Gate de Governança: Apresentação do relatório da Missão EPISTEMIC-DONOR-FOUNDATION-01 e parada mandatória (*STOP*).

---

## 🟡 NEXT (Próximos Passos — Fila de Experimentos e Validações Futuras)
1. [ ] **M05-FINAL-REAL-CANARY / EXP-M05:** Concluir / inspecionar o experimento controlado real A/B/C ou reattack do canário real se pendente.
2. [ ] **EXP-HTR-LITE-REPLAY:** Replay offline de runs históricos do IEE sob o modelo de linhagem `IdeaLineageNode`.
3. [ ] **EXP-FLAT-VS-LINEAGE:** Experimento controlado comparando Simple Loop plano vs Simple Loop com contexto de linhagem/memória negativa.
4. [ ] **EXP-TYPED-INSIGHT:** Experimento comparativo: resultado bruto vs insight livre vs insight tipado condicionado a evidência.
5. [ ] **BRANCHING-MODE-ADMISSION:** Admissão condicional de modo de busca em ramificação apenas se a evidência empírica comprovar valor superando complexidade de custo.
6. [ ] **DONOR-DEEP-AUTOPSIES:** Continuidade das autópsias profundas de doadores (um doador por vez).

---

## 🔴 BLOCKED (Tarefas Bloqueadas)
- **EXP-M05 (Real Inference):** Bloqueado até autorização expressa do operador humano com credencial configurada.
