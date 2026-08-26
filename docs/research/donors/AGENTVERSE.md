# AGENTVERSE — Dynamic Expert Recruitment

> **AUTÓPSIA DE DOADOR — STATUS: ADAPT (Level B)**

---

## 1. O que é o Doador
O **AgentVerse** introduz mecanismos dinâmicos de composição de equipes de agentes LLM, recrutando e descartando especialistas com base no feedback intermediário da tarefa.

---

## 2. Mecanismos Analisados
1. **Dynamic Expert Recruitment:** Composição adaptativa da equipe em vez de um conselho estático.
2. **Feedback-Driven Composition:** Ajuste dos participantes se a rodada anterior falhar em gerar progresso.

---

## 3. Decisão de Transplante para o IEE
- **Adotado:** O conceito no `TeamComposer` do DCE, recrutando *funções epistemológicas* conforme a classificação do problema (`QuestionClassifier`).
- **Rejeitado:** Recrutamento indiscriminado de agentes sem filtro de `coordination_value`.
