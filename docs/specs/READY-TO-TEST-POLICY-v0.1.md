# READY-TO-TEST-POLICY-v0.1.md — Política de Transição para Teste Empírico

> **STATUS: SPECIFICATION CONGELADA — v0.1**

---

## 1. Regra de Disparo
A transição do estado `DECISIONAL_INVESTIGATION` para `READY_TO_TEST` ocorre quando o `TerminationController` constata que:
1. Existe uma incerteza decisiva cuja resolução requer oráculo externo (o mundo real).
2. Um teste empírico discriminativo foi formulado com implicações observáveis claras.
3. Nenhuma investigação puramente deliberativa (por IA ou análise estática) de custo proporcional é capaz de resolver a incerteza com confiança comparável.

---

## 2. Requisitos Mandatórios do TestContract
Para que a transição seja validada deterministicamente pelo `GenomeValidator`, o patch deve conter um `TestContract` completo com:

- [x] **`target_claim`:** Claim específica a ser testada.
- [x] **`rival_hypotheses`:** Hipóteses alternativas mapeadas.
- [x] **`measurable_implications`:** Métrica ou observação empírica mensurável.
- [x] **`test_method`:** Metodologia concreta e viável de teste.
- [x] **`possible_outcomes`:** Mapeamento de resultados possíveis e respectivo impacto no genoma (`decision_effect_per_outcome`).
- [x] **`stopping_rule`:** Critério objetivo de término do teste empírico.
- [x] **`budget`:** Limite de tempo e recursos financeiros/humanos para o teste.

---

## 3. Cláusula de Reabertura (Reopen Conditions)
O veredito de `READY_TO_TEST` e os resultados obtidos carregam condições formais de reabertura:
- Detecção de anomalias estatísticas ou falha metodológica no teste.
- Mudança drástica no ambiente externo (regulatória, tecnológica ou concorrência).
- Alteração soberana de um `Protected Core` pelo criador humano.
