# ACTIVE-QUEUE.md — Fila de Trabalho Ativo e Próximos Passos

> Este documento define a fila estrita de tarefas autorizadas. Nenhuma IA ou colaborador deve iniciar tarefas não listadas ou fora de ordem sem uma decisão registrada no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🚦 Status Atual da Fila: FASE 0 (FOUNDATION / BEDROCK)

### 📌 Tarefas da Fase 0 (Em Conclusão Imediata Nesta Missão):
- [x] **TASK-001:** Criação da infraestrutura documental e de governança (`AI-START-HERE.md`, `AGENTS.md`, `SOURCE-OF-TRUTH.md`, `GOVERNANCE-INVARIANTS.md`, `DECISIONS-LEDGER.md`, `ACTIVE-QUEUE.md`, `TERMINOLOGY.md`, `FOUNDATION-AUDIT.md`).
- [x] **TASK-002:** Especificação dos fundamentos conceituais (`docs/foundations/`).
- [x] **TASK-003:** Especificação da arquitetura conceitual alvo (`docs/architecture/`).
- [x] **TASK-004:** Sistematização metodológica de autópsias e doadores (`docs/research/` e `donors/`).
- [x] **TASK-005:** Formalização das políticas versionadas v0.1 (`docs/specs/`).
- [x] **TASK-006:** Criação dos protocolos de experimentação científica (`docs/experiments/`).
- [x] **TASK-007:** Emissão do `FOUNDATION-READINESS-REPORT.md` e execução do Teste de Continuidade de 20 perguntas.

---

## 🛑 Ponto de Bloqueio Obrigatório (Gate de Fase 0 $\to$ Fase 1)
> **ATENÇÃO:** Ao concluir a TASK-007, a execução DEVE PARAR. Nenhuma linha de código ou schema da Fase 1 pode ser criada sem a aprovação explícita e nova missão dada pelo operador humano.

---

## 🔮 Backlog da Próxima Fase (Fase 1: Constitutional Core — Schemas & Validators)
*(Aguardando autorização humana para desbloqueio)*
1. **TASK-101:** Definição dos schemas JSON / Pydantic estritos para `IdeaGenome`, `GenomePatch`, `DeliberationContract`, `UncertaintyRecord`, `TensionRecord`, `DecisionRelevanceReport`, `DecisionDelta`, `GapRecord` e `TestContract`.
2. **TASK-102:** Implementação do `GenomeValidator` (código Python 100% determinístico, cobrindo Schema, Integridade Referencial, Matriz de Autoridade, Invariantes e Validação de Transições).
3. **TASK-103:** Criação da suíte de testes unitários, testes de invariantes e testes adversariais para o validador.
4. **TASK-104:** Implementação da máquina de estados puramente determinística e aplicação atômica de patches (*all-or-nothing*).
