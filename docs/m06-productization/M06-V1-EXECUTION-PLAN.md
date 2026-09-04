# M06-V1-EXECUTION-PLAN.md — Plano de Execução Sequencial do FioIdeias V1

> **PROGRAMA:** M06 — Productization  
> **SISTEMA:** FioIdeias V1 — Lean L1 Default  
> **ESTADO:** `FROZEN_FOR_SUPERVISOR_REVIEW`  
> **REGRA DE EXECUÇÃO:** Nenhuma implementação em larga escala deve ser iniciada antes da revisão e aprovação formal deste plano pelo supervisor.

---

## 1. Visão Geral das Fases de Implementação

O plano de transição é dividido em 8 fases delimitadas e auditáveis, priorizando **colheita e reuso antes de invenção**:

```
[P1: Service Boundary] ──► [P2: EvolutionArtifact] ──► [P3: Provenance & Ontology]
                                                                  │
[P6: Human Renderer]   ◄── [P5: Stable Entry Point] ◄── [P4: Provider & Cost Guard]
         │
         ▼
[P7: End-to-End Cases] ──► [P8: Product V1 Freeze]
```

---

## 2. Detalhamento Fase a Fase

### Fase 1 (P1) — Service Boundary & Congelamento do Core Lean — `COMPLETED`
- **Status:** `COMPLETED` (Ver [`M06-P1-SERVICE-BOUNDARY-COMPLETION-RECORD.md`](M06-P1-SERVICE-BOUNDARY-COMPLETION-RECORD.md))
- **Objetivo:** Criar a camada de serviço `IdeaEvolutionService` como fachada desacoplada, encapsulando o `LeanLoopRunner` sem alterar seus contratos internos ou sua validação.
- **Arquivos Afetados:**
  - `src/idea_evolution/service/__init__.py` [NEW]
  - `src/idea_evolution/service/contracts.py` [NEW]
  - `src/idea_evolution/service/evolution_service.py` [NEW]
  - `tests/test_fioideias_v1_service_boundary.py` [NEW]
- **Oportunidades de Reuso:**
  - `LeanLoopRunner` (`src/idea_evolution/orchestration/lean_loop.py`): Utilizado 100% como motor de inferência sem mutação.
  - `RunTracer` (`src/idea_evolution/tracing/tracer.py`): Gravação de telemetria e deltas em disco.
- **Testes de Aceite:** 11 testes unitários determinísticos passando em `tests/test_fioideias_v1_service_boundary.py`.
- **Condição de Parada (Stop Condition):** Satisfeita. Serviço executável e testado sem quebra de integridade do core (`LEAN_CORE_HASH_MATCH = YES`).

---

### Fase 2 (P2) — Artefato Canônico de Evolução (`EvolutionArtifact`) — `COMPLETED`
- **Status:** `COMPLETED` (Ver [`M06-P2-EVOLUTION-ARTIFACT-COMPLETION-RECORD.md`](M06-P2-EVOLUTION-ARTIFACT-COMPLETION-RECORD.md))
- **Objetivo:** Formalizar o schema Pydantic unificado de produto `EvolutionArtifact`, consolidando o resultado de `LeanRunResult`, `LeanFirstPassOutput`, `FocusedEscalationOutput` e `DecisionDeltaRecord` em uma estrutura limpa, versionada e imutável.
- **Arquivos Afetados:**
  - `src/idea_evolution/artifacts/__init__.py` [NEW]
  - `src/idea_evolution/artifacts/evolution_artifact.py` [NEW]
  - `src/idea_evolution/artifacts/mapper.py` [NEW]
  - `src/idea_evolution/service/contracts.py` [MODIFY]
  - `src/idea_evolution/service/evolution_service.py` [MODIFY]
  - `tests/test_evolution_artifact.py` [NEW]
- **Oportunidades de Reuso:**
  - `LeanRunResult`, `LeanFirstPassOutput`, `FocusedEscalationOutput`, `DecisionDeltaRecord`, `SourceAnchor`.
- **Testes de Aceite:** 20 testes determinísticos passando em `tests/test_evolution_artifact.py`.
- **Condição de Parada:** Satisfeita. Artefato canônico integrado ao serviço sem mutação no núcleo científico (`LEAN_CORE_HASH_MATCH = YES`).

