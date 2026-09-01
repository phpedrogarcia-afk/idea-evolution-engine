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

### [FINDING-030] Envelope de Capacidade Deve Distinguir Serialização Conhecida de Estado Dependente
- **Claim:** O teto da plataforma é seguro, mas não serve como decisão de capacidade quando existem requests iniciais e repairs cuja serialização pode ser medida. A contagem exata com `HarmonyGptOss` reduziu o teto M05.5R1 de 27.262.976 para 11.226.334 tokens sem alterar A/B/C; as 80 posições dependentes de estado permanecem protegidas pelo guard de contexto porque os schemas permitem strings Unicode sem limite.
- **Evidence:** `M05.5R1-TOKEN-ENVELOPE-CALIBRATION.json`, `tools/experiments/m05_5r1_token_envelope.py` e 23 testes offline de envelope/ordem.
- **Status:** `CONFIRMED_BY_OFFLINE_TOKENIZATION_AND_CONTROLS`
- **Implications:** Capacity check autenticado pode usar o envelope calibrado; ele continua distinto de prova de saldo da conta, preflight ou autorização de execução.

---

### [FINDING-029] Quota Deve Ser Parte do Contrato Experimental, Não um Efeito Colateral do Transporte
- **Claim:** Um experimento comparativo não pode tratar limites de quota como detalhe operacional: output sem cap, reparos implícitos e ordem fixa de tratamentos impedem estimar capacidade e podem confundir o efeito do tratamento com posição na janela do provedor.
- **Evidence:** M05.5R1 Capacity Design Freeze: 104 gerações primárias, até 104 reparos estruturados adicionais, outputs M05.4 válidos e 18 testes sintéticos incluindo controles negativos de ordem, TPD desconhecido e retry não planejado.
- **Status:** `CONFIRMED_BY_OFFLINE_TESTS_AND_SOURCE_INSPECTION`
- **Implications:** A tentativa futura exige schedule comprometido, cap observável, pacing neutro e estado autenticado de TPD; falha de capacidade é `ABORTED_CAPACITY`/`INVALID_EXECUTION`, nunca resultado científico do produto.

---

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

---

### [FINDING-015] Prova Determinística de Autoridade e Soberania dos Gates Finais de Status
- **Claim:** Modelos de linguagem podem cometer *Authority Spoofing* ao alegar falsamente `USER_EXPLICIT` para conceitos não requisitados no input humano (ex: declarar que "mapa mental e criptografia" foram pedidos explícitos do usuário para "organizar ideias vagas"). A introdução do `AuthorityProofValidator` audita deterministicamente provas de ancoragem (`GroundingRecord`), rebaixando alegações espúrias para `MODEL_HYPOTHESIS` e mantendo a proposta como `CANDIDATE`. Além disso, o status final do pipeline é soberanamente governado por `_evaluate_hard_gates`, impedindo categoricamente que `REFINED_IDEA_READY` seja emitido quando houver violação ontológica, essence drift ou rebaixamento de autoridade, mesmo se o modelo de revisão recomendar conclusão.
- **Evidence:** Autópsia causal do RUN-20260826_202600-6639861f e 21 testes determinísticos em `test_adversarial_ontology_provenance.py` (98 testes totais verdes).
- **Status:** `CONFIRMED_BY_TESTS`
- **Implications:** Eliminação definitiva de apropriação indevida de autoridade humana por LLMs e garantia de que nenhum produto corrompido receba status de pronto.
- **Related Decisions:** [AGENTS.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/AGENTS.md), [GOVERNANCE-INVARIANTS.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/GOVERNANCE-INVARIANTS.md)

---

### [FINDING-016] Fonte != Representação e Disciplina Epistêmica de Ancoragem
- **Claim:** A confusão cognitiva entre a fonte humana bruta (`SourceAnchor`) e as representações intermediárias geradas por LLMs (`RepresentationRecord`, resumos, taxonomias, embeddings) é a causa primária do desvio de intenção (*essence drift*). A fonte possui autoridade primária imutável; representações geradas são mapas que não herdam autoridade. Insights destilados (`InsightRecord`) auxiliam a busca mas não constituem evidência empírica; promessas de ações futuras não constituem conclusão de execução.
- **Evidence:** 11 testes determinísticos em `test_adversarial_epistemic_donor_foundation.py` e contratos canônicos em `src/idea_evolution/domain/epistemic_contracts.py`.
- **Status:** `CONFIRMED_BY_TESTS`
- **Implications:** Proteção absoluta da intenção humana e isolamento formal entre observação primária e hipóteses causais inferidas.
- **Related Decisions:** [OBSERVATION-REPRESENTATION-INVARIANTS.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/epistemology/OBSERVATION-REPRESENTATION-INVARIANTS.md)

