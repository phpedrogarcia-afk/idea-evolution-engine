# docs/context/CONTINUITY-CAPSULE.md — Cápsula de Continuidade Viva do IEE

> **PACOTE DE TRANSFERÊNCIA RÁPIDA DE CONTEXTO ENTRE AGENTES E IAs**
> *Se você é uma nova IA entrando no projeto após troca de modelo, perda de sessão ou interrupção, este documento restaura seu estado cognitivo completo em menos de 2 minutos.*

---

## 1. Identidade e Missão Canônica do Projeto
O **Idea Evolution Engine (IEE)** é um sistema de investigação deliberativa governada que reduz, organiza e torna acionável a incerteza ao redor de uma intenção humana. O sistema descobre *o que precisa ser verdade, falso, conhecido ou testado para justificar o próximo passo racional da ideia* — **sem transferir às máquinas a soberania sobre ela**.

- **Problema Humano:** Automatizar e disciplinar o ciclo manual em que criadores copiam e colam ideias entre diferentes IAs, eliminando perda de contexto, prolixidade infinita e ausência de critérios de término.
- **Princípio Mestre:** *Progress over Prose* (aumento de texto não é progresso; progresso é alteração de claim, evidência, premissa ou teste).
- **Regra de Soberania:** *Capability != Authority* (a IA propõe e critica; o humano mantém o monopólio da intenção, dos *Protected Cores* e das decisões normativas).

---

## 2. Onde Estamos Hoje (Estado Operacional)
- **Atualizado em:** 2026-10-04; este estado vigente supersede a cápsula histórica M05/M06 abaixo.
- **Fase atual:** FioIdeias V1.2 M2 — primeira passagem forte, uma chamada, implementação verificada offline.
- **Base M1:** commit `ceb8dc9df6f6f35c644345be068b8a9397c88351`; contrato 1.1 `PASS` e congelado.
- **M2:** `587 passed, 0 failed, 1 PytestCollectionWarning`; schema estrito de first pass com 4.751 caracteres; pin V1.2 do núcleo `cc59c4ba350087f84398a030e5f6a25f5f7a8184ee848e7f494c6e1367ae962a`.
- **Limite epistemológico:** `coverage_status = NOT_EVALUATED`; teste offline prova estrutura e regressões codificadas, não fidelidade semântica geral.
- **Autoridade:** gates, proveniência e autoridade de decisão humana preservados; nenhuma chamada a provedor/Qwen nesta missão.
- **Próximo passo:** concluir o commit/push M2 nesta branch e parar. M3 requer missão separada.
- **Próximo marco candidato:** M3 — cobertura determinística do contrato M1; requer missão separada e não está autorizado por M2.

---

## 3. Arquitetura Conceitual Essencial
1. **IdeaGenome:** Grafo de conhecimento persistente, versionado e imutável ($v_N \to v_{N+1}$). O chat é efêmero; o genoma é a memória durável da ideia.
2. **Claims & Evidence:** Claims são a unidade atômica de investigação (`UNTESTED`, `SUPPORTED`, `REFUTED`, `UNCERTAIN`). Evidências possuem tipagem estrita e proveniência obrigatória.
3. **DeliberationContract:** Toda deliberação ocorre sob contrato formal prévio definindo alvos, atos permitidos, critérios determinísticos de progresso, orçamento e condições de parada.
4. **GenomePatch & GenomeValidator:** IAs propõem mutações atômicas (`GenomePatch`); o kernel determinístico valida 5 camadas (*Schema, Integridade Referencial, Autoridade, Invariantes, Transições*) em regime *all-or-nothing*.
5. **READY_TO_TEST:** Veredito declarando que a deliberação teórica atingiu retornos decrescentes e que o próximo avanço requer contato empírico com a realidade via `TestContract`.
6. **Multi-Agent is Not Default:** Se o `coordination_value` for baixo, o sistema opera em `SINGLE_AGENT_MODE`.

---

## 4. O Sistema de Continuidade e Checkpoints
- **Último Checkpoint Imutável:** [`CP-20261004-001`](checkpoints/CP-20261004-001.md)
- **Manifesto Machine-Readable:** [`docs/context/context-manifest.json`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/context-manifest.json)
- **Validador Determinístico:** Execute `python tools/context/validate_context.py` para verificar integridade da base.
- **Fail-Closed on Conflict:** Se duas fontes documentais de mesmo nível divergirem, pare e registre o conflito em [`docs/context/CONTRADICTIONS.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/CONTRADICTIONS.md).

---

## 5. Rotas para Contexto Profundo
- **Constituição e Invariantes:** [`docs/GOVERNANCE-INVARIANTS.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/GOVERNANCE-INVARIANTS.md)
- **Decisões Arquiteturais Registradas:** [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md)
- **Terminologia Canônica:** [`docs/TERMINOLOGY.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/TERMINOLOGY.md)
- **Arquitetura Alvo Detalhada:** [`docs/TARGET-ARCHITECTURE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/TARGET-ARCHITECTURE.md)
- **Autópsias de Doadores:** [`docs/research/DONOR-INDEX.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/research/DONOR-INDEX.md)
- **Fila de Tarefas Ativas:** [`docs/context/ACTIVE-QUEUE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/ACTIVE-QUEUE.md)
