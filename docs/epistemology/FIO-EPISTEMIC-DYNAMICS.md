# FIO-EPISTEMIC-DYNAMICS.md — Dinâmica Epistêmica do FioIdeias (FioED)

> **DOCUMENTO DOUTRINÁRIO CANÔNICO DE TEORIA, FORMALISMO E ENGENHARIA EPISTÊMICA**
> **NOME DA TEORIA DE TRABALHO:** *Fio Epistemic Dynamics (FioED)*
> **STATUS:** `WORKING_RECEIVER_THEORY` | `FORMALIZED_NOT_EMPIRICALLY_VALIDATED` | `NO_UNSUPPORTED_NOVELTY_CLAIMS`
> **OBJETIVO PRIMÁRIO:** Responder formalmente à questão fundamental: *Como pode um sistema ajudar uma ideia a evoluir profundamente sem se tornar prisioneiro das representações que ele mesmo criou sobre ela?*
> **META-INVARIANTE:** *O mapa que diz que o mapa não é o território continua sendo um mapa.* O FioED não recebe imunidade constitucional e deve ser revisado se a evidência empírica refutar suas hipóteses.

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
- **$S$ (Source Anchors):** Conjunto imutável de artefatos primários de fonte humana e evidências externas primárias ($S_{t+1} \equiv S_t$). Eventos posteriores de fonte ($S_1, S_2$) são adicionados cronologicamente sem reescrever $S_0$.
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

## 4. Auditoria e Classificação Formal de Todas as Fórmulas

Para eliminar confusão entre definições matemáticas, regras arquiteturais e hipóteses empíricas, cada expressão do FioED é formalmente classificada:

| Fórmula / Expressão | Tipo Epistêmico | Variáveis Envolvidas | Observabilidade | Consequência Operacional | Status Atual | O que Falsificaria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$S_{t+1} \equiv S_t$** | `INVARIANT` | $S$ (SourceAnchors) | Direta (hashes de arquivos) | Proíbe mutação retroativa de inputs humanos históricos | `ACTIVE_INVARIANT` | Código permitindo `state.original_idea` ser alterado |
| **$\text{Authority}(I(S)) \equiv \text{MODEL\_HYPOTHESIS}$** | `INVARIANT` | $I(S)$ (Representações) | Direta (auditoria Pydantic) | Zera autoridade humana sobre termos novos gerados por IA | `ACTIVE_INVARIANT` | Modelo autoatribuindo `USER_EXPLICIT` aceito no Core |
| **$A(X_t) \to C_h(X_t) \to A(X_{t+1})$** | `INVARIANT` | $A$ (Atenção), $C_h$ (Foco) | Direta (fluxo do runner) | Exige re-atenção determinística após toda chamada de foco | `ACTIVE_INVARIANT` | $C_h$ promovendo conclusão sem passar por $A$ |
| **$\text{IntermediaryDepth}(c) = \min_{s \in S} \text{dist}_{\mathcal{G}}(s, c)$** | `DEFINITION` | Grafo $\mathcal{G}$, nó $c$, fontes $S$ | Direta (contagem de arestas) | Mede distância de transformação desde a fonte primária | `COMPUTABLE_METRIC` | Grafo de proveniência não-acíclico ou sem raiz |
| **$\text{SourceRefreshRequired} \iff \text{HighImpact}(c) \land \text{Depth}(c) \ge k$** | `HEURISTIC` | $\text{HighImpact}$, $\text{Depth}$, limiar $k$ | Direta | Exige reancoragem na fonte humana antes de decisão crítica | `TO_BE_CALIBRATED` ($k=2$ fixture) | Reancoragem frequente degradar utilidade sem evitar drift |
| **$P_e(h, t) = t - \tau_{\text{evidence}}(h)$** | `DEFINITION` | Passos $t$, último evento de evidência | Direta (contador de etapas) | Conta operações consecutivas sem injeção de evidência | `COMPUTABLE_METRIC` | Não aplicável (é definição pura) |
| **$\text{AttachmentRisk}(h) \iff P_e(h) \ge N \land \Delta D_t = \emptyset$** | `HEURISTIC` | $P_e$, $\Delta D_t$, limiar $N$ | Direta | Dispara alerta de apego e bloqueia chamada automática | `TO_BE_CALIBRATED` ($N=2$ fixture) | Poda prematura de hipóteses férteis em exploração |
| **$\text{ExpectedDecisionDelta} \ge \text{Cost} + \text{Risk}$** | `HEURISTIC` | Delta decisório, custo, risco | Categórica (`JUSTIFIED` / `NOT`) | Governa permissão de escalação no Early Gate | `OPERATIONAL_POLICY` | Sistema gastar inferência em deltas triviais |
| **$\mathbf{DriftRisk}(X_t) = [u, d_{\max}, P_{e,\max}, \tau, \text{spoof}]$** | `DEFINITION` | Claims não ancoradas, profundidade, etc. | Direta (vetor de inteiros) | Sumariza integridade global no `AttentionSnapshot` | `COMPUTABLE_METRIC` | Não aplicável (é vetor descritivo) |

