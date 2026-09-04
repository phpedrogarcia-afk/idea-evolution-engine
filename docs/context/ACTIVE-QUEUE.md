# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](../DECISIONS-LEDGER.md).

---

## 🟢 NOW (Próxima Decisão Imediata)
 
- [ ] **M06-P7-SUPERVISOR-REVIEW-AND-PHASE-P8-AUTHORIZATION:** Supervisor revisa a entrega da Fase P7 (Real End-to-End V1 Acceptance: [`M06-P7-REAL-E2E-ACCEPTANCE-RECORD.md`](../m06-productization/M06-P7-REAL-E2E-ACCEPTANCE-RECORD.md), [`M06-P7-HUMAN-ACCEPTANCE-PACKET.md`](../m06-productization/M06-P7-HUMAN-ACCEPTANCE-PACKET.md)) e autoriza formalmente o avanço para a Fase P8 (Congelamento Final do Produto V1).
 
---
 
## 🟡 NEXT (Condicionado à Autorização do Supervisor)
 
 1. [x] **P1-LEAN-CORE-SERVICE-BOUNDARY:** Implementada a camada de serviço `IdeaEvolutionService` desacoplada, encapsulando o `LeanLoopRunner`. (`COMPLETED`)
 2. [x] **P2-EVOLUTION-ARTIFACT-SCHEMA:** Formalizado o schema Pydantic unificado de produto `EvolutionArtifact` e mapper determinístico. (`COMPLETED`)
 3. [x] **P3-PROVENANCE-ONTOLOGY-GUARD:** Endurecidas as salvaguardas ontológicas e rotulagem estrita de proveniência com `ProvenanceReceipt`. (`COMPLETED`)
 4. [x] **P4-PROVIDER-ZERO-COST-GUARD:** Fronteira operacional e salvaguarda fail-closed de custo zero (`OUT_OF_POCKET_COST = ZERO`, `PAID_INFERENCE_ALLOWED = NO`). (`COMPLETED`)
 5. [x] **P5-CLI-LEAN-DEFAULT:** CLI oficial (`iee evolve`) roteando via `IdeaEvolutionService` com Lean L1 por padrão. (`COMPLETED`)
 6. [x] **P6-HUMAN-RESULT-RENDERER:** Renderizador humano limpo de Markdown focado no usuário final, sem inferência e integrado centralizadamente à CLI. (`COMPLETED`)
 7. [x] **P7-E2E-ACCEPTANCE:** Execução ponta a ponta de 8 casos reais sob cota gratuita ($0), gerando artefatos canônicos e cumprindo os 12 portões de aceitação do V1. (`COMPLETED`)
 8. [ ] **P8-PRODUCT-FREEZE:** Congelamento final e liberação do FioIdeias V1.
 
---
 
## 🔴 BLOCKED (Tarefas Bloqueadas)
 
 - **Início da Fase P8 (Final Freeze) antes da revisão da Fase P7:** Bloqueado (aguarda autorização do supervisor).
 - **Experimentos confirmatórios adicionais para M05.5:** Bloqueado (`M05.5_STATUS = COMPLETE`). Nenhum piloto sacrificial, benchmark ou teste de provedor adicional está autorizado.
 - **Uso de Condição B (Simple Loop) em produção:** Bloqueado até que receba proteções arquiteturais comprovadas contra spoofing de autoridade e contradições ontológicas.
 - **Bridge IEE ↔ FioOS com autoridade de execução:** Bloqueado até autorização formal e marcos futuros (`ADVISORY_SHADOW_NO_AUTHORITY`).



