# FIOED-PRIOR-ART-AUDIT.md — Auditoria Externa de Arte Prévia e Linhagem Intelectual

> **STATUS:** `RESEARCH_AUDIT_VERIFIED` | `PRIOR_ART_BOUNDED`
> **OBJETIVO:** Identificar e declarar rigorosamente as conexões, dívidas intelectuais e fronteiras do FioED com a literatura científica e técnica existente, impedindo a apropriação indevida ou a falsa originalidade de conceitos conhecidos.

---

## 1. Dívidas Intelectuais e Linhagem Científica

O FioED baseia-se em conceitos sólidos desenvolvidos ao longo de décadas nas áreas de metaraciocínio computacional, teoria da decisão, sistemas de manutenção da verdade e proveniência de dados.

### 1.1 Metaraciocínio Racional e Valor da Computação
- **Autores Seminais:** Stuart Russell & Eric Wefald (*Do the Right Thing: Studies in Limited Rationality*, 1991); Eric Horvitz (*Reasoning about beliefs and actions in software agents*, 1988); Shlomo Zilberstein (*Using Anytime Algorithms in Intelligent Systems*, 1996).
- **Problema Resolvido na Literatura:** Como alocar tempo e ciclos de computação de forma que o custo do raciocínio adicional seja compensado pela melhoria esperada na qualidade da decisão.
- **Relação com o FioED:** O conceito de **Epistemic Rent** do FioED é uma adaptação direta do *Value of Computation (VoC)* para o domínio de inferência de LLMs em evolução de ideias, onde o custo é medido em chamadas/tokens e a melhoria é avaliada em destravamento de decisões.
- **O que o FioED NÃO inventou:** O princípio de que a computação deve pagar seu próprio custo de oportunidade.

### 1.2 Teoria da Informação e Utilidade Epistêmica
- **Autores Seminais:** Ronald A. Howard (*Information Value Theory*, 1966); Isaac Levi (*Gambling with Truth: An Essay on Induction and the Aims of Science*, 1967).
- **Problema Resolvido na Literatura:** Quantificar o valor de obter uma nova observação antes de tomar uma decisão irreversível.
- **Relação com o FioED:** O **Decision Delta ($\Delta D_t$)** traduz a utilidade epistêmica em um modelo discreto e qualitativo de eventos de destravamento de escolhas para o tomador de decisão humano.

### 1.3 Sistemas de Manutenção da Verdade (TMS) e Rastreamento de Dependências
- **Autores Seminais:** Jon Doyle (*A Truth Maintenance System*, Artificial Intelligence, 1979); Johan de Kleer (*An Assumption-based TMS*, 1986).
- **Problema Resolvido na Literatura:** Rastrear justificativas para crenças, identificar contradições e revisar conjuntos de proposições quando premissas de suporte são removidas.
- **Relação com o FioED:** Os conceitos de **Evidence-Free Persistence** e **Attachment Risk** formalizam a detecção de proposições que continuam ativas no grafo sem justificativas válidas no TMS.

### 1.4 Revisão de Crenças (AGM) e Contração de Conhecimento
- **Autores Seminais:** Carlos Alchourrón, Peter Gärdenfors, David Makinson (*On the Logic of Theory Change: Partial Meet Contraction and Revision Functions*, Journal of Symbolic Logic, 1985).
- **Problema Resolvido na Literatura:** Postulados lógicos formais para contrair ou revisar teorias na presença de novas informações sem inconsistências.
- **Relação com o FioED:** O gerenciamento de **Negative Knowledge** e as **reopen conditions** são uma realização de contração parcial com memória de escopo.

### 1.5 Proveniência de Dados e Linhagem
- **Autores Seminais:** Peter Buneman, Sanjeev Khanna, Wang-Chiew Tan (*Why and Where: A Characterization of Data Provenance*, ICDT 2001); Luc Moreau et al. (*The Open Provenance Model / PROV-DM*, W3C Recommendation, 2013).
- **Problema Resolvido na Literatura:** Rastrear a história de transformações de um dado desde sua fonte original para garantir auditabilidade.
- **Relação com o FioED:** A métrica **Intermediary Depth** é a aplicação da distância de arestas de transformação semântica em grafos de raciocínio gerados por IA, disparando **Source Refresh** para evitar o efeito "telefone sem fio".

