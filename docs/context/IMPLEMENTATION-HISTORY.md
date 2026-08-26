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
