# docs/context/CURRENT-STATE.md — Snapshot Operacional Dinâmico

> **ESTE DOCUMENTO É A DECLARAÇÃO OPERACIONAL VIVA DO ESTADO DO REPOSITÓRIO.**
> Atualizado em: 2026-09-01 | Checkpoint: CP-20260901-012

---

## 1. Identificação Operacional

- **Projeto:** Idea Evolution Engine (IEE)
- **Fase Ativa:** FASE 1 — SIMPLE IDEA EVOLUTION LOOP MVP
- **Status da Fundação:** `COMPLETE_AND_LOCKED` (`FOUNDATION_READY = TRUE`)
- **Status do Experimento M05.4 (EXP-M05.4-PROSPECTIVE-RERUN-20260829):** `CLOSED_PROSPECTIVE_EXPERIMENT`
  - Efeito de Tratamento Observado: `C_BEST_IN_M05_4`
  - Status do Lean L1: `LEADING_CANDIDATE_PROVISIONAL_DEFAULT`
  - Mecanismo Causal: `UNRESOLVED`
- **Status do Experimento M05.5 (EXP-M05.5-CONTROLLED-REPLICATION-20260831):**
  - Execução: `REAL-EXECUTION-ATTEMPT-001`
  - Papel da evidência: `QUARANTINED_EXECUTION_STRESS_EVIDENCE`
  - Admissibilidade: `INVALID_PRIMARY_REPLICATION`
  - Razão: reutilização de identidade de tentativa, contaminação dos holdouts e interferência de quota/TPD do provedor.
  - Semântica preservada: isto é `EXPERIMENT_EXECUTION_FAILURE`, não `LEAN_L1_REPLICATION_FAILURE`; não é `FAILED`, `REJECTED`, `READY`, `PROVEN` ou `SUPERSEDED`.
  - Evidência: `experiments/EXP-M05.5-CONTROLLED-REPLICATION-20260831/M05.5-ATTEMPT-001-INTEGRITY-AUDIT.md` (commit `26a2a67`).
- **M05.5R1 (EXP-M05.5R1-CONTROLLED-REPLICATION-20260901):** `AUTHENTICATED_CAPACITY_PROVEN_INSUFFICIENT_NOT_EXECUTION_AUTHORIZED`
  - Contrato: `experiments/EXP-M05.5R1-CONTROLLED-REPLICATION-20260901/M05.5R1-PRE-FREEZE-READINESS.md`.
  - Controles offline: namespace/receipt imutável, boundary sintético de holdout e gate de capacidade fail-closed; 12 testes sintéticos passaram.
  - Holdouts: `M05.5R1-HOLDOUT-SET-REV1` foi selado literalmente fora do repositório; receipt hashado está em `experiments/EXP-M05.5R1-CONTROLLED-REPLICATION-20260901/`.
  - Blinding: REV1 foi congelada em cofre externo; o repositório tem somente seu commitment, sem reveal.
  - Capacity design: cap `2048`, envelope máximo específico `11.226.334` tokens (redução de 58,82% sobre 27.262.976), 208 requests máximos incluindo repairs explícitos, schedule CSPRNG comprometido e pacing de concorrência 1 permanecem congelados offline.
  - Evidência autenticada R2: organização `Personal` / `Default Project`, plano `FREE`, sem limites customizados no projeto; `openai/gpt-oss-120b` expõe `30 RPM`, `1.000 RPD`, `8.000 TPM` e `200.000 TPD`. A conta não admite a carga única máxima de `131.072` tokens e não pode garantir o bound diário (gap mínimo de `11.026.334` tokens). Saldos e reset do período não foram expostos pelo console.
  - Bloqueios reais: a capacidade autenticada atual é insuficiente; o namespace `REAL-EXECUTION-ATTEMPT-001` não está novo (diretório `raw/` vazio e sem registry, preservado como scar), preflight e autorização humana separada.
- **Último Checkpoint Imutável:** [`CP-20260901-012`](checkpoints/CP-20260901-012.md)
- **Último Estado Seguro (Last Known Good):** `CP-20260901-012`
- **Git Branch:** `main`
- **Worktree após a checagem autenticada:** `PENDING_CHECKPOINT_COMMIT`

---

## 2. Status do Trabalho

- **Último Trabalho Concluído:**
  - Auditoria forense de `REAL-EXECUTION-ATTEMPT-001`, preservada como evidência quarantinada.
  - `PFI-R0-IDEA-EVOLUTION-ENGINE-READINESS-AUDIT-001`, que confirmou que E10 só prova a fronteira epistêmica/de autoridade, não um bridge de runtime.
  - `PFI-R1-STATE-QUEUE-RECONCILIATION-001`, que substituiu o estado pré-execução obsoleto pela classificação acima.
  - `PFI-R2-M05_5R1-REPLICATION-PLANNING-001`, que congelou o desenho mínimo e identificou os controles determinísticos ainda ausentes.
  - `PFI-R3-M05_5R1-OFFLINE-HARNESS-HARDENING-001`, que corrigiu os controles offline sem chamadas, holdouts reais ou alteração de autoridade.
  - `PFI-M05_5R1-HOLDOUT-SEALING-001`, que congelou REV1 literalmente em cofre externo e publicou somente seu receipt permitido.
  - `PFI-M05_5R1-BLINDING-REV1-001`, que congelou o reveal A/B/C ↔ R1/R2/R3 em cofre externo e publicou somente commitment.
  - `PFI-M05_5R1-REAL-CAPACITY-READINESS-001`, que encontrou TPD restante não comprovado, envelope total de tokens não limitado e ausência de schedule neutro; nenhuma chamada ou tratamento foi feito.
  - `PFI-M05_5R1-CAPACITY-DESIGN-FREEZE-001`, que congelou o cap, bound conservador, schedule neutro, pacing e invalidações sem tocar em holdouts/reveal ou provedor.
  - `PFI-M05_5R1-TOKEN-ENVELOPE-CALIBRATION-001`, que substituiu o bound de contexto inteiro por um envelope tokenizado com `openai-harmony` oficial, sem inferência, reveal ou execução A/B/C.
- **Tarefa Ativa Atual:**
  - `PFI-M05_5R1-AUTHENTICATED-CAPACITY-CHECK-R2` confirmou sessão Groq autenticada e concluiu `NOT_READY_ACCOUNT_CAPACITY` sem calls de inferência, holdouts ou reveal.
- **Próximo Passo Exato:**
- Decisão humana: obter capacidade autenticada que comporte o bound congelado, autorizar uma recalibração científica separada ou adiar M05.5R1. A execução nesta conta permanece vedada.

---

## 3. O Que Explicitamente NÃO Fazer (DO-NOT-DO)

1. ❌ **NÃO** reutilizar `REAL-EXECUTION-ATTEMPT-001`, seus holdouts ou seu mapeamento cego como base confirmatória.
2. ❌ **NÃO** interpretar a quarentena como falha de replicação do Lean L1, rejeição do produto ou evidência positiva.
3. ❌ **NÃO** expor chaves de API (`GROQ_API_KEY`) no console, git ou logs.
4. ❌ **NÃO** implementar bridge FioOS, parser externo, invocação automática ou transferência de autoridade: `IDEA != REQUIREMENT`, `IDEA != TRUTH`, `IDEA != AUTHORITY`.
