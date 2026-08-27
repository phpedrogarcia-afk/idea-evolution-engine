# ACTIVE-QUEUE.md — Fila de Trabalho Ativo e Próximos Passos

> **CASA CANÔNICA: [`docs/context/ACTIVE-QUEUE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/ACTIVE-QUEUE.md)**

---

## 🚦 Status Atual da Fila: PROTÓTIPO LEAN IEE L1 OFFLINE CONCLUÍDO | PRÓXIMO: CALIBRAÇÃO M05.3

### 📌 Marco Recém-Concluído:
- [x] **Protótipo Offline Lean IEE L1 (LEAN-PROTOTYPE-01):** Implementação de `LeanLoopRunner`, `EarlyEpistemicGate`, `LeanFirstPassOutput`, `FocusedEscalationOutput`, `DecisionDeltaRecord`, `EpistemicRentRecord` e validação dos 12 cenários adversariais T1-T12 (126 testes verdes).

---

## 🎯 Próxima Missão Imediata:
- **M05.3 LEAN IEE OFFLINE REPLAY & ADVERSARIAL CALIBRATION:**
  - *Objetivo:* Calibrar limiares de falso positivo/falso negativo de escalação com dados de runs históricas e cenários adversariais adicionais (100% offline).
  - *Regra:* Preservar o Simple Loop de produção como controle; zero chamadas de inferência paga/real.
