# docs/context/CURRENT-STATE.md — Snapshot Operacional Dinâmico

> **ESTE DOCUMENTO É A DECLARAÇÃO OPERACIONAL VIVA DO ESTADO DO REPOSITÓRIO.**
> Atualizado em: 2026-08-27 | Checkpoint: CP-20260827-015

---

## 1. Identificação Operacional

- **Projeto:** Idea Evolution Engine (IEE)
- **Fase Ativa:** FASE 1 — SIMPLE IDEA EVOLUTION LOOP MVP (EXPERIMENTO CONTROLADO REAL A/B/C PREPARADO)
- **Status da Fundação:** `COMPLETE_AND_LOCKED` (`FOUNDATION_READY = TRUE`)
- **Status do Experimento A/B/C (EXP-M05.2):** `SPEC_FROZEN` | `HARNESS_READY` | `BLINDING_PREPARED` | `REAL_EXECUTION = BLOCKED_BY_MISSING_GROQ_CREDENTIAL` (114 testes verdes).
- **Status da Fundação Epistêmica (EPISTEMIC-DONOR-01):** `SOURCE_ANCHORING = ACTIVE` | `REPRESENTATION_DISCIPLINE = ENFORCED` | `DONOR_INTELLIGENCE = INSTITUTIONALIZED` | `ARBOR_AUTOPSY = PERSISTED`.
- **Status do Hardening M05.1-R5:** `AUTHORITY_PROOF = HARDENED` | `GROUNDING_VALIDATOR = ACTIVE` | `FINAL_GATE_ENFORCEMENT = SOVEREIGN`.
- **Status do Hardening M05.1-R4:** `TOPOLOGY_REALITY_ALIGNMENT = HARDENED` | `NON_CIRCULAR_PROMOTION = ENFORCED` | `IMMUTABLE_RUN_IDENTITY = ACTIVE`.
- **Status do Hardening M05.1-R3:** `ONTOLOGY_CONSISTENCY = HARDENED` | `PROMOTION_PROVENANCE = ENFORCED` | `REJECTED_EVIDENCE_ISOLATED = TRUE`.
- **Status do Hardening M05.1-R2:** `UNDERSTAND_PURITY = HARDENED` | `GROQ_STRICT_MODE = IMPLEMENTED` | `FAILED_GENERATION_PRESERVED = TRUE`.
- **Status da Fronteira IEE/FioOS (M06.2):** `IEE_FIOOS_BOUNDARY = CANONICAL_AND_LOCKED` | `IEE_FIOOS_PROTOCOL_V1 = SPECIFIED` | `REAL_BRIDGE = NOT_IMPLEMENTED`.
- **Reconciliação do Repositório Remoto:**
  - `DEFAULT_BRANCH`: `main`
  - `REMOTE_REPOSITORY`: `https://github.com/phpedrogarcia-afk/idea-evolution-engine.git`
  - `SECRET_SCAN`: `PASS` (0 credenciais ou segredos rastreados no Git)
- **Último Checkpoint Imutável:** [`CP-20260827-015`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/checkpoints/CP-20260827-015.md)
- **Último Estado Seguro (Last Known Good):** `CP-20260827-015`
- **Git Branch:** `main`
- **Worktree Status:** CLEAN

---

## 2. Status do Trabalho

- **Último Trabalho Concluído:**
  - Missão M05.2 (Controlled Real A/B/C Value Experiment): Congelamento da especificação experimental (`EXPERIMENT-SPEC-M05.2.md`), inventário e auditoria de não-reusabilidade científica de runs históricos pré-R5 (`PAID-WORK-INVENTORY.md`), implementação do harness `ABCExperimentRunner` com blinding rigoroso 1-to-1 e isolamento de reveal, verificação determinística de ausência de credencial no ambiente e 114 testes automatizados aprovados (100% offline).
- **Tarefa Ativa Atual:**
  - `TASK-000`: Gate de Governança — Apresentação do relatório da Missão M05.2 com parada mandatória (*STOP*) por ausência de credencial Groq no ambiente.
- **Próximo Passo Exato:**
  - Operador humano exportar `GROQ_API_KEY` no ambiente e autorizar o disparo da execução real das condições A, B e C sob o harness congelado.

---

## 3. O Que Explicitamente NÃO Fazer (DO-NOT-DO)
1. ❌ **NÃO** alterar prompts ou parâmetros após inspecionar saídas dos modelos.
2. ❌ **NÃO** trocar silenciosamente de provedor ou modelo quando a chave do Groq não estiver presente.
3. ❌ **NÃO** revelar o mapeamento A/B/C para RESULT 1/2/3 antes da pontuação humana.
4. ❌ **NÃO** auto-atribuir vitória a qualquer condição sem avaliação cega do operador.
