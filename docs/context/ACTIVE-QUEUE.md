# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Próxima Missão Imediata)
- [ ] **MISSION-LEAN-PROTOTYPE-01:** **Lean IEE Minimal Offline Prototype**
  - **Objetivo:** Implementar os contratos offline, schemas Pydantic e o runner desacoplado para a Candidata L1 (`LeanFirstPass` + `EarlyEpistemicGate` + `ConditionalEscalation`), com suíte de testes unitários determinísticos (100% offline).
  - **Diretriz Mandatória:** NÃO alterar o `SimpleLoopRunner` de produção existente (mantido como Controle). NÃO executar chamadas reais de inferência.

---

## 🟡 NEXT (Próximos Passos na Fila)
1. [ ] **EXP-M05.3-REPLICATION-SETUP:** Preparação do harness de teste da suíte de replicação multicaso (IDEA-01 a IDEA-05).
2. [ ] **EXP-HTR-LITE-REPLAY:** Replay offline de runs históricos sob o modelo de linhagem `IdeaLineageNode`.
3. [ ] **DONOR-DEEP-AUTOPSIES:** Continuidade das autópsias profundas de doadores secundários no arsenal.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)
- *Nenhuma tarefa bloqueada no momento.*
