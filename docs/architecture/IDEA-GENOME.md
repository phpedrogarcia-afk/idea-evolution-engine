# IDEA-GENOME.md — A Memória Epistêmica Estruturada

> **STATUS: TARGET / DESIGN_HYPOTHESIS**

---

## 1. Conceito Central
O **IdeaGenome** é o objeto de estado persistente, versionado e imutável que representa o conhecimento acumulado sobre uma ideia. Ele substitui a dependência de janelas de contexto efêmeras por uma estrutura de dados formal.

Cada mutação gera uma nova versão imutável ($v_N \to v_{N+1}$), preservando o histórico de linhagem e auditoria.

---

## 2. Anatomia Estrutural do IdeaGenome

```text
IdeaGenome
├── identity: UUID, version (v1..vN), parent_version, content_hash, created_at
├── essence:
│   ├── human_origin: Descrição original da centelha humana
│   ├── purpose: O objetivo fundamental que a ideia pretende atingir
│   └── protected_cores: Lista de restrições invioláveis pelo sistema
├── problem_space:
│   ├── problem_statement: Definição clara da dor ou necessidade
│   ├── affected_actors: Quem sofre o problema
│   ├── context_bounds: Limites do domínio de aplicação
│   └── existing_alternatives: Como o problema é resolvido hoje
├── claims: Lista de afirmações declarativas (unidade mínima de investigação)
│   └── Claim: id, text, status (UNTESTED/SUPPORTED/REFUTED/UNCERTAIN), lifecycle (ACTIVE/SUPERSEDED/DEPRECATED)
├── claim_relations: Arestas do grafo (depends_on, supports, weakens, contradicts, supersedes)
├── evidence_registry: Lista de evidências com proveniência e tipagem
├── assumptions: Premissas tácitas identificadas
├── constraints: Restrições de contorno (físicas, técnicas, éticas, regulatórias)
├── frames: Molduras conceituais e perspectivas de interpretação
├── open_questions: Perguntas levantadas não investigadas
├── uncertainties: Incertezas promovidas com avaliação de relevância
├── tensions: Conflitos não resolvidos (TensionRecord)
├── human_decisions: Registro formal de decisões soberanas tomadas
├── lineage: Árvore de versões, pivots e branches
├── deliberation_history: Registro de rodadas, contratos executados e deltas
└── workflow_state: Estado atual na máquina de estados (ex: STRUCTURE_BOOTSTRAP, UNDER_INVESTIGATION, READY_TO_TEST)
```

---

## 3. Separação entre Estado Persistido e Métricas Derivadas
Para evitar corrupção e viés cumulativo, o genoma distingue:
- **Estado Persistido (Factual/Histórico):** Claims, evidências, premissas, tensões, linhagem e decisões humanas.
- **Avaliações Derivadas (Calculadas em Runtime):** Entropia epistêmica, *Readiness Score*, prioridade de investigação, poder de compressão e relevância agregada.

Isso permite recalcular métricas sob novas políticas sem precisar alterar ou falsificar a história do genoma.
