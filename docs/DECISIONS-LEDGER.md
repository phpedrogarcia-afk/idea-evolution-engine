# DECISIONS-LEDGER.md — Registro Imutável de Decisões de Arquitetura

> Este documento registra formalmente todas as decisões arquiteturais, epistemológicas e metodológicas tomadas no **Idea Evolution Engine (IEE)**. Nenhuma decisão antiga é apagada; decisões superadas recebem o status `SUPERSEDED` com a justificativa registrada.

---

## Índice de Decisões
- [ADR-001: Separação Estrita de Fases e Proibição de Código Prematuro](#adr-001)
- [ADR-002: IdeaGenome como Grafo Versionado Imutável em vez de Chat Log](#adr-002)
- [ADR-003: Validação Determinística do Kernel e Mutação Exclusiva via GenomePatch](#adr-003)
- [ADR-004: Soberania Humana Irrestrita e Governança de Protected Cores](#adr-004)
- [ADR-005: Deliberação Baseada em Contratos Formais Pré-Execução](#adr-005)
- [ADR-006: Multiagente Não-Default e Avaliação de Coordination Value](#adr-006)
- [ADR-007: Separação Rígida entre Idea Evolution Engine e FioOS](#adr-007)
- [ADR-008: Adoção de Doadores Orientada a Gaps Receptores](#adr-008)
- [ADR-009: READY_TO_TEST como Veredito de Próxima Fonte de Conhecimento](#adr-009)
- [ADR-010: Separação entre Regimes de Bootstrap e Investigação Decisional](#adr-010)
- [ADR-011: Sistema de Continuidade Cognitiva, Checkpoints e Validação Determinística](#adr-011)
- [ADR-012: Proibição de Missões de Fundação por Inércia e Transição Obrigatória para o MVP](#adr-012)

---

### <a id="adr-001"></a> ADR-001: Separação Estrita de Fases e Proibição de Código Prematuro
- **Data:** 2026-08-26
- **Status:** `ACCEPTED`
- **Contexto:** Desenvolvedores e IAs tendem a começar projetos criando classes, interfaces de usuário, dashboards e agentes LLM antes de definir contratos epistêmicos, gerando desperdício e dívida arquitetural massiva.
- **Decisão:** O desenvolvimento do IEE deve seguir estritamente o pipeline: `UNDERSTAND` $\to$ `FORMALIZE` $\to$ `VALIDATE` $\to$ `SIMULATE` $\to$ `PROTOTYPE` $\to$ `MEASURE` $\to$ `SCALE`. A Fase 0 é estritamente documental/constitucional; a Fase 1 conterá apenas schemas e validação determinística sem LLMs.
- **Consequências:** Zero código de produto ou dependências de frameworks multiagente na fase atual.

---

### <a id="adr-002"></a> ADR-002: IdeaGenome como Grafo Versionado Imutável em vez de Chat Log
- **Data:** 2026-08-26
- **Status:** `ACCEPTED`
- **Contexto:** Tratar o histórico de conversas como a memória da ideia resulta em perda de contexto, alucinações cumulativas e impossibilidade de auditoria científica.
- **Decisão:** A memória canônica da ideia é o `IdeaGenome`, um objeto estruturado e imutável que persiste claims, relações, premissas, evidências, tensões e decisões em versões encadeadas ($v_N \to v_{N+1}$).
- **Consequências:** Toda mutação gera uma nova versão auditável; o histórico de chat torna-se efêmero.

---

### <a id="adr-003"></a> ADR-003: Validação Determinística do Kernel e Mutação Exclusiva via GenomePatch
- **Data:** 2026-08-26
- **Status:** `ACCEPTED`
- **Contexto:** Permitir que LLMs modifiquem o estado de forma não-estruturada viola integridade de dados e segurança.
- **Decisão:** LLMs propõem `GenomePatch` atômicos. O `GenomeValidator` (código Python puro, determinístico) valida 5 camadas (Schema, Referência, Autoridade, Invariantes e Transição de Estado) em regime *all-or-nothing*.
- **Consequências:** Falhas de validação não corrompem o estado; garantia de consistência formal.

---

### <a id="adr-004"></a> ADR-004: Soberania Humana Irrestrita e Governança de Protected Cores
- **Data:** 2026-08-26
- **Status:** `ACCEPTED`
- **Contexto:** Sistemas de IA podem "otimizar" uma ideia alterando sorrateiramente a intenção do criador humano.
- **Decisão:** `Capability != Authority`. O humano detém autoridade exclusiva sobre a intenção, valores e `Protected Cores`. O sistema pode criticar e registrar `CorePressureReport`, mas nunca alterar o núcleo sem intervenção humana explícita.
- **Consequências:** Preserva a soberania humana e impede que a IA faça pivots não-autorizados.

---

### <a id="adr-005"></a> ADR-005: Deliberação Baseada em Contratos Formais Pré-Execução
- **Data:** 2026-08-26
- **Status:** `ACCEPTED`
- **Contexto:** Conversas abertas entre IAs geram prolixidade (*prose over progress*) e *moving goalposts*.
- **Decisão:** Toda rodada de deliberação deve operar sob um `DeliberationContract` que estabelece antecipadamente target claims, operação epistêmica, atos permitidos, critérios determinísticos de progresso, orçamento e condições de parada.
- **Consequências:** O progresso passa a ser avaliado em relação ao contrato, eliminando falsa percepção de avanço.

---

### <a id="adr-006"></a> ADR-006: Multiagente Não-Default e Avaliação de Coordination Value
- **Data:** 2026-08-26
- **Status:** `ACCEPTED`
- **Contexto:** Autópsias do framework DCI evidenciam que deliberações multiagente aumentam exponencialmente custos e ruído sem garantir superioridade a um agente único competente.
- **Decisão:** O Deliberation Control Engine (DCE) deve computar `coordination_value`. Se baixo, a execução utiliza `SINGLE_AGENT_MODE`. Multiagente é ativado apenas sob alto valor de coordenação e desacordo estruturado.
- **Consequências:** Eficiência de custos e eliminação de orquestrações ornamentais desnecessárias.

---

### <a id="adr-007"></a> ADR-007: Separação Rígida entre Idea Evolution Engine e FioOS
- **Data:** 2026-08-26
- **Status:** `ACCEPTED`
- **Contexto:** Risco de acoplamento do motor de deliberação epistêmica com a infraestrutura de baixo nível do FioOS.
- **Decisão:** O IEE governa *o que investigar, por que investigar e o significado epistêmico dos achados*. O FioOS (em fases futuras) atua apenas como gateway de execução (sandbox, leases, ferramentas e segurança). O IEE deve ser capaz de rodar autonomamente com executores locais (*DirectRunner*).
- **Consequências:** Desacoplamento arquitetural e portabilidade total do IEE.

---

### <a id="adr-008"></a> ADR-008: Adoção de Doadores Orientada a Gaps Receptores
- **Data:** 2026-08-26
- **Status:** `ACCEPTED`
- **Contexto:** Risco de "turismo tecnológico", adotando frameworks externos (DCI, POPPER, MetaGPT, TRIZ, C-K) de forma indiscriminada.
- **Decisão:** Nenhum mecanismo externo entra no IEE sem uma lacuna receptora explícita e compatibilidade comprovada pelo método de *Donor Autopsy*.
- **Consequências:** Apenas mecanismos essenciais são transplantados (ex: atos epistêmicos do DCI, teste discriminativo do POPPER, ledger do Magentic-One).

---

### <a id="adr-009"></a> ADR-009: READY_TO_TEST como Veredito de Próxima Fonte de Conhecimento
- **Data:** 2026-08-26
- **Status:** `ACCEPTED`
- **Contexto:** Confundir o encerramento da deliberação com "ideia perfeita" ou "ideia aprovada".
- **Decisão:** `READY_TO_TEST` declara estritamente que a deliberação por IA esgotou seu retorno e que o próximo conhecimento de maior valor deve vir de um teste empírico no mundo real via `TestContract`.
- **Consequências:** O sistema é um motor de investigação contínuo e cíclico, não uma esteira de aprovação estática.

---

### <a id="adr-010"></a> ADR-010: Separação entre Regimes de Bootstrap e Investigação Decisional
- **Data:** 2026-08-26
- **Status:** `ACCEPTED`
- **Contexto:** Exigir relevância decisória rigorosa de uma ideia recém-chegada gera estagnação, pois a ideia ainda não possui forma.
- **Decisão:** Uma ideia recém-chegada entra em `STRUCTURE_BOOTSTRAP` com objetivo de maximizar `StructureGain` (claims, relations, assumptions). Somente após atender deterministicamente à `BootstrapExitPolicy` ela migra para `DECISIONAL_INVESTIGATION`.
- **Consequências:** Genomas esparsos são tratados como um regime cognitivo natural, não como erro ou deficiência.

---

### <a id="adr-011"></a> ADR-011: Sistema de Continuidade Cognitiva, Checkpoints e Validação Determinística
- **Data:** 2026-08-26
- **Status:** `ACCEPTED`
- **Contexto:** Risco de perda de contexto e desvio de objetivos durante trocas de agentes ou sessões interrompidas.
- **Decisão:** Criar a infraestrutura de continuidade em `docs/context/` com manifesto machine-readable (`context-manifest.json`), checkpoints imutáveis (`CP-YYYYMMDD-NNN`), regras de *Fail-Closed on Canonical Conflict* e scripts determinísticos de validação (`tools/context/validate_context.py`).
- **Consequências:** Qualquer nova IA recupera o estado operacional exato em segundos sem depender de histórico de chat.

---

### <a id="adr-012"></a> ADR-012: Proibição de Missões de Fundação por Inércia e Transição Obrigatória para o MVP
- **Data:** 2026-08-26
- **Status:** `ACCEPTED`
- **Contexto:** Risco de "paralisia por fundação", acumulando dezenas de documentos teóricos sem nunca testar o produto na prática.
- **Decisão:** Aplicar o princípio *Reality Over Deliberation* ao próprio projeto (Meta-Ready-To-Test). A Fundação 03 encerra o ciclo de fundação prévia. Nenhuma nova missão de fundação (ex: Foundation 04) pode ser criada por inércia; a próxima missão autorizada deve ser a implementação do *Simple Idea Evolution Loop MVP*. Uma nova fundação só poderá existir se for detectado um bloqueador empírico concreto durante a construção e houver autorização humana expressa.
- **Consequências:** Encerramento definitivo da fase pré-código e foco estrito na validação experimental do primeiro produto.
