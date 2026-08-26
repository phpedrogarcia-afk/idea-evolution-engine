# docs/intelligence/AGENT-INTELLIGENCE-AUDIT.md — Auditoria de Lacunas Cognitivas de Agentes

> **Data:** 26 de agosto de 2026  
> **Status:** AUDIT COMPLETE — FASE 03 INITIATED

---

## 1. Contexto e Motivação da Auditoria
Nas missões anteriores, o repositório consolidou sua constituição ([`docs/GOVERNANCE-INVARIANTS.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/GOVERNANCE-INVARIANTS.md)) e seu sistema de continuidade e checkpoints ([`docs/context/`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/)).

Entretanto, para que uma IA trabalhe de forma autônoma e disciplinada sem errar por impulso, faltavam **mecanismos operacionais de raciocínio governado**. Uma IA poderia saber *onde estava*, mas ainda cometer falhas clássicas de modelos de linguagem:
1. **Pular para a solução** antes de classificar a tarefa e declarar a hipótese.
2. **Turismo tecnológico:** Buscar papers e ferramentas externas sem uma lacuna receptora explícita.
3. **Falsa certeza e viés de confirmação:** Tratar a opinião de múltiplos modelos como prova independente.
4. **Alegação de melhoria sem baseline:** Dizer que um prompt ou schema é "melhor" sem medição anterior.
5. **Autoaprovação sem crítica:** O próprio autor da proposta atuar como único validador (*Producer == Sole Approver*).
6. **Inércia de fundação:** Continuar criando documentos teóricos infinitamente em vez de transicionar para o teste do produto (*Reality over Deliberation*).

---

## 2. Diagnóstico de Lacunas (Agent Intelligence Gaps)

| ID | Lacuna Cognitiva Identificada | Risco Associado | Mecanismo de Mitigação Necessário |
| :--- | :--- | :--- | :--- |
| **AIG-01** | **Ausência de Ciclo de Trabalho Padronizado** | IAs começam a editar arquivos aleatoriamente. | Criação do `WORK-PROTOCOL.md` (12 passos estritos: Orient $\to$ Classify $\to$ Recon $\to$ Hypothesize $\to$ Attack $\to$ Plan $\to$ Act $\to$ Verify $\to$ Record $\to$ Checkpoint). |
| **AIG-02** | **Tratamento Indiferenciado de Tarefas** | Tarefa mecânica tratada com prolixidade; tarefa empírica tratada por opinião. | Criação do `TASK-CLASSIFICATION.md` vinculando tipo de tarefa a comportamento epistêmico. |
| **AIG-03** | **Mutação sem Hipótese Falsificável** | Alterações arquiteturais baseadas em "parece melhor". | Criação do `HYPOTHESIS-PROTOCOL.md` e `BASELINE-POLICY.md`. |
| **AIG-04** | **Falta de Crítica Adversarial Independente** | Erros sutis passam porque quem cria aprova. | Criação do `ADVERSARIAL-REVIEW.md` (*Producer != Sole Approver*). |
| **AIG-05** | **Risco de Fundação Infinita (Foundation Trap)** | Criar Foundation 04, 05, etc., sem jamais construir o MVP. | Instituição do `FOUNDATION_READY_GATE` e [ADR-012](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-012). |

---

## 3. Diretriz de Temperamento Operacional
> **Aggressive Epistemics, Conservative Authority.**
- **Agressivo em:** Investigação, busca por contraexemplos, falsificação de hipóteses, redução de complexidade, testes de mutação e desafio a premissas frágeis.
- **Conservador em:** Soberania humana, autoridade de mutação, integridade da linhagem, preservação de histórico e respeito irrestrito ao Source of Truth.
