# docs/context/ACTIVE-QUEUE.md — Fila Ativa de Tarefas

> **FILA DE TRABALHO ESTRUTURADA EM REGIME DE DISCIPLINA OPERACIONAL.**
> Nenhuma IA deve assumir tarefas fora da ordem prescrita sem registro no [`docs/DECISIONS-LEDGER.md`](../DECISIONS-LEDGER.md).

---

## 🟢 NOW (Próxima Decisão Imediata)
 
- [x] **FIOIDEIAS-V1.2-M2-STRONG-FIRST-PASS:** Implementada, verificada e congelada na branch `fioideias/v1.2-maturation`.
- [x] **FIOIDEIAS-V1.2-M3-DETERMINISTIC-COVERAGE-GATE:** Gate determinístico integrado após o mapper; estados `NO_BLOCKING_GAP_DETECTED` e `REPAIR_REQUIRED`; 15 testes M3 e suíte completa 602/602 aprovados offline.
- [ ] **V1.2-M4-FOCUSED-REPAIR:** Marco candidato futuro; requer missão humana separada. Não executar reparo, segunda chamada ou expansão de UI automaticamente.
- **Nota de autoridade:** esta autorização encerra somente M3; não autoriza M4, merge, tag ou release.
 
---

> A fila M06/V1.0 preservada abaixo é histórica e não substitui o estado V1.2 acima.
 
## 🟡 NEXT (Condicionado à Autorização do Supervisor)
 
 1. [x] **P1-LEAN-CORE-SERVICE-BOUNDARY:** Implementada a camada de serviço `IdeaEvolutionService` desacoplada, encapsulando o `LeanLoopRunner`. (`COMPLETED`)
 2. [x] **P2-EVOLUTION-ARTIFACT-SCHEMA:** Formalizado o schema Pydantic unificado de produto `EvolutionArtifact` e mapper determinístico. (`COMPLETED`)
 3. [x] **P3-PROVENANCE-ONTOLOGY-GUARD:** Endurecidas as salvaguardas ontológicas e rotulagem estrita de proveniência com `ProvenanceReceipt`. (`COMPLETED`)
 4. [x] **P4-PROVIDER-ZERO-COST-GUARD:** Fronteira operacional e salvaguarda fail-closed de custo zero (`OUT_OF_POCKET_COST = ZERO`, `PAID_INFERENCE_ALLOWED = NO`). (`COMPLETED`)
 5. [x] **P5-CLI-LEAN-DEFAULT:** CLI oficial (`iee evolve`) roteando via `IdeaEvolutionService` com Lean L1 por padrão. (`COMPLETED`)
 6. [x] **P6-HUMAN-RESULT-RENDERER:** Renderizador humano limpo de Markdown focado no usuário final, sem inferência e integrado centralizadamente à CLI. (`COMPLETED`)
 7. [x] **P7-E2E-ACCEPTANCE:** Execução ponta a ponta de 8 casos reais sob cota gratuita ($0), gerando artefatos canônicos e cumprindo os 12 portões de aceitação do V1. (`COMPLETED`)
 8. [x] **P8-PRODUCT-FREEZE:** Congelamento final, versionamento `1.0.0`, manifesto e liberação do FioIdeias V1. (`COMPLETED`)
 
---
 
## 🔴 BLOCKED (Tarefas Bloqueadas)
 
 - **Desenvolvimento pós-V1 autônomo sem autorização:** Bloqueado (aguarda deliberação humana).
 - **Experimentos confirmatórios adicionais para M05.5:** Bloqueado (`M05.5_STATUS = COMPLETE`). Nenhum piloto sacrificial, benchmark ou teste de provedor adicional está autorizado.
 - **Uso de Condição B (Simple Loop) em produção:** Bloqueado até que receba proteções arquiteturais comprovadas contra spoofing de autoridade e contradições ontológicas.
 - **Bridge IEE ↔ FioOS com autoridade de execução:** Bloqueado até autorização formal e marcos futuros (`ADVISORY_SHADOW_NO_AUTHORITY`).



