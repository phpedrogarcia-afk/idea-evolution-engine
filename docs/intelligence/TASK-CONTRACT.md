# docs/intelligence/TASK-CONTRACT.md — Especificação do Contrato de Tarefas (v0.1)

> **CONTRATO FORMAL PARA DELEGAÇÃO E EXECUÇÃO DE TAREFAS POR AGENTES.**
> *Nenhuma tarefa complexa deve ser iniciada sem um TaskContract explícito.*

---

## 1. Estrutura Canônica do TaskContract v0.1

```markdown
# TASK-[ID]: [Título da Tarefa]

- **task_id:** `TASK-XXX`
- **objective:** [Descrição inequívoca do resultado pretendido]
- **why_now:** [Vínculo com a ACTIVE-QUEUE e justificativa de prioridade]
- **task_type:** `MECHANICAL | SEMANTIC | EMPIRICAL | NORMATIVE | MIXED`
- **risk_level:** `LOW | MEDIUM | HIGH | CRITICAL`
- **authorized_scope:** [Lista de diretórios e arquivos que PODEM ser modificados]
- **forbidden_scope (DO-NOT-DO):** [Ações e módulos estritamente PROIBIDOS]
- **context_profile:** `FAST_ENTRY | DEEP_ENTRY | RESEARCH_ENTRY | IMPLEMENTATION_ENTRY`
- **required_sources:** [Arquivos canônicos de leitura obrigatória antes de iniciar]
- **expected_artifacts:** [Arquivos e saídas estruturadas a serem entregues]
- **acceptance_criteria:** [Condições determinísticas para aprovação da tarefa]
- **baseline:** [Medição do estado atual ou declaração de 'N/A' com justificativa]
- **evidence_required:** [Testes, logs ou hashes que comprovem o resultado]
- **review_required:** `SELF_CHECK | INDEPENDENT_REVIEW | ADVERSARIAL_REVIEW | DETERMINISTIC_VALIDATION | HUMAN_REVIEW`
- **checkpoint_required:** `true | false`
- **stop_condition:** [Condição exata onde a IA deve PARAR a execução e aguardar revisão]
```

---

## 2. Regras de Conformidade do Contrato
1. **Escopo Fechado:** Modificações fora do `authorized_scope` configuram violação contratual e causam rejeição da entrega.
2. **Respeito a Proibições:** O descumprimento de qualquer item em `forbidden_scope` anula a tarefa.
3. **Parada Obrigatória:** Ao atingir a `stop_condition`, a IA deve encerrar o turno e emitir o relatório de handoff.
