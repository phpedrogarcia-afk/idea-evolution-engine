# LEAN-IEE-DONOR-HARVEST.md — Colheita de Mecanismos de Doadores para o Lean IEE

> **STATUS: TARGET / DESIGN_HYPOTHESIS**
> **OBJETIVO DA COLHEITA:** Extrair mecanismos e cicatrizes de doadores comprovados especificamente para responder à incerteza **RU-LEAN-IEE-001**: *Como decidir deterministicamente quando uma ideia merece outra chamada de modelo ou escalação sem incorrer em aluguel de complexidade fixa?*

> **STATUS:** `RESEARCH_HARVEST_COMPLETE` | **AUTORIZAÇÃO DE IMPLEMENTAÇÃO:** `FALSE`

---

## 1. Princípio Epistêmico da Colheita

```text
CONHECIMENTO DE DOADOR != AUTORIDADE DE IMPLEMENTAÇÃO
RESULTADO NO DOADOR != RESULTADO NO IEE
AUTÓPSIA != AUTORIZAÇÃO DE ENGENHARIA DE PRODUTO
```

---

## 2. Matriz de Extração Orientada ao Receptor (Receiver-Oriented Extraction)

### [DONOR-ARBOR] Arbor ( Renmin Univ / Microsoft Research )
- **RECEIVER_GAP:** Decisão de ramificação e busca condicionada a evidência sem gerar árvores desnecessárias para toda ideia.
- **MECHANISM:**
  - `Hypothesis Tree Refinement (HTR-Lite)`: Estados persistentes compactos em JSON/Markdown.
  - `Scoped Negative Knowledge`: Memória explícita de ramos e intervenções que falharam (`pruned lessons`) para impedir exploração repetida da mesma falha.
  - `Fixed Hypothesis during Local Repair`: Manter a identidade da hipótese fixa enquanto repara sua implementação técnica.
  - `Independent Generation vs Validation Lanes`: Separação estrita entre o contexto que gera hipóteses e o contexto que avalia validade.
- **SCAR:**
  - O Arbor consome dezenas de milhões de tokens quando roda em modo aberto; sua lição é *gasto estruturado*, não economia ingênua.
  - LLM-distilled *insight* não é evidência causal comprovada.
  - Advisory policies em prompts não são invariantes até que a transição de estado as imponha mecanicamente.
- **WHAT_UNCERTAINTY_IT_ALREADY_PAID_FOR:** Provou em benchmarks de otimização autônoma que ramificar apenas com evidência discriminativa supera busca cega, e que propagar lições de falhas reduz redundância.
- **WHAT_IT_DOES_NOT_PROVE:** Não prova que ideias vagas iniciais sem métricas prontas devam ser desdobradas em árvores de busca completas.
- **TRANSPLANT_CANDIDATE:** `IdeaLineageNode` (multi-parentesco), `NegativeKnowledgeRecord` e disciplina de hipótese fixa durante reparo.
- **COMPLEXITY_COST:** Baixo a Médio (se mantido como contratos de dados offline e memória determinística).
- **AUTHORITY_RISK:** Baixo (se insights forem tipados como heurísticas e não autoridade causal).
- **DECISION:** **`ADAPT`** (Conceitos de linhagem e memória negativa para escalação condicional; rejeitar runtime de busca em árvore universal).

---

### [DONOR-MAGENTIC-ONE] Magentic-One ( Microsoft Research )
- **RECEIVER_GAP:** Detecção de estagnação e critério de parada quando rodadas adicionais de raciocínio não produzem novo valor decisório (*Decision Delta*).
- **MECHANISM:**
  - `Progress Ledger / Task Ledger`: Registro explícito do progresso factual contra metas contratuais.
  - `Stall Detection`: Detecção mecânica de estagnação quando rodadas consecutivas produzem saídas semanticamente idênticas ou circulares.
  - `Stall -> Reflect -> Replan or Terminate`: Transição forçada quando o progresso estagna, impedindo chamadas cegas adicionais.
- **SCAR:**
  - Orquestrador central monolítico sem validação determinística rígida torna-se frágil e propenso a loops alucinatórios.
- **WHAT_UNCERTAINTY_IT_ALREADY_PAID_FOR:** Provou que sistemas multi-turn precisam de critério determinístico de estagnação para não queimar tokens indefinidamente.
- **WHAT_IT_DOES_NOT_PROVE:** Não resolve a ancoragem em autoridade humana (o orquestrador pode alucinar progresso).
- **TRANSPLANT_CANDIDATE:** Regra de progresso: *Falha sem mudança de estratégia ou ausência de novo delta decisório bloqueia nova chamada*.
- **COMPLEXITY_COST:** Muito Baixo (verificação determinística de hashes e deltas de propostas).
- **AUTHORITY_RISK:** Nenhum (veto mecânico).
- **DECISION:** **`ADOPT_CONCEPT`** (Regra de parada por estagnação: `NO_DECISION_PROGRESS -> TERMINATE`).

---

### [DONOR-DCI] Deliberative Council for Ideation ( Stanford )
- **RECEIVER_GAP:** Preservação de desacordos e tensões fundamentais sem gastar chamadas extras tentando forçar consenso artificial.
- **MECHANISM:**
  - `Tension Preservation / First-Class Tensions`: Desacordos não resolvidos são persistidos como objetos de primeira classe (`TensionRecord`).
  - `Minority Report / Preserved Disagreement`: O encerramento da deliberação não exige convergência unânime; registrar o desacordo é um estado terminal válido.
