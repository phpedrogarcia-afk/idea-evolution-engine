# FOUNDATION-AUDIT.md — Auditoria e Reconciliação Fundacional

> **Relatório de Auditoria Epistemológica e Arquitetural — Fase 0**

---

## 1. Material Recebido e Inventário Inicial
No início da missão, o repositório continha:
1. `README.md` (vazio, 0 bytes).
2. `IDEA-EVOLUTION-ENGINE-PROJETO-FUNDADOR-v0.1.md` (documento fundador extenso contendo intuições, esboços de arquitetura, princípios e propostas de fases).
3. `Idea_Evolution_Engine_Projeto_Fundador_v0.1.docx` (cópia binária do documento fundador).

---

## 2. Inconsistências e Riscos Identificados no Material Original

### 2.1 Mistura de Fases e Tentação de Construção Imediata
- **Problema:** O texto original continha seções que alternavam entre discussões teóricas de ponta (ex: busca MCTS em grafos de workflow, aprendizado por RL com AFlow/GPTSwarm) e propostas de codificação rápida de um orquestrador em Python (`DirectRunner`).
- **Resolução / Congelamento:** Foi congelada a separação estrita em fases ([ADR-001](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-001)). Ficou explicitamente proibido criar código de produto na Fase 0.

### 2.2 Risco de "Turismo Tecnológico" com Doadores Externos
- **Problema:** O texto citava mais de uma dezena de sistemas (DCI, POPPER, Magentic-One, ArbiterOS, ChatDev, AgentVerse, MetaGPT, AFlow, GPTSwarm, TRIZ, C-K Theory), criando a ilusão de que todos poderiam ser integrados simultaneamente.
- **Resolução / Congelamento:** Estabeleceu-se a regra constitucional: *Donor adoption must be gap-driven* ([ADR-008](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-008)). Apenas mecanismos pontuais que resolvem lacunas concretas foram transplantados conceitualmente; o restante foi classificado como `FUTURE_DONOR` ou mantido em estudo.

### 2.3 Ambiguidade entre READY_TO_TEST e Conclusão de Ideia
- **Problema:** Em passagens informais, `READY_TO_TEST` poderia ser interpretado como "a ideia foi aprovada como viável".
- **Resolução / Congelamento:** Definiu-se formalmente que `READY_TO_TEST` é estritamente um veredito sobre a *próxima fonte de conhecimento* (a realidade empírica supera em custo-benefício epistemológico a continuidade da deliberação por IA) ([ADR-009](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-009)).

### 2.4 Ambiguidade em HUMAN_DECISION_REQUIRED
- **Problema:** Risco de usar `HUMAN_DECISION_REQUIRED` como fuga para qualquer incerteza empírica desconhecida pela IA.
- **Resolução / Congelamento:** Congelou-se a distinção: `HUMAN_DECISION_REQUIRED` é estado de *autoridade e valores normativos*, nunca de mera ignorância de fatos do mundo. Perguntas empíricas devem ser investigadas; perguntas normativas exigem decisão humana.

---

## 3. Conceitos Canônicos Congelados
1. **Definição Canônica do IEE:** Sistema de investigação deliberativa governada para redução de incerteza sem perda da soberania humana.
2. **Constituição Intelectual:** *Progress over prose*, *Capability != Authority*, *Memory != Evidence*, *Reality over Deliberation*, *Deterministic First*, *LLM propõe; Kernel valida*, *Multi-agent is not default*.
3. **IdeaGenome:** Grafo persistente e imutável de estado epistêmico versionado ($v_N \to v_{N+1}$).
4. **DeliberationContract:** Governança obrigatória prévia para qualquer rodada de deliberação.
5. **Regimes Cognitivos:** `STRUCTURE_BOOTSTRAP` (foco em `StructureGain`) vs `DECISIONAL_INVESTIGATION` (foco em `Decisive Uncertainty`).
6. **Fronteira com FioOS:** IEE é o cérebro epistêmico/deliberativo; FioOS é o executor auditável de runtime e segurança.

---

## 4. Questões e Decisões que Permanecem Abertas para Fases Futuras
- **Métrica Exata de Entropia Epistêmica:** Como quantificar numericamente a convergência sem recair em falsa precisão.
- **Mecanismo de Descoberta Automática de Topologias:** Se busca de grafos (estilo AFlow/GPTSwarm) será viável frente a templates fixos.
- **Protocolos Específicos para Claims Estatísticas vs Não-Estatísticas:** Limites de aplicabilidade de *e-values* (POPPER) vs oráculos humanos.
- **Mapeamento C-K como Projeção Gráfica:** Como renderizar o `IdeationMap` em UI sem poluir a ontologia canônica do genoma.
