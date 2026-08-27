# FIO-EPISTEMIC-DYNAMICS.md — Dinâmica Epistêmica do FioIdeias (FioED)

> **DOCUMENTO DOUTRINÁRIO CANÔNICO DE TEORIA, FORMALISMO E ENGENHARIA EPISTÊMICA**
> **NOME DA TEORIA DE TRABALHO:** *Fio Epistemic Dynamics (FioED)*
> **STATUS:** `WORKING_THEORY` | `NOT_SCIENTIFICALLY_VALIDATED` | `NO_UNSUPPORTED_NOVELTY_CLAIMS`
> **OBJETIVO PRIMÁRIO:** Responder formalmente à questão fundamental: *Como pode um sistema ajudar uma ideia a evoluir profundamente sem se tornar prisioneiro das representações que ele mesmo criou sobre ela?*

---

## 1. Identidade e Propósito do Projeto

O **FioIdeias** não é uma máquina para produzir o máximo de pensamento possível, nem um orquestrador para multiplicar chamadas cegas de IA.

```text
EVOLVE DEEPLY.
REMAIN ANCHORED.
THINK MORE ONLY WHEN THINKING MORE CHANGES THE DECISION.
```

O FioIdeias é um sistema governado para maturar ideias mantendo contato inquebrável com a fonte primária, com as evidências empíricas, com as incertezas genuínas e com a autoridade humana, alocando inferência adicional apenas quando ela altera a fronteira de decisão humana.

---

## 2. O que o FioED Rejeita Explicitamente

O FioED baseia-se em vetos epistemológicos formais contra falácias comuns em arquiteturas de IA:

1. ❌ $\text{Mais Chamadas} = \text{Mais Inteligência}$
2. ❌ $\text{Mais Agentes} = \text{Mais Inteligência}$
3. ❌ $\text{Mais Memória} = \text{Mais Inteligência}$
4. ❌ $\text{Mais Consenso} = \text{Mais Verdade}$
5. ❌ $\text{Mais Investimento / Tokens} = \text{Mais Verdade}$ ($\text{Sunk Cost} \neq \text{Truth}$)
6. ❌ $\text{Mais Detalhes em Prosa} = \text{Mais Valor Decisório}$
7. ❌ $\text{Interpretação do Modelo} = \text{Intenção do Usuário}$
8. ❌ $\text{Resultado no Doador} = \text{Prova no Receptor}$
9. ❌ $\text{Resumo de Resumo} = \text{Fonte Primária}$
10. ❌ $\text{Recorrência / Repetição} = \text{Confirmação Independente}$
11. ❌ $\text{Sucesso Local no Estágio} = \text{Validade Global}$
12. ❌ $\text{Política em Documento} = \text{Invariante em Código}$
13. ❌ $\text{Declaração de Conclusão pela IA} = \text{Evidência de Conclusão}$
14. ❌ $\text{Incerteza / Desconhecido} = \text{Falha}$
15. ❌ $\text{Parada Antecipada (STOP)} = \text{Falha}$
16. ❌ $\text{Criatividade Especulativa} = \text{Autoridade Humana}$

---

## 3. Estado Formal do FioED ($X_t$)

O estado evolutivo de uma ideia no instante $t$ é definido pela 10-tupla:

$$X_t = \langle S, R_t, H_t, E_t, U_t, M_t, A_t, T_t, D_t, C_t \rangle$$

Onde:
- **$S$ (Source Anchors):** Conjunto imutável de artefatos primários de fonte humana e evidências externas primárias ($S_{t+1} \equiv S_t$).
- **$R_t$ (Representations):** Modelos estruturados, resumos, assinaturas semânticas e interpretações ativas geradas pelo sistema.
- **$H_t$ (Hypotheses / Candidates):** Mecanismos candidatos e possibilidades técnicas que permanecem estritamente no status `MODEL_HYPOTHESIS` ou `CANDIDATE`.
- **$E_t$ (Evidence):** Observações auditáveis, resultados de execução, benchmarks e referências empíricas com IDs formais.
- **$U_t$ (Unknowns):** Incertezas residuais e premissas não verificadas explicitamente registradas.
- **$M_t$ (Memory):** Memória institucional seletiva (conhecimento negativo com condições de reabertura, cicatrizes de doadores e lições podadas).
- **$A_t$ (Authority State):** Estado formal de proveniência que determina quem pode autorizar cada transição ontológica (Humano, Política, Evidência ou Nenhuma).
- **$T_t$ (Tensions):** Contradições ativas, posições minoritárias e objeções residuais não resolvidas preservadas como objetos de primeira classe (`TensionRecord`).
- **$D_t$ (Decision Frontier):** Conjunto estruturado de decisões materiais disponíveis para o tomador de decisão humano no instante $t$.
- **$C_t$ (Cost Accounting):** Contabilidade factual de custos (número de chamadas de modelo, lookups de doadores, ramificações e complexidade estrutural).

