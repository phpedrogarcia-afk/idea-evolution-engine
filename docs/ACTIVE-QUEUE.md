# ACTIVE-QUEUE.md — Fila de Trabalho Ativo e Próximos Passos

> **CASA CANÔNICA: [`docs/context/ACTIVE-QUEUE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/ACTIVE-QUEUE.md)**

---

## 🚦 Status Atual da Fila: REDESENHO LEAN IEE CONCLUÍDO | PRÓXIMO: PROTÓTIPO OFFLINE L1

### 📌 Marco Recém-Concluído:
- [x] **Redesenho Lean IEE (LEAN-IEE-01):** Colheita de doadores (`LEAN-IEE-DONOR-HARVEST.md`), especificação (`LEAN-IEE-DESIGN.md`), orçamento de complexidade (`LEAN-IEE-COMPLEXITY-BUDGET.md`), plano experimental (`LEAN-IEE-EXPERIMENT-PLAN.md`) e decisão `ADR-019` selecionando a Candidata L1.

---

## 🎯 Próxima Missão Imediata:
- **LEAN IEE MINIMAL OFFLINE PROTOTYPE:**
  - *Objetivo:* Criar os contratos Pydantic e o executor offline desacoplado da Candidata L1 com testes unitários determinísticos (100% offline).
  - *Regra:* Preservar intacto o `SimpleLoopRunner` de produção atual como grupo de controle; zero chamadas de inferência real nesta etapa.
