# ACTIVE-QUEUE.md — Fila de Trabalho Ativo e Próximos Passos

> **CASA CANÔNICA: [`docs/context/ACTIVE-QUEUE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/ACTIVE-QUEUE.md)**

---

## 🚦 Status Atual da Fila: MISSÃO 06 CONCLUÍDA & MULTI-MODEL READY OFFLINE

### 📌 Tarefas Concluídas:
- [x] **TASK-001 a TASK-005:** Fundações, Hardening, Arquitetura de Inteligência, Doutrina, MVP e Preflight (Missões 01 a 05).
- [x] **TASK-006 (Multi-Model Integration Readiness):** Especificação `MODEL-ROUTING.md`, `ModelRoutingConfig`, `RunnerRouter`, suporte a Anthropic, `providers doctor`, `routes show`, `--dry-run` e 49 testes automatizados aprovados (`MULTI_MODEL_READY_OFFLINE = TRUE`).

---

## 🛑 Ponto de Parada Mandatório (STOP)
- **Status do Canário Real (M05):** `BLOCKED_PROVIDER_CREDENTIAL_OR_COST`.
- **Status Multi-Modelo (M06):** `MULTI_MODEL_READY_OFFLINE = TRUE`.
- **Ação Necessária:** O operador humano deve configurar a chave de API no `.env` local para desbloquear o Real Canary (M05-B) e a primeira deliberação multi-modelo real (M07).
