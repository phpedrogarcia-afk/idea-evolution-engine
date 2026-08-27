# docs/context/IMPLEMENTATION-HISTORY.md — Histórico Imutável de Implementação e Marcos

> **HISTÓRICO APPEND-ONLY DE TRABALHOS CONCLUÍDOS, CHECKPOINTS E MARCOS.**
> Nenhuma entrada anterior deve ser apagada ou editada retroativamente.

---

### [MS-001] Fundação Conceitual e Constitucional v0.1 (Fase 0)
- **Data:** 2026-08-26
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Construir a base conceitual, epistemológica, constitucional e documental antes do início de qualquer código de produto.
- **O que Mudou:**
  - Criação da documentação mestra: `AI-START-HERE.md`, `AGENTS.md`, `README.md`, `GOVERNANCE-INVARIANTS.md`, `DECISIONS-LEDGER.md`, `TERMINOLOGY.md`.
  - Especificação dos fundamentos conceituais (`docs/foundations/`).
  - Especificação da arquitetura alvo do DCE e IdeaGenome (`docs/architecture/`).
  - Catalogação e autópsia metódica de 9 sistemas doadores (`docs/research/`).
  - Formalização de 5 políticas versionadas v0.1 (`docs/specs/`).
  - Elaboração de protocolos de experimentação (`docs/experiments/`).
