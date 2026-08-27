# docs/context/CURRENT-STATE.md — Snapshot Operacional Dinâmico

> **ESTE DOCUMENTO É A DECLARAÇÃO OPERACIONAL VIVA DO ESTADO DO REPOSITÓRIO.**
> Atualizado em: 2026-08-27 | Checkpoint: CP-20260827-024

---

## 1. Identificação Operacional

- **Projeto:** Idea Evolution Engine (IEE)
- **Fase Ativa:** FASE 1 — SIMPLE IDEA EVOLUTION LOOP MVP (CALIBRAÇÃO E REPLAY OFFLINE M05.3 CONCLUÍDOS)
- **Status da Fundação:** `COMPLETE_AND_LOCKED` (`FOUNDATION_READY = TRUE`)
- **Status do Kernel FioED (Fio Epistemic Dynamics):** `EMPIRICALLY_CALIBRATED_OFFLINE`
  - Relatório de Replay M05.3: [`docs/experiments/M05.3-FIOED-OFFLINE-REPLAY.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/experiments/M05.3-FIOED-OFFLINE-REPLAY.md).
  - Doutrina e Exegese: [`docs/epistemology/KRISHNAMURTI-OJAI-1982-SOURCE-MAP.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/epistemology/KRISHNAMURTI-OJAI-1982-SOURCE-MAP.md) e [`docs/epistemology/FIO-EPISTEMIC-DYNAMICS.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/epistemology/FIO-EPISTEMIC-DYNAMICS.md).
  - Modelo Formal e Máquina de Estados: [`docs/epistemology/FIOED-FORMAL-MODEL.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/epistemology/FIOED-FORMAL-MODEL.md).
  - Ecologia de Ideias: [`docs/epistemology/FIOED-IDEA-ECOLOGY.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/epistemology/FIOED-IDEA-ECOLOGY.md).
  - Fronteira da Realidade: [`docs/epistemology/FIOED-REALITY-BOUNDARY.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/epistemology/FIOED-REALITY-BOUNDARY.md).
  - Auditoria de Arte Prévia: [`docs/research/FIOED-PRIOR-ART-AUDIT.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/research/FIOED-PRIOR-ART-AUDIT.md).
  - Suíte de Testes Totais: **166 / 166 testes verdes** (100% offline).
- **Status do Protótipo Lean IEE (L1):** `EMPIRICALLY_SUPPORTED_OFFLINE` (Invariante `LEAN_L1_MAX_MODEL_CALLS = 2` e Early Epistemic Gate validados).
- **Status do Simple Loop de Produção:** `REFERENCE_IMPLEMENTATION / CONTROL` (Preservado e 100% inalterado).
- **Reconciliação do Repositório Remoto:**
  - `DEFAULT_BRANCH`: `main`
  - `REMOTE_REPOSITORY`: `https://github.com/phpedrogarcia-afk/idea-evolution-engine.git`
  - `SECRET_SCAN`: `PASS` (0 credenciais ou segredos rastreados no Git)
- **Último Checkpoint Imutável:** [`CP-20260827-024`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/checkpoints/CP-20260827-024.md)
- **Último Estado Seguro (Last Known Good):** `CP-20260827-024`
- **Git Branch:** `main`
- **Worktree Status:** CLEAN

---

## 2. Status do Trabalho

- **Último Trabalho Concluído:**
  - Conclusão da Missão M05.3 FioED / Lean IEE Offline Replay & Adversarial Calibration:
    - Replay determinístico dos artefatos do experimento real M05.2 (Condições A, B e C) via `src/idea_evolution/experiments/fioed_replay.py`.
    - Confirmação de que os sinais do FioED ($P_e = 9$, regressões decisórias e profundidade 5) identificam empiricamente o desperdício da Condição B.
    - Validação de que 100% das tentativas de `EvidenceSpoofing` foram bloqueadas (`SPOOF_ACCEPTED = 0`).
    - Validação de 166 testes unitários e determinísticos verdes (100% offline).
- **Tarefa Ativa Atual:**
  - `TASK-000`: Transição de Fila — Preparação para a missão M05.4 (Replicação Multi-Ideia).
- **Próximo Passo Exato:**
  - Iniciar a Missão **M05.4 MULTI-IDEA REAL REPLICATION EXPERIMENT** comparando as Condições A (1 chamada), B (10 chamadas) e C (Lean L1 / FioED) em 5 ideias com blinding estrito e avaliação humana pré-congelada.

---

## 3. O Que Explicitamente NÃO Fazer (DO-NOT-DO)
1. ❌ **NÃO** modificar o `SimpleLoopRunner` de produção ou os prompts de produção existentes.
2. ❌ **NÃO** alterar os dados brutos históricos dos experimentos passados.
3. ❌ **NÃO** aplicar inferência real antes da autorização formal do desenho do protocolo M05.4.
4. ❌ **NÃO** tratar personas sintéticas ou votos de LLMs como evidência empírica externa.
