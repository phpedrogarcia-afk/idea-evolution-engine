# docs/intelligence/CONTEXT-PACK.md — Especificação do Pacote de Contexto (v0.1)

> **ESTRUTURA CANÔNICA DE EMPACOTAMENTO DE CONTEXTO MÍNIMO SUFICIENTE.**
> *Garante que cada subagente ou sessão receba apenas o necessário, sem amputar regras vitais.*

---

## 1. Estrutura Canônica do ContextPack v0.1

```markdown
# CONTEXT-PACK: [Task ID / Objetivo]

### 1. Task Definition
- **task_id:** `TASK-XXX`
- **objective:** [O que fazer]
- **task_type:** `MECHANICAL | SEMANTIC | EMPIRICAL | NORMATIVE | MIXED`

### 2. Operational State
- **current_phase:** `FASE_0_FOUNDATION` (ou fase ativa)
- **latest_checkpoint:** `CP-YYYYMMDD-NNN`
- **git_state:** branch / commit / clean

### 3. Relevant Invariants & Authority
- Invariantes constitucionais aplicáveis a esta tarefa.
- Limitações de autoridade (`CAN`, `MAY`, `MUST_NOT`).

### 4. Relevant Decisions (ADRs)
- Decisões registradas no `DECISIONS-LEDGER.md` que condicionam a tarefa.

### 5. Known Facts & Evidence
- Fatos confirmados em `FINDINGS.md` ou `evidence_registry`.

### 6. Open Uncertainties & Risks
- Dúvidas mapeadas em `OPEN-QUESTIONS.md` ou riscos conhecidos.

### 7. Scope & Allowed Files
- Lista de arquivos que podem ser inspecionados ou editados.

### 8. Expected Output Contract
- Formato da resposta (ex: JSON, patch, relatório, testes).
```
