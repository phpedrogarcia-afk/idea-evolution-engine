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
- **Fase atual:** FioIdeias V1.2 M5 — projeção local dos resultados de maturação na UI.
- **Base M5:** HEAD inicial `544bb9a6884e7d98310e442d31dfb4fd1a8605cd`; contratos e gates M1–M4 e núcleo científico V1.1 permanecem congelados.
- **M5:** adapter/UI projeta ledger de intenção, insights, caminhos candidatos, decisões abertas e cobertura estrutural; possibilidades e próximo passo mantêm seus rótulos epistêmicos; `UNRESOLVED` não se confunde com decisão humana.
- **Verificação:** 46 testes focados, suíte determinística `637 passed, 0 failed, 1 PytestCollectionWarning`, Playwright local offline em desktop/tablet/mobile; zero chamadas a provedor/Qwen.
- **Limite epistemológico:** `NO_BLOCKING_GAP_DETECTED` apenas informa ausência de defeito bloqueante entre checks estruturais; reparo não comprova preservação semântica nem detecta contradição em prosa.
- **Limitação de representação:** wire M2 mantém decisões como strings sem relações; M4 só introduz uma relação explícita no patch estrutural, sem fuzzy match.
- **Autoridade:** o mesmo runner e guarda de custo são reutilizados; nenhuma citação, autoridade, proveniência ou decisão humana é editável. Nenhuma chamada a provedor/Qwen nesta missão.
- **Próximo passo:** concluir commit/push normal de M5 somente nesta branch e parar. M6 requer missão humana separada.

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
- **Último Checkpoint Imutável:** [`CP-20261004-004`](checkpoints/CP-20261004-004.md)
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
