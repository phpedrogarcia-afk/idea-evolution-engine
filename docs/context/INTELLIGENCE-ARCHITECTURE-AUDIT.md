# INTELLIGENCE-ARCHITECTURE-AUDIT.md — Auditoria da Arquitetura de Inteligência (Foundation v0.1)

> **Data:** 26 de agosto de 2026  
> **Status:** AUDIT COMPLETE / RECONCILIATION IN PROGRESS

---

## 1. Inventário e Classificação de Artefatos Existentes

| Arquivo | Classificação | Avaliação de Integridade / Papel |
| :--- | :---: | :--- |
| `AI-START-HERE.md` | `CANONICAL` | Ponto de entrada. Necessita ser mais enxuto e atuar primariamente como roteador de perfis de contexto. |
| `AGENTS.md` | `CANONICAL` | Regras operacionais para agentes. Deve focar estritamente em disciplina de sessão. |
| `README.md` | `SUPPORTING` | Apresentação para humanos. Precisa apontar diretamente para a arquitetura de contexto. |
| `docs/INDEX.md` | `CANONICAL` | Índice global. Deve refletir a nova pasta `docs/context/`. |
| `docs/SOURCE-OF-TRUTH.md` | `CANONICAL` | Hierarquia de autoridade. Precisa formalizar o princípio *Fail Closed on Conflict*. |
| `docs/CURRENT-STATE.md` | `CANONICAL` | Snapshot estático. Precisa virar instrumento operacional sincronizado com Git e checkpoints. |
| `docs/GOVERNANCE-INVARIANTS.md` | `CANONICAL` | Constituição do sistema. Precisa consagrar *State must survive the model*. |
| `docs/DECISIONS-LEDGER.md` | `CANONICAL` | Registro de ADRs. Precisa de campos estruturados completos (`rationale`, `tradeoffs`, etc.). |
| `docs/ACTIVE-QUEUE.md` | `CANONICAL` | Fila de trabalho. Deve explicitar o próximo alvo real (*Simple Idea Evolution Loop*). |
| `docs/TERMINOLOGY.md` | `CANONICAL` | Glossário canônico. Casa única para todas as definições conceituais. |
| `docs/FOUNDATION-AUDIT.md` | `HISTORICAL` | Auditoria da Fase 0 original. Preservado para rastreabilidade. |
| `docs/FOUNDATION-READINESS-REPORT.md` | `HISTORICAL` | Relatório de encerramento da Fase 0. |
| `docs/foundations/*` | `CANONICAL` | Fundamentos conceituais (Visão, Problema, Princípios, Antiobjetivos, Hipóteses). |
| `docs/architecture/*` | `TARGET` | Especificações da arquitetura de longo prazo (IdeaGenome, DCE, Patches, etc.). |
| `docs/research/*` | `RESEARCH` | Autópsias e hipóteses sobre sistemas doadores. |
| `docs/specs/*` | `CANONICAL` | Políticas versionadas v0.1 (Bootstrap Exit, ReadyToTest, Authority, Stall). |
| `docs/experiments/*` | `CANONICAL` | Protocolos e backlog de experimentos empíricos. |
| `IDEA-EVOLUTION-ENGINE-PROJETO-FUNDADOR-v0.1.md` | `HISTORICAL` | Documento fundador original preservado como ancestralidade histórica. |

---

## 2. Inconsistências, Riscos e Ambiguidade Detectados

### 2.1 Ambiguidade do Próximo Alvo de Produto (Roadmap Disconnect)
- **Problema:** Documentos fundadores descrevem o avançado DCE com 13 subcomponentes e topologias adaptativas, criando o risco de uma IA achar que deve construir o DCE completo imediatamente.
- **Correção:** Congelar a hierarquia:
  1. `FOUNDATION` = COMPLETE.
  2. `NEXT PRODUCT TARGET` = **Simple Idea Evolution Loop (MVP Heurístico)**: Ciclo direto *Understand $\to$ Attack $\to$ Alternatives $\to$ Reality Check $\to$ Synthesize $\to$ Review*.
  3. `ADVANCED GOVERNED ENGINE` = TARGET (Fases 2 e 3).
  4. `ADAPTIVE DCE / RL / FioOS` = FUTURE / RESEARCH (Fases 5 e 6).

### 2.2 Duplicação e Dispersão de Perguntas e Contradições
- **Problema:** Dúvidas em aberto e tensões identificadas estavam dispersas em múltiplos documentos (`RESEARCH-GAPS.md`, `DECISIONS-LEDGER.md`, `FOUNDATION-AUDIT.md`).
- **Correção:** Criar casas canônicas dedicadas em `docs/context/`:
  - `docs/context/OPEN-QUESTIONS.md` (Catálogo estruturado `OQ-XXX`).
  - `docs/context/CONTRADICTIONS.md` (Catálogo estruturado `CON-XXX`).

### 2.3 Ausência de Rastreamento de Estado Operacional e Checkpoints
- **Problema:** Não havia um mecanismo padronizado para salvar o estado de uma missão em andamento, identificar o último ponto seguro (*Last Known Good State*) ou retomar o trabalho após interrupção.
- **Correção:** Criação do **Checkpoint System** com manifest machine-readable (`context-manifest.json`), validação determinística via script e diretório `docs/context/checkpoints/`.

### 2.4 Riscos de Sobrecarga de Contexto (Context Cost)
- **Problema:** Uma nova IA precisaria ler dezenas de arquivos para iniciar uma tarefa simples.
- **Correção:** Criação dos **Perfis de Entrada de Contexto** (`FAST`, `DEEP`, `RESEARCH`, `IMPLEMENTATION`) e da **Continuity Capsule** (`CONTINUITY-CAPSULE.md`).

---

## 3. Decisões de Reconciliação Aprovadas
1. Criar a pasta `docs/context/` como centro nevrálgico da continuidade cognitiva.
2. Manter uma única casa canônica por conceito; outros documentos devem utilizar links markdown diretos.
3. Instituir validação determinística automática de integridade documental (`tools/context/validate_context.py`).
4. Instituir política estrita de *Fail-Closed on Canonical Conflict*.