---

## 4. Operadores Fundamentais

```text
       ┌───────────┐
       │   HUMAN   │
       │  SOURCE S │
       └─────┬─────┘
             │
             ▼ O(S)  [Observation Operator: Extracao nao-generativa]
       ┌───────────┐
       │ FIELD S_0 │
       └─────┬─────┘
             │
             ▼ I(O(S)) [Interpretation Operator: Geracao de Representacao R_0]
       ┌───────────┐
       │ STATE X_0 │
       └─────┬─────┘
             │
      ┌──────┴─────────────────────────────────┐
      │                                        │
      ▼ A(X_t) [Attention: Snapshot Global]    │
┌──────────────┐                               │
│ SNAPSHOT F_t │                               │
└──────┬───────┘                               │
       │                                       │
       ▼ Γ(F_t) [Early Epistemic Gate]         │
  ┌────┴──────────────────────────────┐        │
  │                                   │        │
  ▼ RETURN / HUMAN / STOP             ▼ ESCALATE [Se Aluguel Justificado]
┌──────────────────┐            ┌──────────────┐
│  TERMINAL STATE  │            │ C_h(X_t)     │ [Concentration: 1 Foco]
└──────────────────┘            └──────┬───────┘
                                       │
                                       ▼ A(X_{t+1}) [Re-Attention: Reconciliacao]
                                ┌──────────────┐
                                │ STATE X_t+1  │
                                └──────┬───────┘
                                       │
                                       ▼ MemoryAdmission(X_t+1)
                                ┌──────────────┐
                                │  MEMÓRIA M   │
                                └──────────────┘
```

### 1. Operador $O(S)$ — Observação Não-Generativa
Extrai apenas o que a fonte fornece expressamente (termos literais, restrições declaradas, perguntas explícitas). **Não inventa mecanismos nem preenche requisitos ausentes.**
$$\text{Claim}(c) \in O(S) \implies \text{Provenance}(c) = \text{EXPLICIT\_SOURCE\_SPAN}$$

### 2. Operador $I(O(S))$ — Interpretação Semântica
Gera representações estruturadas e propõe hipóteses técnicas candidatas.
$$I(S) \neq S \quad \text{e} \quad \text{Authority}(I(S)) \equiv \text{MODEL\_HYPOTHESIS}$$
Nenhuma claim em $I(S)$ herda silenciosamente a autoridade da fonte.

### 3. Operador $A(X_t)$ — Atenção Epistêmica Global
Operação determinística de baixo custo que produz um snapshot integral do campo ($F_t$), verificando coerência entre fontes, representações, hipóteses, autoridade, evidências e tensões.

### 4. Operador $C_h(X_t)$ — Concentração Focada e Delimitada
Chamada de inferência dirigida para resolver estritamente a incerteza $h$ que justificou o aluguel de complexidade. Exige: alvo fixo, motivo tipado, delta esperado e critério de parada.

### 5. O Ciclo Inegociável $A \to C \to A$ (Attention $\to$ Concentration $\to$ Re-Attention)
Nenhuma operação focada de concentração ($C_h$) pode promover diretamente seu resultado para conclusão global sem passar pela **Re-Atenção** ($A(X_{t+1})$). A coerência local em $C_h$ não implica validade global em $X_{t+1}$.

---

## 5. Leis Epistêmicas e Invariantes Formais

- **LAW-01 (Source Immutability):** $S_{t+1} \equiv S_t$. Mudanças de intenção humana criam novos eventos de fonte ($S_1, S_2$), sem sobrescrever o histórico original.
- **LAW-02 (Representation Non-Authority):** $\text{Authority}(R) \neq \text{Authority}(S)$. A transformação semântica zera a autoridade humana para termos novos.
- **LAW-03 (Material Claim Provenance):** Nenhuma proposição é promovida ao Core sem uma rota auditável até um `SourceAnchor` ou evidência externa válida.
- **LAW-04 (Attention Before Concentration):** $C_h$ só pode ser disparado após avaliação determinística do portão $\Gamma(A(X_t))$.
- **LAW-05 (Re-Attention After Concentration):** Toda saída de $C_h$ é submetida à reconciliação global $A(X_{t+1})$ antes da finalização.
- **LAW-06 (Reasoning Rent Required):** Toda chamada adicional de modelo exige um registro explícito de `EpistemicRentRecord` com veredito `JUSTIFIED`.
- **LAW-07 (Sunk-Cost Immunity):** $C_t(h) > 0 \not\implies \text{Truth}(h) \uparrow$. O custo investido não altera a probabilidade ou o status de verdade de uma hipótese.
- **LAW-08 (Memory Does Not Create Present Evidence):** A memória técnica informa buscas, mas não substitui a validação de fatos no presente.
- **LAW-09 (Negative Knowledge Discipline):** Conhecimento negativo exige escopo estrito, o que não repetir e condições claras de reabertura.
- **LAW-10 (Non-Substitutable Human Authority):** $\lim_{N \to \infty} \text{AI\_Calls}(N) \not\implies \text{HumanAuthority} = \text{True}$. A IA não pode fabricar consentimento normativo.
- **LAW-11 (Generator Cannot Self-Certify):** O modelo que gerou a hipótese $h$ não pode atuar como autoridade de prova independente de $h$.
- **LAW-12 (No Useful Work as Success):** Se nenhuma incerteza material exigir escalação, encerrar com `RETURN_NOW` ou `STOP_NO_USEFUL_WORK` é o resultado ótimo.
- **LAW-13 (Local Improvement != Global Validity):** Otimizar uma parte isolada de uma ideia não autoriza a conclusão se o alinhamento com a fonte for rompido.
- **LAW-14 (Recurrence != Independence):** Múltiplos agentes ou múltiplas repetições do mesmo modelo repetindo uma afirmação não constituem confirmação independente.
- **LAW-15 (Donor Knowledge != Receiver Proof):** Um mecanismo comprovado em um doador externo (ex: Arbor, Magentic-One) é apenas hipótese até ser testado no receptor IEE.

