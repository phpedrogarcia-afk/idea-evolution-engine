# IDEA EVOLUTION ENGINE


Documento fundador e arquitetura de continuidade — v0.1 — 26 de agosto de 2026


Um sistema para transformar uma ideia humana crua em uma hipótese estruturada, investigada, criticada, versionada e pronta para encontrar a realidade — sem transferir às máquinas a soberania sobre a ideia.


```text
CENTELHA HUMANA
      ↓
ESTRUTURA
      ↓
INVESTIGAÇÃO DELIBERATIVA
      ↓
EVIDÊNCIA + CONTRADIÇÃO + ALTERNATIVAS
      ↓
CONVERGÊNCIA SUFICIENTE
      ↓
READY TO TEST
      ↓
REALIDADE
      ↓
NOVO CONHECIMENTO
```


Este documento é simultaneamente: visão de produto, especificação conceitual, constituição intelectual, mapa arquitetural, plano de construção e guia de entrada para qualquer IA ou colaborador.


---


## 0. Como ler este documento


O projeto possui uma visão grande, mas a estratégia deliberada é começar pequeno. A visão final pode incluir descoberta de ideias, deliberação adaptativa, múltiplos modelos, pesquisa externa, testes reais e integração com FioOS. O primeiro produto, porém, pode ser um roteador inteligente de deliberação: recebe uma ideia, passa-a por funções específicas de IA, preserva estado estruturado e encerra quando a discussão cumpriu seu contrato.


> **REGRA:** Não confundir a visão de longo prazo com os requisitos do primeiro protótipo. O MVP deve provar o mecanismo central antes de ampliar autonomia, modelos, topologias ou infraestrutura.


## 1. O problema humano que queremos resolver


Boas ideias raramente nascem prontas. Elas surgem como intuições, incômodos, analogias, perguntas, desejos ou possibilidades ainda malformadas. A pessoa normalmente não sabe quais pressupostos estão escondidos, se algo parecido já existe, qual parte é realmente nova, quais contradições existem, o que é tecnicamente possível ou qual teste deve ser feito primeiro.


Hoje é possível conversar com uma IA, copiar a resposta para outra IA, trazer a crítica de volta para a primeira e repetir. Esse processo já melhora ideias. O problema é que o humano atua como orquestrador manual: escolhe modelo, contexto, função, ordem, o que preservar, o que descartar, quando repetir e quando parar.


O Idea Evolution Engine nasce para automatizar e disciplinar exatamente esse processo, sem transformar a ideia em uma conversa infinita ou em uma votação entre modelos.


### 1.1 A versão simples da necessidade


```text
Hoje:
Pessoa → IA A → copia → IA B → copia → IA C → volta → síntese manual

Queremos:
Pessoa → protocolo → IA adequada → IA adequada → crítica → reconstrução → validação → ideia refinada
```


A primeira versão já pode gerar valor se apenas substituir o trabalho manual de copiar contexto entre modelos por um fluxo dirigido, contextualizado, versionado e com regras de término.


## 2. Definição do projeto


> **REGRA:** O Idea Evolution Engine é um sistema de investigação deliberativa que reduz, organiza e torna acionável a incerteza ao redor de uma intenção humana, utilizando funções e modelos de IA, evidências externas, deliberação adversarial, memória epistêmica estruturada e validação determinística, sem transferir às máquinas a soberania sobre a ideia.


### 2.1 O que ele não é

- Não é um chat com vários bots.

- Não é uma mesa-redonda de personagens de IA.

- Não é um gerador de startups.

- Não é uma máquina que decide se a ideia é boa ou ruim.

- Não é um sistema que força consenso.

- Não é um substituto do autor.

- Não é um módulo do FioOS.

- Não é uma promessa de matemática universal da criatividade.


### 2.2 Resultado desejado


O sistema não deve devolver apenas uma versão “mais bonita” da ideia. Deve devolver um pacote de maturação: origem, essência preservada, problema, mecanismo, claims críticas, evidências, contradições, alternativas, riscos, incertezas restantes, decisões humanas e próximo teste ou ação racional.


## 3. Princípio fundador: progresso não é prosa


> **REGRA:** Progress over prose: aumento de texto não conta como progresso. Progresso precisa alterar estrutura, evidência, decisão, claim, teste ou rota de ação.


Uma rodada pode ser extensa e ainda assim produzir NO_MEASURABLE_PROGRESS. Outra pode produzir apenas uma frase — “esta premissa é falsa” — e mudar toda a arquitetura da ideia.