---

### Fase 3 (P3) — Proveniência Estrita e Salvaguardas Ontológicas — `COMPLETED`
- **Status:** `COMPLETED` (Ver [`M06-P3-PROVENANCE-ONTOLOGY-COMPLETION-RECORD.md`](M06-P3-PROVENANCE-ONTOLOGY-COMPLETION-RECORD.md))
- **Objetivo:** Endurecer o `EvolutionArtifact` para garantir deterministicamente que nenhuma inferência ou hipótese do modelo usurpe a autoridade humana (`USER_EXPLICIT != VALID_USER_DERIVATION != MODEL_CANDIDATE != UNKNOWN`).
- **Arquivos Afetados:**
  - `src/idea_evolution/artifacts/provenance.py` [NEW]
  - `src/idea_evolution/artifacts/evolution_artifact.py` [MODIFY]
  - `src/idea_evolution/artifacts/mapper.py` [MODIFY]
  - `src/idea_evolution/artifacts/__init__.py` [MODIFY]
  - `src/idea_evolution/service/evolution_service.py` [MODIFY]
  - `tests/test_fioideias_v1_provenance_guard.py` [NEW]
- **Oportunidades de Reuso:**
  - `AuthorityProofValidator` (`domain/grounding.py`), `SourceAnchor` (`domain/epistemic_contracts.py`), `PromotionAuthorityBasis`, `OntologyState`.
- **Testes de Aceite:** 20 testes adversariais passando em `tests/test_fioideias_v1_provenance_guard.py`. Total da suíte: 383 testes verdes.
- **Condição de Parada:** Satisfeita. `UNLABELED_SEMANTIC_ITEM_COUNT = 0`, zero modelo chamando modelo, integridade do hash do núcleo científico preservada (`LEAN_CORE_HASH_MATCH = YES`).

---

### Fase 4 (P4) — Fronteira de Provedor e Guard de Custo Zero — `COMPLETED`
- **Status:** `COMPLETED` (Ver [`M06-P4-PROVIDER-BOUNDARY-COMPLETION-RECORD.md`](M06-P4-PROVIDER-BOUNDARY-COMPLETION-RECORD.md))
- **Objetivo:** Estabelecer a fronteira operacional desacoplada de provedor, reutilizando o `ModelRunner` sem duplicações e implementando o guard determinístico contra qualquer chamada paga (`OUT_OF_POCKET_COST = ZERO`, `PAID_INFERENCE_ALLOWED = NO`, `UNKNOWN_COST_FAIL_CLOSED = YES`).
- **Arquivos Afetados:**
  - `src/idea_evolution/config/cost_policy.py` [NEW]
  - `src/idea_evolution/service/contracts.py` [MODIFY]
  - `src/idea_evolution/service/evolution_service.py` [MODIFY]
  - `tests/test_fioideias_v1_provider_guard.py` [NEW]
- **Oportunidades de Reuso:**
  - `ModelRunner` (`providers/base.py` - frozen).
  - `ModelCatalog`, `CostClass`, `LifecycleStatus` (`config/catalog.py`).
  - `CerebrasRunner` (`providers/cerebras.py`).
- **Testes de Aceite:** 20 testes determinísticos passando em `tests/test_fioideias_v1_provider_guard.py`. Total da suíte: 403 testes verdes.
- **Condição de Parada:** Satisfeita. `EXISTING_PROVIDER_ABSTRACTION_REUSED = YES`, `NEW_PROVIDER_ABSTRACTION_CREATED = NO`, `OUT_OF_POCKET_COST = ZERO`, `LEAN_CORE_HASH_MATCH = YES`.

---

