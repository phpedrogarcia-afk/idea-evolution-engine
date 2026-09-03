# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](../DECISIONS-LEDGER.md).

---

## 🟢 NOW (Próxima Decisão Imediata)
 
- [ ] **M06-P1-SUPERVISOR-REVIEW-AND-PHASE-P2-AUTHORIZATION:** Supervisor revisa a entrega da Fase P1 (Service Boundary: [`M06-P1-SERVICE-BOUNDARY-COMPLETION-RECORD.md`](../m06-productization/M06-P1-SERVICE-BOUNDARY-COMPLETION-RECORD.md)) e autoriza formalmente o início da Fase P2 (`EvolutionArtifact`).
 
---
 
## 🟡 NEXT (Condicionado à Autorização do Supervisor)
 
 1. [x] **P1-LEAN-CORE-SERVICE-BOUNDARY:** Implementada a camada de serviço `IdeaEvolutionService` desacoplada, encapsulando o `LeanLoopRunner`. (`COMPLETED`)
 2. [ ] **P2-EVOLUTION-ARTIFACT-SCHEMA:** Formalizar o schema Pydantic unificado de produto `EvolutionArtifact`.
 3. [ ] **P3-PROVENANCE-ONTOLOGY-GUARD:** Integrar salvaguardas ontológicas e rotulagem estrita de proveniência (`CORE_USER_EXPLICIT` vs `MODEL_CANDIDATE`).
 4. [ ] **P4-PROVIDER-ZERO-COST-GUARD:** Formalizar o `ProviderAdapter` com isolamento de transporte e garantia fail-closed de custo de bolso zero.
 5. [ ] **P5-CLI-LEAN-DEFAULT:** Atualizar a CLI oficial (`iee evolve`) para adotar a Condição C (Lean L1 Default) como padrão.
 6. [ ] **P6-HUMAN-RESULT-RENDERER:** Implementar o renderizador limpo de Markdown focado no usuário final, sem jargões ou ruídos de laboratório.
 7. [ ] **P7-E2E-ACCEPTANCE:** Executar bateria de testes ponta a ponta com casos reais e validar os 12 portões de aceitação do V1.
 8. [ ] **P8-PRODUCT-FREEZE:** Congelamento final e liberação do FioIdeias V1.
 
---
 
## 🔴 BLOCKED (Tarefas Bloqueadas)
 
 - **Implementação da Fase P2 antes da revisão da Fase P1:** Bloqueado (aguarda autorização do supervisor).
 - **Experimentos confirmatórios adicionais para M05.5:** Bloqueado (`M05.5_STATUS = COMPLETE`). Nenhum piloto sacrificial, benchmark ou teste de provedor adicional está autorizado.
 - **Uso de Condição B (Simple Loop) em produção:** Bloqueado até que receba proteções arquiteturais comprovadas contra spoofing de autoridade e contradições ontológicas.
 - **Bridge IEE ↔ FioOS com autoridade de execução:** Bloqueado até autorização formal e marcos futuros (`ADVISORY_SHADOW_NO_AUTHORITY`).


