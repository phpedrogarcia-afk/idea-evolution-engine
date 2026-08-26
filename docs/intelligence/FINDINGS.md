# docs/intelligence/FINDINGS.md — Registro Canônico de Achados e Rastreabilidade

> **REGISTRO DE APRENDIZADOS INTERMEDIÁRIOS E RASTREABILIDADE EPISTÊMICA.**
> *Conecta evidências a decisões sem permitir saltos lógicos silenciosos.*

---

## 1. Cadeia Completa de Rastreabilidade

$$\text{Evidence} \longrightarrow \text{Finding} \longrightarrow \text{Decision} \longrightarrow \text{Spec} \longrightarrow \text{Code} \longrightarrow \text{Test}$$

Uma IA que pergunte: *"Por que temos o modo Single Agent como default?"* consegue navegar:
`ADR-006` $\leftarrow$ `FINDING-001` $\leftarrow$ `EVIDENCE-DCI-BENCHMARK` $\leftarrow$ `docs/research/donors/DCI.md`.

---

## 2. Catálogo de Achados Estruturados

### [FINDING-001] Deliberação Multiagente sem Filtro Apresenta Alto Custo e Baixo Retorno Marginal
- **Claim:** A introdução irrestrita de múltiplos agentes em tarefas de ideação aumenta o consumo de tokens exponencialmente sem garantir melhoria na diversidade de falhas críticas detectadas.
- **Evidence:** Autópsia do framework DCI e experimentos de Stanford (Level B).
- **Status:** `CONFIRMED_BY_DONOR`
- **Implications:** O sistema deve avaliar o `coordination_value` e priorizar `SINGLE_AGENT_MODE` como padrão econômico.
- **Related Decisions:** [ADR-006](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-006)
- **Related Hypotheses:** [HYP-002](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/foundations/SCIENTIFIC-HYPOTHESES.md)

---

### [FINDING-002] E-values Popperianos Não se Aplicam Diretamente a Hipóteses Qualitativas
- **Claim:** O método de inferência sequencial por e-values (POPPER) exige distribuições de probabilidade bem calibradas, sendo inviável para validação de proposições qualitativas de comportamento humano.
- **Evidence:** Autópsia do POPPER e análise metodológica de hipóteses de negócios (Level B).
- **Status:** `CONFIRMED_METHODOLOGICAL`
- **Implications:** O `TestContract` deve suportar múltiplos `verification_modes` (`STATISTICAL`, `EMPIRICAL_QUALITATIVE`, `FORMAL_LOGICAL`, `HUMAN_NORMATIVE`).
- **Related Decisions:** [ADR-009](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-009)
- **Related Hypotheses:** [OQ-002](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/OPEN-QUESTIONS.md)

---

### [FINDING-003] Validação Determinística em 5 Camadas Impede Conflitos Concorrentes e Desvio de Intenção
- **Claim:** A separação entre o plano probabilístico da IA (`GenomePatch`) e o plano determinístico do kernel (`GenomeValidator`) bloqueia mutações inválidas em regime all-or-nothing.
- **Evidence:** Autópsia do ArbiterOS e execução de testes de invariantes (Level C).
- **Status:** `DESIGN_CONFIRMED`
- **Implications:** LLMs nunca devem ter permissão de escrita direta no grafo imutável do `IdeaGenome`.
- **Related Decisions:** [ADR-003](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-003), [ADR-004](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-004)
- **Related Hypotheses:** [HYP-004](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/foundations/SCIENTIFIC-HYPOTHESES.md)

---

