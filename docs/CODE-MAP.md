# CODE-MAP.md — Mapa da Base de Código (v0.1)

> **LOCALIZAÇÃO E PAPEL DE CADA COMPONENTE DE SOFTWARE DO IEE SIMPLE LOOP MVP.**
> *A inteligência reside nos contratos, nos prompts e na governança de estado; a infraestrutura é estritamente deliberada, tipada e enxuta.*

---

## 🏛️ Árvore de Arquivos do Núcleo Executável (`src/idea_evolution/`)

```text
src/idea_evolution/
├── __init__.py                     # Versão do pacote (v0.1.0)
│
├── domain/
│   └── state.py                    # SimpleIdeaState, RunStatus, CriticalIssue, AlternativeMechanism, RejectedProposal
│
├── stages/
│   ├── contracts.py                # Schemas Pydantic tipados de saída para todos os 8 estágios
│   ├── stage_base.py               # Classe base BaseStage: carrega prompt, invoca runner, valida e aplica delta
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
│   ├── fake.py                     # FakeModelRunner: simulação determinística offline e mocks para testes unitários
│   └── native.py                   # NativeModelRunner: integração com Groq/OpenAI com validação e repair bounded
│
├── orchestration/
│   ├── simple_loop.py              # SimpleLoopRunner: máquina de estados sequencial, limites de reconstrução e trace
│   └── baseline.py                 # BaselineRunner: executor da Condição A (Prompt único de refinamento)
│
├── tracing/
│   └── tracer.py                   # RunTracer: persistência em runs/RUN-YYYYMMDD-NNN/ (input, state, stages, final, trace)
│
└── cli/
    └── main.py                     # CLI unificada (iee evolve, compare, inspect-run)
```

---

## 📄 Prompts Versionados (`prompts/`)
- `prompts/understand_v0_1.md`: Prompt do estágio UNDERSTAND.
- `prompts/attack_v0_1.md`: Prompt do estágio ATTACK.
- `prompts/critique_logical_v0_1.md`: Prompt do estágio CRITIQUE_1 (Lógica e Premissas).
- `prompts/critique_feasibility_v0_1.md`: Prompt do estágio CRITIQUE_2 (Viabilidade e Mundo Real).
- `prompts/revision_v0_1.md`: Prompt do estágio REVISION.
- `prompts/alternatives_v0_1.md`: Prompt do estágio ALTERNATIVES.
- `prompts/reality_check_v0_1.md`: Prompt do estágio REALITY_CHECK.
- `prompts/synthesize_v0_1.md`: Prompt do estágio SYNTHESIZE.
- `prompts/final_review_v0_1.md`: Prompt do estágio FINAL_REVIEW.
- `prompts/baseline_refine_v0_1.md`: Prompt do estágio BASELINE_REFINE.

---

## 🎯 Princípios Arquiteturais Implementados
1. **Deterministic First:** O fluxo sequencial, contadores de ciclo, limites de retentativas e persistência são controlados 100% por código determinístico em Python.
2. **Original Idea Immutability:** O texto original do usuário é imutável em `state.original_idea`; toda maturação semântica evolui em `state.current_idea`.
3. **Bounded Reconstruction:** O loop de reconstrução é limitado deterministicamente a no máximo 1 ciclo automático.
4. **Preservação de Raw Output:** Toda resposta textual bruta gerada por modelos é gravada no log de estágios (`runs/<run_id>/stages/`).
