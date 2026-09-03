# docs/context/CURRENT-STATE.md — Snapshot Operacional Dinâmico

> **ESTE DOCUMENTO É A DECLARAÇÃO OPERACIONAL VIVA DO ESTADO DO REPOSITÓRIO.**
> Atualizado em: 2026-09-01 | Checkpoint: CP-20260901-015

---

## 1. Identificação Operacional

- **Projeto:** Idea Evolution Engine (IEE)
- **Fase Ativa:** FASE 1 — SIMPLE IDEA EVOLUTION LOOP MVP
- **Status da Fundação:** `COMPLETE_AND_LOCKED` (`FOUNDATION_READY = TRUE`)
- **Status do Experimento M05.4 (EXP-M05.4-PROSPECTIVE-RERUN-20260829):** `CLOSED_PROSPECTIVE_EXPERIMENT`
  - Efeito de Tratamento Observado: `C_BEST_IN_M05_4`
  - Status do Lean L1: `LEADING_CANDIDATE_PROVISIONAL_DEFAULT`
  - Mecanismo Causal: `UNRESOLVED`
- **Status do Experimento M05.5 (EXP-M05.5R2-FREE-PROVIDER-PORTABILITY-REPLICATION):** `COMPLETE_AND_CLOSED`
  - Tentativa Confirmatória Válida: `M05.5R2-REAL-EXECUTION-ATTEMPT-002` (Cerebras Cloud, `gpt-oss-120b`, 24/24 células HTTP 200, custo $0 out-of-pocket).
  - Avaliação Humana Cega: 8/8 holdouts pontuados e congelados no commit `fe81936` antes do desmascaramento.
  - Integridade do Segredo: `REVEAL_COMMITMENT_INTEGRITY = PASS` (hash `d2de9ac1bbcd76c7aaef639b0b61d63dd355f1bea96f9d1c0f41ef7d434eed02`).
  - Desfecho Primário Ordinal: `PRIMARY_REPLICATION_RESULT = PASS` (C: 22 pts > A: 18 pts > B: 8 pts).
  - Convergência de Continuidade: `CONTINUE_CONVERGENCE = PASS` (C: 6/8 > A: 2/8 > B: 0/8).
  - Convergência Secundária Dimensional: `SECONDARY_CONVERGENCE = PASS` (C: 362/400 [méd. 4.525] > A: 282 > B: 143).
  - Eficiência de Chamadas: `CALL_EFFICIENCY_CRITERION = PASS` (C: 11 chamadas [13,75% de B = 80 chamadas]).
  - Status do Lean L1: `REPLICATED_PRIMARY_WITH_PARTIAL_PATTERN_SUPPORT`
  - Mecanismo Causal: `UNRESOLVED` (propriedade do pacote de tratamento, não de componente isolado).
  - Relatório Canônico: `experiments/EXP-M05.5R2-FREE-PROVIDER-PORTABILITY-REPLICATION/M05.5R2-FINAL-SCIENTIFIC-REPORT.md`.
  - Registro de Fechamento: `experiments/EXP-M05.5R2-FREE-PROVIDER-PORTABILITY-REPLICATION/M05.5-CLOSURE-RECORD.md`.
- **Último Checkpoint Imutável:** [`CP-20260901-015`](checkpoints/CP-20260901-015.md)
- **Último Estado Seguro (Last Known Good):** `CP-20260901-015`
- **Git Branch:** `main`
- **Worktree após conclusão de M05.5R2:** `CLEAN`

---

## 2. Status do Trabalho

- **Último Trabalho Concluído:**
  - Conclusão do desmascaramento formal e análise científica pré-registrada de M05.5R2.
  - Geração dos relatórios `M05.5R2-FORMAL-UNBLIND-RESULT.json`, `M05.5R2-FINAL-SCIENTIFIC-REPORT.md` e `M05.5-CLOSURE-RECORD.md`.
  - Encerramento formal do programa M05.5 (`M05_5_STATUS = COMPLETE`).
- **Tarefa Ativa Atual:**
  - Transição para o desenvolvimento e entrega do **Simple Idea Evolution Loop MVP** (Fase 1).
- **Próximo Passo Exato:**
  - Iniciar o planejamento e especificação técnica do Simple Idea Evolution Loop MVP adotando a Condição C (Lean Loop L1 com Early Epistemic Gate) como motor padrão de inferência.

---

## 3. O Que Explicitamente NÃO Fazer (DO-NOT-DO)

1. ❌ **NÃO** abrir novos experimentos, provedores ou pilotos sacrificiais para M05.5 (o programa está encerrado e arquivado).
2. ❌ **NÃO** fazer turismo tecnológico ou adicionar frameworks multiagente arbitrários (LangChain, AutoGen, CrewAI).
3. ❌ **NÃO** confundir TARGET com CURRENT.
4. ❌ **NÃO** implementar bridge FioOS ou transferência de autoridade sem autorização humana formal: `IDEA != REQUIREMENT`, `IDEA != TRUTH`, `IDEA != AUTHORITY`.
