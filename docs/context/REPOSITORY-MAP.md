# docs/context/REPOSITORY-MAP.md — Mapa Topológico do Repositório

> **MAPA COMPLETO DE NAVEGAÇÃO ESTRUTURAL DO REPOSITÓRIO.**
> *Branch Principal:* `main` | *Remote Origin:* `https://github.com/phpedrogarcia-afk/idea-evolution-engine.git`

---

```text
idea-evolution-engine/
├── AI-START-HERE.md               # Ponto de entrada obrigatório e roteador para IAs
├── AGENTS.md                      # Regras operacionais para agentes e modelos
├── README.md                      # Apresentação do projeto para humanos
├── .gitignore                     # Configuração de arquivos ignorados pelo Git
│
├── src/                           # NÚCLEO EXECUTÁVEL DO PRODUTO (FASE 1)
│   └── idea_evolution/
│       ├── domain/                # SimpleIdeaState, RunStatus, CriticalIssue, AlternativeMechanism
│       ├── stages/                # Contratos Pydantic e 8 estágios cognitivos
│       ├── providers/             # Base, FakeModelRunner e NativeModelRunner
│       ├── orchestration/         # SimpleLoopRunner (Cond B & C) e BaselineRunner (Cond A)
│       ├── tracing/               # RunTracer e persistência estruturada em runs/
│       └── cli/                   # CLI unificada (iee evolve, compare, inspect-run)
│
├── prompts/                       # PROMPTS COGNITIVOS VERSIONADOS (v0.1)
│   ├── understand_v0_1.md
│   ├── attack_v0_1.md
│   ├── critique_logical_v0_1.md
│   ├── critique_feasibility_v0_1.md
│   ├── revision_v0_1.md
│   ├── alternatives_v0_1.md
│   ├── reality_check_v0_1.md
│   ├── synthesize_v0_1.md
│   ├── final_review_v0_1.md
│   └── baseline_refine_v0_1.md
│
├── fixtures/                      # FIXTURES PADRONIZADAS DE TESTE
│   ├── fixture_01_software_app.json
│   ├── fixture_02_physical_product.json
│   └── fixture_03_business_service.json
│
├── experiments/                   # EXPERIMENTAÇÃO CONTROLADA
│   └── MISSION-04/
│       └── comparison-packet.md   # Pacote de avaliação cega A/B/C
│
├── docs/
│   ├── INDEX.md                   # Índice mestre da documentação
│   ├── SOURCE-OF-TRUTH.md         # Hierarquia de autoridade e precedência
│   ├── CURRENT-STATE.md           # Declaração do estado real físico
│   ├── GOVERNANCE-INVARIANTS.md   # Constituição intelectual do projeto
│   ├── DECISIONS-LEDGER.md        # Registro formal e imutável de ADRs
│   ├── ACTIVE-QUEUE.md            # Fila de tarefas em execução e próximas
│   ├── TERMINOLOGY.md             # Glossário conceitual canônico
│   ├── CODE-MAP.md                # Mapa detalhado da base de código
│   ├── TEST-MAP.md                # Mapa detalhado da suíte de testes
│   ├── OPERATING-DOCTRINE.md      # Ponteiro para a Doutrina Operacional
│   │
│   ├── doctrine/                  # SUBSISTEMA DE DOUTRINA OPERACIONAL
│   │   ├── INDEX.md
│   │   ├── source/CONSTRUCTION-CONSTITUTION-v1.0.md
│   │   ├── OPERATING-DOCTRINE.md
│   │   ├── CONSTITUTION-APPLICABILITY-MATRIX.md
│   │   └── CONSTITUTIONAL-MATURITY-MAP.md
│   │
│   ├── context/                   # INFRAESTRUTURA DE CONTINUIDADE COGNITIVA
│   │   ├── INDEX.md
│   │   ├── CURRENT-STATE.md       # Snapshot operacional dinâmico
│   │   ├── CONTINUITY-CAPSULE.md  # Cápsula de transferência viva entre IAs
│   │   ├── IMPLEMENTATION-HISTORY.md # Histórico append-only de marcos
│   │   ├── ACTIVE-QUEUE.md        # Fila estruturada (NOW, NEXT, LATER, BLOCKED)
│   │   ├── DECISIONS-SUMMARY.md   # Sumário executivo das ADRs
│   │   ├── OPEN-QUESTIONS.md      # Registro canônico de dúvidas (OQ-XXX)
│   │   ├── CONTRADICTIONS.md      # Registro canônico de divergências (CON-XXX)
│   │   ├── RESEARCH-BACKLOG.md    # Separação: o que saber vs o que construir
│   │   ├── REPOSITORY-MAP.md      # Este mapa topológico
│   │   ├── CONTEXT-PROTOCOL.md    # Protocolos de sessão, perfis e TaskContract
│   │   ├── CHECKPOINT-PROTOCOL.md # Especificação do sistema de checkpoints
│   │   ├── context-manifest.json  # Manifesto machine-readable com hashes
│   │   └── checkpoints/           # Checkpoints imutáveis (CP-001 a CP-005)
│   │
│   ├── foundations/               # FUNDAMENTOS CONCEITUAIS
│   ├── architecture/              # ESPECIFICAÇÕES DA ARQUITETURA ALVO (TARGET)
│   ├── research/                  # DONOR-ARSENAL.md, DONOR-INDEX.md e autópsias
│   └── specs/                     # Políticas versionadas v0.1
│
├── tools/                         # FERRAMENTAS DETERMINÍSTICAS DE GOVERNANÇA
│   ├── context/ (validate_context.py, project_status.py, create_checkpoint.py)
│   └── intelligence/ (validate_intelligence.py, build_context_pack.py)
│
└── tests/                         # SUÍTE DE 38 TESTES AUTOMATIZADOS
    ├── continuity/ (test_continuity.py)
    ├── intelligence/ (test_intelligence.py)
    ├── doctrine/ (test_constitutional_doctrine.py)
    ├── unit/ (test_domain_state.py, test_stage_contracts.py)
    ├── integration/ (test_simple_loop_e2e.py, test_reconstruction_path.py, test_critique_revision_loop.py)
    ├── adversarial/ (test_adversarial_mvp.py)
    └── experiment/ (test_comparison_packet.py)
```