- **SCAR:**
  - Overhead de coordenação de até 62x em tokens quando agentes deliberam livremente sem gatilhos claros.
- **WHAT_UNCERTAINTY_IT_ALREADY_PAID_FOR:** Provou que forçar consenso empobrece a ideação e que tensões estruturadas contêm alto valor epistêmico.
- **WHAT_IT_DOES_NOT_PROVE:** Não justifica múltiplos agentes por padrão para ideias simples.
- **TRANSPLANT_CANDIDATE:** `TensionRecord` e encerramento com `PRESERVED_DISAGREEMENT` como estado terminal válido sem escalação.
- **COMPLEXITY_COST:** Muito Baixo.
- **AUTHORITY_RISK:** Nenhum.
- **DECISION:** **`ADAPT`** (Manter tensão como dado persistido; não escalonar chamadas apenas para eliminar contradições que devem ser decididas pelo humano).

---

### [DONOR-CO-SCIENTIST] Google AI Co-Scientist ( Google DeepMind )
- **RECEIVER_GAP:** Decomposição e teste comparativo de mecanismos concorrentes quando existem múltiplas hipóteses plausíveis.
- **MECHANISM:**
  - `Assumption Decomposition`: Decomposição explícita de premissas ocultas subjacentes a cada mecanismo.
  - `Meta-Review & Test-Time Evolution`: Avaliação pareada e geração de hipóteses concorrentes com métricas de falsificação.
- **SCAR:**
  - Risco de ranking entre modelos ser confundido com evidência do mundo real (*Ranking != Evidence*).
- **WHAT_UNCERTAINTY_IT_ALREADY_PAID_FOR:** Demonstrou eficácia na geração de hipóteses quando o espaço de soluções possui mecanismos alternativos genuínos e critérios de falsificação.
- **WHAT_IT_DOES_NOT_PROVE:** Não compensa seu custo se o usuário forneceu uma ideia simples e direta com apenas um caminho natural.
- **TRANSPLANT_CANDIDATE:** Gatilho de escalação para `ESCALATE_ALTERNATIVES` apenas quando `competing_mechanisms >= 2` forem detectados.
- **COMPLEXITY_COST:** Médio.
- **AUTHORITY_RISK:** Médio (se hipóteses geradas por IA forem tratadas como autoridade humana).
- **DECISION:** **`ADOPT_CONCEPT`** (Usar decomposição de mecanismos apenas sob gatilho de escalação condicional).

---

### [DONOR-MULTIAGENT-IDEATOR] MultiAgent Research Ideator ( Stanford / ICLR )
- **RECEIVER_GAP:** Determinar se críticas sequenciais ou paralelas agregam valor e quando encerrar a crítica.
- **MECHANISM:**
  - `Iterative Critique-Revision`: Crítica dirigida sequencial (lógica primeiro, depois viabilidade empírica).
- **SCAR:**
  - *Parallelism penalty*: Múltiplos críticos paralelos aumentam o custo linearmente e geram ruído superficial. Mais de 2 rodadas sofrem retornos decrescentes severos.
- **WHAT_UNCERTAINTY_IT_ALREADY_PAID_FOR:** Provou que 1 ou 2 rodadas dirigidas de crítica focada superam múltiplos agentes abertos.
- **WHAT_IT_DOES_NOT_PROVE:** Não prova que toda ideia precise passar por crítica se não houver vulnerabilidade material detectada.
- **TRANSPLANT_CANDIDATE:** `ESCALATE_CRITIQUE` limitado a no máximo 1 rodada focalizada quando o gate inicial detectar vulnerabilidade crítica.
- **COMPLEXITY_COST:** Baixo a Médio.
- **AUTHORITY_RISK:** Nenhum.
- **DECISION:** **`ADAPT`** (Crítica condicionada a gatilho, não em esteira mandatória).

---

## 3. Síntese dos Gatilhos de Decisão Colhidos dos Doadores

| Situação Detectada no Lean First Pass | Doador de Referência | Mecanismo Colhido | Ação de Escalação no Lean IEE |
| :--- | :--- | :--- | :--- |
| **Ideia Clara, Direta e Sem Contradições** | *M05.2 Evidence (Baseline A)* | One-shot execution + Gate Check | **`RETURN_NOW` (1 chamada)** |
| **Vulnerabilidade Estrutural / Premissa Frágil** | *MultiAgent Ideator* | Single-round focused critique | **`ESCALATE_CRITIQUE` (+1 chamada)** |
| **Mecanismos Técnicos Concorrentes Genuínos** | *Google Co-Scientist / Arbor* | Hypothesis branching / Trade-off analysis | **`ESCALATE_ALTERNATIVES` (+1 chamada)** |
| **Incerteza Factual / Dependência Crítica** | *STORM / Popper* | Targeted empirical test definition | **`ESCALATE_REALITY_TESTS` (+1 chamada)** |
| **Mecanismo Já Falho em Execução Anterior** | *Arbor / IDEAgent* | Negative knowledge matching | **`REJECT_OR_REOPEN_WITH_EVIDENCE` (0 chamadas)** |
| **Progresso Nulo / Estagnação Semântica** | *Magentic-One* | Stall termination | **`STOP_NO_USEFUL_WORK` (0 chamadas)** |
| **Decisão Normativa / Mudança de Escopo** | *DCI / Human Authority Rule* | Tension preservation & Human Query | **`REQUEST_HUMAN_DECISION` (0 chamadas)** |

---
*Este documento é um artefato de pesquisa e arquitetura canônica.*