## 4. Começo, meio e fim do ciclo de uma ideia


### 4.1 Começo — centelha e bootstrap estrutural


A ideia entra no estado RAW_IDEA. O sistema não tenta julgá-la imediatamente. Primeiro precisa entendê-la e torná-la estruturalmente legível.


```text
RAW_IDEA
   ↓
STRUCTURE_BOOTSTRAP
   ↓
problem statement + claims + relações + assumptions + decisões futuras
   ↓
DECISIONAL_INVESTIGATION
```


Durante STRUCTURE_BOOTSTRAP, o objetivo é StructureGain: produzir uma representação mínima que permita saber quais perguntas realmente importam. Decision relevance pode permanecer UNKNOWN sem ser erro.


### 4.2 Meio — investigação decisional


Quando existe estrutura mínima, o sistema passa a priorizar incertezas decisivas: perguntas cuja resolução pode mudar uma ação, uma claim estrutural ou uma decisão. Deliberações passam a ter contratos formais, funções epistemológicas, topologias e critérios de progresso definidos antes da execução.


```text
Epistemic Assessor
      ↓
Investigation Selector
      ↓
Question Classifier / Decomposer
      ↓
Team Composer
      ↓
Topology Planner
      ↓
Contract Builder
      ↓
Execution
      ↓
Structured Delta
      ↓
Genome Validator
      ↓
Progress / Replan / Ready to Test
```


### 4.3 Fim de uma fase — READY_TO_TEST


> **REGRA:** READY_TO_TEST não significa “a ideia está boa” nem “acabamos”. Significa que o próximo ganho relevante de conhecimento deve vir da realidade, não de mais deliberação.


O teste deve ser discriminativo: resultados diferentes precisam alterar uma claim, uma decisão ou a próxima ação. Depois do teste, novas evidências entram e a ideia pode retornar a UNDER_INVESTIGATION. O sistema é cíclico, não um pipeline de conclusão definitiva.


## 5. O IdeaGenome — memória durável da ideia


O IdeaGenome é o objeto central de estado. O chat é efêmero; o genoma é versionado, auditável e reconstruível. Uma versão nunca é sobrescrita: qualquer mutação gera uma nova versão.


|Bloco|Função|
|---|---|

|identity|ID, versão, parent, timestamps e content hash.|

|essence|Origem humana, propósito e protected cores.|

|problem_space|Problema, atores, contexto e alternativas existentes.|

|claims|Afirmações investigáveis.|

|claim_relations|depends_on, supports, weakens, contradicts, supersedes.|

|evidence_registry|Evidências com tipo, proveniência e verificação.|

|assumptions / constraints / frames|Premissas, limites e molduras de interpretação.|

|open_questions / uncertainties|Perguntas abertas e incertezas promovidas.|

|tensions / contradictions|Conflitos lógicos, empíricos, normativos ou de frame.|

|human_decisions|Decisões soberanas e intervenções humanas.|

|lineage|Versões, branches e pivots.|

|deliberation_history|Contratos, rodadas, deltas e resultados.|

|workflow_state|Estado atual e eventos de transição.|


### 5.1 Claims


Claims são a unidade mínima de investigação. Uma ideia inteira é abstrata demais para ser confrontada de modo disciplinado.


```text
CLAIM-01: “Existe um problema real.”
CLAIM-02: “O mecanismo proposto resolve esse problema.”
CLAIM-03: “Usuários aceitariam o comportamento necessário.”
CLAIM-04: “A solução é tecnicamente viável.”
```


Status epistêmicos iniciais: UNTESTED, SUPPORTED, REFUTED, UNCERTAIN. Ciclo de vida estrutural é separado: ACTIVE, SUPERSEDED, DEPRECATED.


### 5.2 Evidence Registry


> **REGRA:** Memória não é evidência. Tool output não é automaticamente evidência. Opinião de modelo não vira fato por repetição.


Toda evidência deve declarar tipo e proveniência adequados. Evidência externa pode vir de paper, web, experimento, arquivo, humano ou inferência de modelo. A independência deve considerar source_family, method_family, data_origin e model_family.


### 5.3 TensionRecord


Contradição é apenas uma classe de tensão. O sistema deve preservar desacordos sem “alisar” tudo em síntese.


```text
TensionRecord types:
LOGICAL_CONTRADICTION
EMPIRICAL_DISAGREEMENT
VALUE_CONFLICT
TRADEOFF
FRAME_CONFLICT
AMBIGUITY
EVIDENCE_CONFLICT
```