---

### [FINDING-017] Inteligência de Doadores: Colheita de Incertezas Pagas sem Dependência de Runtime (Arbor HTR-Lite)
- **Claim:** A incorporação de doadores externos (como Arbor / HTR) não deve ocorrer via importação de frameworks ou dependência cega de runtime, mas através da colheita cirúrgica de mecanismos de alto valor (linhagem condicionada a evidência, estado de pesquisa compacto, lições podadas com escopo e condições de reabertura, separação de geração e validação de novidade) combinada com a rejeição explícita de suas cicatrizes (merge threshold não imposto, fallback em score não verificado de LLM, sobreajuste adaptativo e árvore estrita de pai único).
- **Evidence:** Autópsia canônica em `docs/research/donors/ARBOR-DEEP-AUTOPSY.md` e visualizador determinístico `DonorIntelligenceCatalog`.
- **Status:** `CONFIRMED_BY_TESTS`
- **Implications:** Redução agressiva de incertezas sem turismo tecnológico nem inchaço arquitetural.
- **Related Decisions:** [DONOR-ARSENAL.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/research/DONOR-ARSENAL.md)

---

### [FINDING-018] Protocolo Experimental A/B/C Controlado (EXP-M05.2) e Auditoria de Proveniência Real
- **Claim:** A comparação de valor entre o IEE (Condição B), um modelo único (Condição A) e um loop de crítica-revisão (Condição C) exige rigor experimental absoluto: especificação congelada antes da inspeção dos resultados, proibição de troca de modelo/fallback, blinding total (A/B/C mapeados para RESULT 1/2/3 sem vazar identidades) e auditoria de trabalho pago prévio (`PAID-WORK-INVENTORY.md`). Runs históricos pré-R5 não são cientificamente reusáveis devido a falhas de autoridade e ontologia anteriores à ativação do `AuthorityProofValidator`.
- **Evidence:** `PAID-WORK-INVENTORY.md`, `EXPERIMENT-SPEC-M05.2.md` e 5 testes de controle em `tests/experiment/test_abc_controlled_experiment.py`.
- **Status:** `CONFIRMED_BY_TESTS`
- **Implications:** O harness experimental garante avaliação cega sem auto-justificação do modelo produtor.
- **Related Decisions:** [EXPERIMENT-PROTOCOL.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/experiments/EXPERIMENT-PROTOCOL.md)

---

### [FINDING-019] Epistemic Waste Before Gate (Observação Empírica EXP-M05.2)
- **Claim:** Um sistema cognitivo dotado de *hard gates* determinísticos de proveniência e autoridade (R5) pode vetar com sucesso a promoção de hipóteses não ancoradas na fonte humana ao final da execução (gerando o status correto e honesto `REFINEMENT_INCOMPLETE`), mas ainda despender computação substancial, múltiplas chamadas de modelo e elaboração de hipóteses fracas nos estágios intermediários antes do veto acontecer no gate final (*Epistemic Waste Before Gate*).
- **Evidence:** Execução real `EXP-M05-ABC-REAL-20260827_110000` (Condição B consumiu 10 estágios/chamadas e reconstrução antes de barrar a promoção) e avaliação humana congelada em `experiments/EXP-M05.2-REAL/HUMAN-REVIEW-EVALUATION.md`.
- **Status:** `OBSERVED_IN_REAL_EXPERIMENT`
- **Implications:** A integridade de autoridade final funciona, mas sugere a necessidade futura de podas antecipadas de hipóteses não-ancoradas antes de estágios aprofundados de síntese/teste.
- **Related Decisions:** [HUMAN-REVIEW-EVALUATION.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/experiments/EXP-M05.2-REAL/HUMAN-REVIEW-EVALUATION.md)

