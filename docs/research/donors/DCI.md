# DCI — Deliberative Collective Intelligence (Stanford)

> **AUTÓPSIA DE DOADOR — STATUS: ADAPT (Level B)**

---

## 1. O que é o Doador
O framework **DCI (Deliberative Collective Intelligence)** propõe um protocolo estruturado para deliberação entre múltiplos agentes LLM, substituindo conversas livres por atos de fala tipados e mecanismos de convergência com preservação de pontos de vista minoritários.

---

## 2. Mecanismos Analisados
1. **Atos Epistêmicos Tipados:** Em vez de respostas livres em linguagem natural, agentes executam ações como `PROPOSE`, `CHALLENGE`, `GROUND`, `UPDATE`, `SYNTHESIZE`.
2. **First-Class Tensions:** Desacordos não são descartados ou forçados a consenso; tornam-se objetos persistidos de primeira classe.
3. **Bounded Openness & Structured Closure:** Abertura controlada para ideias divergentes com encerramento formal da deliberação.
4. **Minority Report:** Registro explícito de argumentos divergentes válidos para consideração futura.

---

## 3. Riscos e Fraquezas Reveladas no Doador
- **Custo e Complexidade Extremos:** A coordenação estruturada de muitos agentes pode gerar custos astronômicos de tokens com ganhos marginais em relação a um único agente bem instruído.
- **Taxonomia Hipertrofiada:** O DCI original propõe até 14 atos complexos, o que sobrecarrega a atenção dos modelos.

---

## 4. Decisão de Transplante para o IEE
- **Adotado:** Atos epistêmicos reduzidos e versionados no `DeliberationContract`, conceito de `TensionRecord` e regra de não-consenso forçado.
- **Rejeitado:** Framework completo de 14 atos e dependência automática de múltiplos agentes (adotada a verificação prévia de `coordination_value`).
