# docs/context/CHECKPOINT-PROTOCOL.md — Especificação do Sistema de Checkpoints Imutáveis

> **CONTRATO FORMAL DO SISTEMA DE CHECKPOINTS DO IDEA EVOLUTION ENGINE.**
> *Checkpoints são marcos imutáveis de estado operacional. Uma vez emitidos, nunca devem ser editados silenciosamente.*

---

## 1. Princípio da Imutabilidade
> **State must survive the model that created it.**

Checkpoints fornecem snapshots auditáveis e recuperáveis da integridade do projeto. Se uma IA for substituída ou desaparecer, o checkpoint informa o *Last Known Good State* sem depender de memória de chat.

---

## 2. Quando Emitir um Checkpoint Obrigatório
Checkpoints não são gerados a cada mensagem. São emitidos estritamente nos seguintes eventos:
1. Encerramento de uma Missão Mestre ou bloco de tarefas.
2. Decisão arquitetural material ou alteração constitucional.
3. Conclusão de uma entrega de código, schemas ou fixtures.
4. Conclusão de um experimento empírico.
5. Mudança de fase no roadmap.
6. Ponto seguro antes de uma operação arriscada de refatoração ou migração.

---

## 3. Convenção de Nomenclatura e Formato
Os checkpoints são nomeados no padrão:
`CP-YYYYMMDD-NNN` (exemplo: `CP-20260826-001`, `CP-20260826-002`)

Cada checkpoint é salvo em dois formatos sincronizados em `docs/context/checkpoints/`:
- `CP-YYYYMMDD-NNN.json`: Formato machine-readable para validação determinística.
- `CP-YYYYMMDD-NNN.md`: Formato human/AI-readable para navegação e inspeção rápida.

---

## 4. Campos Obrigatórios do Checkpoint

```json
{
  "checkpoint_id": "CP-YYYYMMDD-NNN",
  "created_at": "ISO-8601 Timestamp",
  "author": "Nome da IA ou Humano",
  "phase": "FASE_ATUAL",
  "objective": "Objetivo do marco atingido",
  "repository": {
    "branch": "master",
    "commit": "SHA-128 / SHA-7",
    "worktree_state": "CLEAN | DIRTY"
  },
  "completed_tasks": ["TASK-001", "TASK-002"],
  "changed_files": ["docs/context/...", "..."],
  "new_decisions": ["ADR-011"],
  "tests_executed": ["test_continuity.py (7 passed)"],
  "unresolved_questions": ["OQ-001", "OQ-002"],
  "known_contradictions": ["CON-002", "CON-003"],
  "known_risks": ["Risco de prolixidade"],
  "blockers": [],
  "next_exact_action": "Descrição do próximo passo imediato",
  "authorized_next_scope": ["Escopo estrito permitido"],
  "do_not_repeat": ["Tarefas que já foram concluídas e não devem ser refeitas"],
  "recovery_notes": "Orientações para retomada sem perda de contexto"
}
```

---

## 5. Correção e Sucessão de Checkpoints
Se for constatado um erro factual em um checkpoint anterior, **é expressamente proibido editar o arquivo original**. Deve-se emitir um novo checkpoint contendo o campo `"supersedes": "CP-YYYYMMDD-OLD"`, registrando a justificativa da revisão.
