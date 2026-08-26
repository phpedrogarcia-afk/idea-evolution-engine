# docs/context/CURRENT-STATE.md — Snapshot Operacional Dinâmico

> **ESTE DOCUMENTO É A DECLARAÇÃO OPERACIONAL VIVA DO ESTADO DO REPOSITÓRIO.**
> Atualizado em: 2026-08-26 | Checkpoint: CP-20260826-011

---

## 1. Identificação Operacional

- **Projeto:** Idea Evolution Engine (IEE)
- **Fase Ativa:** FASE 1 — SIMPLE IDEA EVOLUTION LOOP MVP (ONTOLOGY CONSISTENCY & PROMOTION PROVENANCE)
- **Status da Fundação:** `COMPLETE_AND_LOCKED` (`FOUNDATION_READY = TRUE`)
- **Status do Hardening M05.1-R3:** `ONTOLOGY_CONSISTENCY = HARDENED` | `PROMOTION_PROVENANCE = ENFORCED` | `REJECTED_EVIDENCE_ISOLATED = TRUE` (81 testes verdes).
- **Status do Hardening M05.1-R2:** `UNDERSTAND_PURITY = HARDENED` | `GROQ_STRICT_MODE = IMPLEMENTED` | `FAILED_GENERATION_PRESERVED = TRUE`.
- **Status da Fronteira IEE/FioOS (M06.2):** `IEE_FIOOS_BOUNDARY = CANONICAL_AND_LOCKED` | `IEE_FIOOS_PROTOCOL_V1 = SPECIFIED` | `REAL_BRIDGE = NOT_IMPLEMENTED`.
- **Status da Preservação de Essência (M05.1):** `ESSENCE_PRESERVATION = HARDENED` | `SPECULATIVE_ACCRETION_BLOCKED = TRUE`.
- **Status da Missão 05:** `REAL_MODEL_CANARY = READY_FOR_FINAL_REAL_REATTACK` (Linhagem ontológica e proveniência de promoção 100% blindadas offline).
- **Status da Missão 06 / 06.1:** `MULTI_MODEL_READY_OFFLINE = TRUE` | `FREE_ONLY_POLICY = INSTITUTIONALIZED`.
- **Reconciliação do Repositório Remoto:**
  - `DEFAULT_BRANCH`: `main`
  - `REMOTE_REPOSITORY`: `https://github.com/phpedrogarcia-afk/idea-evolution-engine.git`
  - `SECRET_SCAN`: `PASS` (0 credenciais ou segredos rastreados no Git)
- **Último Checkpoint Imutável:** [`CP-20260826-011`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/checkpoints/CP-20260826-011.md)
- **Último Estado Seguro (Last Known Good):** `CP-20260826-011`
- **Git Branch:** `main`
- **Worktree Status:** CLEAN

---

## 2. Status do Trabalho

- **Último Trabalho Concluído:**
  - Missão M05.1-R3: Autópsia causal da falha do RUN-009, institucionalização da regra de proveniência de promoção (`AcceptedChangeItem` e `core_mechanism_justification`), exclusão mútua estrita entre candidatas e rejeitadas, isolamento de testes do Core vs `exploratory_candidate_tests`, detecção determinística de contradições ontológicas no `FINAL_REVIEW`, modelo `ProposalRecord` e 81 testes automatizados aprovados (100% offline).
- **Tarefa Ativa Atual:**
  - `TASK-000`: Gate de Governança — Apresentação do relatório da Missão M05.1-R3 e parada mandatória (*STOP*).
- **Próximo Passo Exato:**
  - Disparo do Reattack Real com Groq `openai/gpt-oss-120b` sob a nova blindagem ontológica.

---

## 3. O Que Explicitamente NÃO Fazer (DO-NOT-DO)
1. ❌ **NÃO** promover mecanismos para o Core sem justificativa explícita.
2. ❌ **NÃO** permitir que propostas rejeitadas continuem ativas como candidatas ou poluam os testes do Core.
3. ❌ **NÃO** enfraquecer os contratos de validação determinística.
