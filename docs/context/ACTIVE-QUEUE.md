# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Trabalho Atual — Máximo 1–2 tarefas)
- [x] **TASK-002:** Conclusão da Missão Mestre 02 (Intelligence & Continuity Hardening):
  - [x] Criação de `docs/context/` e artefatos de continuidade.
  - [x] Criação de `context-manifest.json` com validação de hashes.
  - [x] Criação de `tools/context/validate_context.py` e utilitários.
  - [x] Criação da suíte de testes de continuidade (`tests/continuity/`).
  - [x] Emissão do checkpoint `CP-20260826-001`.
  - [x] Geração do relatório `INTELLIGENCE-HARDENING-REPORT.md`.
- [ ] **TASK-000:** Gate de Governança: Parada obrigatória e apresentação ao operador humano para validação e autorização de transição de fase.

---

## 🟡 NEXT (Próximos Passos Imediatos — 2–3 tarefas)
*(Desbloqueadas exclusivamente após autorização humana)*
- [ ] **TASK-101 (Fase 1):** Schemas JSON / Pydantic estritos para `IdeaGenome`, `GenomePatch`, `DeliberationContract`, `UncertaintyRecord`, `TensionRecord`, `DecisionRelevanceReport`, `DecisionDelta`, `GapRecord` e `TestContract`.
- [ ] **TASK-102 (Fase 1):** Implementação do `GenomeValidator` (código Python 100% determinístico com validação de 5 camadas) e suíte de testes unitários/adversariais.
- [ ] **TASK-201 (Fase 2 / Simple Loop MVP):** Implementação do *Simple Idea Evolution Loop* (Pipeline heurístico: *Understand $\to$ Attack $\to$ Alternatives $\to$ Reality Check $\to$ Synthesize $\to$ Review*).

---

## 🔵 LATER (Trabalhos Futuros Planejados)
- **Fase 3:** Execução do experimento científico EXP-001 (Single Model vs Contratos).
- **Fase 4:** Deliberação Multi-Agent Heurística com topologias fixas (`CRITIQUE_LOOP`, `SEQUENTIAL`).
- **Fase 5:** Experimentos controlados de valor de coordenação (EXP-002 e EXP-003).
- **Fase 6:** Deliberation Control Engine Adaptativo (Otimização dinâmica de topologia e busca de workflows).

---

## 🔴 BLOCKED (Tarefas Bloqueadas)
- *Nenhuma tarefa bloqueada no momento.*
