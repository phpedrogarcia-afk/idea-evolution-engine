# OBSERVATION-REPRESENTATION-INVARIANTS.md — Invariantes de Ancoragem de Origem e Disciplina de Representação

> **DOCUMENTO CANÔNICO DE ENGENHARIA EPISTÊMICA DO PROJETO FIOIDEIAS / IDEA EVOLUTION ENGINE (IEE)**
> *Versão:* 1.0.0 | *Status:* `INSTITUTIONALIZED_AND_LOCKED` | *Fase:* Fase 1 — Simple Idea Evolution Loop MVP

---

## 0. Filosofia Central e Inspiração

> **ANTES DE INVENTAR, COLHA.**  
> **COLHA SEM APEGO.**  
> **OBSERVE ANTES DE INTERPRETAR.**  
> **FONTE $\neq$ REPRESENTAÇÃO.**  
> **REPRESENTAÇÃO $\neq$ AUTORIDADE.**  
> **INTERPRETAÇÃO $\neq$ EVIDÊNCIA.**  
> **MEMÓRIA $\neq$ VERDADE PRESENTE.**  
> **CONHECIMENTO DO DOADOR $\neq$ PROVA NO RECEPTOR.**  
> **AUTÓPSIA $\neq$ AUTORIZAÇÃO DE IMPLEMENTAÇÃO.**  
> **PRINCÍPIO DECLARADO $\neq$ COMPORTAMENTO OBSERVADO.**  
> **AÇÃO PROMETIDA $\neq$ CONCLUSÃO.**  
> **RECORRÊNCIA $\neq$ CONFIRMAÇÃO INDEPENDENTE.**  
> **PRESERVE A HISTÓRIA SEM SE TORNAR PRISIONEIRO DA HISTÓRIA.**  
> **COERÊNCIA LOCAL $\neq$ VALIDADE GLOBAL.**  
> **A AUTORIDADE DA FONTE HUMANA NUNCA DEVE SER CRIADA POR AFIRMAÇÃO DE MODELO, RESUMO, TIMEOUT, MEMÓRIA OU CONHECIMENTO DE DOADORES.**

