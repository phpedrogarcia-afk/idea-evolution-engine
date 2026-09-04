# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](../DECISIONS-LEDGER.md).

---

## 🟢 NOW (Próxima Decisão Imediata)
 
- [ ] **M06-P5-SUPERVISOR-REVIEW-AND-PHASE-P6-AUTHORIZATION:** Supervisor revisa a entrega da Fase P5 (Stable User Entry Point / `iee evolve` $\to$ Lean L1: [`M06-P5-STABLE-ENTRY-POINT-COMPLETION-RECORD.md`](../m06-productization/M06-P5-STABLE-ENTRY-POINT-COMPLETION-RECORD.md)) e autoriza formalmente o início da Fase P6 (Renderizador Humano Limpo `HumanResultRenderer`).
 
---
 
## 🟡 NEXT (Condicionado à Autorização do Supervisor)
 
 1. [x] **P1-LEAN-CORE-SERVICE-BOUNDARY:** Implementada a camada de serviço `IdeaEvolutionService` desacoplada, encapsulando o `LeanLoopRunner`. (`COMPLETED`)
 2. [x] **P2-EVOLUTION-ARTIFACT-SCHEMA:** Formalizado o schema Pydantic unificado de produto `EvolutionArtifact` e mapper determinístico. (`COMPLETED`)
 3. [x] **P3-PROVENANCE-ONTOLOGY-GUARD:** Endurecidas as salvaguardas ontológicas e rotulagem estrita de proveniência com `ProvenanceReceipt`. (`COMPLETED`)
 4. [x] **P4-PROVIDER-ZERO-COST-GUARD:** Fronteira operacional e salvaguarda fail-closed de custo zero (`OUT_OF_POCKET_COST = ZERO`, `PAID_INFERENCE_ALLOWED = NO`). (`COMPLETED`)
 5. [x] **P5-CLI-LEAN-DEFAULT:** CLI oficial (`iee evolve`) roteando via `IdeaEvolutionService` com Lean L1 por padrão. (`COMPLETED`)
 6. [ ] **P6-HUMAN-RESULT-RENDERER:** Implementar o renderizador limpo de Markdown focado no usuário final, sem jargões ou ruídos de laboratório.
 7. [ ] **P7-E2E-ACCEPTANCE:** Executar bateria de testes ponta a ponta com casos reais e validar os 12 portões de aceitação do V1.
 8. [ ] **P8-PRODUCT-FREEZE:** Congelamento final e liberação do FioIdeias V1.
 
---
 
## 🔴 BLOCKED (Tarefas Bloqueadas)
 
 - **Implementação da Fase P6 antes da revisão da Fase P5:** Bloqueado (aguarda autorização do supervisor).
 - **Experimentos confirmatórios adicionais para M05.5:** Bloqueado (`M05.5_STATUS = COMPLETE`). Nenhum piloto sacrificial, benchmark ou teste de provedor adicional está autorizado.
 - **Uso de Condição B (Simple Loop) em produção:** Bloqueado até que receba proteções arquiteturais comprovadas contra spoofing de autoridade e contradições ontológicas.
 - **Bridge IEE ↔ FioOS com autoridade de execução:** Bloqueado até autorização formal e marcos futuros (`ADVISORY_SHADOW_NO_AUTHORITY`).