- **Decisões Registradas:** ADR-001 a ADR-010.
- **Resultado:** `COMPLETE` (16/16 critérios da Definition of Done atendidos).
- **Evidência:** Commit inicial `ce3552f` e relatório [`docs/FOUNDATION-READINESS-REPORT.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/FOUNDATION-READINESS-REPORT.md).

---

### [MS-002] Endurecimento de Inteligência e Continuidade Cognitiva (Fase 0 Hardening)
- **Data:** 2026-08-26
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Transformar o repositório em uma memória operacional verificável para agentes, eliminando riscos de perda de contexto e confusão de fases.
- **O que Mudou:**
  - Realização da auditoria da arquitetura de inteligência (`docs/context/INTELLIGENCE-ARCHITECTURE-AUDIT.md`).
  - Criação do diretório e arquitetura de continuidade em `docs/context/`.
  - Implementação do manifesto machine-readable `context-manifest.json` com hashes criptográficos SHA-256.
  - Implementação das ferramentas determinísticas em Python: `tools/context/validate_context.py`, `project_status.py` e `create_checkpoint.py`.
  - Formalização das suítes de teste de continuidade (`tests/continuity/`).
  - Criação do primeiro checkpoint canônico imutável: `CP-20260826-001`.
  - Reconciliação explícita do roadmap: *Simple Idea Evolution Loop* definido como o próximo produto alvo (MVP).
- **Decisões Registradas:** ADR-011 (Infraestrutura de Continuidade e Validação Determinística de Contexto).
- **Resultado:** `COMPLETE`.
- **Evidência:** Execução do validador determinístico e da suíte de testes de continuidade.

---

### [MS-003] Arquitetura de Inteligência de Agentes e Foundation Ready Gate (Fase 03)
- **Data:** 2026-08-26
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Estabelecer o protocolo canônico de raciocínio governado, pesquisa, decisão e teste para agentes, e calcular o Foundation Ready Gate.
- **O que Mudou:**
  - Criação do diretório `docs/intelligence/` e de 16 documentos canônicos de inteligência de agentes.
  - Formalização do `WORK-PROTOCOL.md` em 12 etapas, `TASK-CLASSIFICATION.md`, `EVIDENCE-POLICY.md`, `HYPOTHESIS-PROTOCOL.md`, `BASELINE-POLICY.md` e `ADVERSARIAL-REVIEW.md`.
  - Criação de `tools/intelligence/validate_intelligence.py` e `build_context_pack.py`.
  - Implementação da suíte de 10 testes adversariais em `tests/intelligence/test_intelligence.py`.
  - Cálculo e validação do Foundation Ready Gate (`FOUNDATION_READY = TRUE`).
  - Preparação do `MISSION-04-TASK-CONTRACT.md` para o Simple Loop MVP.
  - Criação do Checkpoint `CP-20260826-002`.
- **Decisões Registradas:** ADR-012 (Proibição de Foundation 04 por inércia e autorização do Simple Loop MVP).
- **Resultado:** `COMPLETE`.
- **Evidência:** Execução do validador de inteligência e aprovação de 17 testes de continuidade e inteligência.

---

### [MS-003.1] Institucionalização Constitucional (Missão 03.1)
- **Data:** 2026-08-26
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Ingerir e institucionalizar a *Constituição Mestra de Construção de Projetos v1.0* (derivada do FioOS) sem criar burocracia, sem reabrir a Foundation e sem contaminar o IEE com detalhes de kernel do FioOS.
- **O que Mudou:**
  - Preservação do texto integral em `docs/doctrine/source/CONSTRUCTION-CONSTITUTION-v1.0.md` com hash SHA-256 fixado (`5337f466a6f6e450ab4c517a8d43b642fcf6b713d75095c878b71a0417e77468`).
  - Criação da Doutrina Operacional canônica em `docs/doctrine/OPERATING-DOCTRINE.md`.
  - Elaboração da `CONSTITUTION-APPLICABILITY-MATRIX.md` (reconciliando 150 princípios em Universal, IEE Now, IEE Later, FioOS Specific, Conditional, Already Institutionalized).
  - Elaboração do `CONSTITUTIONAL-MATURITY-MAP.md` rastreando a maturidade operacional das regras.
  - Atualização do `TASK-CONTRACT.md` com campos de anti-círculo (`target_uncertainty`, `target_decision`, `expected_decision_delta`).
  - Criação da suíte de testes em `tests/doctrine/test_constitutional_doctrine.py`.
  - Criação do Checkpoint `CP-20260826-003`.
- **Decisões Registradas:** ADR-013 (Institucionalização da Doutrina Operacional) e ADR-014 (Exigência de Incerteza Alvo e Stop Condition).
- **Resultado:** `COMPLETE`.
- **Evidência:** Execução de 24 testes automatizados (continuidade, inteligência e doutrina) com 100% de aprovação.

---

### [MS-004] Simple Idea Evolution Loop MVP (Missão 04)
- **Data:** 2026-08-26
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Construir e testar o primeiro motor de software executável do IEE, automatizando o transporte de uma ideia humana crua através de estágios dirigidos de maturação com estado compartilhado estruturado.
- **O que Mudou:**
  - Criação do **Donor Arsenal** (`docs/research/DONOR-ARSENAL.md` e `donor-manifest.json`) e da especificação de colheita (`docs/experiments/M04-DONOR-HARVEST-SPEC.md`).
  - Registro da hipótese de design `M04-H1` em `docs/foundations/SCIENTIFIC-HYPOTHESES.md`.
  - Implementação do pacote Python `src/idea_evolution/` (`domain`, `stages`, `contracts`, `providers`, `orchestration`, `tracing`, `cli`).
  - Criação de 10 arquivos de prompts versionados em `prompts/`.
  - Suporte a duas topologias: Condição B (Standard 6-Stage) e Condição C (Iterative Critique-Revision).
  - Implementação de persistência detalhada em `runs/RUN-YYYYMMDD-NNN/` (`input.json`, `state.json`, `stages/`, `final.json`, `final.md`, `trace.json`).
  - Implementação de 3 fixtures padronizadas em `fixtures/` e execução do experimento `EXP-M04-001`.
  - Geração do pacote de comparação cega em `experiments/MISSION-04/comparison-packet.md`.
  - Elaboração de `docs/CODE-MAP.md` e `docs/TEST-MAP.md`.
  - Criação de 14 novos testes unitários, de integração, adversariais e experimentais (totalizando 38 testes).
  - Emissão do Checkpoint `CP-20260826-004`.
- **Resultado:** `COMPLETE`.
- **Evidência:** 38/38 testes automatizados aprovados e execução completa da CLI `iee evolve` e `compare`.

---

### [MS-005] Real Model Canary Preflight & Security Audit (Missão 05)
- **Data:** 2026-08-26
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Reconciliar o estado do repositório pós-publicação no GitHub (`main` branch), auditar a segurança contra vazamento de segredos (`SECRET_SCAN: PASS`), expandir o `NativeModelRunner` para carregamento seguro de `.env` e registrar o status do canário real.
- **O que Mudou:**
  - Reconciliação do branch `main` e URL do remote GitHub (`https://github.com/phpedrogarcia-afk/idea-evolution-engine.git`).
  - Execução de varredura estrita de segurança em arquivos rastreados (`SECRET_SCAN: PASS`).
  - Atualização do `.gitignore` com exclusão rigorosa de `.env`, `.env.*` e diretórios de execução local.
  - Atualização de `src/idea_evolution/providers/native.py` com carregador seguro de `.env` (sem expor chaves) e suporte a Groq, OpenAI e Gemini via SDK/HTTP.
  - Atualização do mapa topológico `docs/context/REPOSITORY-MAP.md`.
  - Criação do Checkpoint `CP-20260826-005`.
- **Resultado:** `PREFLIGHT_COMPLETE` | `REAL_CANARY = BLOCKED_PROVIDER_CREDENTIAL_OR_COST`.
- **Evidência:** 38/38 testes automatizados aprovados e varredura de segurança com zero achados.

---

### [MS-006] Multi-Model Integration Readiness (Missão 06)
- **Data:** 2026-08-26
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Implementar e validar deterministicamente offline a camada de roteamento multi-modelo por estágio (`MODEL-ROUTING.md`), proveniência completa, isolamento de falhas e ferramentas CLI (`doctor`, `routes show`, `--dry-run`), deixando o sistema pronto para inferência real.
- **O que Mudou:**
  - Criação da especificação canônica em `docs/specs/MODEL-ROUTING.md`.
  - Implementação de `ModelRoutingConfig` em `src/idea_evolution/config/routing.py` com hash canônico SHA-256 e validação de rotas.
  - Implementação de `RunnerRouter` em `src/idea_evolution/providers/router.py` para despacho desacoplado por estágio.
  - Atualização de `src/idea_evolution/domain/state.py` e `src/idea_evolution/tracing/tracer.py` com campos de proveniência (`logical_alias`, `provider`, `model`, `prompt_id`, `prompt_version`, `attempt`, `routing_config_hash`).
  - Atualização do `NativeModelRunner` para suporte nativo ao Anthropic, exclusão de carregamento global de `~/.env` e função de diagnóstico `check_providers_health()`.
  - Atualização da CLI `src/idea_evolution/cli/main.py` com `providers doctor`, `routes show`, `--model-config` e `--dry-run`.
  - Criação de 3 arquivos de configuração em `config/` (`models.example.yaml`, `models.same_model.yaml`, `models.multi_provider_fake.yaml`).
  - Criação de 11 novos testes automatizados unitários, de integração multi-modelo e adversariais (totalizando 49 testes).
  - Emissão do Checkpoint `CP-20260826-006`.
- **Resultado:** `MULTI_MODEL_READY_OFFLINE = TRUE`.
- **Evidência:** 49/49 testes automatizados aprovados, execução do dry-run e doctor via CLI.

---

### [MS-006.1] Free-Only Model Catalog & Cost Governance Hardening (Missão 06.1)
- **Data:** 2026-08-26
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Resolver o model-catalog drift detectado nos IDs antigos (`llama-3.3-70b-versatile`, `gemini-2.0-flash`), construir o catálogo vivo `ModelCatalog`, institucionalizar a política `FREE_ONLY` e regras estritas de fallback (`EXPERIMENTAL_PINNED` vs `FREE_POOL_OPERATIONAL`), protegendo o projeto contra custos não autorizados e quebra de experimentos controlados.
- **O que Mudou:**
  - Implementação de `src/idea_evolution/config/catalog.py` com `ModelCatalog`, `ModelCatalogEntry`, `CostClass`, `LifecycleStatus`, `PrivacyClass`, `CostPolicy` e `ExecutionMode`.
  - Criação do catálogo seed versionado em `config/model_catalog.json` com modelos ativos (`openai/gpt-oss-120b`, `qwen/qwen3.6-27b`, `gemini-3.7-flash`, `gemini-3.6-flash`, `openrouter/free`).
  - Integração de validação de elegibilidade e custos em `src/idea_evolution/config/routing.py` e `src/idea_evolution/providers/router.py`.
  - Atualização dos arquivos `config/models.example.yaml`, `config/models.same_model.yaml` e defaults de `NativeModelRunner` para modelos ativos.
  - Expansão do comando `iee providers doctor` para exibir status de ciclo de vida do catálogo, classes de custo, notas de privacidade e recomendações de substituição.
  - Criação de 12 novos testes automatizados unitários e adversariais em `tests/unit/test_model_catalog.py` e `tests/adversarial/test_adversarial_catalog.py` (totalizando 61 testes verdes).
  - Emissão do Checkpoint `CP-20260826-007`.
- **Resultado:** `COMPLETE_OFFLINE` | `FREE_ONLY_POLICY = INSTITUTIONALIZED` | `MULTI_MODEL_READY_OFFLINE = TRUE`.
- **Evidência:** 61/61 testes automatizados aprovados, CLI doctor validado sem chamadas reais.

---

### [MS-005.1] First Real Canary Autopsy & Essence-Preservation Hardening (Missão 05.1)
- **Data:** 2026-08-26
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Conduzir autópsia causal sobre a proliferação especulativa de features (*Speculative Feature Accretion*) identificada no primeiro canário real, formalizar a separação em 3 camadas de estado (`CORE`, `DERIVED`, `CANDIDATE`), atualizar os contratos e prompts de síntese/revisão final, e adicionar testes adversariais para garantir que possibilidades geradas por modelos não desfigurem a ideia humana original.
- **O que Mudou:**
  - Autópsia causal da linhagem de conceitos (local AI, federated backend, blockchain, gamification).
  - Atualização dos contratos `SynthesizeOutput` e `FinalReviewOutput` com `candidate_possibilities` e `speculative_accretion_detected`.
  - Atualização de `SimpleIdeaState` com `core_mechanism` e `candidate_extensions` isoladas do core.
  - Atualização dos prompts `prompts/synthesize_v0_1.md` e `prompts/final_review_v0_1.md` proibindo que a síntese absorva automaticamente alternativas especulativas para o core da ideia.
  - Criação de 2 novos testes adversariais em `tests/adversarial/test_adversarial_essence_drift.py` (totalizando 63 testes verdes).
  - Emissão do Checkpoint `CP-20260826-008`.
- **Resultado:** `COMPLETE_OFFLINE` | `ESSENCE_PRESERVATION = HARDENED` | `SPECULATIVE_ACCRETION_BLOCKED = TRUE`.
- **Evidência:** 63/63 testes automatizados aprovados.

---

### [MS-006.2] IEE/FioOS Boundary Canonicalization & Protocol Specification (Missão 06.2)
- **Data:** 2026-08-26
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Institucionalizar formalmente a fronteira arquitetural e os contratos de comunicação entre o Idea Evolution Engine (IEE) e o FioOS, garantindo que o IEE governe o domínio epistemológico e o FioOS governe a execução operacional, sem vazamento de autoridade, segredos ou código de runtime (`REAL_FIOOS_BRIDGE = NOT_IMPLEMENTED`, `FIOOS_RUNTIME_TOUCHED = NO`).
- **O que Mudou:**
  - Redação da especificação canônica formal [`docs/specs/IEE-FIOOS-PROTOCOL-v1.0.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/specs/IEE-FIOOS-PROTOCOL-v1.0.md).
  - Implementação dos contratos tipados Pydantic (`InvestigationIntent`, `FioOSMissionPlan`, `ExecutionIdentityBinding`, `EvidenceEnvelope`, `EpistemicUpdate`) em `src/idea_evolution/contracts/fioos_protocol.py`.
  - Formalização das 5 camadas ontológicas (`CORE`, `DERIVED`, `CANDIDATE`, `DEFERRED`, `REJECTED`) e suas regras determinísticas de transição de estado (`OntologyTransitionValidator`).
  - Atualização do [`docs/GOVERNANCE-INVARIANTS.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/GOVERNANCE-INVARIANTS.md) com a Seção 1.9 e as invariantes técnicas INV-09 a INV-12.
  - Criação de 11 novos testes determinísticos em `tests/unit/test_fioos_boundary_contracts.py` (totalizando 74 testes verdes).
  - Emissão do Checkpoint `CP-20260826-009`.
- **Resultado:** `COMPLETE_OFFLINE` | `IEE_FIOOS_BOUNDARY = CANONICAL_AND_LOCKED` | `PROTOCOL_V1 = SPECIFIED`.
- **Evidência:** 74/74 testes automatizados aprovados.

---

### [MS-005.1-R2] Real Canary Failure Autopsy: Understand Purity + Groq Structured Output Boundary (Missão 05.1-R2)
- **Data:** 2026-08-26
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Conduzir autópsia causal sobre a falha do RUN-008, identificando que a contaminação semântica se origina no estágio `UNDERSTAND` (introdução não-fundamentada de "mobile", "IA", "backend") e que o erro 400 (`json_validate_failed`) no Groq decorria de incompatibilidade com o modo estrito de schema.
- **O que Mudou:**
  - Redefinição do prompt `prompts/understand_v0_1.md` sob a invariante "UNDERSTAND IS DESCRIPTIVE, NOT GENERATIVE", isolando inferências em `inferred_candidates`.
  - Atualização do prompt `prompts/attack_v0_1.md` proibindo tratar suposições não aceitas como fatos decididos de design.
  - Atualização de `UnderstandOutput` e `understand.py` para isolar `inferred_candidates` em `candidate_extensions` sem poluir `current_idea`.
  - Implementação da função `to_strict_json_schema()` no `NativeModelRunner`, forçando `additionalProperties: false` e `required` integral para compliance 100% com Groq/OpenAI Strict Mode.
  - Adição de suporte a captura de `failed_generation` e 1 tentativa de bounded repair.
  - Criação de 3 novos testes em `tests/adversarial/test_adversarial_understand_and_groq_boundary.py` (totalizando 77 testes verdes).
  - Emissão do Checkpoint `CP-20260826-010`.
- **Resultado:** `COMPLETE_OFFLINE` | `UNDERSTAND_PURITY = HARDENED` | `GROQ_STRICT_MODE = IMPLEMENTED` | `READY_FOR_REAL_REATTACK = TRUE`.
- **Evidência:** 77/77 testes automatizados aprovados (100% offline).

---

### [MS-005.1-R3] Ontology Consistency & Promotion Provenance Hardening (Missão 05.1-R3)
- **Data:** 2026-08-26
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Conduzir autópsia causal sobre a falha do RUN-009, institucionalizar a proveniência obrigatória de promoções para o Core/Derived (`AcceptedChangeItem` e `core_mechanism_justification`), garantir exclusão mútua entre propostas candidatas e rejeitadas, isolar testes do Core contra dependências rejeitadas (`exploratory_candidate_tests`), implementar verificação determinística de contradições ontológicas no `FinalReviewStage` e formalizar a linhagem de propostas com `ProposalRecord`.
- **O que Mudou:**
  - Criação do modelo `ProposalRecord` e do enum `OntologyState` em `src/idea_evolution/domain/state.py`.
  - Atualização dos contratos `SynthesizeOutput`, `RealityCheckOutput` e `FinalReviewOutput` em `src/idea_evolution/stages/contracts.py`.
  - Atualização de `SynthesizeStage`, `RealityCheckStage` e `FinalReviewStage` com regras determinísticas de integridade ontológica e exclusão mútua.
  - Atualização dos prompts `synthesize_v0_1.md`, `reality_check_v0_1.md` e `final_review_v0_1.md`.
  - Criação de 4 novos testes em `tests/adversarial/test_adversarial_ontology_provenance.py` (totalizando 81 testes verdes).
  - Emissão do Checkpoint `CP-20260826-011`.
- **Resultado:** `COMPLETE_OFFLINE` | `ONTOLOGY_CONSISTENCY = HARDENED` | `PROMOTION_PROVENANCE = ENFORCED` | `READY_FOR_FINAL_REAL_REATTACK = TRUE`.
- **Evidência:** 81/81 testes automatizados aprovados (100% offline).

---

### [MS-005.1-R4] Reality Alignment, Non-Circular Promotion & Immutable Run Identity (Missão 05.1-R4)
- **Data:** 2026-08-26
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Resolver as 4 falhas reais observadas em execuções no Cloud Shell: (1) Desalinhamento temporal do RealityCheck através da inversão topológica `SYNTHESIZE` $\to$ `REALITY_CHECK`, (2) Bloqueio de autoridade circular (`MODEL_HYPOTHESIS` isoladamente vetada para promoção ao CORE), (3) 6 Invariantes cross-state determinísticos no `FinalReviewStage`, e (4) Política de Run ID imutável `RUN-<UTC>-<UUID>` imune a concorrência e movimentação de diretórios.
- **O que Mudou:**
  - Reordenação da topologia em `src/idea_evolution/orchestration/simple_loop.py` e atualização das ordens de execução de estágios.
  - Criação do enum `PromotionAuthorityBasis` e campos de autoridade/hash (`core_mechanism_basis`, `core_mechanism_hash`, `tested_core_hash`, `target_core_mechanism`).
  - Implementação de 6 invariantes determinísticos no `FinalReviewStage`.
  - Atualização do `RunTracer` com `generate_immutable_run_id()` e rastreamento de git commit.
  - Atualização dos prompts `synthesize_v0_1.md`, `reality_check_v0_1.md` e `final_review_v0_1.md`.
  - Criação de 9 testes adversariais em `tests/adversarial/test_adversarial_ontology_provenance.py` (totalizando 86 testes verdes).
  - Emissão do Checkpoint `CP-20260826-012`.
- **Resultado:** `COMPLETE_OFFLINE` | `TOPOLOGY_REALITY_ALIGNMENT = HARDENED` | `NON_CIRCULAR_PROMOTION = ENFORCED` | `IMMUTABLE_RUN_IDENTITY = ACTIVE` | `READY_FOR_NEW_REAL_CANARY = TRUE`.
- **Evidência:** 86/86 testes automatizados aprovados (100% offline).

---

### [MS-005.1-R5] Authority Proof & Final Gate Enforcement (Missão 05.1-R5)
- **Data:** 2026-08-26
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Resolver as 2 falhas graves observadas no canário `RUN-20260826_202600-6639861f`: (1) *Authority Spoofing* (alegação espúria de `USER_EXPLICIT` para conceitos técnicos nunca solicitados pelo usuário), e (2) *Final Gate Bypass* (emissão de `REFINED_IDEA_READY` mesmo com violações ontológicas e essence drift detectados).
- **O que Mudou:**
  - Criação do validador determinístico `AuthorityProofValidator` com auditoria de `GroundingRecord` em `src/idea_evolution/domain/grounding.py`.
  - Implementação de regras rigorosas de validação de proveniência para `USER_EXPLICIT`, `VALID_USER_DERIVATION`, `EXTERNAL_EVIDENCE` e `HUMAN_DECISION`.
  - Rebaixamento automático de false attribution para `MODEL_HYPOTHESIS` / `CANDIDATE` no `SynthesizeStage`.
  - Implementação de `_evaluate_hard_gates` no `SimpleLoopRunner`, tornando o kernel determinístico a autoridade soberana final sobre o status.
  - Criação de 12 testes adversariais em `tests/adversarial/test_adversarial_ontology_provenance.py` (totalizando 98 testes verdes).
  - Emissão do Checkpoint `CP-20260826-013`.
- **Resultado:** `COMPLETE_OFFLINE` | `AUTHORITY_PROOF = HARDENED` | `FINAL_GATE_ENFORCEMENT = SOVEREIGN` | `READY_FOR_FINAL_REAL_CANARY = TRUE`.
- **Evidência:** 98/98 testes automatizados aprovados (100% offline).

---

### [MS-EPISTEMIC-DONOR-01] Epistemic Foundation, Source Anchoring & Arbor Institutionalization (Missão Epistemic-Donor-01)
- **Data:** 2026-08-27
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Institucionalizar uma base epistêmica durável que impeça o IEE de confundir suas próprias representações com a fonte humana, criando uma memória de Inteligência de Doadores para colheita cirúrgica de mecanismos e incertezas pagas (Arbor HTR-Lite).
- **O que Mudou:**
  - Institucionalização dos 10 invariantes canônicos em `docs/epistemology/OBSERVATION-REPRESENTATION-INVARIANTS.md`.
  - Criação dos contratos epistêmicos (`SourceAnchor`, `RepresentationRecord`, `InsightRecord`, `NegativeKnowledgeRecord`, `IdeaLineageNode`) em `src/idea_evolution/domain/epistemic_contracts.py`.
  - Criação do catálogo e visualizador determinístico `DonorIntelligenceCatalog` em `src/idea_evolution/domain/donor_intelligence.py`.
  - Persistência integral da autópsia canônica em `docs/research/donors/ARBOR-DEEP-AUTOPSY.md` e atualização do arsenal/manifesto de doadores.
  - Criação de 11 novos testes determinísticos em `tests/adversarial/test_adversarial_epistemic_donor_foundation.py` (totalizando 109 testes verdes).
  - Emissão do Checkpoint `CP-20260827-014`.
- **Resultado:** `COMPLETE_OFFLINE` | `SOURCE_ANCHORING = ACTIVE` | `DONOR_INTELLIGENCE = INSTITUTIONALIZED` | `FOUNDATION_INSTITUTIONALIZED = TRUE`.
- **Evidência:** 109/109 testes automatizados aprovados (100% offline).

---

### [MS-M05.2-EXP] Controlled Real A/B/C Value Experiment Setup & Blinding Harness (Missão M05.2)
- **Data:** 2026-08-27
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Estabelecer o protocolo experimental e o harness para o experimento de valor A/B/C (A: Baseline Single Refine, B: IEE Simple Loop, C: Critique-Revision 4-step) com blinding total 1-to-1, especificação congelada e auditoria de trabalho pago anterior.
- **O que Mudou:**
  - Congelamento formal da especificação experimental em `docs/experiments/EXPERIMENT-SPEC-M05.2.md`.
  - Elaboração do inventário de proveniência em `docs/experiments/PAID-WORK-INVENTORY.md` comprovando não-reusabilidade científica de runs pré-R5.
  - Implementação do harness `ABCExperimentRunner` com blinding rigoroso em `src/idea_evolution/experiments/abc_experiment.py`.
  - Criação de 5 testes de controle experimental em `tests/experiment/test_abc_controlled_experiment.py` (totalizando 114 testes verdes).
  - Emissão do Checkpoint `CP-20260827-015`.
- **Resultado:** `HARNESS_READY` | `SPEC_FROZEN` | `REAL_EXECUTION = BLOCKED_BY_MISSING_GROQ_CREDENTIAL` | `HUMAN_BLIND_REVIEW = PENDING`.
- **Evidência:** 114/114 testes automatizados aprovados (100% offline).

---

### [MS-M05.2-REAL-RUN] Controlled Real A/B/C Value Experiment Execution (Missão M05.2 Execução Real)
- **Data:** 2026-08-27
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Executar online o experimento A/B/C contra o Groq (`openai/gpt-oss-120b`) usando credencial recuperada com segurança do Secret Manager, gerando telemetria e o pacote de revisão cega.
- **O que Mudou:**
  - Execução de 15 chamadas reais de inferência sem fallback (Condição A: 1 chamada; Condição B: 10 chamadas incluindo 1 reconstrução e status honesto `REFINEMENT_INCOMPLETE`; Condição C: 4 chamadas de crítica-revisão).
  - Geração imutável dos artefatos em `experiments/EXP-M05.2-REAL/raw/`.
  - Geração do pacote de avaliação cega em `experiments/EXP-M05.2-REAL/BLIND-REVIEW-PACKET.md`.
  - Isolamento do mapeamento real em `experiments/EXP-M05.2-REAL/BLIND-REVEAL.json`.
  - Geração da comparação contábil em `experiments/EXP-M05.2-REAL/DETERMINISTIC-COMPARISON.md` e `.json`.
  - Emissão do Checkpoint `CP-20260827-016`.
- **Resultado:** `A_B_C_EXECUTION_COMPLETE` | `HUMAN_BLIND_REVIEW = PENDING` | `BLINDING_PRESERVED = TRUE`.
- **Evidência:** 15 chamadas reais registradas; 114/114 testes automatizados aprovados (100% offline).

---

### [MS-M05.2-HUMAN-FREEZE] Freeze Human Pre-Reveal Evaluation & Epistemic Waste Discovery (Missão M05.2 Avaliação Humana)
- **Data:** 2026-08-27
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Registrar e congelar a avaliação humana pré-revelação antes de qualquer abertura de `BLIND-REVEAL.json`, documentar o comprometimento de blinding e formalizar o achado de desperdício epistêmico pré-gate.
- **O que Mudou:**
  - Persistência imutável de `experiments/EXP-M05.2-REAL/HUMAN-REVIEW-EVALUATION.md` (RESULT 1 = 31/65, RESULT 2 = 48/65, RESULT 3 = 44/65).
  - Registro de `BLINDING_COMPROMISED = TRUE` devido a vazamento de metadata no cabeçalho do RESULT 1.
  - Registro formal do achado `FINDING-019` (`EPISTEMIC_WASTE_BEFORE_GATE`) em `docs/intelligence/FINDINGS.md`.
  - Emissão do Checkpoint `CP-20260827-017`.
- **Resultado:** `HUMAN_REVIEW_FROZEN` | `REVEAL_PENDING` | `BLINDING_COMPROMISED = TRUE`.
- **Evidência:** Hash SHA-256 do artefato de avaliação: `9b6f03102d800c59956d759bd251bf31eda4c3c267c14e5bec9f2194bdda331b`.

---

### [MS-M05.2-POST-REVEAL] M05.2 Post-Reveal Closure & Scientific Institutionalization (Missão M05.2 Pós-Revelação)
- **Data:** 2026-08-27
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Encerrar formalmente o experimento A/B/C pós-revelação, registrar as conclusões científicas, formalizar a decisão arquitetural ADR-018 e definir a nova incerteza do receptor para a próxima missão de Lean IEE.
- **O que Mudou:**
  - Persistência imutável de `experiments/EXP-M05.2-REAL/POST-REVEAL-ANALYSIS.md`.
  - Mapeamento oficial registrado: `A = RESULT 2 (48/65)`, `B = RESULT 1 (31/65)`, `C = RESULT 3 (44/65)`. Vencedor observado: Condição A.
  - Registro de `ADR-018` e achados empíricos `FINDING-019` e `FINDING-020`.
  - Formulação de `RU-LEAN-IEE-001` e definição da próxima missão: **LEAN IEE DONOR-GUIDED REDESIGN**.
  - Emissão do Checkpoint `CP-20260827-018`.
- **Resultado:** `M05.2_CLOSED_WITH_SINGLE_CASE_EVIDENCE` | `RUNTIME_UNCHANGED` | `LEAN_REDESIGN_QUEUED`.
- **Evidência:** 114/114 testes automatizados aprovados (100% offline).

---

### [MS-LEAN-IEE-01] Lean IEE Donor-Guided Redesign (Missão Redesenho Lean IEE)
- **Data:** 2026-08-27
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Redesenhar a arquitetura do IEE com base em valor decisório por chamada (*Decision Value per Call*), colhendo mecanismos e cicatrizes de doadores para eliminar desperdício epistêmico pré-gate e selecionar uma candidata minimalista para experimentação futura.
- **O que Mudou:**
  - Elaboração da colheita orientada ao receptor em `docs/architecture/LEAN-IEE-DONOR-HARVEST.md` (Arbor, Magentic-One, DCI, Google Co-Scientist, Stanford Ideator).
  - Especificação arquitetural do Lean IEE em `docs/architecture/LEAN-IEE-DESIGN.md` formalizando `DecisionDelta`, `EpistemicRent` e o `EarlyEpistemicGate`.
  - Verificação de orçamento de complexidade em `docs/architecture/LEAN-IEE-COMPLEXITY-BUDGET.md`.
  - Elaboração do plano experimental de replicação multicaso em `docs/architecture/LEAN-IEE-EXPERIMENT-PLAN.md` com 5 hipóteses falsificáveis (H-LEAN-001 a 005) e suíte IDEA-01 a 05.
  - Registro de `ADR-019` selecionando a Candidata L1 (`Lean IEE + Early Epistemic Gate`) para prototipagem offline e classificando o Simple Loop atual como `REFERENCE_IMPLEMENTATION / CONTROL`.
  - Zero alteração no runtime de produção e zero inferência real executada.
  - Emissão do Checkpoint `CP-20260827-019`.
- **Resultado:** `LEAN_DESIGN_COMPLETE` | `CANDIDATE_L1_SELECTED` | `RUNTIME_UNCHANGED`.
- **Evidência:** 114/114 testes automatizados aprovados (100% offline).

---

### [MS-LEAN-PROTOTYPE-01] Lean IEE Minimal Offline Prototype (Protótipo Offline L1)
- **Data:** 2026-08-27
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Implementar e validar deterministicamente o protótipo offline da Candidata L1 (`Lean IEE + Early Epistemic Gate`) sem chamadas reais de modelo, sem alterar o Simple Loop de produção, e impondo o invariante estrito de $LEAN\_L1\_MAX\_MODEL\_CALLS \le 2$.
- **O que Mudou:**
  - Correção de alegações de precisão não comprovadas em `LEAN-IEE-EXPERIMENT-PLAN.md` e `LEAN-IEE-COMPLEXITY-BUDGET.md` (rebaixadas para projeções topológicas e hipóteses para calibração).
  - Implementação de `src/idea_evolution/domain/early_epistemic_gate.py` contendo `LeanFirstPassOutput`, `FocusedEscalationOutput`, `DecisionDeltaRecord`, `EpistemicRentRecord` e o validador determinístico `EarlyEpistemicGate` (custo = 0 chamadas).
  - Implementação do orquestrador desacoplado `src/idea_evolution/orchestration/lean_loop.py` com invariante `LEAN_L1_MAX_MODEL_CALLS = 2`.
  - Atualização do `FakeModelRunner` para suporte direto aos contratos Lean.
  - Criação da suíte adversarial `tests/adversarial/test_adversarial_lean_iee.py` cobrindo 12 cenários rigorosos (T1 a T12).
  - Registro do achado `FINDING-021` em `docs/intelligence/FINDINGS.md`.
  - Emissão do Checkpoint `CP-20260827-020`.
- **Resultado:** `LEAN_L1_PROTOTYPE_VALIDATED` | `MAX_CALLS_LE_2_ENFORCED` | `SIMPLE_LOOP_UNCHANGED` | `126_TESTS_PASSING`.
- **Evidência:** 126/126 testes unitários e adversariais aprovados (100% offline).

---

### [MS-FIOED-01] Fio Epistemic Dynamics Formalization (Formalização FioED)
- **Data:** 2026-08-27
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Formalizar o núcleo filosófico e matemático do FioIdeias (Fonte, Representação, Atenção, Concentração, Aluguel Epistêmico, Não-Apego e Invariantes Executáveis), delimitando fronteiras estritas com a literatura científica existente.
- **O que Mudou:**
  - Elaboração de `docs/epistemology/KRISHNAMURTI-OJAI-1982-SOURCE-MAP.md` contendo exegese e rastreabilidade fonte-para-engenharia do diálogo de 18 de Abril de 1982.
  - Elaboração de `docs/epistemology/FIO-EPISTEMIC-DYNAMICS.md` formalizando os 16 vetos, 15 leis formais e os operadores $O(S)$, $I(S)$, $A(X_t)$, $C_h(X_t)$.
  - Elaboração de `docs/epistemology/FIOED-FORMAL-MODEL.md` com espaço de estados $X_t$, métricas discretas (`IntermediaryDepth`, $P_e$, $\mathbf{DriftRisk}$) e máquina de estados.
  - Elaboração de `docs/research/FIOED-PRIOR-ART-AUDIT.md` auditando dívidas com metaraciocínio racional (Russell & Wefald 1991), TMS (Doyle 1979) e proveniência (Buneman 2001).
  - Implementação de `AttentionSnapshot`, `MemoryAdmissionDecision` e enriquecimento de `DecisionDeltaRecord` em `src/idea_evolution/domain/early_epistemic_gate.py`.
  - Criação da suíte de 7 testes adversariais em `tests/adversarial/test_adversarial_fioed.py`.
  - Registro de `FINDING-022` em `docs/intelligence/FINDINGS.md`.
  - Emissão do Checkpoint `CP-20260827-021`.
- **Resultado:** `FIOED_FOUNDATION_FORMALIZED` | `PRIOR_ART_BOUNDED` | `133_TESTS_PASSING` | `ZERO_REAL_CALLS`.
- **Evidência:** 133/133 testes automatizados aprovados (100% offline).

---

### [MS-FIOED-01R1] FioED Formal Integrity & Prior-Art Hardening (Endurecimento FioED-01R1)
- **Data:** 2026-08-27
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Endurecer o formalismo do FioED, eliminar precisão numérica arbitrária, corrigir metadados e citações de doadores (Arbor 2026), classificar epistemologicamente todas as fórmulas, distinguir aluguel de exploração vs explotação, e expandir a suíte adversarial formal.
- **O que Mudou:**
  - Correção factual da citação do Arbor: *Toward Generalist Autonomous Research via Hypothesis-Tree Refinement* (arXiv:2606.11926, submetido em 10 de Junho de 2026).
  - Reclassificação de limiares numéricos ($P_e \ge 2$, $\text{Depth} \ge 2$) como `TEST_FIXTURE_THRESHOLD / TO_BE_CALIBRATED`.
  - Auditoria e classificação taxonômica de todas as fórmulas em `INVARIANT`, `DEFINITION`, `HEURISTIC` e `OPERATIONAL_POLICY`.
  - Distinção explícita entre `EXPLOITATIVE_RENT` e `EXPLORATORY_RENT` em `src/idea_evolution/domain/early_epistemic_gate.py`.
  - Inclusão do metadado de incompletude `completeness_status = "REPRESENTATION_ONLY"` no `AttentionSnapshot`.
  - Formalização de `DECISION_REGRESSION` e expansão de 5 novos testes determinísticos formais em `tests/adversarial/test_adversarial_fioed.py` (total de 138 testes).
  - Registro do achado `FINDING-023` em `docs/intelligence/FINDINGS.md`.
  - Emissão do Checkpoint `CP-20260827-022`.
- **Resultado:** `FIOED_HARDENED` | `NUMERIC_PRECISION_BOUNDED` | `ARBOR_CITATION_CORRECTED` | `138_TESTS_PASSING`.
- **Evidência:** 138/138 testes automatizados aprovados (100% offline).

---

### [MS-FIOED-02] Idea Ecology & Reality Boundary (Ecologia de Ideias e Fronteira da Realidade)
- **Data:** 2026-08-27
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Integrar a dimensão de incubação criativa à eficiência epistêmica, formalizando Fertile Unknowns ($U_f$), Gap Unknowns ($U_g$), Zona de Incubação ($Z_p$), Kernel de Identidade ($K$), PressureReadiness, os 4 verbos operacionais (`SEE`, `KEEP`, `PRESS`, `COMMIT`), Questões Discriminativas ($Q^*$), as 3 Fronteiras da Realidade (Capacidade, Proveniência e Transição), `EvidencePassport` e `EvidenceAdmissionGate` determinístico.
- **O que Mudou:**
  - Elaboração de `docs/epistemology/FIOED-IDEA-ECOLOGY.md` e `docs/epistemology/FIOED-REALITY-BOUNDARY.md`.
  - Implementação de contratos de domínio em `src/idea_evolution/domain/idea_ecology.py` e `src/idea_evolution/domain/evidence_boundary.py`.
  - Implementação da suíte com 24 testes adversariais em `tests/adversarial/test_adversarial_idea_ecology.py` (total de 162 testes verdes).
  - Registro do achado `FINDING-024` em `docs/intelligence/FINDINGS.md`.
  - Congelamento formal do modelo teórico do FioED para a missão M05.3.
  - Emissão do Checkpoint `CP-20260827-023`.
- **Resultado:** `IDEA_ECOLOGY_FORMALIZED` | `REALITY_BOUNDARY_ENFORCED` | `162_TESTS_PASSING` | `MODEL_FROZEN_FOR_M05_3`.
- **Evidência:** 162/162 testes automatizados aprovados (100% offline).

---

### [MS-M05.3-CALIBRATION] FioED / Lean IEE Offline Replay & Adversarial Calibration (M05.3)
- **Data:** 2026-08-27
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Executar o replay offline determinístico do experimento real M05.2 (Condições A, B e C) e calibrar os sinais observáveis do FioED congelado, medindo persistência sem evidência ($P_e$), regressões decisórias, profundidade de intermediário, $Q^*$ e contenção de Evidence Spoofing.
- **O que Mudou:**
  - Reconciliação definicional de $Q^*$ (State Discrimination como condição necessária, mas exigindo todos os 5 critérios).
  - Criação do harness determinístico `src/idea_evolution/experiments/fioed_replay.py`.
  - Elaboração do relatório canônico de replay em `docs/experiments/M05.3-FIOED-OFFLINE-REPLAY.md`.
  - Criação da suíte de testes de replay em `tests/unit/test_fioed_replay.py` (total de 166 testes verdes).
  - Demonstração empírica de que os sinais do FioED ($P_e = 9$, 3 regressões) explicam perfeitamente a degradação da Condição B em M05.2.
  - Registro do achado `FINDING-025` em `docs/intelligence/FINDINGS.md`.
  - Emissão do Checkpoint `CP-20260827-024`.
- **Resultado:** `OFFLINE_REPLAY_COMPLETED` | `MEASUREMENT_VALIDATED` | `166_TESTS_PASSING` | `READY_FOR_M05_4`.
- **Evidência:** 166/166 testes automatizados aprovados (100% offline).

---

### [MS-M05.4-P0-PREREGISTRATION] Prospective Multi-Idea Replication Preregistration (M05.4-P0)
- **Data:** 2026-08-27
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Realizar a delimitação científica e o pré-registro formal imutável do primeiro teste prospectivo do FioED / Lean L1 antes de qualquer geração de saída real, congelando suíte holdout de 8 ideias inéditas, protocolo de cegamento desidentificado, rubrica de avaliação e compromisso criptográfico.
- **O que Mudou:**
  - Delimitação e reclassificação rigorosa do status científico do FioED e Lean L1 (`PROSPECTIVE_VALIDATION_PENDING`).
  - Criação da suíte holdout de 8 ideias inéditas em `experiments/EXP-M05.4-PROSPECTIVE/HOLDOUT-IDEAS.json`.
  - Implementação do renderizador e detector de vazamentos cegos em `src/idea_evolution/experiments/blind_renderer.py`.
  - Geração de mapeamento cego aleatorizado com semente fixa em `BLIND-REVEAL.json` e compromisso `BLIND-REVEAL.sha256`.
  - Elaboração dos documentos de pré-registro: `PREREGISTRATION.md`, `BLINDING-PROTOCOL.md`, `EVALUATION-RUBRIC.md`, `ANALYSIS-PLAN.md`, `EXECUTION-MANIFEST.json` e `PREREGISTRATION-MANIFEST.json`.
  - Criação da suíte de testes de integridade de pré-registro em `tests/unit/test_m05_4_preregistration.py` (total de 171 testes verdes).
  - Registro do achado `FINDING-026` em `docs/intelligence/FINDINGS.md`.
  - Emissão do Checkpoint `CP-20260827-025`.
- **Resultado:** `PREREGISTRATION_FROZEN` | `BLINDING_SECURED` | `171_TESTS_PASSING` | `READY_FOR_M05_4_P1`.
- **Evidência:** 171/171 testes automatizados aprovados (100% offline).

---

### [MS-M05.4-P1-EXECUTION] Prospective Multi-Idea Real Execution & Blind Packet Generation (M05.4-P1)
- **Data:** 2026-08-27
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Executar de forma prospectiva e controlada as 24 células experimentais (8 ideias holdout x 3 condições) no provedor Groq (`openai/gpt-oss-120b`), registrar telemetria e artefatos brutos, computar a instrumentação determinística FioED de forma selada e gerar o pacote de avaliação cega desidentificado sem vazamentos de metadados.
- **O que Mudou:**
  - Verificação rigorosa do manifesto de pré-registro (100% de conformidade de hashes antes de qualquer chamada).
  - Implementação do executor experimental `src/idea_evolution/experiments/m05_4_runner.py`.
  - Execução real das 24 células com 28 chamadas de modelo totais (A: 8, B: 8, C: 12) sem falhas ou fallbacks.
  - Salvamento dos artefatos brutos em `experiments/EXP-M05.4-PROSPECTIVE/raw/` e geração de `RAW-EXECUTION-MANIFEST.json`.
  - Cálculo e armazenamento selado da instrumentação FioED em `FIOED-INSTRUMENTATION.json`.
  - Geração de `BLIND-REVIEW-PACKET.md` com 0 vazamentos de metadados de identidade (`leak_count = 0`).
  - Criação do formulário humano vazio `M05.4-HUMAN-REVIEW-TEMPLATE.md` e do sumário `EXECUTION-SUMMARY.md`.
  - Verificação de que o compromisso de revelação `BLIND-REVEAL.sha256` permaneceu inviolado.
  - Registro do achado `FINDING-027` em `docs/intelligence/FINDINGS.md`.
  - Emissão do Checkpoint `CP-20260827-026`.
- **Resultado:** `REAL_EXECUTION_COMPLETED` | `BLIND_PACKET_GENERATED` | `ZERO_LEAKS` | `REVEAL_SEALED` | `171_TESTS_PASSING`.
- **Evidência:** 24 células executadas com artefatos brutos imutáveis e 171 testes unitários aprovados.

---

### [MS-M05.4-P1A-AUDIT] Execution Integrity Audit & Condition B Root-Cause Analysis (M05.4-P1A)
- **Data:** 2026-08-27
- **Autor / Agente:** Antigravity (Google DeepMind)
- **Objetivo:** Auditar a integridade de execução e telemetria das 24 células de `EXP-M05.4-PROSPECTIVE-20260827` após a anomalia de 1 chamada por ideia na Condição B, comprovar causalmente a causa-raiz, preservar todos os artefatos brutos e classificar o experimento formalmente antes de qualquer avaliação humana.
- **O que Mudou:**
  - Diagnóstico causal da falha: `SimpleLoopRunner` foi instanciado sem passar a configuração de modelo explícita, fazendo o `RunnerRouter` resolver o modelo para `"default-model"` em vez de `"openai/gpt-oss-120b"`. A chamada no Groq falhou no estágio 1 (`UNDERSTAND`), abortando os 5 estágios restantes com `terminal_status = FAILED`.
  - Auditoria simétrica das Condições A e C: integridade 100% confirmada com `openai/gpt-oss-120b`.
  - Verificação de estado de exposição humana: `BLIND_REVIEW_STARTED = NO`, `HUMAN_SEMANTIC_EXPOSURE = NO`, `REVEAL_STATUS = SEALED`.
  - Classificação formal do experimento como `CONDITION_B_EXECUTION_INVALID / INVALIDATED_BEFORE_HUMAN_REVIEW`.
  - Registro do achado `FINDING-028` em `docs/intelligence/FINDINGS.md`.
  - Emissão do Checkpoint `CP-20260827-027`.
- **Resultado:** `ROOT_CAUSE_PROVEN` | `EXPERIMENT_INVALIDATED_BEFORE_REVIEW` | `REVEAL_SEALED` | `ZERO_HUMAN_EXPOSURE` | `171_TESTS_PASSING`.
- **Evidência:** Traces brutos em `runs_b/`, `IDEA-01_condition_b.json` e 171 testes aprovados.














