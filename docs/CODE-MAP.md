# CODE-MAP.md — Mapa da Base de Código (v0.3)

> **LOCALIZAÇÃO E PAPEL DE CADA COMPONENTE DE SOFTWARE DO IEE SIMPLE LOOP MVP & MULTI-MODEL ROUTING.**
> *A inteligência reside nos contratos, nos prompts e na governança de estado; a infraestrutura é estritamente deliberada, tipada e enxuta.*

---

## 🏛️ Árvore de Arquivos do Núcleo Executável (`src/idea_evolution/`)

```text
src/idea_evolution/
├── __init__.py                     # Versão do pacote (v0.1.0)
│
├── config/
│   ├── __init__.py
│   ├── catalog.py                  # ModelCatalog, ModelCatalogEntry, CostClass, LifecycleStatus, PrivacyClass, CostPolicy, ExecutionMode
│   └── routing.py                  # ModelRoutingConfig, ModelDefinition: mapeamento determinístico de aliases, rotas e validação de catálogo
│
├── domain/
│   └── state.py                    # SimpleIdeaState, RunStatus, CriticalIssue, AlternativeMechanism, RejectedProposal, StageHistoryEntry (com proveniência multi-modelo)
│
├── stages/
│   ├── contracts.py                # Schemas Pydantic tipados de saída para todos os 8 estágios
│   ├── stage_base.py               # Classe base BaseStage: carrega prompt, invoca runner, valida e aplica delta com proveniência
│   ├── understand.py               # Estágio 1: Extrai problema, intenção humana e premissas
│   ├── attack.py                   # Estágio 2: Crítica adversarial severa (Condição B)
│   ├── critique.py                 # Estágio 2/4 (Condição C): Crítica lógica e de viabilidade
│   ├── revision.py                 # Estágio 3/5 (Condição C): Revisão evolutiva intermediária
│   ├── alternatives.py             # Estágio 3: Geração de 2–4 mecanismos causais alternativos
│   ├── reality_check.py            # Estágio 4: Mapeamento de dependências e testes do mundo real
│   ├── synthesize.py               # Estágio 5: Síntese estruturada, mudanças aceitas e rejeitadas
│   └── final_review.py             # Estágio 6: Detecção de essence drift e verificação de liberação/reconstrução
│
├── providers/
│   ├── base.py                     # Interface ModelRunner, ModelResponse e ModelUsage
│   ├── fake.py                     # FakeModelRunner: simulação determinística offline com identidades multi-provedor (fake_a, fake_b, fake_c)
│   ├── native.py                   # NativeModelRunner: integração com Groq, OpenAI, Gemini e Anthropic com validação, repair bounded e doctor integrado ao catálogo
│   └── router.py                   # RunnerRouter: despachador de modelos por estágio e governança de fallback
│
├── orchestration/
│   ├── simple_loop.py              # SimpleLoopRunner: máquina de estados sequencial, despacho multi-modelo, limites de reconstrução e trace
│   └── baseline.py                 # BaselineRunner: executor da Condição A (Prompt único de refinamento)
│
├── tracing/
│   └── tracer.py                   # RunTracer: persistência em runs/RUN-YYYYMMDD-NNN/ (input, state, stages com proveniência, final, trace)
│
└── cli/
    └── main.py                     # CLI unificada (iee evolve, compare, inspect-run, providers doctor, routes show)
```

---

## 📄 Arquivos de Configuração e Catálogo de Modelos (`config/`)
- `config/model_catalog.json`: Catálogo de seed versionado com ciclo de vida, classes de custo, capacidades e fontes de verificação.
- `config/models.example.yaml`: Exemplo canônico de roteamento multi-modelo sob política `FREE_ONLY` (Groq gpt-oss-120b, Groq qwen3.6-27b, Gemini 3.7-flash).
- `config/models.same_model.yaml`: Configuração de modelo único para todas as etapas (Groq gpt-oss-120b).
- `config/models.multi_provider_fake.yaml`: Configuração com múltiplos fake runners para testes E2E offline.

---

## 🎯 Princípios Arquiteturais Implementados
1. **Cost Authority is Authority:** O sistema opera por padrão em `FREE_ONLY`, rejeitando modelos pagos ou não verificados antes da inferência.
2. **MODEL_ID Is Not Timeless Knowledge:** Modelos encerrados (`SHUT_DOWN`) são bloqueados com sugestão de substituto ativo.
3. **The Kernel is the Mediator:** Modelos não conversam diretamente em chat livre; o kernel orquestra contexto mínimo, valida esquemas e despacha.
4. **Zero Silent Fallback (`NO_CROSS_PROVIDER_FALLBACK`):** Falhas em um modelo não acionam provedores alternativos silenciosamente.
5. **Deterministic Routing Hash:** Toda configuração gera um hash canônico SHA-256 gravado nos artefatos de execução.
