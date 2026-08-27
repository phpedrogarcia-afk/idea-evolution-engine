# docs/research/DONOR-ARSENAL.md — Arsenal Operacional de Doadores (v1.0)

> **O ARSENAL DE DOADORES É INDEXADO POR GAPS E MECANISMOS, NÃO POR FAMA.**
> *Antes de inventar arquitetura, colha mecanismos e cicatrizes de quem já resolveu problemas semelhantes.*

---

## 🎯 Índice Rápido por Gaps Receptores

| Gap Receptor do IEE | Doador Primário / Candidato | Mecanismo Essencial | Decisão de Transplante | Fase |
| :--- | :--- | :--- | :---: | :---: |
| **Estrutura de Crítica e Revisão Iterativa** | **MultiAgent Research Ideator** | Iterative critique-revision vs parallel critics | `ADAPT` | **M04** |
| **Saída Estruturada e Validação de Schemas** | **PydanticAI / Instructor** | Pydantic validation, schema repair, typed outputs | `ADAPT / DEPEND` | **M04** |
| **Representação de Tensão e Desacordo** | **DCI (Deliberative Council)** | Epistemic speech acts, tension preservation | `ADAPT` | **M04** |
| **Evolução de Hipóteses sem Perda de Linhagem** | **Google AI Co-Scientist** | Candidate preservation, meta-review, mutation tracking | `ADOPT_CONCEPT` | M05+ |
| **Perguntas de Pesquisa e Checagem de Fatos** | **STORM / Co-STORM** | Perspective-guided questioning, fact checking | `ADOPT_CONCEPT` | M05+ |
| **Testes de Regressão e Red-Teaming de Prompts** | **Promptfoo** | Fixtures, assertions, automated red-teaming | `ADAPT` | **M04** |
| **Execução Durável de Grafos e Checkpoints** | **LangGraph** | Graph checkpointing, interrupt, resume | `REJECT_NOW (DEFER)` | Later |
| **Orquestração Multiagente Corporativa** | **Microsoft Agent Framework / AutoGen** | Distributed agent orchestration | `DEFER` | Later |
| **Roteamento Multi-Provider e Fallbacks de Custo** | **LiteLLM** | Provider abstraction, token/cost accounting | `DEFER` | Later |
| **Otimização de Prompts / Programas de LM** | **DSPy** | Teleprompters, metric-driven prompt optimization | `DEFER` | Later |
| **Falsificação Estatística e Testes Sequenciais** | **POPPER** | Sequential e-values, discriminative tests | `ADAPT` | Later |
| **Geração com Gramáticas Estritas (Modelos Locais)**| **Outlines** | Regex/CFG constrained decoding | `DEFER` | Later |

---

## 🔬 Registros Detalhados dos Doadores (Tier A — M04 Priority)

### [DONOR-001] MultiAgent Research Ideator
- **donor_id:** `DONOR-001`
- **name:** MultiAgent Research Ideator (Stanford / ICLR Ideation Research)
- **category:** `research_system`
- **receptor_gap:** Estruturação da profundidade de crítica e revisão vs largura de múltiplos críticos paralelos.
- **why_relevant:** Primeiro trabalho rigoroso a avaliar trade-offs entre número de agentes, diversidade de personas e profundidade de rodadas iterativas de crítica/revisão na ideação.
- **mechanism:** `iterative_critique_revision`, `bounded_critic_diversity`.
- **how_it_actually_works:** Um agente gerador produz uma ideia inicial; críticos com lentes diferentes (lógica, viabilidade, novidade) apontam falhas; o revisor sintetiza melhorias em ciclos iterativos.
- **evidence_level:** `PEER_REVIEWED_BENCHMARK` (Level B).
- **what_was_tested:** Comparação entre críticas sequenciais vs múltiplos críticos paralelos em geração de hipóteses de pesquisa.
- **scars / failures:** 
  - Aumento descontrolado de críticos paralelos aumenta custo exponencialmente e introduz ruído/trivialidades (*parallelism penalty*).
  - Avaliações dependem parcialmente de LLM-as-a-judge, exigindo cautela na calibração.
- **transplant_decision:** `ADAPT` (M04).
- **exact_mechanisms_to_harvest:** Sequência dirigida `Critique 1 (Lógica/Premissas) -> Revision -> Critique 2 (Viabilidade/Mundo Real) -> Revision`.
- **what_not_to_import:** Torneios massivos de hipóteses, pools de 10+ críticos paralelos.
- **reopen_condition:** Se novos experimentos provarem que múltiplos críticos paralelos superam a revisão iterativa com mesmo custo.
- **last_verified:** 2026-08-26.

---

