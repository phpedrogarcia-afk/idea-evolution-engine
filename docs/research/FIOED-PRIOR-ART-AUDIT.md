# FIOED-PRIOR-ART-AUDIT.md — Auditoria Externa de Arte Prévia e Linhagem Intelectual

> **STATUS:** `RESEARCH_AUDIT_VERIFIED`
> **OBJETIVO:** Identificar e declarar rigorosamente as conexões, dívidas intelectuais e fronteiras do FioED com a literatura científica e técnica existente, impedindo a apropriação indevida de conceitos conhecidos.

---

## 1. Dívidas Intelectuais e Linhagem Científica

O FioED baseia-se em conceitos sólidos desenvolvidos ao longo de décadas nas áreas de metaraciocínio computacional, teoria da decisão, sistemas de manutenção da verdade e proveniência de dados.

### 1.1 Metaraciocínio Racional e Valor da Computação
- **Autores Seminais:** Stuart Russell & Eric Wefald (*Do the Right Thing: Studies in Limited Rationality*, 1991); Eric Horvitz (*Reasoning about beliefs and actions in software agents*, 1988).
- **Problema Resolvido na Literatura:** Como alocar tempo e ciclos de computação de forma que o custo do raciocínio adicional seja compensado pela melhoria esperada na qualidade da decisão.
- **Relação com o FioED:** O conceito de **Epistemic Rent** do FioED é uma adaptação direta do *Value of Computation (VoC)* para o domínio de inferência de LLMs em evolução de ideias, onde o custo é medido em chamadas/tokens e a melhoria é avaliada em destravamento de decisões.
- **O que o FioED NÃO inventou:** O princípio de que a computação deve pagar seu próprio custo de oportunidade.

### 1.2 Teoria da Informação e Utilidade Epistêmica
- **Autores Seminais:** Ronald A. Howard (*Information Value Theory*, 1966); Isaac Levi (*Gambling with Truth: An Essay on Induction and the Aims of Science*, 1967).
- **Problema Resolvido na Literatura:** Quantificar o valor de obter uma nova observação antes de tomar uma decisão irreversível.
- **Relação com o FioED:** O **Decision Delta ($\Delta D_t$)** traduz a utilidade epistêmica em um modelo discreto e qualitativo de eventos de destravamento de escolhas para o tomador de decisão humano.

### 1.3 Sistemas de Manutenção da Verdade (TMS) e Revisão de Crenças (AGM)
- **Autores Seminais:** Jon Doyle (*A Truth Maintenance System*, 1979); Carlos Alchourrón, Peter Gärdenfors, David Makinson (*On the Logic of Theory Change*, 1985).
- **Problema Resolvido na Literatura:** Rastrear justificativas para crenças, identificar contradições e revisar conjuntos de proposições quando premissas são falseadas.
- **Relação com o FioED:** Os conceitos de **Evidence-Free Persistence** e **Attachment Risk** formalizam a detecção de proposições que continuam ativas no grafo sem suporte de justificativas válidas no TMS.

### 1.4 Proveniência de Dados e Linhagem
- **Autores Seminais:** Peter Buneman, Sanjeev Khanna, Wang-Chiew Tan (*Why and Where: A Characterization of Data Provenance*, 2001); W3C PROV Data Model (PROV-DM, 2013).
- **Problema Resolvido na Literatura:** Rastrear a história de transformações de um dado desde sua fonte original para garantir auditabilidade.
- **Relação com o FioED:** A métrica **Intermediary Depth** é a aplicação da distância de arestas de transformação semântica em grafos de raciocínio gerados por IA, disparando **Source Refresh** para evitar o efeito "telefone sem fio".

### 1.5 Arquiteturas de Raciocínio em LLMs (Arbor, Reflexion, Tree of Thoughts)
- **Autores Recentes:** Yao et al. (*Tree of Thoughts*, 2023); Shinn et al. (*Reflexion: Language Agents with Verbal Reinforcement Learning*, 2023); Renmin/Microsoft (*Arbor*, 2024).
- **Problema Resolvido na Literatura:** Busca e reflexão iterativa sobre trajetórias de raciocínio geradas por modelos de linguagem.
- **Relação com o FioED:** O FioED colhe as cicatrizes desses sistemas (onde busca cega e multiagentes abertos geram inchaço de custo de 10x a 60x) para criar o portão determinístico de parada precoce e o invariante de no máximo 2 chamadas.

---

## 2. Matriz de Classificação de Novidade

| Componente / Proposição do FioED | Base Teórica na Literatura | Diferenciação Específica no FioED | Classificação Formal |
| :--- | :--- | :--- | :---: |
| **Epistemic Rent** | Metaraciocínio Racional / VoC | Avaliação categórica determinística sem fake probabilities | `KNOWN_CONCEPT_ADAPTED` |
| **Decision Delta** | Value of Information / Epistemic Utility | Vetor discreto de destravamento de opções práticas para o usuário | `KNOWN_CONCEPT_ADAPTED` |
| **Intermediary Depth** | Data Provenance / PROV-DM | Gatilho mecânico de reancoragem (`SOURCE_REFRESH`) | `KNOWN_CONCEPT_ADAPTED` |
| **Negative Knowledge Memory** | Scoped Heuristic Pruning | Tuplas de falha com escopo e `can_reopen_under()` | `COMBINATION_OF_KNOWN_MECHANISMS` |
| **A $\to$ C $\to$ A Dynamic** | Dual-Process Cognition / Plan-Act-Review | Portão determinístico intercalado com 1 chamada de foco | `RECEIVER_SPECIFIC_SYNTHESIS` |
| **Evidence-Free Persistence** | Truth Maintenance / Contradiction Tracking | Contagem de passos sem suporte para bloquear alucinação recursiva | `RECEIVER_SPECIFIC_SYNTHESIS` |
| **Source Anchoring + Non-Authority** | Filosofia Epistêmica / Teoria Constitucional | Invariante estrito: representações de IA jamais herdam autoridade | **`POTENTIALLY_DISTINCT_SYNTHESIS`** |

---

## 3. Conclusão da Auditoria

O FioED **não alega** ter descoberto uma nova teoria matemática pura do conhecimento. Sua contribuição reside na **arquitetura de contenção constitucional de IA**, combinando:
1. Ancoragem de Origem Humana Soberana;
2. Não-Autoridade sobre Representações Geradas;
3. Avaliação Global Determinística de Custo Zero (Atenção);
4. Concentração Escalonada sob Demanda de Aluguel Epistêmico (Máximo 2 chamadas);
5. Imunidade Rigorosa a Custos Afundados.
