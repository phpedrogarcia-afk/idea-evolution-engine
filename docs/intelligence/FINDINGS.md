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
