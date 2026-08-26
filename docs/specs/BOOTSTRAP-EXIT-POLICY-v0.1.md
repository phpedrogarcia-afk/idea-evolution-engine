# BOOTSTRAP-EXIT-POLICY-v0.1.md — Política de Saída do Bootstrap Estrutural

> **STATUS: SPECIFICATION CONGELADA — v0.1**

---

## 1. Objetivo
Determinar deterministicamente quando uma ideia recém-chegada em `STRUCTURE_BOOTSTRAP` atingiu o grau mínimo de legibilidade estrutural necessário para migrar para `DECISIONAL_INVESTIGATION`.

---

## 2. Critérios Mínimos Obrigatórios (Conjunção Lógica Estrita)
A função determinística `is_eligible_for_bootstrap_exit(genome: IdeaGenome) -> bool` retorna `True` se, e somente se, **TODOS** os 10 critérios abaixo forem satisfeitos:

1. **Problem Statement Validado:** O `problem_statement` foi formalizado e não foi rejeitado pelo humano.
2. **Claims Centrais Identificadas:** Existem ao menos 2 claims atômicas estruturadas no `claims`.
3. **Relação Mínima:** Existe ao menos 1 relação explícita no `claim_relations` (ex: `depends_on`, `supports`, `weakens`).
4. **Premissa Crítica Exposta:** Ao menos 1 premissa tácita estruturada no `assumptions`.
5. **Ação/Decisão Futura Identificada:** Ao menos 1 ação, decisão ou bifurcação dependente dessas claims mapeada.
6. **Incerteza Candidata Promovida:** Ao menos 1 incerteza no `uncertainties` formulada de forma investigável.
7. **Protected Cores Registrados:** `protected_cores` contém as restrições declaradas pelo humano OU declaração explícita de ausência registrada.
8. **Viabilidade de Relevância Decisória:** O genoma contém estrutura suficiente para permitir a geração de ao menos 1 `DecisionRelevanceReport` prospectivo mínimo.
9. **Ausência de Conflito Crítico de Intenção:** Não há `TensionRecord` ativo do tipo `VALUE_CONFLICT` não resolvido sobre o propósito essencial da ideia.
10. **Orçamento Não Excedido:** O custo acumulado no bootstrap está dentro do limite estipulado no contrato.

---

## 3. Avaliação Determinística
> **REGRA:** O LLM não pode simplesmente "declarar" que a ideia está pronta para sair do bootstrap. A validação é 100% computada pelo kernel sobre a estrutura do grafo do `IdeaGenome`.
