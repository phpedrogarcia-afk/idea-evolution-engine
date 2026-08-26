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