---

## 5. Auditoria de Precisão Numérica e Limiares

> **REGRA CANÔNICA:** $\text{MEDIÇÃO} \neq \text{LIMIAR}$. Uma métrica computável (ex: profundidade $d$ ou persistência $P_e$) é um fato mensurável; o limiar de corte para disparar ações é uma política a ser calibrada empiricamente no receptor.

1. **Limiar de Persistência sem Evidência ($P_e \ge 2$):**
   - *Status:* `TEST_FIXTURE_THRESHOLD` / `TO_BE_CALIBRATED_FROM_RECEIVER_DATA`.
   - *Significado:* Nos testes unitários adversariais, adotamos $N=2$ eventos como fixture determinística para verificar se o detector reage. O limiar canônico de produção será calibrado na missão M05.3 com base no replay de traces históricos.
2. **Limiar de Profundidade de Intermediário ($\text{IntermediaryDepth} \ge 2$):**
   - *Status:* `TEST_FIXTURE_THRESHOLD` / `TO_BE_CALIBRATED_FROM_RECEIVER_DATA`.
   - *Significado:* A necessidade de `SOURCE_REFRESH` é disparada quando uma claim de alto impacto depende exclusivamente de transformações semânticas derivadas sem ancoragem primária comprovada. O número de arestas $k=2$ é uma fixture experimental.
3. **Invariante de Chamadas ($LEAN\_L1\_MAX\_MODEL\_CALLS = 2$):**
   - *Status:* `ARCHITECTURAL_INVARIANT` (Rígido para a Candidata L1).
   - *Significado:* Não é uma estimativa empírica, mas o teto máximo inegociável de complexidade imposto pelo contrato da arquitetura Lean L1. Se uma tarefa exigir $>2$ chamadas, ela não pertence à classe L1.

---

## 6. Red-Team Aprofundado dos Pilares do FioED

### 6.1 Red-Team do Decision Delta ($\Delta D_t$)
- **Vulnerabilidade 1 (Viés de Ação Imediata):** O foco em Decision Delta pode favorecer passos rápidos e pragmáticos de curto prazo, penalizando reflexões conceituais profundas cujo valor decisório é de longo prazo.
  - *Mitigação:* O FioED reconhece eventos do tipo `ASSUMPTION_EXPOSED` e `TENSION_CLARIFIED` como Decision Deltas positivos de alto valor, mesmo que não gerem código imediato.
- **Vulnerabilidade 2 (Ilusão de Volume de Opções):** O modelo pode inflar o Decision Delta multiplicando opções fracas (`OPTION_ADDED`).
  - *Mitigação:* Apenas opções materiais com trade-offs discriminativos contam como progresso. Adições superficiais geram `UNSUPPORTED_REQUIREMENT_ADDED` (regressão).
- **Vulnerabilidade 3 (Regressão Decisória):** Uma chamada pode degradar a clareza do decisor.
  - *Mitigação:* O FioED formaliza eventos explícitos de `DECISION_REGRESSION` (`SOURCE_DRIFT_INCREASED`, `FALSE_CERTAINTY_CREATED`, `VALID_OPTION_ERASED`, `TENSION_SILENTLY_REMOVED`).

### 6.2 Red-Team do Epistemic Rent (Exploitative vs Exploratory Rent)
- **Vulnerabilidade (Burocracia Anti-Exploração):** Exigir justificativa estrita de Decision Delta pode sufocar a exploração de ideias inovadoras onde o retorno é desconhecido *a priori*.
  - *Mitigação:* O FioED formaliza explicitamente duas modalidades de aluguel:
    1. **`EXPLOITATIVE_RENT`:** Aplicado ao refinamento de mecanismo. Exige justificativa determinística estrita baseada em risco ou alternativas conhecidas.
    2. **`EXPLORATORY_RENT`:** Aplicado à ideação aberta no modo `DEEP_EXPLORATION`. Permite inferência sob incerteza se: (a) houver pergunta de exploração clara; (b) budget de chamadas for explícito e limitado; (c) todos os outputs permanecerem `CANDIDATE`; (d) houver condição determinística de parada.

### 6.3 Red-Team do Operador de Atenção ($A(X_t)$)
- **Vulnerabilidade (A Armadilha do Mapa Total):** O `AttentionSnapshot` pode ser confundido com a realidade completa da ideia, recriando a ilusão de que o sistema "compreendeu o todo".
  - *Mitigação:* Todo `AttentionSnapshot` carrega metadados de incompletude (`completeness_status: REPRESENTATION_ONLY`) e proveniência estrita. O operador $A$ é não-generativo, determinístico e de custo zero ($0$ chamadas de IA).

