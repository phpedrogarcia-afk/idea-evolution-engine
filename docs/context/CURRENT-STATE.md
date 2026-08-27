# docs/context/CURRENT-STATE.md — Snapshot Operacional Dinâmico

> **ESTE DOCUMENTO É A DECLARAÇÃO OPERACIONAL VIVA DO ESTADO DO REPOSITÓRIO.**
> Atualizado em: 2026-08-27 | Checkpoint: CP-20260827-020

---

## 1. Identificação Operacional

- **Projeto:** Idea Evolution Engine (IEE)
- **Fase Ativa:** FASE 1 — SIMPLE IDEA EVOLUTION LOOP MVP (PROTÓTIPO OFFLINE LEAN IEE L1 CONCLUÍDO)
- **Status da Fundação:** `COMPLETE_AND_LOCKED` (`FOUNDATION_READY = TRUE`)
- **Status do Protótipo Lean IEE (L1):** `OFFLINE_PROTOTYPE_VALIDATED` (12/12 cenários adversariais verdes)
  - Implementação Desacoplada: [`src/idea_evolution/orchestration/lean_loop.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/src/idea_evolution/orchestration/lean_loop.py) e [`src/idea_evolution/domain/early_epistemic_gate.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/src/idea_evolution/domain/early_epistemic_gate.py).
  - Invariante Comprovado: `LEAN_L1_MAX_MODEL_CALLS = 2` (Max absoluto 2 chamadas; 1 chamada para ideias diretas).
  - Status do Simple Loop de Produção: `REFERENCE_IMPLEMENTATION / CONTROL` (Preservado e 100% inalterado).
  - Suíte de Testes Totais: **126 / 126 testes verdes** (100% offline).
- **Status da Fundação Epistêmica (EPISTEMIC-DONOR-01):** `SOURCE_ANCHORING = ACTIVE` | `REPRESENTATION_DISCIPLINE = ENFORCED` | `DONOR_INTELLIGENCE = INSTITUTIONALIZED` | `ARBOR_AUTOPSY = PERSISTED`.
- **Status do Hardening M05.1-R5:** `AUTHORITY_PROOF = HARDENED` | `GROUNDING_VALIDATOR = ACTIVE` | `FINAL_GATE_ENFORCEMENT = SOVEREIGN`.
- **Reconciliação do Repositório Remoto:**
  - `DEFAULT_BRANCH`: `main`
  - `REMOTE_REPOSITORY`: `https://github.com/phpedrogarcia-afk/idea-evolution-engine.git`
  - `SECRET_SCAN`: `PASS` (0 credenciais ou segredos rastreados no Git)
- **Último Checkpoint Imutável:** [`CP-20260827-020`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/checkpoints/CP-20260827-020.md)
- **Último Estado Seguro (Last Known Good):** `CP-20260827-020`
- **Git Branch:** `main`
- **Worktree Status:** CLEAN

---

## 2. Status do Trabalho

- **Último Trabalho Concluído:**
  - Implementação do protótipo offline da Candidata L1 (`LeanLoopRunner`, `EarlyEpistemicGate`, `LeanFirstPassOutput`, `FocusedEscalationOutput`, `DecisionDeltaRecord`, `EpistemicRentRecord`). Correção de alegações de precisão não comprovadas em `LEAN-IEE-EXPERIMENT-PLAN.md` e `LEAN-IEE-COMPLEXITY-BUDGET.md`. Validação de 12 cenários adversariais (T1 a T12) em `tests/adversarial/test_adversarial_lean_iee.py`. Total de 126 testes aprovados.
- **Tarefa Ativa Atual:**
  - `TASK-000`: Transição de Fila — Preparação para a missão M05.3 de calibração e replay offline.
- **Próximo Passo Exato:**
  - Iniciar a Missão **M05.3 LEAN IEE OFFLINE REPLAY & ADVERSARIAL CALIBRATION** calibrando limiares de falso positivo/negativo com dados de runs históricas antes de autorizar novos testes reais.

---

## 3. O Que Explicitamente NÃO Fazer (DO-NOT-DO)
1. ❌ **NÃO** modificar o `SimpleLoopRunner` de produção ou os prompts de produção existentes.
2. ❌ **NÃO** acionar inferência real/paga sem calibração prévia offline em M05.3.
3. ❌ **NÃO** importar frameworks de agentes externos por conveniência (manter disciplina anti-turismo tecnológico).
4. ❌ **NÃO** reinterpretar retrospectivamente as notas atribuídas na avaliação humana congelada do M05.2.