---

## 6. Modelos de Quantidades e Variáveis Mensuráveis

### 1. Profundidade de Intermediário (Intermediary Depth)
Define o número de arestas de transformação semântica entre uma claim $c$ e sua fonte primária de suporte:
$$\text{IntermediaryDepth}(c) = \text{dist}_{\mathcal{G}}(c, S)$$
Se $c$ for uma decisão de alto impacto e $\text{IntermediaryDepth}(c) \ge 2$, o sistema dispara um alerta de **`SOURCE_REFRESH_REQUIRED`**, reancorando a decisão diretamente no input humano antes da promoção.

### 2. Persistência Sem Evidência (Evidence-Free Persistence)
Mede o número de operações consecutivas de raciocínio que elaboram uma hipótese $h$ sem injeção de nova evidência empírica ou autoridade humana:
$$P_e(h) = \text{count\_events\_since\_last\_evidence}(h)$$
Se $P_e(h) \ge 2$ e $\Delta D_t = \emptyset$, o sistema aciona alerta de **`ATTACHMENT_RISK`**, forçando a preservação como mero candidato ou encerramento da esteira.

### 3. Vetor de Risco de Desvio (Drift Risk Vector)
Em vez de um score escalar arbitrário, o risco de desvio é um vetor determinístico:
$$\mathbf{DriftRisk}(X_t) = \begin{bmatrix} \text{ungrounded\_material\_claims} \\ \max(\text{intermediary\_depth}) \\ \max(P_e) \\ \text{authority\_mismatch\_count} \\ \text{unresolved\_tensions} \end{bmatrix}$$

### 4. Eventos de Decision Delta ($\Delta D_t$)
Representado como um conjunto tipado de eventos que alteram a capacidade de ação do tomador de decisão:
- *Deltas Positivos:* `AMBIGUITY_RESOLVED`, `ASSUMPTION_EXPOSED`, `OPTION_ADDED`, `OPTION_REJECTED`, `TEST_IDENTIFIED`, `HUMAN_DECISION_IDENTIFIED`, `EVIDENCE_CHANGED_DECISION`, `FALSE_REQUIREMENT_PREVENTED`, `NEXT_ACTION_CHANGED`.
- *Regressões Decisórias:* `SOURCE_DRIFT_INCREASED`, `UNSUPPORTED_REQUIREMENT_ADDED`, `FALSE_CERTAINTY_CREATED`, `VALID_OPTION_ERASED`, `TENSION_SILENTLY_REMOVED`.

---

## 7. Mapeamento dos Doadores no FioED

Os doadores colhidos são operadores condicionais sob demanda, e não estágios fixos:

| Doador | Incerteza / Gap no Receptor | Mecanismo Doado no FioED | Condição de Ativação |
| :--- | :--- | :--- | :--- |
| **Arbor** | Ramificação de hipóteses e reparo local | `NegativeKnowledgeRecord`, `IdeaLineageNode`, Hipótese Fixa | Múltiplas hipóteses viáveis com testes discriminativos |
| **Magentic-One** | Detecção de estagnação e critério de parada | `ProgressLedger`, `StallDetection`, Terminação sem progresso | Segunda chamada não gera novo delta decisório |
| **DCI** | Preservação de desacordos e tensões | `TensionRecord`, `PRESERVED_DISAGREEMENT` | Conflito de premissas sem base de evidência imediata |
| **Google Co-Scientist** | Decomposição de premissas concorrentes | `AssumptionDecomposition`, Trade-off comparison | $\ge 2$ mecanismos técnicos viáveis identificados |
| **Stanford Ideator** | Crítica sequencial focalizada de 1 rodada | `FocusedEscalation` (Max 1 rodada) | Vulnerabilidade de severidade HIGH detectada no Gate |

