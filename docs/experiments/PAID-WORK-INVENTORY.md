# PAID-WORK-INVENTORY.md — Inventário e Reconhecimento de Trabalho Real Pago Anterior

> **DOCUMENTO DE PROVENIÊNCIA E REUSABILIDADE DE EVIDÊNCIA REAL (EXP-M05.2)**
> *Data:* 27 de agosto de 2026 | *Status:* `AUDIT_COMPLETE` | *Regra Canônica:* `SAME_RUN_NAME != SAME_EVIDENCE`

---

## 1. Inventário de Artefatos Reais Candidatos

| Identificador do Run | Timestamp Real | Provedor / Modelo | Topologia / Estágios | Código / Commit Relevante | Reusável para EXP-M05.2 (Cond B)? | Veredito Causal de Não-Reusabilidade |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `RUN-20260826-006` | 2026-08-26T14:30 | Groq / `openai/gpt-oss-120b` | 8 estágios (Synthesize antes de Reality) | `6486fdc` (M05.1-R2) | ❌ **NÃO** | **Essence Drift / Inchaço:** Não possuía topologia pós-síntese corrigida (R4), nem prova de autoridade (R5). Contaminado por hipóteses alucinadas no Core. |
| `RUN-20260826-008` | 2026-08-26T16:00 | Groq / `openai/gpt-oss-120b` | UNDERSTAND poluído | `6486fdc` (M05.1-R2) | ❌ **NÃO** | **Contaminação Semântica:** UNDERSTAND injetou aplicativo móvel/IA sem grounding; JSON Schema inválido sem strict mode. |
| `RUN-20260826-009` (A) | 2026-08-26T16:30 | Groq / `openai/gpt-oss-120b` | 6 estágios (Pre-R4) | `0fe5f69` (M05.1-R3) | ❌ **NÃO** | **Contradição Ontológica & Desalinhamento:** RealityCheck rodou antes da Síntese (Topologia antiga R3). |
| `RUN-20260826_202600-6639861f` | 2026-08-26T20:26 | Groq / `openai/gpt-oss-120b` | 6 estágios (Pre-R5) | `450505d` (M05.1-R4) | ❌ **NÃO** | **Authority Spoofing & Gate Bypass:** Modelo alegou `USER_EXPLICIT` para mapa mental/criptografia; finalizou com `REFINED_IDEA_READY` apesar de violações ontológicas. |
| `RUN-20260826_204203-82236930` | 2026-08-26T20:42 | - | Não persistido localmente | - | ❌ **NÃO** | **Artefato Ausente no Disco Local:** Execução em Cloud Shell sem persistência em worktree. |

---

## 2. Conclusão da Auditoria de Trabalho Pago
1. **Nenhum run real histórico possui equivalência com a produção pós-R5:** Todas as execuções reais passadas ocorreram antes da ativação do `AuthorityProofValidator`, da ancoragem `GroundingRecord` e do `_evaluate_hard_gates` determinístico.
2. **Reuso Científico Impossível:** Utilizar qualquer execução pré-R5 para representar a Condição B contaminaria o experimento científico com falhas estruturais que já foram comprovadamente sanadas no código.
3. **Preservação Histórica:** Todos os runs anteriores permanecem preservados em `runs/` como evidência de autópsia evolutiva imutável.
