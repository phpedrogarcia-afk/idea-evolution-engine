# PREREGISTRATION.md — Pré-registro Experimental M05.4

> **DOCUMENTO DE PRÉ-REGISTRO EXPERIMENTAL PROSPECTIVO CONGELADO**
> **EXPERIMENT_ID:** `EXP-M05.4-PROSPECTIVE-20260827`
> **STATUS:** `PREREGISTERED` | `FROZEN_BEFORE_EXECUTION`
> **PRODUÇÃO:** 100% Inalterada | **CHAMADAS DE MODELO NESTA MISSÃO:** 0

---

## 1. Pergunta Científica Primária

Em ideias completamente inéditas (holdout suite com 8 ideias independentes), a arquitetura **Lean L1 / FioED (Condição C)** produz melhor evolução de ideias valorizada por humanos por chamada de modelo do que:
1. **Condição A — Baseline de Refinamento Único (1 chamada)**
2. **Condição B — Simple Loop de Controle Fixo (10 chamadas)**?

---

## 2. Condições Experimentais

| Condição | Nome Canônico | Topologia / Chamadas | Papel Científico |
| :--- | :--- | :--- | :--- |
| **Condição A** | `BASELINE_SINGLE_REFINE` | Exatamente 1 chamada de refinamento genérico forte. | Baseline de alta eficiência mínima. |
| **Condição B** | `CURRENT_SIMPLE_LOOP_CONTROL` | Simple Loop fixo atual (6 estágios, até 10 chamadas) com R5 e salvaguardas existentes. | Controle de referência de alta intensidade. |
| **Condição C** | `LEAN_L1_FIOED` | Lean First Pass $\to$ Early Epistemic Gate $\to$ (Return / Human Decision / Waiting / 1 Focused Escalation). Máximo 2 chamadas. | Tratamento experimental de inferência condicionada a rentabilidade epistêmica. |

*Nota Constitucional:* Nenhuma quarta arquitetura ou condição adicional é permitida. A complexidade deve justificar sua inclusão.

---

## 3. Parâmetros de Execução Prospectiva (Congelados)

- **Provedor:** Groq (Free Tier / Pinned)
- **Modelo:** `openai/gpt-oss-120b` (sem fallback automático)
- **Settings:** Parâmetros de geração padrão idênticos entre chamadas comparáveis.
- **Context Isolation:** Cada execução de condição para cada ideia começa em ambiente limpo, sem memória cruzada de ideias ou condições anteriores.
- **Ordem de Execução:** Ordem de chamada das condições rotacionada deterministicamente por ideia.

---

## 4. Predições Pré-registradas do FioED

- **PRED-01 (Mecânica de Topologia):** A Condição C utilizará substancialmente menos chamadas que a Condição B (máximo 2 vs 10).
- **PRED-02 (Controle de Acréscimo):** A Condição C produzirá menos premissas materiais especulativas não ancoradas que a Condição B.
- **PRED-03 (Regressões Decisórias):** A Condição C acumulará menos eventos de `DecisionRegression` que a Condição B.
- **PRED-04 (Preservação de Ideias Férteis):** Na `IDEA-02` (ideia poética/incubativa), a Condição C preservará a intenção original melhor que A e B.
- **PRED-05 (Restrição de Pressão):** A Condição C evitará pressão racionalizante prematura sobre `IDEA-02`.
- **PRED-06 (Autoridade Humana):** Na `IDEA-06` (escolha normativa), a Condição C solicitará/preservará a decisão humana sem impor uma escolha fabricada.
- **PRED-07 (Resistência a Traps):** Na `IDEA-07` (bloco de notas simples), a Condição C resistirá à invenção de recursos ornamentais não solicitados.
- **PRED-08 (Discriminação de Incerteza):** Na `IDEA-08` (mista), a Condição C distinguirá o aspecto $U_f$ do aspecto local testável $U_g$.
- **PRED-09 (Alinhamento de Persistência):** Menor Persistência Sem Evidência ($P_e$) tenderá a se correlacionar positivamente com a preferência humana.
- **PRED-10 (Limitação do DecisionDelta):** O `DecisionDelta` sozinho não explicará toda a preferência humana, especialmente em ideias de incubação artística/poética.

---

## 5. Critérios Claros de Derrota e Vitória

### 5.1 O que faz o Lean L1 / FioED (C) PERDER credibilidade:
- A Condição A (1 chamada) ser consistentemente preferida por humanos sobre a Condição C na maioria das 8 ideias;
- A Condição C retornar prematuramente em incertezas materiais reais onde a Condição B gerou valor genuíno;
- A Condição C abusar de `KEEP` e falhar em aplicar pressão localizada em gaps óbvios;
- A complexidade do Lean L1 não se justificar perante a simplicidade do Baseline A.

### 5.2 O que faz o Simple Loop (B) VENCER / Justificar sua existência:
- Apesar do custo de 10 chamadas, a qualidade avaliada por humanos em blinding ser consistente e materialmente superior à de A e C, pagando seu aluguel epistêmico.

### 5.3 O que faz o Baseline One-Shot (A) VENCER como Produto V1:
- Manter preferência humana equivalente ou superior a B e C com custo mínimo de 1 chamada, sem violar restrições constitucionais.

---

## 6. Regras Rígidas de Exclusão

Um caso só pode ser excluído se:
1. Houver falha de conexão/API não recuperável pelo provedor;
2. Houver corrupção de arquivo bruto;
3. Houver quebra de schema que impossibilite leitura semântica;
4. Houver vazamento acidental de identidade antes da avaliação humana.

*Veto:* É expressamente proibido excluir outputs com status `REFINEMENT_INCOMPLETE`, `WAITING_FOR_REALITY`, `PRESERVE_UNKNOWN` ou requisições de decisão humana.
