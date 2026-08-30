# docs/context/CURRENT-STATE.md — Snapshot Operacional Dinâmico

> **ESTE DOCUMENTO É A DECLARAÇÃO OPERACIONAL VIVA DO ESTADO DO REPOSITÓRIO.**
> Atualizado em: 2026-08-30 | Checkpoint: CP-20260829-028

---

## 1. Identificação Operacional

- **Projeto:** Idea Evolution Engine (IEE)
- **Fase Ativa:** FASE 1 — SIMPLE IDEA EVOLUTION LOOP MVP (PREFLIGHT M05.4 RERUN CONGELADO — ATTEMPT-004)
- **Status da Fundação:** `COMPLETE_AND_LOCKED` (`FOUNDATION_READY = TRUE`)
- **Status do Rerun M05.4 (EXP-M05.4-PROSPECTIVE-RERUN-20260829):** `ATTEMPT_004_PREFLIGHT_FROZEN`
  - **Tentativa 001:** `INVALID_FOR_PRIMARY_ANALYSIS` (harness alterado pós-freeze).
  - **Tentativa 002:** `INVALID_FOR_PRIMARY_ANALYSIS` (exceção não capturada na célula 01).
  - **Tentativa 003:** `EXECUTION_INTEGRITY = PASS`, `HUMAN_REVIEW_ADMISSIBILITY = NOT_ADMISSIBLE_AS_PREREGISTERED` (22/24 células com falha de adapter mascarada).
  - **Autópsia & Hardening de Adapter:** `NativeModelRunner` corrigido com extração tipada de erros (`ProviderErrorDetails`), sanitização de segredos e retentativas de transporte delimitadas.
  - **Micro-Probe 001:** 3/3 esquemas representativos aprovados (A: 1.65s, B: 2.91s, C: PASS).
  - **Treatment Delivery Pilot 01:** 6/6 células concluídas (A: 2/2 DELIVERED, B: 2/2 PARTIALLY_DELIVERED com candidato substantivo, C: 2/2 DELIVERED).
  - **Decisão do Supervisor:** `CONDITION_B_REFINEMENT_INCOMPLETE_WITH_SUBSTANTIVE_CANDIDATE = ADMISSIBLE_TREATMENT_OUTPUT`.
  - **Tentativa 004:** `REAL-EXECUTION-ATTEMPT-004` (FROZEN_NOT_EXECUTED).
  - **Blinding Revision 3:** Compromisso `b2e271ff9dd35a8215c067d1e545f84dfa8add7f33335a69845ebd8d5ed82cf3` em `BLIND-REVEAL.sha256`. Segredo selado fora do repositório.
  - **Human Review:** `NOT_STARTED`
- **Último Checkpoint Imutável:** [`CP-20260829-028`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/checkpoints/CP-20260829-028.md)
- **Último Estado Seguro (Last Known Good):** `CP-20260829-028`
- **Git Branch:** `main`
- **Worktree Status:** CLEAN

---

## 2. Status do Trabalho

- **Último Trabalho Concluído:**
  - Freeze do Attempt-004 (`REAL-EXECUTION-ATTEMPT-004-PREFLIGHT.md` e `RERUN-FREEZE-MANIFEST.json` atualizado com 22 hashes).
  - Conclusão do Piloto de Entrega de Tratamento 01 com veredicto `END_TO_END_TREATMENT_DELIVERY_PROVEN_ON_CALIBRATION`.
- **Tarefa Ativa Atual:**
  - Execução Real do Attempt-004 (`REAL-EXECUTION-ATTEMPT-004`).
- **Próximo Passo Exato:**
  - Executar as 24 células prospectivas com `execute_m05_4_frozen.py`.

---

## 3. O Que Explicitamente NÃO Fazer (DO-NOT-DO)
1. ❌ **NÃO** reutilizar saídas do Attempt-001, 002, 003 ou Pilot.
2. ❌ **NÃO** abrir ou inspecionar `BLIND-REVEAL-REV3.json` durante a execução.
3. ❌ **NÃO** expor ou persistir chaves de API (`GROQ_API_KEY`).
4. ❌ **NÃO** modificar o código de produção durante a execução real.