### [DONOR-002] PydanticAI / Instructor
- **donor_id:** `DONOR-002`
- **name:** PydanticAI & Instructor
- **category:** `engineering_framework`
- **receptor_gap:** Saída estruturada tipada, validação em tempo de execução e bounded retry/repair.
- **why_relevant:** Converte saídas semânticas de LLMs em instâncias válidas de classes Pydantic com reparo determinístico.
- **mechanism:** `schema_enforced_generation`, `validation_repair_loop`.
- **how_it_actually_works:** Envia o JSON schema no prompt/tool call do modelo; intercepta exceções do Pydantic no parse; se inválido, reenvia a mensagem de erro ao modelo (max 1 retry).
- **evidence_level:** `PRODUCTION_OPEN_SOURCE` (Level A).
- **scars / failures:** 
  - Frameworks externos pesados introduzem dependências excessivas, acoplamento de runtime e ofuscação de logs brutos (*raw responses*).
  - Retries infinitos silenciosos podem estourar orçamento.
- **transplant_decision:** `ADAPT` (Camada fina nativa em Python/Pydantic no M04; dependência do Pydantic core sem frameworks intermediários desnecessários).
- **exact_mechanisms_to_harvest:** Validação Pydantic v2 + 1 tentativa de repair mecânica/semântica + preservação da resposta bruta (`raw_response`).
- **what_not_to_import:** Dependências transitivas desnecessárias ou abstrações mágicas de agentes.
- **reopen_condition:** Se a camada fina nativa exigir suporte a mais de 5 providers com tool calling heterogêneo.
- **last_verified:** 2026-08-26.

---

### [DONOR-003] DCI (Deliberative Council for Ideation)
- **donor_id:** `DONOR-003`
- **name:** Deliberative Council for Ideation (DCI - Stanford)
- **category:** `research_system`
- **receptor_gap:** Representação formal de desacordos, atos epistêmicos e preservação de tensões não resolvidas.
- **why_relevant:** Define vocabulário explícito para deliberação estruturada.
- **mechanism:** `speech_acts (CHALLENGE, GROUND, REFRAME, SYNTHESIZE)`, `tension_preservation`.
- **evidence_level:** `PEER_REVIEWED_BENCHMARK` (Level B).
- **scars / failures:** Overhead de coordenação de 62x em tokens sem ganho proporcional se ativado indiscriminadamente.
- **transplant_decision:** `ADAPT` (M04).
- **exact_mechanisms_to_harvest:** Registro explícito de `critical_issues`, `assumptions`, `contradictions` e `rejected_changes`.
- **what_not_to_import:** Conselho de múltiplos agentes por default, 14 atos conversacionais simultâneos.
- **reopen_condition:** Quando o motor avançar para deliberação multipessoal na Fase 4.
- **last_verified:** 2026-08-26.

---

## 🔍 Registros Detalhados (Tier B & Tier C — Donors Futuros)

| Donor ID | Nome | Gap | Decisão M04 | Motivo da Decisão |
| :--- | :--- | :--- | :---: | :--- |
| `DONOR-004` | **Google AI Co-Scientist** | Preservação de linhagem e reflexão evolutiva | `ADOPT_CONCEPT` | Adotar a regra de que revisão gera nova versão sem destruir a anterior (`original_idea` imutável). |
| `DONOR-005` | **STORM / Co-STORM** | Formulação de perguntas dirigidas à realidade | `ADOPT_CONCEPT` | Reality Check formula perguntas empíricas sem instanciar web scraping no MVP. |
| `DONOR-006` | **Promptfoo** | Red-teaming determinístico de prompts | `ADAPT` | Usar fixtures JSON padronizadas e asserções unitárias em Python puro. |
| `DONOR-007` | **LangGraph** | Execução de grafos duráveis | `REJECT_NOW (DEFER)` | Um loop de 6 estágios sequenciais não justifica a sobrecarga de framework de grafos. |
| `DONOR-008` | **LiteLLM** | Roteamento multi-provider e fallback | `DEFER` | MVP foca em um provider/fake runner inicial com medição limpa. |
| `DONOR-009` | **POPPER** | Testes sequenciais e e-values | `ADAPT_CONCEPT` | Reality Check formula hipóteses com métrica de falsificação sem statistical machinery. |
| `DONOR-010` | **DSPy** | Otimização paramétrica de prompts | `DEFER` | Exige dataset e baseline consolidados primeiro. |
| `DONOR-011` | **Arbor** | Hypothesis Tree Refinement (HTR), Linhagem de Ideias Condicionada a Evidência, Insights Tipados e Memória Negativa | `ADAPT_STRONGLY` | Transplante conceitual de HTR-Lite, insights tipados e lições podadas com escopo (Autópsia em `docs/research/donors/ARBOR-DEEP-AUTOPSY.md`). |