---

### [FINDING-020] Aluguel de Complexidade Não Pago pelo Simple Loop Fixo (EXP-M05.2)
- **Claim:** Mais estágios e mais chamadas de modelo não se traduzem automaticamente em mais valor de decisão ($\text{More Stages} \neq \text{More Value}$). Na avaliação empírica do `EXP-M05.2`, a baseline de 1 chamada (Condição A = 48/65) e a crítica-revisão de 4 chamadas (Condição C = 44/65) superaram o pipeline fixo de 10 chamadas (Condição B = 31/65). O aluguel de complexidade de uma esteira multiestágio rígida não foi pago nesta execução e requer escalação condicional orientada por gaps.
- **Evidence:** `POST-REVEAL-ANALYSIS.md` e pontuação da rubrica humana em `HUMAN-REVIEW-EVALUATION.md`.
- **Status:** `SUPPORTED_BY_SINGLE_RUN` / `REQUIRES_REPLICATION`
- **Implications:** Direciona a evolução arquitetural para o Lean IEE (primeira passada enxuta + verificação determinística + escalação condicional).
- **Related Decisions:** [POST-REVEAL-ANALYSIS.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/experiments/EXP-M05.2-REAL/POST-REVEAL-ANALYSIS.md)

---

### [FINDING-021] Validação Adversarial Offline do Lean IEE L1 e Invariante de 2 Chamadas
- **Claim:** O Lean IEE com Early Epistemic Gate (L1) provou offline que: (1) ideias simples e bem ancoradas terminam após 1 chamada nominal; (2) invenções de hipóteses por modelos não autorizam escalação automática nem geram desperdício epistêmico; (3) autoridade normativa humana é respeitada com saída antecipada (`REQUEST_HUMAN_DECISION`) sem substituição por raciocínio de IA; (4) incertezas materiais reais disparam no máximo 1 escalação focada; (5) nenhuma condição ou saída de modelo ultrapassa o limite rígido de 2 chamadas de modelo (`LEAN_L1_MAX_MODEL_CALLS = 2`).
- **Evidence:** 12 cenários adversariais determinísticos em `tests/adversarial/test_adversarial_lean_iee.py` e implementação desacoplada em `src/idea_evolution/orchestration/lean_loop.py` e `src/idea_evolution/domain/early_epistemic_gate.py`.
- **Status:** `CONFIRMED_BY_OFFLINE_ADVERSARIAL_TESTS`
- **Implications:** Arquitetura candidata L1 pronta para calibração e replay offline (M05.3).
- **Related Decisions:** [ADR-019](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-019), [LEAN-IEE-DESIGN.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/architecture/LEAN-IEE-DESIGN.md)

---

### [FINDING-022] Formalização Doutrinária e Validação Offline do Fio Epistemic Dynamics (FioED-01)
- **Claim:** A formalização matemática e filosófica do FioED estruturou com sucesso: (1) a separação rigorosa em 4 camadas epistêmicas (Filosofia da Fonte $\neq$ Engenharia FioIdeias $\neq$ Arte Prévia $\neq$ Evidência do Receptor); (2) as 15 Leis Epistêmicas formais; (3) o ciclo inegociável $A \to C \to A$ onde toda concentração focada exige re-atenção determinística global; (4) métricas computáveis de `IntermediaryDepth`, `EvidenceFreePersistence` e `DriftRiskVector`; (5) admissão seletiva de memória institucional; (6) auditoria de arte prévia delimitando dívidas intelectuais com metaraciocínio racional e TMS sem falsas alegações de primeira descoberta.
- **Evidence:** Documentos doutrinários em `docs/epistemology/`, auditoria em `docs/research/FIOED-PRIOR-ART-AUDIT.md` e 7 testes adversariais formais em `tests/adversarial/test_adversarial_fioed.py` (total de 133 testes verdes).
- **Status:** `FORMALIZED_AND_VERIFIED_OFFLINE`
- **Implications:** Estabelece o alicerce teórico e as métricas necessárias para a missão M05.3 de replay offline e calibração de falsos positivos/negativos.
- **Related Decisions:** [KRISHNAMURTI-OJAI-1982-SOURCE-MAP.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/epistemology/KRISHNAMURTI-OJAI-1982-SOURCE-MAP.md), [FIO-EPISTEMIC-DYNAMICS.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/epistemology/FIO-EPISTEMIC-DYNAMICS.md), [FIOED-FORMAL-MODEL.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/epistemology/FIOED-FORMAL-MODEL.md)

