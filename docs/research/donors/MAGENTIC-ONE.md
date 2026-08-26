# MAGENTIC-ONE — Multi-Agent Task Ledgers (Microsoft)

> **AUTÓPSIA DE DOADOR — STATUS: ADOPT-CONCEPT (Level B)**

---

## 1. O que é o Doador
O **Magentic-One** é uma arquitetura geral multiagente da Microsoft Research para resolução de tarefas complexas na web e em código, baseada em um agente orquestrador central e agentes especialistas.

---

## 2. Mecanismos Analisados
1. **Task Ledger e Progress Ledger:** Mapeamento explícito do plano da tarefa e do log de progresso factual.
2. **Detecção de Estagnação (Stall Detection):** Mecanismo para detectar quando os agentes entram em loops redundantes.
3. **Stall $\to$ Reflect $\to$ Replan:** Transição forçada para reflexão e replanejamento quando o progresso estagna.

---

## 3. Riscos e Fraquezas Reveladas no Doador
- **Orquestrador Central "Deus":** Dependência excessiva de um único agente orquestrador com prompts gigantescos em linguagem natural sem validação determinística rígida.

---

## 4. Decisão de Transplante para o IEE
- **Adotado:** O conceito de `Task/Progress Ledger` no `ProgressMonitor` e a política formal de detecção de estagnação (`StallPolicy`).
- **Rejeitado:** Orquestrador monolítico não determinístico (substituído pela governança contratual e validador determinístico no DCE).
