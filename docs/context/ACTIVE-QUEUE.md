# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Trabalho Atual — Máximo 1–2 tarefas)
- [x] **MISSION-04:** Implementação e teste do **Simple Idea Evolution Loop MVP**:
  - [x] Construção do Donor Arsenal (`DONOR-ARSENAL.md`, `donor-manifest.json`).
  - [x] Elaboração de `M04-DONOR-HARVEST-SPEC.md` e hipótese `M04-H1`.
  - [x] Implementação de `SimpleIdeaState`, contratos Pydantic e prompts versionados.
  - [x] Implementação de `FakeModelRunner` e `NativeModelRunner`.
  - [x] Implementação de `SimpleLoopRunner` (Condições B e C) e `BaselineRunner` (Condição A).
  - [x] Implementação de `RunTracer` e CLI (`iee evolve`, `compare`, `inspect-run`).
  - [x] Criação de 3 fixtures sintéticas e execução do experimento EXP-M04-001.
  - [x] Criação de `CODE-MAP.md` e `TEST-MAP.md`.
  - [x] Suíte de 38 testes aprovados.
  - [x] Emissão do checkpoint `CP-20260826-004`.
- [ ] **TASK-000:** Gate de Governança: Apresentação do relatório final da Missão 04 e parada mandatória (*STOP*).

---

## 🟡 NEXT (Próximos Passos Candidatos — Pós-Avaliação Humana)
*(Aguardando avaliação humana do pacote de comparação cega)*
- [ ] **HUMAN-EVAL-001:** Avaliação humana cega das saídas do experimento EXP-M04-001 (`experiments/MISSION-04/comparison-packet.md`).
- [ ] **MISSION-05:** Definição da próxima missão (Refinamento de Prompts vs Comparação Multi-Modelos).

---

## 🔵 LATER (Trabalhos Futuros Planejados)
- **Fase 4:** Deliberação Multi-Agent Heurística com topologias fixas.
- **Fase 5:** Experimentos controlados de valor de coordenação (EXP-002 e EXP-003).
- **Fase 6:** Deliberation Control Engine Adaptativo (Otimização dinâmica de topologia e busca de workflows).
