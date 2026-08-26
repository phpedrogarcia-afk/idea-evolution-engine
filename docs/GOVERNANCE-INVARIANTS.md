# GOVERNANCE-INVARIANTS.md — Constituição Intelectual e Invariantes do IEE

> **ESTE DOCUMENTO É A CONSTITUIÇÃO SUPREMA DO PROJETO.**
> Nenhuma funcionalidade, otimização, IA ou proposta arquitetural pode violar estas invariantes.

---

## 1. Princípios Constitucionais Inegociáveis

### 1.1 Progress Over Prose
> **Texto adicional não é progresso.**
- Resumos maiores, paráfrases estilísticas, reformulações retóricas e expansão de verbosidade não contam como progresso epistêmico.
- Progresso real exige: nova claim falsificável, evidência independente, premissa oculta exposta, tensão tipada identificada, redução de incerteza decisiva, alternativa materializada ou teste empírico desenhado.

### 1.2 Capability != Authority (Soberania Humana)
> **Capacidade cognitiva não confere autoridade normativa.**
- Um LLM mais inteligente ou potente não ganha poder sobre a intenção, valores, escopo essencial ou decisões soberanas do criador humano.
- A autoridade humana é exclusiva sobre: propósito essencial da ideia, *Protected Cores*, julgamentos normativos/morais, pivots fundamentais e encerramento/arquivamento.
- *Protected Cores* são protegidos contra alteração automática por IA, mas nunca contra crítica adversarial.

### 1.3 Memory != Evidence
> **Histórico de conversa não é evidência; inferência de modelo não é fato.**
- O fato de uma IA ter afirmado algo em uma rodada anterior não transforma a afirmação em verdade.
- Toda evidência no `evidence_registry` deve conter proveniência, tipo estrito (`FACT`, `OBSERVATION`, `HYPOTHESIS`, `INTERPRETATION`, `MODEL_INFERENCE`, `HUMAN_INPUT`, `EXPERIMENT_RESULT`) e avaliação de independência. Quantidade de modelos concordando não implica independência estatística ou factual.

### 1.4 Reality Over Deliberation (READY_TO_TEST)
> **Quando o próximo conhecimento de maior valor deve vir da realidade, a deliberação cessa.**
- A deliberação por IA possui retornos decrescentes rápidos. `READY_TO_TEST` ocorre quando existe um teste no mundo real capaz de discriminar entre hipóteses rivais a custo inferior ou com valor epistemológico superior ao de continuar a discussão abstrata.

### 1.5 Conversa Não É Processo (DeliberationContract)
> **Nenhuma investigação por IA ocorre sem um contrato formal prévio.**
- Cada rodada de deliberação deve declarar antes de começar: objetivo investigativo, claims-alvo, operação epistemológica, participantes, topologia, artefatos esperados, critérios determinísticos de progresso, orçamento e condições de parada.
- O que conta como progresso é julgado pelo contrato prévio, impedindo o *moving goalposts* a posteriori.

### 1.6 Inteligência Propõe; Kernel Valida (GenomePatch)
> **Nenhum LLM escreve diretamente no estado canônico da ideia.**
- Todo output de IA é transformado em uma proposta atômica (`GenomePatch`).
- O `GenomeValidator` (código 100% determinístico) valida schema, integridade referencial, autoridade de segurança, invariantes constitucionais e transições válidas de estado. Se qualquer teste falhar, o patch é descartado integralmente e o estado permanece idêntico (*all-or-nothing*).

### 1.7 Multi-Agent is Not Default
> **Não assumir que múltiplos agentes superam um único agente.**
- Múltiplos agentes introduzem overhead de coordenação, amplificação de viés e custos exponenciais. O DCE deve calcular o `coordination_value`. Se baixo, a tarefa deve rodar estritamente em `SINGLE_AGENT_MODE`.

### 1.8 Preservação de Tensões e Não-Obrigação de Consenso
> **Tensões epistêmicas e contradições nunca devem ser "alisadas" ou silenciadas por síntese forçada.**
- Se dois modelos ou evidências divergirem fundamentalmente, o sistema registra um `TensionRecord` estruturado e preserva a divergência para investigação ou decisão humana.

---

## 2. Invariantes Técnicas e de Dados

| ID | Invariante | Descrição |
| :--- | :--- | :--- |
| **INV-01** | **Imutabilidade de Versão** | Uma versão do `IdeaGenome` ($v_N$) é estritamente imutável após commit. Qualquer alteração gera $v_{N+1}$ com ponteiro para o ancestral e hash criptográfico. |
| **INV-02** | **Atomicidade de Patches** | Um `GenomePatch` é aplicado totalmente ou rejeitado totalmente. Não existem mutações parciais. |
| **INV-03** | **Rastreabilidade de Proveniência** | Nenhuma claim, evidência, premissa ou tensão pode existir sem metadados de proveniência (`created_by`, `round_id`, `policy_version`, `timestamp`). |
| **INV-04** | **Separação Estado vs Avaliação** | O genoma persiste apenas o grafo epistemológico factual e histórico. Métricas derivadas (entropia, readiness score, prioridade) são calculadas em tempo de execução e não corrompem o estado imutável. |
| **INV-05** | **Prevenção de Mutação Concorrente** | Um patch deve declarar `base_version`. Se o genoma estiver em versão diferente da base declarada, a aplicação é rejeitada por conflito. |
| **INV-06** | **Separação Epistemológica de Claims** | O status de veracidade de uma claim (`UNTESTED`, `SUPPORTED`, `REFUTED`, `UNCERTAIN`) jamais pode ser misturado com seu ciclo de vida no projeto (`ACTIVE`, `SUPERSEDED`, `DEPRECATED`). |
| **INV-07** | **Autoridade Externa ao Payload** | O campo `"actor"` ou declaração de quem é o usuário em JSON não confere autoridade. O validador deve receber um `ExecutionContext` externo e confiável. |
| **INV-08** | **Preservação de Histórico em Branches** | Um pivot ou divergência gera uma nova branch no grafo de linhagem. A linhagem original nunca é sobrescrita ou destruída. |
