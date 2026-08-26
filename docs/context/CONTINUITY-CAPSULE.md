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
- **Fase Atual:** **Fase 0 (Foundation & Continuity Hardening)** concluída com sucesso.
- **O que Existe Fisicamente:** Toda a base constitucional, arquitetural, metodológica, glossário, políticas versionadas, sistema de checkpoints e validadores determinísticos em `tools/context/`.
- **O que NÃO Existe:** Nenhum runtime de produto, zero código de produção, zero orquestradores de LLM ativos, zero chamadas a APIs pagas, zero dashboards ou UIs.
- **Próximo Alvo de Produto Aprovado:** **Simple Idea Evolution Loop (MVP Heurístico)**: Um pipeline simples e determinístico (*Understand $\to$ Attack $\to$ Alternatives $\to$ Reality Check $\to$ Synthesize $\to$ Review*).
- **Arquitetura Avançada (DCE Adaptativo, MCTS, RL, FioOS):** É classificada como `TARGET` / `FUTURE_RESEARCH` e NÃO deve ser implementada agora.

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
- **Último Checkpoint Imutável:** [`CP-20260826-001`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/checkpoints/CP-20260826-001.md)
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