### 1.6 Computação Seletiva e Abstenção
- **Autores Seminais:** Ran El-Yaniv & Yair Wiener (*On the Foundations of Selective Classification*, JMLR 2010); David Cohn et al. (*Active Learning with Statistical Models*, JAIR 1996).
- **Problema Resolvido na Literatura:** Saber quando um modelo deve responder vs quando deve se abster ou consultar um humano/oráculo externo.
- **Relação com o FioED:** A saída antecipada **`REQUEST_HUMAN_DECISION`** e o veredito **`STOP_NO_USEFUL_WORK`** são instâncias de abstenção epistêmica no Early Gate.

### 1.7 Busca sobre Raciocínio em LLMs (ToT, Reflexion, Arbor)
- **Autores Recentes:** Shunyu Yao et al. (*Tree of Thoughts*, NeurIPS 2023); Noah Shinn et al. (*Reflexion: Language Agents with Verbal Reinforcement Learning*, NeurIPS 2023); Renmin University / Microsoft Research (*Toward Generalist Autonomous Research via Hypothesis-Tree Refinement — Arbor*, arXiv:2606.11926, submetido em 10 de Junho de 2026).
- **Problema Resolvido na Literatura:** Busca e reflexão iterativa sobre trajetórias de raciocínio geradas por modelos de linguagem.
- **Relação com o FioED:** O FioED colhe as cicatrizes desses sistemas (onde busca cega e multiagentes abertos geram inchaço de custo de 10x a 60x) para criar o portão determinístico de parada precoce e o invariante de no máximo 2 chamadas.

### 1.8 Argumentação Formal e Preservação de Desacordo
- **Autores Seminais:** Phan Minh Dung (*On the Acceptability of Arguments and Its Fundamental Properties*, Artificial Intelligence, 1995); Stanford Deliberative Council for Ideation (DCI, 2024).
- **Problema Resolvido na Literatura:** Modelagem de sistemas de deliberação onde desacordos legítimos não são destruídos por agregação forçada.
- **Relação com o FioED:** O construto **`TensionRecord`** e o estado terminal **`PRESERVED_DISAGREEMENT`** tratam tensões como cidadãos de primeira classe.

---

## 2. Registro Canônico de Dívidas Intelectuais (Intellectual Debt Register)

