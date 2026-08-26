# docs/context/CURRENT-STATE.md — Snapshot Operacional Dinâmico

> **ESTE DOCUMENTO É A DECLARAÇÃO OPERACIONAL VIVA DO ESTADO DO REPOSITÓRIO.**
> Atualizado em: 2026-08-26 | Checkpoint: CP-20260826-008

---

## 1. Identificação Operacional

- **Projeto:** Idea Evolution Engine (IEE)
- **Fase Ativa:** FASE 1 — SIMPLE IDEA EVOLUTION LOOP MVP (ESSENCE PRESERVATION & FEATURE ACCRETION HARDENING)
- **Status da Fundação:** `COMPLETE_AND_LOCKED` (`FOUNDATION_READY = TRUE`)
- **Status do Produto:** `SIMPLE IDEA EVOLUTION LOOP` com isolamento em 3 camadas (`CORE`, `DERIVED`, `CANDIDATE`), detecção de `Speculative Feature Accretion` e 63 testes verdes.
- **Status da Missão 05:** `REAL_MODEL_CANARY = BLOCKED_PROVIDER_CREDENTIAL_OR_COST` (Incerteza real mantida honestamente bloqueada).
- **Status da Missão 05.1:** `CANARY_AUTOPSY_AND_ESSENCE_HARDENING = COMPLETE_OFFLINE` (`ESSENCE_PRESERVATION = HARDENED`, `SPECULATIVE_ACCRETION_BLOCKED = TRUE`).
- **Status da Missão 06 / 06.1:** `MULTI_MODEL_READY_OFFLINE = TRUE` | `FREE_ONLY_POLICY = INSTITUTIONALIZED`.
- **Reconciliação do Repositório Remoto:**
  - `DEFAULT_BRANCH`: `main`
  - `REMOTE_REPOSITORY`: `https://github.com/phpedrogarcia-afk/idea-evolution-engine.git`
  - `SECRET_SCAN`: `PASS` (0 credenciais ou segredos rastreados no Git)
- **Último Checkpoint Imutável:** [`CP-20260826-008`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/checkpoints/CP-20260826-008.md)
- **Último Estado Seguro (Last Known Good):** `CP-20260826-008`
- **Git Branch:** `main`
- **Worktree Status:** CLEAN

---

## 2. Status do Trabalho

- **Último Trabalho Concluído:**
  - Missão 05.1: Autópsia causal da proliferação especulativa de features, correção dos prompts `SYNTHESIZE` e `FINAL_REVIEW`, adição de `candidate_extensions` e `core_mechanism` ao estado compartilhado, e aprovação de 63 testes automatizados.
- **Tarefa Ativa Atual:**
  - `TASK-000`: Gate de Governança — Apresentação do relatório da Missão 05.1 e parada mandatória (*STOP*).
- **Próximo Passo Exato:**
  - Inserção da chave de API gratuita no `.env` local para disparar o Real Model Canary (M05-B) com o prompt protegido contra inchaço especulativo.

---

## 3. O Que Explicitamente NÃO Fazer (DO-NOT-DO)
1. ❌ **NÃO** permitir que mecanismos de alternativas virem requisitos obrigatórios do core sem justificativa humana.
2. ❌ **NÃO** fazer chamadas reais a APIs sem autorização/credencial explícita.
3. ❌ **NÃO** permitir fallback para provedores pagos (`PAID_FALLBACK: FORBIDDEN`).