## 6. Soberania humana e Protected Cores


> **REGRA:** Protected core é protegido contra alteração automática, não contra crítica.


O sistema pode pressionar um protected core com evidência e registrar CORE_PRESSURE_REPORT. Pode marcar STABLE, UNDER_PRESSURE ou IN_CONFLICT. Só o humano autorizado pode reafirmar ou alterar o núcleo. Pivots são branches, nunca substituições silenciosas da ideia original.


## 7. Bootstrap estrutural


### 7.1 Objetivo


Um genoma esparso não é falha. É um regime cognitivo. Durante bootstrap, o sistema maximiza StructureGain, não decision-relevant information gain.


### 7.2 O que conta como StructureGain

- nova claim falsificável

- nova relação entre claims

- assumption escondida tornada explícita

- frame dominante identificado

- separação problema/solução

- decisão futura relevante identificada

- teste possível tornado formulável

- alternativa plausível criada


### 7.3 O que não conta

- texto mais longo

- paráfrase

- sinônimos

- reescrita estética

- claim duplicada

- explicação mais elegante sem consequência estrutural


### 7.4 BOOTSTRAP_EXIT_POLICY_V0.1


Saída do bootstrap é estrutural e mínima, nunca uma contagem arbitrária de rodadas.

- problem statement não rejeitado pelo humano

- ao menos duas claims centrais

- ao menos uma relação explícita entre claims

- ao menos uma assumption relevante

- ao menos uma ação/decisão/teste dependente dessas claims

- ao menos uma pergunta promovível a candidate uncertainty

- protected cores registrados ou ausência explicitamente registrada

- pelo menos um DecisionRelevanceReport mínimo possível

- nenhum conflito crítico de intenção pendente

- budget não excedido


> **REGRA:** eligible_to_exit é sempre derivado por policy versionada. O LLM não pode simplesmente declará-lo true.


## 8. Incerteza decisiva


> **REGRA:** Uma incerteza é decisiva quando sua resolução plausivelmente muda a próxima ação, uma claim estruturalmente relevante ou uma decisão.


```text
DECISIVE_UNCERTAINTY iff
ActionImpact OR ClaimImpact OR DecisionImpact
```


A avaliação deve ser contrafactual: se suportada, o que muda? Se refutada, o que muda? Se continuar incerta, o que muda? Se quase nada muda, a pergunta pode ser interessante, mas não é decisiva.


## 9. Três artefatos de relevância e progresso


### 9.1 UncertaintyRecord


Registra a incerteza, tipo, claims relacionadas, estado atual da evidência e status: OPEN, UNDER_INVESTIGATION, RESOLVED ou DEFERRED. Tipos: EMPIRICAL, MECHANISM, VALUE, FEASIBILITY, FRAME, DEPENDENCY, AUTHORITY.


### 9.2 DecisionRelevanceReport


Olha para frente. Explicita contrafactuais, ActionImpact, ClaimImpact, DecisionImpact, dependency effect, evidence state e se a incerteza é decisiva. Contrafactuais são hipóteses com proveniência, não fatos.


### 9.3 DecisionDelta


Olha para trás. Registra o que realmente mudou depois da investigação: ação anterior→nova, claims alteradas, decisões afetadas, material_change, custo e notas. Isso permite calibrar previsões de impacto contra impacto realizado.


## 10. O Deliberation Control Engine (DCE)


O DCE é o sistema nervoso central. Ele não é moderador de chat; governa por que uma deliberação existe, quem participa, como interage, qual artefato deve sair e quando aquela rodada cumpriu sua função.


|Componente|Pergunta|
|---|---|

|Epistemic Assessor|O que sabemos, não sabemos e onde há tensão/gap?|

|Gap Detector|Qual lacuna é informacional, lógica, evidencial, de dependência, testabilidade ou frame?|

|Investigation Selector|Qual incerteza merece recurso agora?|

|Question Classifier|É empírica, normativa, mista, estrutural ou desconhecida?|

|Question Decomposer|Se mista, quais partes podem ser investigadas e quais exigem humano?|

|Team Composer|Precisamos de equipe? Quais funções/modelos?|

|Topology Planner|Sequencial, paralelo, critique loop, tree, synthesis loop?|

|Contract Builder|Quais outputs, critérios de progresso, falha, budget e parada?|

|Execution Orchestrator|Executa o contrato; no futuro pode delegar ao FioOS.|

|Progress Monitor|O contrato produziu delta material?|

|GenomePatch Builder|Converte outputs em proposta estruturada de mutação.|