---

### [FINDING-023] Endurecimento Epistêmico, Correção de Metadados de Doadores e Red-Team Formal (FioED-01R1)
- **Claim:** O endurecimento formal do FioED eliminou com rigor pseudoleis e imprecisões numéricas: (1) correção factual da citação do Arbor (*Toward Generalist Autonomous Research via Hypothesis-Tree Refinement*, arXiv:2606.11926, 10 de Junho de 2026); (2) remoção de precisão numérica arbitrária ($P_e \ge 2$ e $\text{Depth} \ge 2$ reclassificados como `TEST_FIXTURE_THRESHOLD` pendentes de calibração empírica); (3) auditoria e classificação epistemológica de todas as fórmulas em `INVARIANT`, `DEFINITION`, `HEURISTIC` e `OPERATIONAL_POLICY`; (4) distinção explícita entre `EXPLOITATIVE_RENT` e `EXPLORATORY_RENT` para preservar coragem investigativa; (5) registro de metadados de incompletude (`REPRESENTATION_ONLY`) no `AttentionSnapshot`; (6) preservação da soberania da fonte sem obediência a premissas faticamente impossíveis; (7) registro de `DECISION_REGRESSION` e expansão de 5 novos testes determinísticos formais (138 testes verdes).
- **Evidence:** Documentos revisados em `docs/epistemology/`, `docs/research/FIOED-PRIOR-ART-AUDIT.md` e 12 testes adversariais formais em `tests/adversarial/test_adversarial_fioed.py`.
- **Status:** `HARDENED_AND_BOUNDED`
- **Implications:** FioED pronto com máxima integridade para a Missão M05.3 de replay offline e calibração de limiares com dados reais.
- **Related Decisions:** [FIO-EPISTEMIC-DYNAMICS.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/epistemology/FIO-EPISTEMIC-DYNAMICS.md), [FIOED-FORMAL-MODEL.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/epistemology/FIOED-FORMAL-MODEL.md), [FIOED-PRIOR-ART-AUDIT.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/research/FIOED-PRIOR-ART-AUDIT.md)

---

### [FINDING-024] Institucionalização da Ecologia de Ideias e Fronteira da Realidade (FioED-02)
- **Claim:** A expansão FioED-02 integrou com sucesso a dimensão da incubação criativa à eficiência epistêmica: (1) Rejeição do modelo 'apenas arena' e formalização de $U_f$ (Fertile Unknown) e $U_g$ (Gap Unknown); (2) Zona de Incubação Protegida ($Z_p$) e Kernel de Identidade ($K(h)$) com isolamento estrito de falhas locais; (3) Vetor estruturado `PressureReadiness` e 4 verbos operacionais (`SEE`, `KEEP`, `PRESS`, `COMMIT`); (4) Questões Discriminativas ($Q^*$) com requisito mandatório de discriminação de estado; (5) As 3 Fronteiras da Realidade (Capacidade, Proveniência e Transição), `EvidencePassport` emitido por canal físico e estado `WAITING_FOR_REALITY`; (6) `TestabilityBinding` pré-declarado e congelado antes da observação; (7) Veto mecânico a `EVIDENCE_SPOOFING` via `EvidenceAdmissionGate` determinístico e validação de 24 novos testes adversariais (total de 162 testes verdes).
- **Evidence:** `docs/epistemology/FIOED-IDEA-ECOLOGY.md`, `docs/epistemology/FIOED-REALITY-BOUNDARY.md`, `src/idea_evolution/domain/idea_ecology.py`, `src/idea_evolution/domain/evidence_boundary.py` e `tests/adversarial/test_adversarial_idea_ecology.py`.
- **Status:** `FORMALIZED_AND_VERIFIED_OFFLINE`
- **Implications:** O modelo epistêmico completo está congelado para a execução da missão M05.3 de replay offline e calibração de limiares com traces reais.
- **Related Decisions:** [FIOED-IDEA-ECOLOGY.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/epistemology/FIOED-IDEA-ECOLOGY.md), [FIOED-REALITY-BOUNDARY.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/epistemology/FIOED-REALITY-BOUNDARY.md)