### [FINDING-004] Separação de Lentes Críticas (Lógica vs Viabilidade) Melhora Rastreabilidade de Falhas
- **Claim:** Submeter uma ideia a críticas especializadas sequenciais (`LogicalCritique` $\to$ `Revision` $\to$ `FeasibilityCritique` $\to$ `Revision`) isola falhas causais internas de gargalos práticos do mundo real, evitando que o crítico misture inconsistência conceitual com atrito de adoção.
- **Evidence:** Autópsia do MultiAgent Research Ideator e execução experimental EXP-M04-001 (Condição C).
- **Status:** `DESIGN_HYPOTHESIS_FORMALIZED`
- **Implications:** O IEE deve suportar topologia de crítica/revisão iterativa como opção de alta profundidade.
- **Related Decisions:** [M04-DONOR-HARVEST-SPEC](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/experiments/M04-DONOR-HARVEST-SPEC.md)
- **Related Hypotheses:** [M04-H1](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/foundations/SCIENTIFIC-HYPOTHESES.md#m04-h1)

---

### [FINDING-005] Kernel Determinístico com Bounded Repair (1 Retry) Evita Travamentos e Loops Infinitos
- **Claim:** Limitar deterministicamente o reparo mecânico de schemas a no máximo 1 tentativa e os ciclos de reconstrução a no máximo 1 ciclo garante terminação estrita e *fail-closed* ruidoso em caso de saídas corrompidas.
- **Evidence:** Testes unitários e adversariais da suíte M04 (`test_adversarial_mvp.py`, `test_reconstruction_path.py`).
- **Status:** `CONFIRMED_BY_TESTS`
- **Implications:** O loop do MVP atinge 100% de previsibilidade de fluxo com zero risco de divergência não controlada.
- **Related Decisions:** [ADR-014](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-014)

---

### [FINDING-006] Roteamento Multi-Modelo Não Exige Frameworks Pesados de Grafo
- **Claim:** A separação estrita entre contratos de estágio (`Stage contracts`) e despachadores de modelo (`RunnerRouter` via `ModelRoutingConfig`) permite rotear diferentes provedores/modelos por estágio através de uma camada fina nativa em Python, sem necessidade de dependências complexas como LangGraph ou LiteLLM.
- **Evidence:** Implementação e suíte de 49 testes automatizados da Missão 06 (`test_model_routing.py`, `test_multi_model_e2e.py`).
- **Status:** `CONFIRMED_BY_TESTS`
- **Implications:** Mantém a base de código ultra-leve, determinística e facilmente auditável.
- **Related Decisions:** [MODEL-ROUTING.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/specs/MODEL-ROUTING.md)

---

### [FINDING-007] Isolamento Rígido de Falha Impede Contaminação de Custo e Experimento
- **Claim:** Proibir explicitamente fallback silencioso entre provedores (`NO_CROSS_PROVIDER_FALLBACK`) garante que uma falha de API interrompa o fluxo com status `FAILED` e preserve o estado original sem distorcer medições empíricas ou gerar custos inesperados.
- **Evidence:** Teste adversarial `test_03_provider_failure_isolation_no_cross_fallback`.
- **Status:** `CONFIRMED_BY_TESTS`
- **Implications:** Experimentos científicos futuros permanecem válidos e isolados.
- **Related Decisions:** [MODEL-ROUTING.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/specs/MODEL-ROUTING.md)

---

### [FINDING-008] Model IDs Não São Conhecimento Atemporal (Model-Catalog Drift)
- **Claim:** Tratar identificadores de modelos de provedores como constantes estáticas leva a envelhecimento rápido do código (ex: `llama-3.3-70b-versatile` encerrado em 16/08/2026 e `gemini-2.0-flash` encerrado em 01/06/2026). A introdução de um catálogo de modelos versionado com `last_verified`, `status` (`SHUT_DOWN`, `ACTIVE`), classes de custo explícitas (`FREE_TIER`, `PAID`) e validação estrita impede falhas em tempo de execução e gastos acidentais.
- **Evidence:** Implementação do `ModelCatalog` e 12 novos testes da Missão 06.1 (`test_model_catalog.py`, `test_adversarial_catalog.py`).
- **Status:** `CONFIRMED_BY_TESTS`
- **Implications:** O IEE é capaz de operar com inteligência gratuita sob a política `FREE_ONLY` e diagnosticar modelos obsoletos via `iee providers doctor`.
- **Related Decisions:** [MODEL-ROUTING.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/specs/MODEL-ROUTING.md)

---

### [FINDING-009] Prevenção de Inchaço Especulativo Exige Isolamento de Três Camadas (CORE vs CANDIDATE)
- **Claim:** Modelos tendem a confundir alternativas geradas com requisitos obrigatórios do produto, inflando a ideia humana com arquiteturas desnecessárias (*Speculative Feature Accretion*). A instrução de síntese permissiva ("integrate the best mechanisms") é a causa raiz desse vazamento. Exigir que a síntese refine o `CORE` e isole possibilidades conceituais em `candidate_extensions` (não incorporadas ao core sem justificativa humana) restaura a fidelidade à intenção original.
- **Evidence:** Autópsia causal da Missão 05.1 e testes adversariais `test_adversarial_essence_drift.py`.
- **Status:** `CONFIRMED_BY_TESTS`
- **Implications:** O IEE mantém criatividade exploratória sem permitir que alucinações arquiteturais desfigurem a ideia humana.
- **Related Decisions:** [MODEL-ROUTING.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/specs/MODEL-ROUTING.md)

---

### [FINDING-010] Desacoplamento Estrito de Fronteira IEE/FioOS (Protocol V1)
- **Claim:** O desacoplamento formal entre Estado Epistêmico (IEE) e Governança Operacional/Execução (FioOS) via contratos tipados (`InvestigationIntent`, `FioOSMissionPlan`, `ExecutionIdentityBinding`, `EvidenceEnvelope`) previne vazamento de autoridade, segredos e comandos de execução no domínio epistemológico, respeitando o princípio de que arquitetura pode se preparar, mas a evidência deve conquistar a integração real.
- **Evidence:** Especificação canônica [`docs/specs/IEE-FIOOS-PROTOCOL-v1.0.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/specs/IEE-FIOOS-PROTOCOL-v1.0.md) e 11 testes determinísticos em `tests/unit/test_fioos_boundary_contracts.py`.
- **Status:** `CONFIRMED_BY_TESTS`
- **Implications:** O IEE permanece 100% autônomo e seguro em modo `STANDALONE`, com contratos prontos para integração futura governada pelo FioOS sem modificação do runtime atual.
- **Related Decisions:** [IEE-FIOOS-PROTOCOL-v1.0.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/specs/IEE-FIOOS-PROTOCOL-v1.0.md)

---

### [FINDING-011] Pureza Descritiva do UNDERSTAND é a Primeira Linha de Defesa Anti-Drift
- **Claim:** A contaminação semântica observada no primeiro canário real nasce no estágio `UNDERSTAND` quando o modelo introduz escolhas arquiteturais não solicitadas (ex: "mobile", "IA", "backend"). O estágio `UNDERSTAND` deve ser puramente descritivo e fiel à intenção; inferências úteis não explícitas devem ser isoladas estritamente em `assumptions` ou `candidate_extensions`.
- **Evidence:** Autópsia do RUN-008 e testes adversariais `test_adversarial_understand_and_groq_boundary.py`.
- **Status:** `CONFIRMED_BY_TESTS`
- **Implications:** O `current_idea` permanece fiel ao criador humano desde o estágio inicial, impedindo que o `ATTACK` downstream critique hipóteses não contratadas como fatos de design.
- **Related Decisions:** [MODEL-ROUTING.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/specs/MODEL-ROUTING.md)

---

### [FINDING-012] Groq Structured Outputs Exige Strict JSON Schema Recursivo e Bounded Repair
- **Claim:** Provedores como Groq (utilizando `openai/gpt-oss-120b`) rejeitam requisições estruturadas com código `json_validate_failed` se o schema não impuser `additionalProperties: false` e listar todas as propriedades em `required`. O uso do `to_strict_json_schema()` com modo `json_schema` strict=True no cliente Groq e a preservação de `failed_generation` com 1 tentativa de bounded repair garantem robustez e rastreabilidade total.
- **Evidence:** Testes automatizados `test_02_groq_strict_json_schema_compliance_all_stages` e integração do `NativeModelRunner`.
- **Status:** `CONFIRMED_BY_TESTS`
- **Implications:** Eliminação de erros 400 em provedores de inferência rápida sem enfraquecer o contrato de domínio Pydantic.
- **Related Decisions:** [MODEL-ROUTING.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/specs/MODEL-ROUTING.md)

---

### [FINDING-013] Consistência Ontológica, Proveniência de Promoção e Isolamento de Evidência Rejeitada
- **Claim:** A evolução de ideias gera contradições semânticas se (1) mecanismos forem promovidos ao Core sem justificativa registrada, (2) propostas rejeitadas permanecerem ativas como candidatas, ou (3) planos de teste do Core exigirem evidências para alternativas descartadas. A introdução do modelo `ProposalRecord`, a exigência de `core_mechanism_justification` / `AcceptedChangeItem`, e o isolamento de `exploratory_candidate_tests` com detecção determinística no `FINAL_REVIEW` garantem integridade total de linhagem.
- **Evidence:** Autópsia causal do RUN-009 e 4 testes determinísticos em `test_adversarial_ontology_provenance.py`.
- **Status:** `CONFIRMED_BY_TESTS`
- **Implications:** Eliminação de contradições ontológicas e contenção estrita do plano de testes do Core no IEE.
- **Related Decisions:** [IEE-FIOOS-PROTOCOL-v1.0.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/specs/IEE-FIOOS-PROTOCOL-v1.0.md)

---

### [FINDING-014] Alinhamento Pós-Síntese de Realidade, Autoridade Não Circular e Imutabilidade de Run ID
- **Claim:** Para que o `REALITY_CHECK` teste o Core aceito sem desalinhamento temporal, a topologia canônica deve posicionar `SYNTHESIZE` antes de `REALITY_CHECK`. A promoção para o Core exige base de autoridade tipada (`USER_EXPLICIT`, `VALID_USER_DERIVATION`, `EXTERNAL_EVIDENCE`, `HUMAN_DECISION`), proibindo que `MODEL_HYPOTHESIS` (preocupações técnicas auto-geradas por LLMs) redefinam circularmente a essência do produto. Além disso, a identidade do Run ID deve ser imutável (`RUN-<UTC_TIMESTAMP>-<UUID4_HEX8>`), independente do sistema de arquivos e imune a colisões concorrentes.
- **Evidence:** Autópsia das execuções reais em Cloud Shell e 9 testes determinísticos em `test_adversarial_ontology_provenance.py` (86 testes totais verdes).
- **Status:** `CONFIRMED_BY_TESTS`
- **Implications:** Eliminação definitiva de circularidade epistêmica, garantia de que o plano de testes avalia exatamente o Core aceito e integridade histórica inquestionável de evidências.
- **Related Decisions:** [OPERATING-DOCTRINE.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/doctrine/OPERATING-DOCTRINE.md)