|Genome Validator|Valida schema, referências, autoridade, invariantes e transições.|

|Termination Controller|Continua, replana, vai ao mundo, consulta humano ou encerra a fase?|


## 11. DeliberationContract


> **REGRA:** Toda deliberação deve ter contrato. Conversa sem contrato não é unidade oficial de investigação.


Campos conceituais: target, objective, target_claims, uncertainty_id, epistemic_operation, team, topology, allowed/required epistemic acts, required_artifacts, candidate_admission_policy, progress_criteria, non_progress_criteria, failure_condition, interpretation_of_failure, stop_condition, safety_bound, coordination_budget e reopen_policy.


### 11.1 Progress is contract-relative


> **REGRA:** O que conta como progresso é definido antes da execução e depende do contrato daquela rodada. O sistema não pode olhar o resultado e depois inventar por que ele foi útil.


### 11.2 Atos epistêmicos tipados


Inspirados parcialmente por DCI, movimentos concretos podem ser tipados. O v0.1 deve começar pequeno, por exemplo: FRAME, PROPOSE, CHALLENGE, GROUND, UPDATE, REFRAME, SYNTHESIZE, RECOMMEND. Não copiar uma taxonomia inteira sem teste.


## 12. Team Composer e Topology Planner


Não existem personagens permanentes obrigatórios. Existem funções epistemológicas recrutáveis dinamicamente: search_external_evidence, find_disconfirming_evidence, seek_alternative_explanation, estimate_feasibility, challenge_causal_mechanism, detect_hidden_assumptions, design_real_world_test, synthesize_state e outras.


O DCE deve decidir antes se multiagente realmente agrega valor. DCI mostrou que coordenação estruturada pode ser muito cara e nem sempre supera um agente único. Portanto SINGLE_AGENT_MODE é um modo legítimo.


```text
coordination_value LOW  → single strong model
coordination_value HIGH → structured multi-agent deliberation
```


Topologias do v0.1 podem ser templates fixos: SEQUENTIAL, PARALLEL, CRITIQUE_LOOP, TREE e SYNTHESIS_LOOP. max_cycles existe apenas como safety bound, nunca como critério de maturidade.


## 13. GenomePatch e GenomeValidator


> **REGRA:** LLM propõe; kernel valida.


Nenhum modelo altera o IdeaGenome diretamente. Ele propõe um GenomePatch. O patch inteiro é simulado em memória e aplicado atomicamente apenas se passar por todas as camadas.


```text
GenomePatch
  ↓
Schema validation
  ↓
Reference validation
  ↓
Authority validation
  ↓
Invariant validation
  ↓
Transition validation
  ↓
ALL PASS? → commit vN+1
FAIL?     → reject, vN permanece byte-identical
```


Patches carregam base_version e precondições para impedir aplicação silenciosa sobre estado antigo. Identidade declarada não equivale a autoridade verificada; authority deve vir de execution_context confiável.


### 13.1 Invariantes constitucionais principais

- Versões são imutáveis e encadeadas.

- Patches são atômicos.

- Toda mutação possui proveniência.

- LLMs propõem; nunca escrevem diretamente.

- Protected cores exigem autoridade humana para alteração.

- Evidência produzida por IA não vira fato por declaração.

- Relações históricas ficam separadas de avaliações derivadas.

- Transições precisam de trigger e basis explícitos.

- Branches nunca destroem linhagens anteriores.

- Conflito de versão impede aplicação silenciosa.

- Aumento de texto não pode mascarar ausência de progresso.

- Decisões humanas nunca podem ser inferidas pelo sistema.


## 14. Estados e transições


```text
RAW_IDEA
  ↓
STRUCTURE_BOOTSTRAP
  ↓
DECISIONAL_INVESTIGATION / UNDER_INVESTIGATION
  ├─ READY_TO_TEST
  ├─ HUMAN_DECISION_REQUIRED
  ├─ PIVOT_CANDIDATE
  ├─ REPLAN_REQUIRED
  ├─ STALLED
  ├─ RESOURCE_LIMIT_REACHED
  ├─ NOT_CURRENTLY_VIABLE
  └─ ARCHIVED
```


HUMAN_DECISION_REQUIRED é reservado para valores, autoridade, protected cores, intenção e trade-offs soberanos. Ignorância empírica deve ser investigada, não escalada ao humano por padrão.


## 15. READY_TO_TEST e TestContract


> **REGRA:** READY_TO_TEST é um veredito sobre a fonte do próximo conhecimento, não sobre a qualidade da ideia.


