# TERMINOLOGY.md — Glossário Canônico do IEE

> **ESTE É O GLOSSÁRIO CANÔNICO DE TERMOS DO IDEA EVOLUTION ENGINE.**
> Nenhuma IA ou documento pode redefinir, distorcer ou inventar novos significados para estes termos.

---

### Idea (Ideia)
Intenção ou hipótese humana que busca resolver um problema, criar um valor ou explorar uma possibilidade no mundo real. Pode entrar no sistema em estado bruto (`RAW_IDEA`) e evoluir para uma representação estruturada.

### IdeaGenome (Genoma da Ideia)
Objeto persistente, versionado e imutável que representa o estado epistemológico total da ideia em um dado momento. Contém identidade, essência, problema, claims, relações, evidências, premissas, restrições, frames, incertezas, tensões, decisões humanas e histórico de linhagem.

### Claim (Afirmação Investigável)
Unidade mínima de investigação epistêmica do sistema. Uma proposição declarativa atômica com status epistêmico independente (`UNTESTED`, `SUPPORTED`, `REFUTED`, `UNCERTAIN`) e status de ciclo de vida (`ACTIVE`, `SUPERSEDED`, `DEPRECATED`).

### Evidence (Evidência)
Dado ou observação com proveniência verificável que altera a plausibilidade de uma claim. Não se confunde com inferência pura de modelo ou histórico de chat. Possui tipagem estrita (`FACT`, `OBSERVATION`, `HYPOTHESIS`, `INTERPRETATION`, `MODEL_INFERENCE`, `HUMAN_INPUT`, `EXPERIMENT_RESULT`).

### Assumption (Premissa / Pressuposto)
Condição ou hipótese implícita que é aceita como verdadeira sem evidência suficiente e da qual depende a validade de uma ou mais claims.

### Constraint (Restrição)
Limite de contorno rígido (físico, regulatório, econômico, ético ou técnico) que restringe o espaço de soluções viáveis da ideia.

### Frame (Moldura Conceitual)
Perspectiva ou paradigma cognitivo através do qual o problema e as soluções são formulados e interpretados.

### Tension (Tensão)
Desacordo estruturado ou divergência não resolvida entre claims, evidências, premissas, frames ou valores. Não é necessariamente uma contradição lógica pura e nunca deve ser silenciada por consenso artificial.

### Gap (Lacuna Epistêmica)
Falta identificada de informação, lógica, evidência, dependência, testabilidade ou clareza de frame necessária para justificar o próximo passo da ideia.

### Uncertainty (Incerteza)
Questão ou dúvida explicitada sobre uma claim ou propriedade do sistema cujo valor de verdade é atualmente desconhecido.

### Decisive Uncertainty (Incerteza Decisiva)
Incerteza cuja resolução plausivelmente modifica a próxima ação recomendada, o estado de uma claim estruturalmente importante ou uma decisão soberana. Avaliada via contrafactuais (`if_supported`, `if_refuted`, `if_uncertain`).

### Decision Relevance (Relevância Decisória)
Grau de impacto que o conhecimento de uma incerteza tem sobre decisões, claims centrais e ações. Registrado prospectivamente no `DecisionRelevanceReport`.

### Decision Delta (Delta Decisório)
Registro retrospectivo do que de fato se alterou em decisões, claims e ações após a conclusão de uma investigação ou teste, permitindo calibrar previsões.

### Structure Gain (Ganho de Estrutura)
Aumento na clareza estrutural, identificação de novas claims falsificáveis, exposição de premissas ocultas, relações de dependência ou mapeamento de incertezas. Métrica primária de progresso durante o bootstrap.

### Bootstrap (Regime de Estruturação)
Regime cognitivo inicial onde o `IdeaGenome` é esparso e o objetivo exclusivo do sistema é tornar a ideia estruturalmente legível, antes de exigir relevância decisória sofisticada.

### Deliberation (Deliberação)
Processo estruturado e adversarial de investigação epistêmica executado por funções de IA sob um contrato prévio, visando reduzir incertezas ou resolver gaps.

### DeliberationContract (Contrato de Deliberação)
Contrato formal pré-execução que governa uma rodada de deliberação, especificando objetivo, claims-alvo, operação epistêmica, topologia, participantes, atos permitidos, critérios de progresso, orçamento e condições de parada.

### Epistemic Act (Ato Epistêmico)
Movimento cognitivo tipado e atômico executado durante uma deliberação (ex: `FRAME`, `PROPOSE`, `CHALLENGE`, `GROUND`, `UPDATE`, `REFRAME`, `SYNTHESIZE`, `RECOMMEND`).

### Function (Função Epistemológica)
Papel cognitivo especializado (ex: `find_disconfirming_evidence`, `detect_hidden_assumptions`, `estimate_feasibility`) independente de modelos específicos.

### Agent (Agente)
Instância autônoma ou semi-autônoma encarregada de executar uma ou mais funções epistemológicas sob as restrições de um contrato.

### Model (Modelo / LLM)
Provedor de capacidade de inferência de linguagem natural (ex: GPT-4, Claude 3.5, Gemini 1.5, DeepSeek) utilizado como executor de funções.

### Topology (Topologia de Deliberação)
Estrutura formal de fluxo e comunicação entre participantes em uma rodada (ex: `SEQUENTIAL`, `PARALLEL`, `CRITIQUE_LOOP`, `TREE`, `SYNTHESIS_LOOP`).

### GenomePatch (Patch do Genoma)
Proposta estruturada e atômica de mutação do `IdeaGenome`. Contém operações, versão-base e justificativa epistêmica. Submetida ao `GenomeValidator`.

### ReadyToTest (Pronto para o Teste)
Veredito de transição que declara que a investigação puramente deliberativa atingiu retornos decrescentes e que o próximo conhecimento de maior valor deve vir de um teste empírico no mundo real via `TestContract`.

### ProtectedCore (Núcleo Protegido)
Dimensão essencial, valor ou premissa fundacional da ideia blindada contra modificação automática por IA. Pode ser criticada, mas só pode ser alterada por autoridade humana.

### HumanDecisionRequired (Decisão Humana Obrigatória)
Estado do sistema indicando que a resolução de uma encruzilhada exige autoridade normativa, julgamento de valores ou escolha de propósito humano, e não investigação empírica adicional.

### Pivot (Pivot)
Mudança fundamental de hipótese central, problema ou mecanismo que cria uma nova branch de linhagem a partir de um estado anterior, preservando o histórico.

### Branch (Ramificação de Linhagem)
Linhagem alternativa de evolução de uma ideia que se desenvolve paralelamente ou após um pivot, sem destruir a versão de origem.

### ReopenCondition (Condição de Reabertura)
Critério explícito sob o qual uma conclusão, claim resolvida ou veredito de `READY_TO_TEST` deve ser reaberto para reinvestigação (ex: surgimento de evidência contraditória material).
