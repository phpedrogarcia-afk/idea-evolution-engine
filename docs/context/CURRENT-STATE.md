# docs/context/CURRENT-STATE.md — Snapshot Operacional Dinâmico

> **ESTE DOCUMENTO É A DECLARAÇÃO OPERACIONAL VIVA DO ESTADO DO REPOSITÓRIO.**
> Atualizado em: 2026-08-31 | Checkpoint: CP-20260829-028

---

## 1. Identificação Operacional

- **Projeto:** Idea Evolution Engine (IEE)
- **Fase Ativa:** FASE 1 — SIMPLE IDEA EVOLUTION LOOP MVP (REPLICAÇÃO CONTROLADA M05.5 CONGELADA — PRÉ-EXECUÇÃO)
- **Status da Fundação:** `COMPLETE_AND_LOCKED` (`FOUNDATION_READY = TRUE`)
- **Status do Experimento M05.4 (EXP-M05.4-PROSPECTIVE-RERUN-20260829):** `CLOSED_PROSPECTIVE_EXPERIMENT`
  - Efeito de Tratamento Observado: `C_BEST_IN_M05_4`
  - Status do Lean L1: `LEADING_CANDIDATE_PROVISIONAL_DEFAULT`
  - Mecanismo Causal: `UNRESOLVED`
- **Novo Experimento de Replicação M05.5 (EXP-M05.5-CONTROLLED-REPLICATION-20260831):**
  - **Objetivo:** Replicação direta de confiabilidade do efeito de tratamento principal M05.4 em 8 novas ideias holdout independentes (`REP-01` a `REP-08`).
  - **Execução:** `REAL-EXECUTION-ATTEMPT-001`
  - **Status de Cegamento:** Revisão 2 ativa (Rev1 invalidada antes de qualquer chamada semântica conforme `M05.5-PREEXECUTION-AMENDMENT-001.md`).
  - **Compromisso de Cegamento (Rev2):** `791197eab62e714e5284bbc616ed34a6e83cd3b86551664ed99a62f0c8b340f3` em `BLIND-REVEAL.sha256`. Segredo Rev2 selado fora do repositório.
  - **Variáveis Fixas:** Provedor `groq`, modelo `openai/gpt-oss-120b`, condições A/B/C idênticas, rubrica e regras de reviewability idênticas.
- **Último Checkpoint Imutável:** [`CP-20260829-028`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/checkpoints/CP-20260829-028.md)
- **Último Estado Seguro (Last Known Good):** `CP-20260829-028`
- **Git Branch:** `main`
- **Worktree Status:** CLEAN

---

## 2. Status do Trabalho

- **Último Trabalho Concluído:**
  - Rotação de cegamento para Revisão 2 com CSPRNG seguro e registro da Emenda 001.
  - Pré-registro, holdout ideas e manifestos de congelamento M05.5 devidamente assinados e verificados.
- **Tarefa Ativa Atual:**
  - `M05.5`: Execução Real de Replicação Controlada (`REAL-EXECUTION-ATTEMPT-001`).
- **Próximo Passo Exato:**
  - Recuperar chave da API Groq do GCP Secret Manager de forma segura, executar as 24 células e limpar a chave de ambiente.

---

## 3. O Que Explicitamente NÃO Fazer (DO-NOT-DO)
1. ❌ **NÃO** expor chaves de API (`GROQ_API_KEY`) no console, git ou logs.
2. ❌ **NÃO** expor o mapeamento cego Rev2.
3. ❌ **NÃO** modificar o conjunto de ideias holdout ou código dos runners durante a execução.