Um TestContract deve declarar target_claim, rival_hypotheses, measurable_implications, test_method, possible_outcomes, decision_effect_per_outcome, stopping_rule e evidence_protocol. POPPER é donor importante aqui para claims estatisticamente testáveis, mas e-values não viram métrica universal de evidência.


## 16. Regra de reabertura


Conclusões são provisórias dentro de um envelope de conhecimento. READY_TO_TEST, decisões e sínteses podem carregar ReopenCondition: nova evidência contraditória, resultado fora da faixa esperada, alteração de protected core ou surgimento de mecanismo rival material.


## 17. Discovery e Evolution


O sistema pode alternar entre regimes. Discovery expande o espaço de possibilidades; Evolution investiga uma possibilidade. Contradições de frame podem fazer Evolution retornar a Discovery. C-K Theory é donor conceitual importante, mas deve ser usado como projection opcional, não ontologia universal.


```text
EVOLUTION → frame contradiction → DISCOVERY → new branch → EVOLUTION
```


## 18. Filosofia científica e regras do projeto

- Não reinventar a roda: pesquisar antes de construir.

- Não copiar projetos inteiros: extrair mecanismos.

- Donor adoption must be gap-driven.

- Capability não é Authority.

- Memória não é Evidência.

- Contexto não é Autoridade.

- Determinístico primeiro; IA nas bordas semânticas.

- Preservar contradições e status epistêmico.

- Não forçar consenso.

- Falha, aborto e NO_USEFUL_WORK_FOUND são dados legítimos.

- Um run bem-sucedido prova possibilidade, não confiabilidade.

- Juiz é instrumento e precisa ser calibrado.

- Sem baseline, não alegar melhoria.

- Prompts, policies, schemas e judges precisam de versão.

- Reversibilidade é obrigatória para mudanças relevantes.

- Quem cria não deve ser o único aprovador.

- Delegação transfere trabalho, não autoridade.

- Uma fronteira contornável não é fronteira.

- Formalizar o que pode ser formalizado; governar semanticamente o resto.

- Custo e budget fazem parte do experimento.

- Usar o modelo mais econômico capaz da tarefa.

- Autonomia deve crescer com evidência.

- Parar é um resultado legítimo.

- Progress over prose.

- Reality over deliberation.

- Human intent sovereignty.

- Human cognitive theory → AI mechanism exige validação empírica.


> **REGRA:** Regra de ouro: dar às IAs liberdade suficiente para nos surpreender, mas nunca liberdade suficiente para destruir nossa capacidade de estudar o que fizeram.


## 19. Donor Autopsy — metodologia


Um donor nunca entra porque parece moderno ou popular. Ele entra para responder uma lacuna concreta. Cada autópsia deve separar CONFIRMED, PLAUSIBLE/NEEDS VERIFICATION, DESIGN_HYPOTHESIS e REJECT.


```text
GAP NOSSO
  ↓
DONOR CANDIDATE
  ↓
MECANISMO REAL
  ↓
EVIDÊNCIA
  ↓
COMPATIBILIDADE + RISCO
  ↓
KEEP / ADOPT-CONCEPT / ADAPT / DEPEND / REJECT
```


### 19.1 Principais doadores atuais


|Doador|Mecanismo|Uso|
|---|---|---|

|DCI|atos epistêmicos, tensions, bounded closure, minority/reopen|DeliberationContract, TensionRecord, closure de rodada|

|POPPER|falsificação sequencial e desenho de teste|TestContract / READY_TO_TEST para claims elegíveis|

|Magentic-One|task/progress ledgers, stall → replan|Progress Monitor / Termination Controller|

|ArbiterOS|instruction binding, static + runtime validation|Contratos e fronteira probabilístico→determinístico|

|C-K Theory|espaço conceito/conhecimento problema/solução|Discovery/bootstrap como projection|

|ChatDev/Puppeteer|orquestração dinâmica e custo|futuro Topology/Team policy|

|AgentVerse|recrutamento dinâmico|Team Composer|

|MetaGPT|SOP + artefatos obrigatórios|Contract Builder|

|AFlow|busca MCTS de workflows tipados|futuro workflow search|

|GPTSwarm|grafos e otimização de nós/arestas|futura otimização de topologia|

|hdri|gap-driven reinvestigation|Gap Detector|

|TRIZ/AutoTRIZ|operadores de contradição|plugin de Discovery, não kernel|


## 20. O que deliberadamente NÃO faremos no início

