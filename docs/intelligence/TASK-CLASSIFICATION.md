# docs/intelligence/TASK-CLASSIFICATION.md — Taxonomia de Tarefas e Adaptação de Comportamento

> **A CLASSIFICAÇÃO DA TAREFA CONDICIONA O COMPORTAMENTO EPISTÊMICO DO AGENTE.**
> *Não classificar apenas para rotular; a taxonomia dita as restrições operacionais.*

---

## 1. Eixo Epistemológico (Natureza do Conhecimento)

| Tipo Epistêmico | Definição | Adaptação de Comportamento Obrigatória |
| :--- | :--- | :--- |
| **`MECHANICAL`** | Tarefas determinísticas (validação de schemas, lint, hashes, links, formatação). | **Deterministic tools first.** Proibido usar LLM para tarefas resolvíveis por scripts em Python/PowerShell. |
| **`SEMANTIC`** | Reformulação conceitual, síntese de ideias, extração de premissas, tradução conceitual. | **Single strong model.** Aplicar *Progress Over Prose* para evitar prolixidade e paráfrases redundantes. |
| **`EMPIRICAL`** | Questões sobre fatos do mundo externo, viabilidade técnica, comportamento de usuários, mercado. | **Investigation over Opinion.** Proibido responder por suposição; buscar papers, dados, benchmarks ou testes no mundo real. |
| **`NORMATIVE`** | Questões de valores morais, propósito essencial, limites éticos, *Protected Cores*, pivots. | **Human Authority Required.** A IA está proibida de decidir; deve isolar a encruzilhada e consultar o humano criador. |
| **`MIXED`** | Perguntas que misturam dimensões empíricas e normativas. | **Decompose mixed question.** Separar estritamente o componente empírico (para investigação) do componente normativo (para o humano). |

---

## 2. Eixo de Domínio Operacional

| Domínio | Requisito Metodológico Estrito |
| :--- | :--- |
| **`DOCUMENTATION`** | Mapear para uma única casa canônica. Evitar duplicação; usar links diretos. Atualizar manifest se alterar arquivos críticos. |
| **`ARCHITECTURE`** | Exigir *Simplicity Challenge*, *Reconnaissance* de doadores e registro formal de `DecisionProposal` antes de alterar o `DECISIONS-LEDGER.md`. |
| **`IMPLEMENTATION`** | Permitido apenas quando formalmente desbloqueado na fila ativa. Exige testes unitários e respeito aos contratos. |
| **`BUG`** | **Reproduce First.** Escrever teste de falha mínimo antes de propor o patch de correção. Validar regressão. |
| **`TEST`** | Testes devem ser falsificáveis e determinísticos. Evitar testes tautológicos que sempre passam. |
| **`RESEARCH`** | **Gap First.** Proibido pesquisar sem lacuna receptora explícita. Marcar status epistêmico de todas as fontes. |
| **`DONOR_AUTOPSY`** | Seguir rigorosamente os 7 passos do `DONOR-AUTOPSY-METHOD.md`. Extrair apenas o mecanismo essencial, nunca o framework inteiro. |
| **`EXPERIMENT`** | **Baseline Required.** Exigir hipótese formal, grupo de controle/baseline e métrica de falsificação prévia. |
| **`CONTINUITY`** | Validar integridade via `validate_context.py` e garantir emissão de checkpoint imutável ao terminar. |