---

### [FINDING-025] Replay Offline e Consistência Retrospectiva do FioED com M05.2 (M05.3)
- **Claim:** O replay determinístico do experimento real M05.2 e das fixtures adversariais demonstrou que os sinais observáveis do FioED são retrospectivamente consistentes com os dados conhecidos de M05.2: (1) O caso de desperdício (Condição B, Simple Loop 10 chamadas) acumulou 9 passos de Persistência Sem Evidência ($P_e = 9$), 3 Regressões Decisórias graves e profundidade de intermediário 5, disparando os alertas de `AttachmentRisk` e `SourceRefresh`; (2) Os casos de alto valor (A=48 e C=44 na avaliação humana) apresentaram baixa persistência sem evidência e alto rendimento de `DecisionDelta` por chamada; (3) 0 tentativas de `EvidenceSpoofing` foram admitidas (100% bloqueadas); (4) $Q^*$ demonstrou $0\%$ de falsos positivos com os 5 critérios formais; (5) Ressalva epistêmica: como o FioED foi em parte motivado por M05.2, essa consistência retrospectiva não substitui a validação prospectiva independente.
- **Evidence:** `docs/experiments/M05.3-FIOED-OFFLINE-REPLAY.md`, `src/idea_evolution/experiments/fioed_replay.py` e `tests/unit/test_fioed_replay.py`.
- **Status:** `MECHANICALLY_VALIDATED_OFFLINE / RETROSPECTIVELY_CONSISTENT_WITH_M05.2 / PROSPECTIVE_VALIDATION_PENDING`
- **Implications:** FioED e Lean L1 demonstraram conformidade mecânica e consistência retrospectiva, estando prontos para o primeiro teste empírico prospectivo cego em ideias inéditas (M05.4).
- **Related Decisions:** [M05.3-FIOED-OFFLINE-REPLAY.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/experiments/M05.3-FIOED-OFFLINE-REPLAY.md)

---

### [FINDING-026] Pré-registro Prospectivo e Congelamento da Suíte Holdout (M05.4-P0)
- **Claim:** A primeira avaliação empírica prospectiva do FioED / Lean L1 foi formalmente pré-registrada e congelada antes da geração de qualquer saída real: (1) Suíte holdout de 8 ideias inéditas e minimalistas (`HOLDOUT-IDEAS.json`, hash `8c098995...`) cobrindo 8 classes epistêmicas distintas sem jargão interno; (2) Três condições congeladas: A (Baseline 1 chamada), B (Simple Loop controle 10 chamadas) e C (Lean L1 máx 2 chamadas); (3) Desfecho primário definido como Preferência Humana Cega por Ideia, complementado por 10 dimensões secundárias (incluindo Preservação Criativa e Moderação Apropriada); (4) Eliminação total de vazamentos de metadados via `BlindRenderer` determinístico (`src/idea_evolution/experiments/blind_renderer.py`); (5) Mapeamento cego aleatorizado por ideia com compromisso de hash imutável (`BLIND-REVEAL.sha256`); (6) 10 predições pré-registradas (PRED-01 a PRED-10) e critérios explícitos de derrota para C e vitória para A/B; (7) Manifesto de pré-registro congelado (`PREREGISTRATION-MANIFEST.json`) e 171 testes verdes (100% offline).
- **Evidence:** `experiments/EXP-M05.4-PROSPECTIVE/`, `src/idea_evolution/experiments/blind_renderer.py` e `tests/unit/test_m05_4_preregistration.py`.
- **Status:** `PREREGISTERED_AND_FROZEN_BEFORE_EXECUTION`
- **Implications:** O experimento M05.4 está cientificamente protegido contra fitting retrospectivo e p-hacking, pronto para a execução com API key na missão M05.4-P1.
- **Related Decisions:** [PREREGISTRATION.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/experiments/EXP-M05.4-PROSPECTIVE/PREREGISTRATION.md), [BLINDING-PROTOCOL.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/experiments/EXP-M05.4-PROSPECTIVE/BLINDING-PROTOCOL.md)

---