- Não usar RL no DCE v0.1.

- Não aprender topologia antes de ter traces.

- Não usar score de confiança universal.

- Não usar e-values para toda evidência.

- Não assumir multiagente como default.

- Não copiar taxonomias de donors integralmente.

- Não transformar C-K ou TRIZ em ontologia universal.

- Não usar quantidade fixa de rodadas como critério epistemológico.

- Não confundir fechamento de sessão com READY_TO_TEST.

- Não construir dashboard antes de provar o motor.


## 21. Relação com o FioOS


Idea Evolution Engine e FioOS permanecem projetos separados. O Idea Engine governa epistemologia e deliberação. O FioOS, futuramente, pode governar execução de modelos, ferramentas, budgets, sandboxes, identidade, leases e auditoria.


```text
IDEA ENGINE
“o que investigar, por quê, com quem e o que significa?”
        ↓ Investigation Request
FioOS
“como executar sob autoridade, custo, isolamento e auditoria?”
        ↓ Observation / Evidence
IDEA ENGINE
“como isso altera o estado epistêmico?”
```


> **REGRA:** O FioOS nunca decide que uma claim é verdadeira. O Idea Engine nunca deve virar responsável por shell, credenciais, leases ou sandbox.


## 22. A estratégia de construção — começo, meio e fim do projeto


### 22.1 Fase 0 — Fundação documental

- Congelar visão e constituição intelectual.

- Criar AI-START-HERE.md e SOURCE-OF-TRUTH.md.

- Criar schemas/specs sem LLM.

- Registrar donor synthesis e research map.


### 22.2 Fase 1 — MVP simples: automatizar o fluxo manual atual


Primeiro objetivo prático: automatizar o que hoje é feito copiando respostas entre modelos.


```text
Idea → UNDERSTAND → ATTACK → ALTERNATIVES → REALITY CHECK → SYNTHESIZE → FINAL REVIEW
```


Cada etapa recebe Context Pack, missão precisa e output estruturado. O orquestrador usa regras simples. Sem RL. Sem FioOS obrigatório. Sem interface sofisticada.


### 22.3 Fase 2 — IdeaGenome e Validator reais

- IdeaGenome schema

- GenomePatch schema

- TransitionEvent

- atomic patch applier

- authority context

- tests adversariais


### 22.4 Fase 3 — DCE heurístico

- bootstrap mode

- decisional mode

- gap detector

- promotion gate

- 3–5 topologias fixas

- contract-relative progress

- replan before stalled


### 22.5 Fase 4 — Piloto científico


Comparar A: single agent; B: single model/multiple roles; C: multi-model/multiple roles. Mesmo orçamento e mesmas ferramentas. Medir progresso decisório, evidence quality, independence, test quality, redundancy e custo.


### 22.6 Fase 5 — Integração opcional com FioOS


Substituir DirectRunner por FioOSRunner quando houver benefício claro de governança e execução auditável.


### 22.7 Fase 6 — Aprendizado de política


Somente depois de acumular traces: state_before, strategy, team, topology, cost, artifacts, delta, state_after, outcome. Então estudar policy learning, AFlow-like workflow search ou Puppeteer-like orchestration.


## 23. Organização ideal do repositório


```text
idea-evolution/
├── AI-START-HERE.md
├── README.md
├── AGENTS.md
├── pyproject.toml
├── docs/
│   ├── INDEX.md
│   ├── SOURCE-OF-TRUTH.md
│   ├── CURRENT-STATE.md
│   ├── TARGET-ARCHITECTURE.md
│   ├── GOVERNANCE-INVARIANTS.md
│   ├── DECISIONS-LEDGER.md
│   ├── ACTIVE-QUEUE.md
│   ├── CODE-MAP.md
│   ├── TEST-MAP.md
│   ├── research/
│   │   ├── IDEATION-SCIENCE-MAP.md
│   │   ├── DONOR-SYNTHESIS.md
│   │   └── donors/
│   └── specs/
│       ├── IDEA-GENOME-v0.1.md
│       ├── GENOME-PATCH-v0.1.md
│       ├── DELIBERATION-CONTRACT-v0.1.md
│       ├── BOOTSTRAP-EXIT-POLICY-v0.1.md
│       ├── DECISION-RELEVANCE-POLICY-v0.1.md
│       └── READY-TO-TEST-POLICY-v0.1.md
├── schemas/
│   ├── idea-genome.v0.1.schema.json
│   ├── genome-patch.v0.1.schema.json
│   ├── transition-event.v0.1.schema.json
│   ├── uncertainty-record.v0.1.schema.json
│   ├── decision-relevance-report.v0.1.schema.json
│   ├── decision-delta.v0.1.schema.json
│   ├── tension-record.v0.1.schema.json
│   ├── gap-record.v0.1.schema.json
│   └── test-contract.v0.1.schema.json
├── src/idea_evolution/
│   ├── genome/
│   ├── validation/
│   ├── assessment/
│   ├── planning/
│   ├── deliberation/
│   ├── workflow/
│   ├── evidence/
│   ├── runners/
│   │   ├── direct.py
│   │   └── fioos.py
│   └── cli/
├── experiments/
│   ├── protocols/
│   ├── fixtures/
│   ├── runs/
│   └── analyses/
├── tests/
│   ├── unit/
│   ├── invariants/
│   ├── adversarial/
│   └── integration/
└── archive/
```


