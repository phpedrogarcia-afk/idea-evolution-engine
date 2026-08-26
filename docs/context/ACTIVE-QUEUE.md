# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

## 🟢 NOW (Trabalho Atual — Concluído)
- [x] **TASK-006.2-A:** Especificação Canônica da Fronteira IEE/FioOS e Protocolo V1 ([`docs/specs/IEE-FIOOS-PROTOCOL-v1.0.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/specs/IEE-FIOOS-PROTOCOL-v1.0.md)).
- [x] **TASK-006.2-B:** Contratos tipados Pydantic (`InvestigationIntent`, `FioOSMissionPlan`, `ExecutionIdentityBinding`, `EvidenceEnvelope`, `EpistemicUpdate`) em `src/idea_evolution/contracts/fioos_protocol.py`.
- [x] **TASK-006.2-C:** Atualização das Invariantes Constitucionais (Seção 1.9 e INV-09 a INV-12 em [`docs/GOVERNANCE-INVARIANTS.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/GOVERNANCE-INVARIANTS.md)).
- [x] **TASK-006.2-D:** Criação de 11 novos testes de invariantes de fronteira em `tests/unit/test_fioos_boundary_contracts.py` (total: 74 testes verdes).
- [ ] **TASK-000:** Gate de Governança: Apresentação do relatório da Missão 06.2 e parada mandatória (*STOP*).

---

## 🟡 NEXT (Próximos Passos — Após configuração de credenciais reais)
- [ ] **M05-B:** Reattack do Canário Real de modelo único (Groq `openai/gpt-oss-120b`) sobre a ideia de clarificação socrática com o prompt corrigido.
- [ ] **EXP-M05:** Execução do experimento controlado A/B/C sobre as 3 fixtures.

---

## 🔴 BLOCKED (Tarefas Bloqueadas)
- **M05-B:** Bloqueado por ausência de chaves de API configuradas no ambiente local.
