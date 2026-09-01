# PREREGISTRATION: EXP-M05.5R1-CONTROLLED-REPLICATION

**Status:** FROZEN (Awaiting Supervisor Approval, DO NOT EXECUTE)
**Type:** Controlled Replication (Clean Rerun of M05.5)

## 1. Goal
Repeat the intended M05.5 reliability experiment without carrying forward contaminated holdouts, attempt identity, blind mapping, or provider state.

## 2. Treatments (Unchanged from M05.5)
- **Condition A (Baseline):** The frozen baseline prompt.
- **Condition B (Simple Loop):** The frozen iterative execution loop.
- **Condition C (Lean L1):** The frozen deterministic Lean L1.
- **Provider:** groq
- **Model:** openai/gpt-oss-120b

## 3. New Holdouts (N=8)
To guarantee uncontaminated provenance, 8 completely new holdouts are defined, maintaining the original conceptual classes:

- **REP-01 (Simple constrained utility):** Um aplicativo de menu de barra (menu bar) que exibe apenas a velocidade atual de download/upload da rede e permite definir um alarme se a conexão cair por mais de 10 segundos, sem histórico.
- **REP-02 (Fertile/incubative):** Como usar o modelo mental de "jardinagem" em vez de "arquitetura" para o desenvolvimento de software colaborativo, aceitando o crescimento orgânico e a poda.
- **REP-03 (Two plausible mechanisms):** Um sistema de votação para pequenas equipes que pode funcionar através de alocação de pontos distribuídos (token voting) ou através de veto único (consensus minus one) para aprovar designs.
- **REP-04 (Hard local/privacy constraint):** Um diário pessoal em áudio no celular onde a transcrição é feita por um modelo rodando 100% no dispositivo (on-device) e o áudio original é destruído imediatamente após a transcrição.
- **REP-05 (Physical operational idea):** Um sensor de umidade de solo feito com sucata eletrônica que acende um LED vermelho quando a planta precisa de água, sem nenhum tipo de conectividade Wi-Fi ou Bluetooth.
- **REP-06 (Normative human decision):** Um comitê de moderação deve priorizar a exclusão de conteúdos que causam dano emocional comprovado aos membros da comunidade, mesmo que isso restrinja o humor ácido e a sátira?
- **REP-07 (Simple developer tool):** Um script de linha de comando que lê um arquivo .env e verifica se todas as variáveis obrigatórias estão presentes no sistema antes de iniciar um serviço de backend.
- **REP-08 (Testable product hypothesis):** Se exibirmos o tempo estimado de leitura no topo de cada artigo, a taxa de rejeição (bounce rate) diminuirá em pelo menos 15%, pois os usuários terão expectativas mais claras.

## 4. New Blinding (Rev3)
An entirely fresh mapping will be created using an OS-backed CSPRNG. 
- Mapping must NEVER be printed or logged.
- Reveal is stored only in a canonical external sealed directory.
- Only the commitment hash is committed to this repository.

## 5. Execution Integrity Rules

### Attempt Immutability Guard
Once an attempt performs its first semantic provider call, its `ATTEMPT_ID` becomes **IMMUTABLE**.
- Its directory MUST NEVER be deleted, emptied, recreated, or reused.
- If execution fails (e.g., due to rate limits), that attempt is closed as FAILED/INVALID.
- The next execution must become `REAL-EXECUTION-ATTEMPT-002` (or incremented attempt).
- 429 Rate Limits are evidence. Do not erase them or restart the same attempt.

### Provider Quota Readiness Gate
Before the first real holdout call, a deterministic `PROVIDER_QUOTA_READINESS_GATE` will verify adequate same-model quota exists for the complete experiment.
- No holdout text may be sent through this gate. Use a neutral non-holdout synthetic string (recorded as `INFRASTRUCTURE_QUOTA_PROBE`).
- Estimate Required Quota: Based on M05.4, if token counts are unavailable, the gate requires a freshly reset provider quota window (e.g., full 200,000 TPD for Groq) and NO competing Groq work during the experiment.

### Exclusive Provider Window
During primary execution:
- NO diagnostic model calls.
- NO Groq pings.
- NO unrelated Groq workloads.
- The primary runner owns the experimental provider window.

## 6. Execution Readiness Contract
Before execution, the following MUST be confirmed:
- [ ] NEW_HOLDOUTS_FROZEN = YES
- [ ] TREATMENT_HASHES_MATCH_REFERENCE = YES
- [ ] RUBRIC_MATCH = YES
- [ ] MODEL_PROVIDER_MATCH = YES
- [ ] BLIND_MAPPING_SEALED = YES
- [ ] MAPPING_PRINTED = NO
- [ ] ATTEMPT_DIRECTORY_FRESH = YES
- [ ] ATTEMPT_IMMUTABILITY_GUARD = ACTIVE
- [ ] PROVIDER_QUOTA_READY = YES
- [ ] COMPETING_PROVIDER_WORKLOADS = NONE_KNOWN
- [ ] WORKTREE_CLEAN = YES