---

## 8. Auditoria de Arte Prévia e Posicionamento de Novidade

Para evitar apropriação indevida e falsas alegações de novidade científica, classificamos rigorosamente os conceitos do FioED:

| Conceito FioED | Problema que Resolve | Arte Prévia Existente na Literatura Científica | Relação com FioED | Classificação de Novidade |
| :--- | :--- | :--- | :--- | :---: |
| **Epistemic Rent** | Alocação de computação em inferência | Metaraciocínio Racional (Russell & Wefald 1991), Value of Computation (Horvitz 1988) | O FioED adapta o valor da computação para o domínio de evolução de ideias | `KNOWN_CONCEPT_ADAPTED` |
| **Decision Delta** | Medição de progresso semântico | Value of Information (Howard 1966), Epistemic Utility (Levi 1967) | FioED utiliza eventos discretos de destravamento em vez de probabilidades bayesianas | `KNOWN_CONCEPT_ADAPTED` |
| **Intermediary Depth** | Telefone sem fio em cadeias de IA | Linhagem de Dados e Proveniência (Buneman et al. 2001, PROV-DM) | Medição de arestas de transformação semântica em grafos de raciocínio | `KNOWN_CONCEPT_ADAPTED` |
| **Evidence-Free Persistence** | Elaboração circular sem fatos | Truth Maintenance Systems (Doyle 1979), AGM Belief Revision (Alchourrón et al. 1985) | Contagem de passos sem suporte empírico para acionar poda de apego | `RECEIVER_SPECIFIC_SYNTHESIS` |
| **Negative Knowledge Reopen** | Evitar repetição sem bloquear inovação | Scoped Pruning em Busca Heurística (Pearl 1984), HTR (Arbor 2024) | Memória estruturada com tuplas de falha e condições de reabertura | `COMBINATION_OF_KNOWN_MECHANISMS` |
| **A $\to$ C $\to$ A Dynamic** | Evitar otimização local míope | Arquiteturas Cognitivas Dual-Process (Kahneman 2011, Evans & Stanovich 2013) | Portão determinístico global intercalado com inferência focada | `RECEIVER_SPECIFIC_SYNTHESIS` |
| **Source-Anchored Lineage** | Impedir que a IA invente intenção | Ancoragem Semântica e Proveniência Soberana | Integração constitucional: Ancoragem de Origem + Não-Autoridade de Representação | **`POTENTIALLY_DISTINCT_SYNTHESIS`** |

> **Veredito de Novidade:** A singularidade do FioIdeias não reside em equações isoladas, mas na **síntese arquitetural integrada** que une ancoragem imutável de origem humana, disciplina de não-autoridade sobre representações geradas, portão determinístico de custo zero, alocação de inferência governada por aluguel epistêmico e imunidade a custos afundados.

---

## 9. Red-Team da Teoria e Questões Adversariais

O FioED aplica seu próprio princípio a si mesmo: **O modelo do FioED não é a realidade**.

1. **E se o baseline de prompt único (Condição A) continuar vencendo na maioria das ideias?**  
   *Resposta:* Isso confirmará a premissa de que a maioria das ideias é simples e que o Early Epistemic Gate deve escolher `RETURN_NOW` (1 chamada) como rota nominal padrão.
2. **E se a preservação estrita da fonte matar a criatividade e a exploração de ideias ousadas?**  
   *Resposta:* O FioED define o modo `DEEP_EXPLORATION`. A IA tem total liberdade para propor novidades arrojadas, desde que sejam tipadas como `MODEL_HYPOTHESIS / CANDIDATE`. A criatividade é incentivada; o que é proibido é a falsificação da intenção do usuário.
3. **E se a Atenção ($A$) se tornar um portão pesado e caro que recria o desperdício do Simple Loop?**  
   *Resposta:* O operador $A$ é estritamente determinístico ($0$ chamadas de IA). Ele executa em $<5\text{ms}$ usando matching estrutural, parsing de Pydantic e checagem de hashes.
4. **E se a intenção do usuário humano mudar ao longo do tempo?**  
   *Resposta:* Mudanças de intenção são registradas como novos eventos de fonte ($S_1, S_2$). A história antiga é preservada, e a nova decisão humana governa o estado presente explicitamente.
5. **E se o próprio framework FioED se tornar uma representação dogmática que perseguimos sem evidência?**  
   *Resposta:* Meta-Atenção ativa: Qualquer métrica ou operador do FioED que aumentar a complexidade sem melhorar a capacidade de decisão do usuário será impiedosamente podado.
