# docs/context/CONTRADICTIONS.md — Registro Canônico de Tensões e Contradições

> **REGISTRO DE DIVERGÊNCIAS, CONTRADIÇÕES E TENSÕES PRESERVADAS.**
> Nenhuma divergência deve ser "suavizada" ou silenciada por consenso artificial.

---

### [CON-001] Escopo do MVP: Ciclo Heurístico Simples vs Infraestrutura Avançada de DCE
- **Source A:** Documento Fundador Original (`IDEA-EVOLUTION-ENGINE-PROJETO-FUNDADOR-v0.1.md`) descreve o DCE com 13 subcomponentes complexos, topologias em árvore, MCTS e integração com FioOS como meta do sistema.
- **Source B:** Diretriz Estratégica da Missão Mestre 02 define o próximo alvo imediato como o *Simple Idea Evolution Loop* (Understand $\to$ Attack $\to$ Alternatives $\to$ Reality Check $\to$ Synthesize $\to$ Review).
- **Type:** `ROADMAP_SCOPE`
- **Status:** `RESOLVED_IN_HARDENING`
- **Impact:** `HIGH`
- **Resolution / Next Action:** Reconciliado pelo [ADR-001](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-001) e [ADR-011](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-011): A fundação está concluída; o próximo produto é estritamente o Simple Loop heurístico. A arquitetura avançada permanece como `TARGET` para fases posteriores.

---

### [CON-002] Aplicabilidade de E-Values de POPPER vs Oráculos Qualitativos
- **Source A:** POPPER donor defende *e-values* e inferência sequencial estrita como métrica única de encerramento empírico.
- **Source B:** Realidade de ideação humana e modelos de negócios exige validação empírica qualitativa e comportamental (entrevistas, landing pages, protótipos descartáveis) que não geram distribuições paramétricas limpas.
- **Type:** `METHODOLOGY`
- **Status:** `OPEN_PRESERVED`
- **Impact:** `MEDIUM`
- **Next Action:** Manter múltiplos `verification_modes` no `TestContract` (`STATISTICAL`, `EMPIRICAL_QUALITATIVE`, `FORMAL_LOGICAL`, `HUMAN_NORMATIVE`), aplicando *e-values* somente no modo estatístico.

---

### [CON-003] Custo de Coordenação Multiagente vs Ganhos de Crítica Adversarial
- **Source A:** Abordagens de DCI e MetaGPT assumem que multiagentes produzem sofisticação e diversidade de pontos de vista.
- **Source B:** Estudos de benchmarking do DCI evidenciam alto consumo de tokens com frequência gerando acordos redundantes e degradação de contexto.
- **Type:** `EMPIRICAL_ARCHITECTURE`
- **Status:** `OPEN_PRESERVED`
- **Impact:** `HIGH`
- **Next Action:** Preservar a divergência e validar formalmente no experimento EXP-002 com cálculo estrito de `coordination_value`.