### Proveniência da Inspiração Filosófica
*Origem de inspiração conceitual (proveniência histórica, não autoridade normativa):*  
Diálogo entre J. Krishnamurti, David Bohm, Rupert Sheldrake e John Hidley (Ojai, Califórnia, 18 de Abril de 1982 — *"What is a healthy mind?"*, [YouTube Record](https://youtu.be/OYp707Fofb8)).  
> *Nota de Rigor:* Este diálogo inspirou os invariantes de engenharia contra a confusão entre o símbolo/mapa e o fato observado. Suas alegações filosóficas não constituem fatos científicos nem autoridade jurídica sobre o software; servem unicamente como linhagem histórica do insight que fundamenta os 10 invariantes a seguir.

---

## 1. Os 10 Invariantes Canônicos

### 1. Observar Antes de Interpretar (Observe Before Interpret)
A expressão humana bruta, a evidência empírica externa ou o artefato primário devem ser capturados e registrados de forma imutável **antes** de qualquer processamento, resumo ou interpretação por modelos de IA.

### 2. Fonte $\neq$ Representação (Source != Representation)
O input humano original, as decisões normativas expressas e as fontes primárias são **artefatos de fonte** (`SourceAnchor`).  
Resumos, campos do IdeaGenome, interpretações de LLMs, assinaturas semânticas, formulações alternativas e insights destilados são **representações** (`RepresentationRecord`).  
Uma representação jamais se torna uma fonte por repetição ou antiguidade.

### 3. A Representação é um Mapa, Não o Território (Representation Is a Map, Not the Source)
Nenhuma representação gerada tem o poder de alterar silenciosamente o que a fonte original estabeleceu. Qualquer divergência entre o mapa gerado pelo modelo e a fonte bruta é resolvida em favor da fonte.

### 4. Rastreabilidade Estrita da Representação à Fonte (Traceable Representation)
Toda claim, derivação ou mecanismo promovido deve reter referências determinísticas auditáveis (`source_refs`) apontando para os `SourceAnchor` fundamentais que o autorizam.

### 5. Interpretação $\neq$ Evidência (Interpretation != Evidence)
A explicação de um modelo de linguagem sobre *por que* algo aconteceu, ou uma hipótese causal destilada de um teste, é uma **interpretação** (`INFERENCE` / `CAUSAL_HYPOTHESIS`), e não evidência factual. Interpretação auxilia a busca; evidência empírica valida o estado.

### 6. Memória Sem Apego (Memory Without Attachment)
Descobertas e falhas históricas constrangem e guiam buscas futuras, mas não recebem poder de veto permanente e universal. O conhecimento negativo (`NegativeKnowledgeRecord`) exige **escopo** delimitado e **condições explícitas de reabertura** (`reopen_conditions`).

### 7. Coerência Local $\neq$ Validade Global (Local Coherence != Global Validity)
Cada estágio individual de um pipeline pode produzir saídas localmente elegantes, plausíveis e sem erros de sintaxe, enquanto a ideia global como um todo sofreu *essence drift* e perdeu o alinhamento com a intenção humana. A integridade deve ser verificada cross-state e contra a fonte.

### 8. Princípio Declarado $\neq$ Comportamento Observado (Declared Principle != Observed Behavior)
Uma regra descrita em documentação Markdown, instruções de prompt ou descrições de ferramentas **não é um invariante** até que a transição de estado no código executável e os testes adversariais a apliquem de forma estrita e mecanicamente verificável.

### 9. Ação Prometida $\neq$ Conclusão (Promised Action != Completion)
Um texto em prosa gerado por LLM dizendo *"Vou testar estas abordagens a seguir"* ou promessas no tempo futuro **não constituem conclusão de trabalho nem evidência de execução**. Conclusão exige transição verificável de estado e artefatos de evidência.

### 10. Proximidade da Fonte Importa (Source Proximity Matters)
Para decisões de alto impacto (especialmente promoção para o Core ou descarte de intenções), o sistema deve ser capaz de percorrer a linhagem determinística regressiva até o input humano original ou à evidência primária, em vez de depender indefinidamente de cadeias de resumos-de-resumos.

---

## 2. Matriz de Autoridade e Proibições Constitucionais

| Entidade | Tipo Epistêmico | Cria Autoridade Humana? | Pode Ser Promovido ao Core Sem Ancoragem? |
| :--- | :---: | :---: | :---: |
| **Input Humano Original** | `SOURCE_ANCHOR` | **SIM (Soberana)** | N/A (É a própria raiz da intenção) |
| **Decisão Humana Registrada** | `SOURCE_ANCHOR` | **SIM (Normativa)** | SIM (Com `human_intervention = True`) |
| **Evidência Externa Auditável** | `SOURCE_ANCHOR` | NÃO (É factual) | SIM (Com ID de evidência formal) |
| **Interpretação / Resumo de LLM** | `REPRESENTATION` | **NÃO (Zero)** | **NÃO (Rebaixado a CANDIDATE)** |
| **Insight Destilado de Doador** | `DONOR_KNOWLEDGE` | **NÃO (Zero)** | **NÃO (Exige prova no receptor IEE)** |
| **Timeout de Resposta Humana** | `OPERATIONAL_EVENT` | **NÃO (Zero)** | **NÃO (Proibido fabricar consentimento)** |

---

## 3. Aplicação nos Contratos e Pipeline

1. **Validação de Autoridade:** O [`AuthorityProofValidator`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/src/idea_evolution/domain/grounding.py) audita a ancoragem determinística de toda proposição.
2. **Isolamento de Linhagem:** Nenhum candidato herda autoridade de representações intermediárias sem prova de derivação ou ancoragem direta.
3. **Hard Gates Soberanos:** O método `_evaluate_hard_gates` no orquestrador veta `REFINED_IDEA_READY` caso haja qualquer substituição da fonte por representações alucinadas.