## 24. Hierarquia de fonte de verdade para qualquer IA


Qualquer IA que entre no projeto deve saber o que ler e em que ordem. Isso evita decisões baseadas em conversa antiga ou documentação ultrapassada.

1. AI-START-HERE.md — entrada obrigatória e curta.

2. docs/SOURCE-OF-TRUTH.md — hierarquia de autoridade documental.

3. docs/CURRENT-STATE.md — o que existe de fato hoje.

4. docs/GOVERNANCE-INVARIANTS.md — o que não pode ser violado.

5. docs/ACTIVE-QUEUE.md — trabalho atual e próximo passo.

6. docs/specs/ — contratos congelados/versionados.

7. Código e testes — realidade implementada.

8. DECISIONS-LEDGER.md — por que decisões foram tomadas.

9. Research/donor docs — candidatos e hipóteses; nunca confundir com estado implementado.


> **REGRA:** Uma IA nunca deve inferir que algo existe em código apenas porque aparece em TARGET-ARCHITECTURE ou research.


## 25. Conteúdo mínimo de AI-START-HERE.md


```text
1. What this project is
2. What it is NOT
3. Current phase
4. Read order
5. Constitutional invariants
6. Current architecture
7. Current blockers
8. Active task
9. How to propose changes
10. What must never be assumed
11. How to report evidence
12. Where experimental/research material lives
```


O arquivo deve ser curto o suficiente para caber no contexto default de qualquer agente, mas apontar para documentos profundos conforme necessidade. Economia de contexto por roteamento, não por amputação.


## 26. AGENTS.md — regras para qualquer IA que trabalhe no repositório

- Leia AI-START-HERE.md antes de agir.

- Não implemente TARGET como se fosse CURRENT.

- Não altere invariantes constitucionais sem registrar decisão explícita.

- Não invente autoridade; execution context é externo à saída do modelo.

- LLM output é proposta, não mutação.

- Antes de criar dependência, faça donor/gap check.

- Prefira código determinístico para validações mecânicas.

- Toda alegação de melhoria precisa de baseline e teste.

- Preserve reversibilidade e histórico.

- Falha ou inconclusão devem ser registradas honestamente.

- Não esconder divergências em sínteses.

- Não expandir escopo sem vínculo com ACTIVE-QUEUE.


## 27. Convenção de status epistemológico para documentos


Toda pesquisa e autópsia deve marcar afirmações para evitar que inferências virem fatos por repetição.


```text
CONFIRMED          — explicitamente sustentado por fonte/execução
PLAUSIBLE           — coerente, mas precisa verificação
BORROWED_MODEL      — modelo externo adaptado
DESIGN_HYPOTHESIS   — proposta nossa para testar
SPECULATION         — possibilidade ainda aberta
REJECTED            — não adotar / refutada no contexto atual
```


## 28. Estratégia de contexto para IAs


Não entregar o repositório inteiro a cada agente. Cada tarefa recebe um Context Pack mínimo suficiente: intenção, estado atual, invariantes relevantes, artefatos-alvo, evidência necessária e saída esperada. Deep context continua disponível por links internos.


> **REGRA:** Minimum sufficient context = menor contexto que ainda permite a decisão correta. Economizar tokens por roteamento, não apagando conhecimento.


## 29. Primeiro MVP executável


O primeiro MVP não precisa implementar toda a teoria. Ele deve automatizar o fluxo manual que motivou o projeto.


