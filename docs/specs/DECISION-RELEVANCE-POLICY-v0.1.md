# DECISION-RELEVANCE-POLICY-v0.1.md — Política de Relevância Decisória e Incertezas Decisivas

> **STATUS: SPECIFICATION CONGELADA — v0.1**

---

## 1. Definição Canônica de Incerteza Decisiva
> **Uma incerteza é decisiva se, e somente se, sua resolução modifica plausivelmente a próxima ação recomendada, o status de uma claim estruturalmente relevante ou uma decisão soberana.**

$$\text{DecisiveUncertainty} \iff \text{ActionImpact} \lor \text{ClaimImpact} \lor \text{DecisionImpact}$$

Se nenhuma dessas três dimensões for materialmente afetada, a incerteza é classificada como `NOT_DECISIVE` e não deve receber recursos prioritários de deliberação.

---

## 2. Protocolo Contrafactual Obrigatório
Para avaliar a relevância de uma incerteza, o sistema deve gerar um `DecisionRelevanceReport` explicitando:

1. **Cenário Suportado (`if_supported`):**
   - Se a hipótese for comprovada verdadeira, o que muda na arquitetura da ideia ou no plano de ação?
2. **Cenário Refutado (`if_refuted`):**
   - Se a hipótese for derrubada, qual claim é invalidada? A ideia sofre pivot ou encerramento?
3. **Cenário de Incerteza Persistente (`if_uncertain`):**
   - Se continuarmos sem saber, qual o risco ou custo de avançar às cegas?

---

## 3. Proveniência e Auditoria
Contrafactuais são hipóteses avaliativas geradas por modelos de IA, não fatos empíricos. Cada `DecisionRelevanceReport` deve declarar `generated_by`, `model_family`, `policy_version` e `timestamp`.
Após a realização da investigação ou teste real, o impacto efetivo deve ser registrado no `DecisionDelta` para aferir a calibração do sistema.