| Construto no FioED | Arte Prévia Mais Próxima | Mecanismo Emprestado | Adaptação Específica no FioIdeias | Acoplamento Distintivo | Status de Reivindicação |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Source Invariance ($S_{t+1} \equiv S_t$)** | Teoria da Proveniência Imutável (W3C PROV-DM) | Artefatos de fonte primária não sofrem mutação retroativa | Inputs humanos formam raiz imutável de autoridade soberana | Acoplado a veto determinístico contra reescrita de intenção | `KNOWN_CONCEPT_ADAPTED` |
| **Representation Non-Authority ($R \neq S$)** | Filosofia Epistêmica / Teoria Constitucional de IA | Representações geradas são mapas e não a fonte | Modelos de IA recebem zero autoridade sobre termos novos gerados | Acoplado ao `AuthorityProofValidator` | **`POTENTIALLY_DISTINCT_SYNTHESIS`** |
| **Attention Operator ($A(X_t)$)** | Dual-Process Theory (Kahneman 2011), Snapshot de Auditoria | Snapshot global do estado do sistema sem foco local estreito | Operador de custo zero (0 chamadas de IA) avaliando integridade | Acoplado ao Early Epistemic Gate | `RECEIVER_SPECIFIC_SYNTHESIS` |
| **Concentration Operator ($C_h(X_t)$)** | Raciocínio Focalizado / Heuristic Search | Chamada de inferência dirigida para resolver uma incerteza $h$ | Exige alvo fixo, motivo tipado e orçamento de no máximo 1 chamada | Acoplado ao aluguel epistêmico pré-aprovado | `KNOWN_CONCEPT_ADAPTED` |
| **A $\to$ C $\to$ A Dynamic** | Plan-Act-Review, Metaraciocínio de Malha Fechada | Alternância obrigatória entre avaliação ampla e ação local | Toda concentração $C_h$ exige re-atenção $A$ antes de qualquer promoção | Acoplado à proibição de recursão $C \to C$ sem re-atenção | `RECEIVER_SPECIFIC_SYNTHESIS` |
| **Decision Frontier ($D_t$)** | Teoria da Decisão Clássica (Raiffa 1968) | Espaço de ações viáveis abertas para o tomador de decisão | Conjunto estruturado de escolhas práticas disponíveis ao humano | Acoplado à medição de avanço prático do usuário | `KNOWN_CONCEPT_ADAPTED` |
| **Decision Delta ($\Delta D_t$)** | Value of Information (Howard 1966), Epistemic Utility (Levi 1967) | Medição de progresso pelo destravamento de opções | Modelo discreto de eventos (`OPTION_ADDED`, `ASSUMPTION_EXPOSED`, etc.) | Acoplado ao rastreamento de regressões decisórias | `KNOWN_CONCEPT_ADAPTED` |
| **Epistemic Rent** | Metaraciocínio Racional (Russell & Wefald 1991), VoC (Horvitz 1988) | A computação deve justificar seu custo de oportunidade | Alocação de chamadas de LLM governada por destravamento de decisões | Acoplado à distinção entre `EXPLOITATIVE` e `EXPLORATORY` rent | `KNOWN_CONCEPT_ADAPTED` |
| **Intermediary Depth** | Data Provenance (Buneman 2001), Lineage Graphs | Contagem de arestas de transformação em grafos | Medição de distância semântica desde a fonte humana | Acoplado ao gatilho determinístico de `SOURCE_REFRESH` | `KNOWN_CONCEPT_ADAPTED` |
| **Evidence-Free Persistence ($P_e$)** | Truth Maintenance (Doyle 1979), Dependency Tracking | Detecção de crenças mantidas sem suporte de evidência | Contagem de eventos de elaboração sem injeção factual | Acoplado à detecção de `ATTACHMENT_RISK` | `RECEIVER_SPECIFIC_SYNTHESIS` |
| **Attachment Risk** | Heuristic Pruning / Loop Prevention | Poda de ramos que estagnaram ou geram custos circulares | Bloqueio de chamadas automáticas em hipóteses não ancoradas | Acoplado à preservação como mero candidato | `RECEIVER_SPECIFIC_SYNTHESIS` |
| **Memory Admission** | Selective Experience Replay / Case-Based Reasoning | Filtro rigoroso de admissão em memória de longo prazo | Conversação efêmera $\neq$ memória durável; exige escopo e reopen | Acoplado à rejeição de especulações verbosas | `COMBINATION_OF_KNOWN_MECHANISMS` |
| **Source Refresh** | Re-anchoring em Protocolos de Comunicação | Consulta à fonte original quando a mensagem se degrada | Revalidação de claims de alto impacto contra o input humano inicial | Acoplado ao combate ao "telefone sem fio" de LLMs | `RECEIVER_SPECIFIC_SYNTHESIS` |
| **Sunk-Cost Immunity** | Racionalidade Econômica (Thaler 1980) | Custos afundados não devem influenciar decisões presentes | O número de tokens ou chamadas gastas não altera o $ClaimStatus$ | Acoplado à integridade ontológica de hipóteses | `KNOWN_CONCEPT_ADAPTED` |
| **Tension Preservation** | Argumentation Frameworks (Dung 1995), DCI (2024) | Preservação de contradições sem falso consenso forçado | `TensionRecord` e `PRESERVED_DISAGREEMENT` como estados terminais | Acoplado à doutrina *Truth Over Agreement* | `KNOWN_CONCEPT_ADAPTED` |
| **Donor Conditionality** | Transfer Learning / Case Adaptation | Uso de conhecimento prévio de sistemas semelhantes | Doadores são operadores condicionais ativados por gaps e não etapas fixas | Acoplado à regra *Before Inventing, Harvest* | `COMBINATION_OF_KNOWN_MECHANISMS` |

---

## 3. O que Realmente Parece Distintivo no FioIdeias

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
