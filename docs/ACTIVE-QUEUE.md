# ACTIVE-QUEUE.md — Fila de Trabalho Ativo e Próximos Passos

> **CASA CANÔNICA: [`docs/context/ACTIVE-QUEUE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/ACTIVE-QUEUE.md)**

---

## 🚦 Status Atual da Fila: MISSÃO 06.1 CONCLUÍDA & FREE-ONLY HARDENED

### 📌 Tarefas Concluídas:
- [x] **TASK-001 a TASK-005:** Fundações, Hardening, Arquitetura de Inteligência, Doutrina, MVP e Preflight (Missões 01 a 05).
- [x] **TASK-006 & TASK-006.1:** Roteamento multi-modelo, `ModelCatalog`, governança de custos `FREE_ONLY`, remoção de modelos encerrados (`llama-3.3-70b-versatile`, `gemini-2.0-flash`), `providers doctor` expandido e 61 testes automatizados aprovados (`MULTI_MODEL_READY_OFFLINE = TRUE`, `FREE_ONLY_POLICY = INSTITUTIONALIZED`).

---

## 🛑 Ponto de Parada Mandatório (STOP)
- **Status do Canário Real (M05):** `BLOCKED_PROVIDER_CREDENTIAL_OR_COST`.
- **Status Multi-Modelo & Custo (M06.1):** `MULTI_MODEL_READY_OFFLINE = TRUE`, `FREE_ONLY_POLICY = INSTITUTIONALIZED`.
- **Ação Necessária:** O operador humano deve configurar a chave de API gratuita no `.env` local para desbloquear o Real Canary de custo zero (M05-B) e a deliberação real multi-modelo (M07).
