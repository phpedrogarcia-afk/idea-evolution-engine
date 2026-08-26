# docs/context/OPEN-QUESTIONS.md — Registro Canônico de Perguntas e Incertezas Abertas

> **CASA CANÔNICA DE TODAS AS QUESTÕES EM ABERTO NO IDEA EVOLUTION ENGINE.**
> Nenhuma dúvida ou lacuna deve existir apenas em conversas ou notas dispersas.

---

### [OQ-001] Métrica Determinística de Saturação Semântica no Bootstrap
- **Question:** Como detectar com 100% de confiabilidade determinística que o bootstrap de uma ideia atingiu saturação sem depender de notas subjetivas dadas por outro LLM?
- **Why It Matters:** Evita loops infinitos de reformulação prolixa (*prose over progress*) e gastos desnecessários de compute.
- **Type:** `EPISTEMIC_ALGORITHMIC`
- **Status:** `OPEN`
- **Blocks What:** Otimização fina da `BootstrapExitPolicy` na Fase 2+.
- **Owner / Function:** DCE / ProgressMonitor
- **Related Decisions:** [ADR-005](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-005), [ADR-010](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-010)
- **Related Research:** [`docs/research/donors/MAGENTIC-ONE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/research/donors/MAGENTIC-ONE.md)
- **Next Investigation:** Testar heurística de sobreposição de n-gramas e embeddings de premissas nas fixtures do experimento EXP-001.

---

### [OQ-002] Extensão do Falsificacionismo Popperiano para Claims Subjetivas e de Mercado
- **Question:** Como estruturar o `TestContract` e as implicações mensuráveis para hipóteses de comportamento humano, desejo de usuário ou proposições normativas sem gerar pseudociência?
- **Why It Matters:** Nem toda claim é física ou estatisticamente pura como no POPPER original; o IEE lida com produtos e ideias humanas.
- **Type:** `METHODOLOGICAL`
- **Status:** `OPEN`
- **Blocks What:** Especificação avançada do `TestContract` na Fase 3.
- **Owner / Function:** DCE / TerminationController
- **Related Decisions:** [ADR-009](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-009)
- **Related Research:** [`docs/research/donors/POPPER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/research/donors/POPPER.md)
- **Next Investigation:** Mapear oráculos empíricos para 3 classes: *Willingness-to-pay*, *Usabilidade/Adesão* e *Viabilidade Técnica*.

---

### [OQ-003] Limiares Práticos de Ativação do Modo Multiagente (Coordination Value)
- **Question:** Qual é a função de corte exata onde o overhead de coordenação multiagente compensa financeiramente e epistemologicamente frente a um único agente forte?
- **Why It Matters:** Evita o desperdício massivo observado no framework DCI.
- **Type:** `EMPIRICAL_BENCHMARK`
- **Status:** `OPEN`
- **Blocks What:** `TeamComposer` adaptativo (Fase 4+).
- **Owner / Function:** DCE / TeamComposer
- **Related Decisions:** [ADR-006](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-006)
- **Related Research:** [`docs/research/donors/DCI.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/research/donors/DCI.md), [`docs/research/donors/AGENTVERSE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/research/donors/AGENTVERSE.md)
- **Next Investigation:** Executar o experimento EXP-002 comparando diretamente Single-Model vs Multi-Model.

---

### [OQ-004] Renderização Gráfica da Projeção C-K sem Poluição Ontológica
- **Question:** Como renderizar visualmente o mapa de ideação C-K em interfaces futuras sem que a teoria se torne uma restrição rígida na estrutura do `IdeaGenome`?
- **Why It Matters:** Preserva a agilidade do grafo de claims enquanto oferece uma visualização intuitiva para criadores humanos.
- **Type:** `INTERFACE_ARCHITECTURAL`
- **Status:** `OPEN`
- **Blocks What:** UI / Visualizador de Genoma (Fase 5+).
- **Owner / Function:** Frontend / Visualizer
- **Related Decisions:** [ADR-002](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-002), [ADR-008](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-008)
- **Related Research:** [`docs/research/donors/CK-THEORY.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/research/donors/CK-THEORY.md)
- **Next Investigation:** Projetar um algoritmo derivado que mapeia nós de `claims` e `evidence` nos 4 quadrantes (PC, PK, SC, SK) sob demanda.
