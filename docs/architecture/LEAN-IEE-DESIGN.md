# LEAN-IEE-DESIGN.md — Redesenho do IEE Baseado em Valor Decisório por Chamada

> **STATUS:** `DESIGN_HYPOTHESIS / CANDIDATE_FOR_EXPERIMENT`  
> **CLASSIFICAÇÃO DO SIMPLE LOOP ATUAL:** `REFERENCE_IMPLEMENTATION / CONTROL` (Preservado e inalterado)  
> **ALVO ARQUITETURAL:** Responder à incerteza `RU-LEAN-IEE-001` maximizando o *Decision Delta por Chamada de Modelo* sem abrir mão da disciplina constitucional de autoridade.

---

## 1. Princípio Fundamental de Design

```text
THINK LITTLE BY DEFAULT.
ESCALATE ONLY WHEN UNCERTAINTY EARNS THE COST.
```

O IEE não deve impor uma esteira fixa e pesada de 6 ou 10 estágios para todas as ideias. Ele deve partir de uma **primeira passada enxuta**, submetê-la a uma **verificação determinística barata** e acionar **escalação condicional** apenas para incertezas que justifiquem seu aluguel epistêmico.

```text
                     HUMAN SOURCE (SourceAnchor)
                                 │
                                 ▼
                     [LEAN FIRST PASS (1 call)]
                   (Intent + Core + Dependencies)
                                 │
                                 ▼
                 [EARLY EPISTEMIC GATE (Deterministic)]
               (Source Grounding, Ontology, Authority)
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
        [GATE: CLEAR / NO GAPS]        [GATE: MATERIAL UNCERTAINTY]
                 │                               │
                 ▼                               ▼
            RETURN_NOW                 CONDITIONAL ESCALATION (Max 1-2 calls)
           (1 call total)                        │
                                   ┌─────────────┼─────────────┐
                                   │             │             │
                              [CRITIQUE]   [ALTERNATIVES]  [REALITY]
                                   │             │             │
                                   └─────────────┼─────────────┘
                                                 │
                                                 ▼
                                        [FINAL_GATE_CHECK]
                                                 │
                                                 ▼
                                            RETURN_STATE
```

---

## 2. Formalização de Conceitos Centrais

### 2.1 Decision Delta (`DecisionDelta`)
O valor gerado por uma rodada de raciocínio não é o volume de texto, nem o número de críticas, nem a prolixidade de novas features. É a **mudança concreta que melhora a capacidade humana de decidir o próximo passo**.

$$\text{DecisionDelta} = f(\Delta \text{Clareza}, \Delta \text{Premissas Expostas}, \Delta \text{Testabilidade}, \Delta \text{Opções Reais})$$

**Sinais de Decision Delta Positivo:**
1. Resolução de ambiguidade que bloqueava o escopo.
2. Exposição de premissa frágil que causaria falha precoce.
3. Distinção clara entre 2 mecanismos técnicos excludentes.
4. Identificação de um teste empírico simples e discriminativo para o MVP.
5. Preservação de uma escolha normativa para decisão do operador humano.
6. Prevenção de um requisito falso ou inchaço especulativo.

### 2.2 Aluguel Epistêmico (`EpistemicRent`)
Todo passo adicional de inferência precisa pagar seu custo em *Decision Delta* esperado.

$$\text{Decisão de Escalação} = \begin{cases} 
\text{JUSTIFIED}, & \text{se } \mathbb{E}[\text{DecisionDelta}] > \text{Custo}(\text{Call}) + \text{Risco de Ruído} \\
\text{NOT\_JUSTIFIED}, & \text{caso contrário}
\end{cases}$$

Categorias de Aluguel:
- `LOW_COST / HIGH_DELTA`: Exposição direta de premissa oculta (Justificado).
- `HIGH_COST / LOW_DELTA`: Brainstorming livre sem restrições ou críticas genéricas redundantes (Não-justificado / Vetado).

---

## 3. Early Epistemic Gate (Portão Epistêmico Precoce)

O Early Epistemic Gate é executado **imediatamente após a primeira passada** de forma determinística/barata, antes de despender chamadas adicionais.

