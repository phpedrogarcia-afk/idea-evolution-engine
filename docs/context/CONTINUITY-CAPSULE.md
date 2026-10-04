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
- **Fase atual:** FioIdeias V1.2 M3 — primeira passagem forte seguida por gate determinístico de cobertura.
- **Base M3:** HEAD inicial `d2ed90345ab10c7273b0227aff856779c85dc00e`; contrato M1.1, M1 e M2 permanecem congelados.
- **M3:** gate separado do `EarlyEpistemicGate`, aplicado após mapear a resposta Lean; 15 testes dirigidos e suíte inteira `602 passed, 0 failed, 1 PytestCollectionWarning` offline.
- **Limite epistemológico:** `NO_BLOCKING_GAP_DETECTED` só informa ausência de defeito bloqueante entre as verificações determinísticas implementadas. Não prova preservação semântica nem detecta contradição em prosa.
- **Limitação de representação:** o wire M2 representa `open_decisions` como strings sem IDs de intenção. O mapper não infere relações; provisional/deferred só ficam expostos quando um `OpenDecision` traz a intenção ligada por ID, então os casos sem vínculo são `REPAIR_REQUIRED`.
- **Autoridade:** gates, proveniência e autoridade de decisão humana preservados; nenhuma chamada a provedor/Qwen nesta missão.
- **Próximo passo:** concluir commit/push M3 na mesma branch e parar. M4 requer missão humana separada; nenhuma correção é automática.

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
- **Último Checkpoint Imutável:** [`CP-20261004-002`](checkpoints/CP-20261004-002.md)
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