### 6.4 Red-Team da Fidelidade à Fonte vs Obediência Cega
- **Vulnerabilidade (Literalismo Dogmático):** Preservar a fonte não pode significar que o sistema deve concordar com erros factuais ou premissas absurdas do usuário.
  - *Mitigação:* **$\text{Preservar a Fonte} \neq \text{Obedecer às Alegações como Fato}$.** O FioIdeias tem o dever de desafiar premissas, expor contradições e propor contra-argumentos, rotulando o desafio como `CRITIQUE` ou `MODEL_HYPOTHESIS`. O que é estritamente proibido é alegar que o usuário pediu o que ele não pediu.

### 6.5 Tratamento de Eventos Históricos de Fonte ($S_0, S_1$)
- Se o usuário expressa uma ideia em $t=0$ ($S_0$) e altera ou refina sua preferência em $t=1$ ($S_1$), ambos permanecem como registros imutáveis de fonte.
- A decisão em $t=1$ governa a autoridade presente com proveniência explícita (`supersedes: S_0`), sem apagar ou reescrever retroativamente o histórico de $S_0$.

---

## 7. Registro Canônico de Dívidas Intelectuais (Intellectual Debt Register)

| Construto no FioED | Arte Prévia Mais Próxima | Mecanismo Emprestado | Adaptação Específica no FioIdeias | Acoplamento Distintivo | Status de Reivindicação |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Epistemic Rent** | Metaraciocínio Racional (Russell & Wefald 1991), VoC (Horvitz 1988) | A computação deve justificar seu custo de oportunidade | Alocação de chamadas de LLM governada por destravamento de decisões | Acoplado a veto determinístico de custo zero no Early Gate | `KNOWN_CONCEPT_ADAPTED` |
| **Decision Delta** | Value of Information (Howard 1966), Epistemic Utility (Levi 1967) | Valor de obter nova observação antes da decisão | Modelo discreto de eventos de destravamento e regressão de opções | Acoplado à fronteira prática de decisão humana | `KNOWN_CONCEPT_ADAPTED` |
| **Intermediary Depth** | Data Provenance (Buneman 2001), W3C PROV-DM (2013) | Rastreabilidade de arestas de transformação em grafos | Contagem de transformações semânticas em trajetórias de IA | Acoplado ao gatilho mecânico de `SOURCE_REFRESH` | `KNOWN_CONCEPT_ADAPTED` |
| **Negative Knowledge** | Scoped Pruning (Pearl 1984), HTR (*Arbor*, arXiv:2606.11926, 2026) | Poda de ramos que falharam para não repetir buscas | Tupla de falha com escopo delimitado e `can_reopen_under()` | Acoplado à preservação de histórico sem veto dogmático | `COMBINATION_OF_KNOWN_MECHANISMS` |
| **A $\to$ C $\to$ A Dynamic** | Dual-Process Theory (Kahneman 2011), Plan-Act-Review | Alternância entre checagem ampla e foco executivo | Portão determinístico global $A$ seguido de 1 chamada $C$ e re-atenção $A$ | Acoplado à proibição de recursão $C \to C$ sem re-atenção | `RECEIVER_SPECIFIC_SYNTHESIS` |
| **Evidence-Free Persistence** | Truth Maintenance (Doyle 1979), AGM (Alchourrón et al. 1985) | Rastreamento de justificações e detecção de crenças sem suporte | Contagem de passos consecutivos sem evidência para acionar poda | Acoplado ao combate ao *Epistemic Waste Before Gate* | `RECEIVER_SPECIFIC_SYNTHESIS` |
| **Source-Anchored Lineage** | Filosofia Epistêmica / Teoria Constitucional de IA | Separação estrita entre fonte originária e símbolo gerado | Invariante: representações geradas jamais herdam autoridade humana | Acoplado ao validador determinístico `AuthorityProofValidator` | **`POTENTIALLY_DISTINCT_SYNTHESIS`** |

---

## 8. O que Realmente Parece Distintivo no FioIdeias

A auditoria científica demonstra com clareza: **nenhum primitivo isolado do FioED é uma descoberta sem precedentes**.

A contribuição singular do FioIdeias reside na **arquitetura de integração constitucional**, que articula de forma coesa e mecanicamente verificável:
1. Ancoragem de Origem Humana Imutável ($S$);
2. Não-Autoridade sobre Representações Geradas ($R \neq S$);
3. Auditoria Determinística de Proveniência (`AuthorityProofValidator`);
4. Portão Global de Atenção de Custo Zero ($A$);
5. Concentração Escalonada Condicionada a Aluguel Epistêmico ($C_h$, Max 2 chamadas);
6. Admissão de Raciocínio Orientada a Delta Decisório ($\Delta D$);
7. Memória Técnica com Condições Explícitas de Reabertura ($M$);
8. Preservação de Tensões como Objeto de Primeira Classe ($T$);
9. Imunidade Rigorosa a Custos Afundados;
10. Evolução Condicionada a Evidência Empírica.