```text
1. Usuário escreve ideia
2. UNDERSTAND model cria estado estruturado
3. ATTACK model procura falhas
4. ALTERNATIVE model reconstrói opções
5. REALITY_CHECK identifica o que depende do mundo
6. SYNTHESIZER produz nova versão
7. FINAL REVIEW procura issue material restante
8. Gatilho: REFINED_IDEA_READY ou CONTINUE/RECONSTRUCT
```


Cada etapa recebe um Context Pack e retorna JSON estruturado. A primeira versão pode usar regras fixas e dois ou três provedores. O objetivo é eliminar a orquestração manual e medir se o resultado melhora com direção explícita.


## 30. Critério de sucesso do primeiro protótipo


O protótipo inicial é bem-sucedido se, em comparação ao fluxo manual ou a um único modelo, conseguir preservar a intenção, reduzir repetição, produzir estrutura rastreável, expor mais falhas materiais, terminar com próximo passo claro e fazê-lo com custo aceitável.


Ele não precisa provar uma teoria universal de criatividade. Precisa provar que a condução estruturada é útil.


## 31. Riscos centrais que devem permanecer visíveis


|Risco|Proteção|
|---|---|

|Consenso artificial|funções adversariais, tension records, independência de evidência|

|Burocracia epistêmica|artefatos mínimos, promotion gate, contract-relative progress|

|Bootstrap infinito|exit policy, saturation, budget|

|Deliberação infinita|progress monitor, replan, reality over deliberation|

|Protected core virar dogma|core pressure report + decisão humana|

|LLM julgando LLM|calibração, múltiplas fontes, realidade externa|

|Precisão fictícia|categorias discretas, políticas explícitas, evitar scores arbitrários|

|Topologia sofisticada sem ganho|templates simples primeiro, traces antes de aprendizado|

|Multiagente caro|coordination_value e SINGLE_AGENT_MODE|

|Donor tourism|gap-driven donor autopsy|

|Confundir design com implementação|CURRENT/TARGET/RESEARCH separados|


## 32. A pergunta científica central


> **REGRA:** Dado um estado epistêmico de uma ideia humana, um sistema consegue selecionar adaptativamente a estratégia de investigação de maior valor — incluindo decidir entre agente único, deliberação estruturada ou teste do mundo real — e produzir maior progresso decisório por custo do que políticas fixas?


Essa formulação é mais forte do que “multiagentes são melhores”. O projeto deve estar preparado para descobrir que, em muitas situações, um único modelo forte é superior.


## 33. Onde queremos chegar


A experiência final pode começar com uma pergunta simples: “O que está na sua cabeça?”. A pessoa escreve uma ideia malformada. O sistema não responde “ótima ideia”; ele organiza a intenção, identifica claims, encontra lacunas, chama a estratégia apropriada, preserva tensões e decide quando o próximo conhecimento deve vir do mundo.


```text
Entrada:
“Eu pensei numa coisa... talvez fosse possível...”

Saída madura:
- intenção original
- essência preservada
- claims críticas
- evidências
- tensões
- alternativas
- riscos
- decisões humanas
- incertezas restantes
- próximo teste discriminativo
- condições de reabertura
```


## 34. Próximo passo recomendado a partir deste documento


Não começar pelo produto visual. Criar o repositório separado e materializar primeiro a continuidade documental e os contratos mínimos.

1. Criar estrutura do repositório.

2. Criar AI-START-HERE.md, SOURCE-OF-TRUTH.md, CURRENT-STATE.md e GOVERNANCE-INVARIANTS.md a partir deste documento.

3. Congelar DeliberationContract v0.1 e BootstrapExitPolicy v0.1.

4. Formalizar UncertaintyRecord, DecisionRelevanceReport e DecisionDelta.

5. Formalizar IdeaGenome/GenomePatch apenas com campos realmente necessários ao MVP.

6. Implementar validators determinísticos e testes adversariais.

7. Construir DirectRunner e o fluxo simples UNDERSTAND → ATTACK → ALTERNATIVES → REALITY_CHECK → SYNTHESIZE.

8. Executar piloto pequeno antes de ampliar arquitetura.


## 35. Declaração final


> **REGRA:** A IA não recebe a missão de “melhorar” uma ideia. Ela recebe a missão de ajudar o humano a descobrir o que precisa ser verdade, o que ainda é incerto e qual próximo passo merece existir.


A ambição completa pode levar anos para amadurecer; a hipótese central pode e deve ser testada cedo com um protótipo pequeno. A estratégia do projeto é construir uma constituição determinística primeiro, automatizar o fluxo manual real em seguida, medir o ganho e só então aumentar autonomia, diversidade de modelos e inteligência de orquestração.