### [FINDING-027] Execução Real Prospectiva e Geração do Pacote Cego M05.4 (M05.4-P1)
- **Claim:** A execução prospectiva das 24 células experimentais (8 ideias holdout x 3 condições) foi concluída contra o provedor Groq (`openai/gpt-oss-120b`): (1) 28 chamadas reais registradas; (2) Manifesto de execução bruta congelado (`RAW-EXECUTION-MANIFEST.json`); (3) Instrumentação determinística FioED salva em `FIOED-INSTRUMENTATION.json`; (4) Pacote de avaliação cega desidentificado gerado via `BlindRenderer` (`BLIND-REVIEW-PACKET.md`, hash `5bce05da...`) com 0 vazamentos de metadados; (5) Compromisso do reveal verificado (`BLIND-REVEAL.sha256`); (6) Auditoria de integridade identificou defeito de roteamento na Condição B antes do início do review humano.
- **Evidence:** `experiments/EXP-M05.4-PROSPECTIVE/raw/`, `RAW-EXECUTION-MANIFEST.json`, `BLIND-REVIEW-PACKET.md` e `EXECUTION-SUMMARY.md`.
- **Status:** `EXECUTED_AUDITED_INVALIDATED_BEFORE_HUMAN_REVIEW`
- **Implications:** Identificada falha de execução na Condição B (defeito de injeção de modelo no router do Simple Loop), exigindo invalidação prévia ao review humano e rerun limpo.
- **Related Decisions:** [EXECUTION-SUMMARY.md](file:///c:/Users/phped/Documents/ProjetoFioIedeias/experiments/EXP-M05.4-PROSPECTIVE/EXECUTION-SUMMARY.md)

---

### [FINDING-028] Auditoria de Integridade de Execução M05.4-P1A e Causa-Raiz da Condição B
- **Claim:** A auditoria estrutural e de telemetria das 24 células de `EXP-M05.4-PROSPECTIVE-20260827` revelou que a Condição B (Simple Loop Control) não executou sua topologia multistage real de 6 estágios, falhando sistematicamente no estágio 1 (`UNDERSTAND`) com `terminal_status = FAILED`: (1) **Causa-Raiz:** Ao instanciar `SimpleLoopRunner(runner=self.runner)`, o construtor invoca `ModelRoutingConfig.default_single_model()`, que define o nome do modelo como `"default-model"`. O método `get_runner_for_stage()` repassa `"default-model"` ao `NativeModelRunner`, que tenta chamar o endpoint do Groq com esse identificador inválido em vez de `"openai/gpt-oss-120b"`. O estágio `UNDERSTAND` falha na chamada de rede com `PROVIDER_STRUCTURED_OUTPUT_REPAIR_FAILED`, acionando o retorno prematuro `state.status = RunStatus.FAILED` e abortando os 5 estágios subsequentes; (2) **Condição A e Condição C:** Executaram com 100% de integridade com `openai/gpt-oss-120b` (A: 8 chamadas completas; C: 12 chamadas governadas por `EarlyEpistemicGate`); (3) **Estado de Exposição:** `BLIND_REVIEW_STARTED = NO`, `HUMAN_SEMANTIC_EXPOSURE = NO`, `REVEAL_STATUS = SEALED` (o avaliador humano não inspecionou as respostas); (4) **Veredito:** `EXP-M05.4-PROSPECTIVE-20260827` classificado formalmente como `CONDITION_B_EXECUTION_INVALID / INVALIDATED_BEFORE_HUMAN_REVIEW`.
- **Evidence:** `src/idea_evolution/orchestration/simple_loop.py`, `experiments/EXP-M05.4-PROSPECTIVE/raw/runs_b/EXP-M05.4-IDEA-01-COND-B/stages/01_UNDERSTAND.json` e `IDEA-01_condition_b.json`.
- **Status:** `DIAGNOSED_ROOT_CAUSE_PROVEN`
- **Implications:** Proibido realizar avaliação humana sobre o pacote atual. O harness deve ser corrigido em missão dedicada (M05.4-P1R) com novo ID experimental, mantendo o protocolo pré-registrado e as 8 ideias holdout intactas.
- **Related Decisions:** [M05.4-P1A AUDIT](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/checkpoints/CP-20260827-027.md)



