### Fase 5 (P5) — Ponto de Entrada Estável (CLI `iee evolve`) — [COMPLETED]
- **Objetivo:** Estabelecer a CLI oficial em `src/idea_evolution/cli/main.py` apontando `FioIdeias V1 — Lean L1 Default` como a rota padrão incondicional através do `IdeaEvolutionService`, sem bypass e sem expor loops experimentais.
- **Arquivos Afetados:**
  - `src/idea_evolution/cli/main.py` [MODIFY]
  - `src/idea_evolution/cli/__init__.py` [NEW]
  - `pyproject.toml` [NEW]
  - `iee.cmd` [NEW]
  - `iee` [NEW]
  - `tests/test_fioideias_v1_cli.py` [NEW]
  - `docs/m06-productization/M06-P5-STABLE-ENTRY-POINT-COMPLETION-RECORD.md` [NEW]
- **Oportunidades de Reuso:**
  - Estrutura de subparsers `argparse` existente, roteada exclusivamente para `IdeaEvolutionService`.
  - Empacotamento padrão com `pyproject.toml` e wrappers de terminal.
- **Testes de Aceite:** 20 testes determinísticos em `tests/test_fioideias_v1_cli.py` cobrindo roteamento, serialização de `EvolutionArtifact`, sanitização e tratamento de erros operacionais. Total da suíte: 423 testes verdes.
- **Condição de Parada:** Satisfeita. `CLI_ENTRY_POINT_EXISTS = YES`, `IEE_EVOLVE_WORKS = YES`, `CLI_DEFAULT_TREATMENT = LEAN_L1`, `CLI_USES_IDEA_EVOLUTION_SERVICE = YES`, `CLI_BYPASSES_SERVICE = NO`, `CONDITION_B_PUBLICLY_EXPOSED = NO`, `LEAN_CORE_HASH_MATCH = YES`.

---

### Fase 6 (P6) — Renderizador Humano Limpo (`HumanResultRenderer`) — [COMPLETED]
- **Objetivo:** Implementar o renderizador de Markdown focado no usuário final, sem jargões de laboratório ou resíduos de validação, integrado centralizadamente à CLI `iee evolve`.
- **Arquivos Afetados:**
  - `src/idea_evolution/rendering/__init__.py` [NEW]
  - `src/idea_evolution/rendering/human_result.py` [NEW]
  - `src/idea_evolution/cli/main.py` [MODIFY]
  - `tests/test_fioideias_v1_human_renderer.py` [NEW]
  - `docs/m06-productization/M06-P6-HUMAN-RESULT-RENDERER-COMPLETION-RECORD.md` [NEW]
- **Oportunidades de Reuso:**
  - `sanitize_secret_text` para mascaramento de segredos.
  - Formato Markdown compatível para exibição em terminal e persistência.
- **Testes de Aceite:** 22 testes determinísticos em `tests/test_fioideias_v1_human_renderer.py` aprovados, cobrindo todas as 9 seções canônicas, honestidade epistêmica de autoridade, supressão de jargões experimentais e determinismo. Total da suíte: 445 testes verdes.
- **Condição de Parada:** Satisfeita. `HUMAN_RESULT_RENDERER_EXISTS = YES`, `RENDERER_MODEL_CALLS = 0`, `DEFAULT_CLI_USES_HUMAN_RENDERER = YES`, `CLI_JSON_OUTPUT_UNCHANGED = YES`, `ORIGINAL_IDEA_VISIBLE = YES`, `REFINED_IDEA_VISIBLE = YES`, `DERIVED_INTENT_NOT_PRESENTED_AS_EXPLICIT = YES`, `LEAN_CORE_HASH_MATCH = YES`.

---

### Fase 7 (P7) — Casos Reais de Ponta a Ponta & Auditoria de Aceite — `COMPLETED`
- **Status:** `COMPLETED` (Ver [`M06-P7-REAL-E2E-ACCEPTANCE-RECORD.md`](M06-P7-REAL-E2E-ACCEPTANCE-RECORD.md), [`M06-P7-REAL-E2E-RESULTS.json`](M06-P7-REAL-E2E-RESULTS.json), [`M06-P7-HUMAN-ACCEPTANCE-PACKET.md`](M06-P7-HUMAN-ACCEPTANCE-PACKET.md))
- **Objetivo:** Executar o motor FioIdeias V1 sobre um conjunto de 8 ideias reais representativas através da CLI pública `iee evolve` sob política estrita de custo zero (`OUT_OF_POCKET_COST = ZERO`), avaliando os 12 portões de aceitação do V1.
- **Arquivos Criados/Afetados:**
  - `docs/m06-productization/M06-P7-REAL-E2E-ACCEPTANCE-RECORD.md` [NEW]
  - `docs/m06-productization/M06-P7-REAL-E2E-RESULTS.json` [NEW]
  - `docs/m06-productization/M06-P7-HUMAN-ACCEPTANCE-PACKET.md` [NEW]
  - `src/idea_evolution/cli/main.py` [MODIFY - persistência de `evolution_artifact.json` no diretório de run]
