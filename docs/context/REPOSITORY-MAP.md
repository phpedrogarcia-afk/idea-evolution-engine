# docs/context/REPOSITORY-MAP.md — Mapa Topológico do Repositório

> **MAPA COMPLETO DE NAVEGAÇÃO ESTRUTURAL DO REPOSITÓRIO.**

---

```text
c:\Users\phped\Documents\ProjetoFioIedeias/
├── AI-START-HERE.md               # Ponto de entrada obrigatório e roteador para IAs
├── AGENTS.md                      # Regras operacionais para agentes e modelos
├── README.md                      # Apresentação do projeto para humanos
├── .gitignore                     # Configuração de arquivos ignorados pelo Git
│
├── docs/
│   ├── INDEX.md                   # Índice mestre da documentação
│   ├── SOURCE-OF-TRUTH.md         # Hierarquia de autoridade e precedência
│   ├── CURRENT-STATE.md           # Declaração do estado real físico
│   ├── GOVERNANCE-INVARIANTS.md   # Constituição intelectual do projeto
│   ├── DECISIONS-LEDGER.md        # Registro formal e imutável de ADRs
│   ├── ACTIVE-QUEUE.md            # Fila de tarefas em execução e próximas
│   ├── TERMINOLOGY.md             # Glossário conceitual canônico
│   ├── TARGET-ARCHITECTURE.md     # Visão geral da arquitetura de destino
│   ├── FOUNDATION-AUDIT.md        # Auditoria da Fase 0 original
│   ├── FOUNDATION-READINESS-REPORT.md # Relatório de conclusão da Fase 0
│   │
│   ├── context/                   # INFRAESTRUTURA DE CONTINUIDADE COGNITIVA
│   │   ├── INDEX.md               # Índice do subsistema de continuidade
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
│   │   └── checkpoints/           # Diretório de checkpoints imutáveis
│   │       ├── CP-20260826-001.md
│   │       └── CP-20260826-001.json
│   │
│   ├── foundations/               # FUNDAMENTOS CONCEITUAIS
│   │   ├── PROJECT-VISION.md      # A visão de longo prazo do IEE
│   │   ├── PROBLEM-DEFINITION.md  # O problema da orquestração manual
│   │   ├── PRINCIPLES.md          # Princípios herdados e específicos
│   │   ├── NON-GOALS.md           # Antiobjetivos explícitos
│   │   └── SCIENTIFIC-HYPOTHESES.md # Pergunta científica e hipóteses falsificáveis
│   │
│   ├── architecture/              # ESPECIFICAÇÕES DA ARQUITETURA ALVO (TARGET)
│   │   ├── IDEA-GENOME.md         # O grafo persistente imutável
│   │   ├── DCE.md                 # Deliberation Control Engine
│   │   ├── BOOTSTRAP.md           # Regime cognitivo de bootstrap
│   │   ├── DELIBERATION-CONTRACT.md # Contratos formais pré-execução
│   │   ├── PROGRESS-MONITOR.md    # Artefatos de medição de progresso
│   │   ├── READY-TO-TEST.md       # Veredito de transição para a realidade
│   │   ├── GENOME-PATCH.md        # Mutação atômica e 5 camadas do validador
│   │   └── STATE-MACHINE.md       # Máquina de estados finitos
│   │
│   ├── research/                  # PESQUISA E AUTÓPSIAS DE DOADORES (RESEARCH)
│   │   ├── DONOR-AUTOPSY-METHOD.md# Protocolo metodológico de autópsia
│   │   ├── DONOR-INDEX.md         # Catálogo consolidado e matriz de transplante
│   │   ├── RESEARCH-GAPS.md       # Lacunas ativas em investigação
│   │   ├── IDEATION-SCIENCE-MAP.md# Epistemologia e mapa C-K
│   │   └── donors/                # Autópsias detalhadas de sistemas doadores
│   │       ├── DCI.md, POPPER.md, MAGENTIC-ONE.md, ARBITEROS.md,
│   │       ├── CHATDEV-PUPPETEER.md, AGENTVERSE.md, METAGPT.md,
│   │       └── CK-THEORY.md, TRIZ.md
│   │
│   ├── specs/                     # POLÍTICAS VERSIONADAS V0.1 (CANONICAL)
│   │   ├── BOOTSTRAP-EXIT-POLICY-v0.1.md
│   │   ├── DECISION-RELEVANCE-POLICY-v0.1.md
│   │   ├── READY-TO-TEST-POLICY-v0.1.md
│   │   ├── STALL-POLICY-v0.1.md
│   │   └── AUTHORITY-MATRIX-v0.1.md
│   │
│   └── experiments/               # EXPERIMENTAÇÃO CIENTÍFICA
│       ├── EXPERIMENT-PROTOCOL.md
│       └── EXPERIMENT-BACKLOG.md
│
├── tools/                         # FERRAMENTAS DETERMINÍSTICAS DE GOVERNANÇA
│   └── context/
│       ├── validate_context.py    # Script de validação determinística de integridade
│       ├── project_status.py      # CLI de status operacional
│       └── create_checkpoint.py   # CLI de emissão de checkpoints
│
└── tests/                         # TESTES DE INTEGRIDADE E CONTINUIDADE
    └── continuity/
        └── test_continuity.py     # Suíte de testes adversariais de continuidade
```