### 3.1 Perguntas do Gate:
1. **Source Grounding:** A primeira passada introduziu claims ou mecanismos que não decorrem estritamente da fonte humana? (Sim $\to$ rebaixa base para `MODEL_HYPOTHESIS`).
2. **Ambiguity Check:** A intenção original é ambígua a ponto de inviabilizar a arquitetura?
3. **Competing Mechanisms:** Existem 2 ou mais mecanismos técnicos viáveis e concorrentes?
4. **Severe Vulnerability:** Existe risco fatal de viabilidade óbvio no core proposto?
5. **Negative Knowledge Match:** Esse mecanismo já falhou em uma run anterior com condições idênticas?
6. **Human Authority Required:** A incerteza é normativa/de valores e só pode ser decidida pelo humano?

### 3.2 Estados de Saída do Early Gate:
- `RETURN_NOW`: Ideia bem ancorada, clara e sem dependências ocultas críticas (Custo final: 1 chamada).
- `ESCALATE_CRITIQUE`: Premissa frágil crítica detectada que exige teste adversarial focado (+1 chamada).
- `ESCALATE_ALTERNATIVES`: Múltiplos caminhos técnicos plausíveis que exigem trade-offs (+1 chamada).
- `ESCALATE_REALITY_TESTS`: Incerteza empírica central que exige definição de teste discriminativo (+1 chamada).
- `REQUEST_HUMAN_DECISION`: Decisão normativa ou mudança de intenção que exige autoridade humana (+0 chamadas).
- `STOP_NO_USEFUL_WORK`: Estagnação ou ausência de novo delta decisório (+0 chamadas).

---

## 4. Comparação das Candidatas Arquiteturais

### Candidata L0: One-Shot + Constitutional Post-Check
- **Estrutura:** 1 chamada de modelo + validação determinística de autoridade/ontologia + retorno.
- **Chamadas:** Exatamente 1.
- **Prós:** Custo mínimo, rápida, elimina inchaço multiestágio.
- **Contras:** Não explora alternativas nem faz crítica adversarial profunda quando necessário.

### Candidata L1: Lean IEE + Early Gate *(SELECIONADA PARA EXPERIMENTO)*
- **Estrutura:** 1 chamada principal de primeira passada + Early Epistemic Gate determinístico + no máximo 1 escalação condicional se justificada.
- **Chamadas:** 1 (típica) a 2 (quando escalonada).
- **Prós:** Resolve o *Epistemic Waste Before Gate*, mantém custo proporcional à incerteza da ideia, preserva 100% das proteções de autoridade e ontologia.
- **Contras:** Requer calibração determinística rigorosa dos gatilhos de escalação.

### Candidata L2: Lean IEE + Evidence-Conditioned Escalation
- **Estrutura:** Primeira passada + Early Gate + busca seletiva de evidência/doador + memória de linhagem `IdeaLineageNode` + parada dinâmica por saturação de delta.
- **Chamadas:** 1 a 4 chamadas (dinâmica).
- **Prós:** Máximo poder epistêmico para ideias altamente complexas.
- **Contras:** Maior complexidade de implementação; risco de reintroduzir aluguel de complexidade não justificado em ideias simples.

---

## 5. Seleção e Justificativa

- **Candidata Selecionada:** **`L1 (Lean IEE + Early Gate)`**
- **Por que L1 foi selecionada:**
  1. É a menor arquitetura capaz de resolver o achado central do M05.2 (`EPISTEMIC_WASTE_BEFORE_GATE`).
  2. Mantém o custo em 1 chamada para ideias diretas (igualando a eficiência da Condição A).
  3. Permite escalação cirúrgica de +1 chamada apenas quando uma vulnerabilidade ou alternativa real for detectada.
  4. Preserva 100% das garantias constitucionais (`SourceAnchor`, `AuthorityProofValidator`, `GroundingRecord`).
  5. Não requer banco de vetores, nem runtime de árvore de agentes, nem frameworks externos.
  6. É 100% reversível e testável offline.

---
*Este documento é a especificação canônica da arquitetura candidata Lean IEE.*
