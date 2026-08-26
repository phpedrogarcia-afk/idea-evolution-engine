# DCE.md — Deliberation Control Engine

> **STATUS: TARGET / DESIGN_HYPOTHESIS**

---

## 1. Visão Geral
O **Deliberation Control Engine (DCE)** é o motor de governança cognitiva do IEE. Ele não é um mediador de chat informal; ele determina a estratégia de investigação, os recursos alocados e as condições de término de cada ciclo deliberativo.

---

## 2. Anatomia e Pipeline de Execução do DCE

```text
                     IdeaGenome (vN)
                            │
                            ▼
                  [Epistemic Assessor]
               Avalia o estado epistêmico
                            │
                            ▼
                     [Gap Detector]
          Classifica lacunas (lógica, evidência...)
                            │
                            ▼
                 [Investigation Selector]
              Seleciona incerteza prioritária
                            │
                            ▼
              [Question Classifier / Decomposer]
             Empírica / Normativa / Mista
                            │
                            ▼
                  [Coordination Decision]
               Calcula coordination_value
              (SINGLE_AGENT vs MULTI_AGENT)
                            │
                            ▼
                     [Team Composer]
              Recruta funções epistemológicas
                            │
                            ▼
                    [Topology Planner]
              Sequencial, Paralelo, Loops...
                            │
                            ▼
                    [Contract Builder]
               Gera o DeliberationContract
                            │
                            ▼
                 [Execution Orchestrator]
               Executa a rodada deliberativa
                            │
                            ▼
                    [Progress Monitor]
              Verifica delta material gerado
                            │
                            ▼
                  [GenomePatch Builder]
               Estrutura proposta de mutação
                            │
                            ▼
                  [Termination Controller]
         (Próxima rodada / Stall / READY_TO_TEST)
```

---

## 3. Responsabilidades Específicas dos Componentes

1. **Epistemic Assessor:** Examina o `IdeaGenome` para mapear o que é suportado, o que é refutado, premissas não testadas e tensões ativas.
2. **Gap Detector:** Identifica e classifica lacunas em 6 categorias fundamentais: `INFORMATIONAL`, `LOGICAL`, `EVIDENTIARY`, `DEPENDENCY`, `TESTABILITY` e `FRAME`.
3. **Investigation Selector:** Seleciona a lacuna com maior potencial de impacto decisório ou estrutural.
4. **Question Classifier / Decomposer:** Classifica perguntas em `EMPIRICAL`, `NORMATIVE`, `STRUCTURAL` ou `MIXED`. Decompõe perguntas mistas, isolando a dimensão factual (para investigação por IA) da dimensão de valores (para consulta humana).
5. **Coordination Decision:** Avalia o `coordination_value`. Se a tarefa for direta ou de síntese, aciona `SINGLE_AGENT_MODE`; se houver alta incerteza e necessidade de crítica adversarial, aciona `STRUCTURED_MULTI_AGENT_MODE`.
6. **Team Composer:** Define as funções epistemológicas necessárias (ex: `find_disconfirming_evidence`, `challenge_causal_mechanism`, `estimate_feasibility`) antes de selecionar modelos.
7. **Topology Planner:** Seleciona o grafo de fluxo dos participantes a partir de templates fixos (`SEQUENTIAL`, `PARALLEL`, `CRITIQUE_LOOP`, `TREE`, `SYNTHESIS_LOOP`).
8. **Contract Builder:** Consolida todos os parâmetros no `DeliberationContract` prévio e imutável daquela rodada.
9. **Progress Monitor:** Compara o resultado com os critérios de progresso do contrato.
10. **Termination Controller:** Decide deterministicamente se o ciclo deve avançar, replanejar por estagnação (`STALLED`), requisitar decisão humana (`HUMAN_DECISION_REQUIRED`) ou transicionar para teste empírico (`READY_TO_TEST`).