- **Resultados de Aceite:**
  - 8/8 casos reais executados com sucesso (10 chamadas no total, média 1.25 chamadas/caso).
  - 1 smoke test de fallback rápido (`--fast`) aprovado (1 chamada).
  - 1 teste negativo de Condição B rejeitado com sucesso (não exposta publicamente).
  - 12/12 portões de aceitação satisfeitos (`P7_ACCEPTANCE = PASS`).
  - Suíte de regressão global: 445/445 testes verdes.
  - Custo de bolso total: `$0.00`.
- **Condição de Parada:** Satisfeita. `P7_ACCEPTANCE = PASS`, `V1_BLOCKERS = 0`, integridade do núcleo científico preservada (`LEAN_CORE_HASH_MATCH = YES`). Parada formal para revisão do supervisor antes da Fase P8.

---

### Fase 8 (P8) — Congelamento Final do Produto V1 & Documentação — `COMPLETED`
- **Status:** `COMPLETED` (Ver [`M06-P8-FIOIDEIAS-V1-FINAL-FREEZE.md`](M06-P8-FIOIDEIAS-V1-FINAL-FREEZE.md), [`M06-CLOSURE-RECORD.md`](M06-CLOSURE-RECORD.md), [`FIOIDEIAS-V1-RELEASE-MANIFEST.json`](../../FIOIDEIAS-V1-RELEASE-MANIFEST.json))
- **Objetivo:** Auditar metadados de empacotamento, atualizar a documentação viva do repositório (`README.md`, `CURRENT-STATE.md`, `ACTIVE-QUEUE.md`, `INDEX.md`), verificar a integridade invariante do núcleo científico, gerar manifesto de release e formalizar a versão canônica 1.0.0 (`v1.0.0`).
- **Arquivos Criados/Afetados:**
  - `pyproject.toml` [MODIFY - versão 1.0.0 e metadados refinados]
  - `README.md` [MODIFY - quickstart e documentação canônica de usuário do V1]
  - `FIOIDEIAS-V1-RELEASE-MANIFEST.json` [NEW - manifesto legível por máquina]
  - `docs/m06-productization/M06-P8-FIOIDEIAS-V1-FINAL-FREEZE.md` [NEW - registro de congelamento]
  - `docs/m06-productization/M06-CLOSURE-RECORD.md` [NEW - encerramento formal do programa M06]
  - `docs/m06-productization/M06-V1-ACCEPTANCE-GATES.md` [MODIFY - status PASS em todos os 12 portões]
  - `docs/context/CURRENT-STATE.md` [MODIFY - snapshot de produto released]
  - `docs/context/ACTIVE-QUEUE.md` [MODIFY - encerramento do M06]
  - `docs/INDEX.md` [MODIFY - indexação dos artefatos finais]
- **Testes de Aceite:** 445/445 testes passando, integridade do hash do núcleo científico intacta (`LEAN_CORE_HASH_MATCH = YES`), worktree limpa e tag `v1.0.0` gerada.
- **Condição de Parada:** Satisfeita. `FIOIDEIAS_V1_STATUS = RELEASED`, `M06_STATUS = COMPLETE`. Parada definitiva para decisão humana sobre próximos passos pós-V1.

---

## 3. Resumo de Governança

> [!CAUTION]
> **RELEMBRANDO A REGRA DE OURO:**  
> A presente missão encerra-se com a entrega do planejamento e dos contratos congelados (Mapear, Congelar, Desenhar, Planejar). A execução física das Fases P1 a P8 ocorrerá nas missões operacionais subsequentes conforme autorizado pelo supervisor.
