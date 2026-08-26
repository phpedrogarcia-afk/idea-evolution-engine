# STALL-POLICY-v0.1.md — Política de Detecção de Estagnação e Saturação

> **STATUS: SPECIFICATION CONGELADA — v0.1**

---

## 1. Princípio da Detecção de Estagnação
Inspirado no mecanismo de *stall detection* do Magentic-One, o IEE impede que o sistema continue consumindo recursos de computação quando sucessivas rodadas de deliberação falharem em produzir progresso epistêmico real (*Progress Over Prose*).

---

## 2. Condições de Disparo de Estagnação (Stall Trigger)
O estado `STALLED` é acionado deterministicamente se qualquer um dos seguintes cenários for verificado pelo `ProgressMonitor`:

1. **Saturação Estrutural (Structure Saturation):** Em regime de `STRUCTURE_BOOTSTRAP`, 2 rodadas consecutivas geram 0 novas claims não-redundantes, 0 novas relações e 0 premissas expostas.
2. **Ausência de Delta Decisório:** Em regime de `DECISIONAL_INVESTIGATION`, 2 rodadas consecutivas produzem `DecisionDelta` nulo (nenhuma claim alterou status, nenhuma ação recomendada mudou e nenhuma incerteza foi reduzida).
3. **Loop de Duplicação Semântica:** Detecção de alta similaridade semântica (paráfrase) entre as propostas de novas rodadas e as já rejeitadas ou consolidadas anteriormente.
4. **Esgotamento de Orçamento:** O consumo de tokens da rodada atingiu o teto sem satisfazer os critérios de progresso do contrato.

---

## 3. Protocolo de Resolução de Estagnação (Stall $\to$ Reflect $\to$ Replan)
Quando `STALLED` é acionado:
1. O DCE interrompe imediatamente a execução da topologia atual.
2. É emitido um `StallReport` estruturado diagnosticando a causa da paralisia.
3. O sistema transiciona para `REPLAN_REQUIRED` para tentar uma das seguintes alternativas:
   - Alterar a função epistemológica ou recrutar outro modelo.
   - Mudar a topologia de deliberação (ex: de paralelo para critique loop).
   - Decompor a questão em sub-perguntas mais simples.
   - Escalar para o criador humano se for detectado um bloqueio de valores (`HUMAN_DECISION_REQUIRED`).
