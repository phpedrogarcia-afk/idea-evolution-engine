# EXPERIMENT-SPEC-M05.2.md — Especificação Congelada do Experimento A/B/C

> **PROTOCOLO CIENTÍFICO CONGELADO — EXP-M05.2-VALUE-EVALUATION**
> *Status:* `SPECIFICATION_FROZEN` | *Data:* 27 de agosto de 2026

---

## 1. Pergunta Científica Central
> **O Idea Evolution Engine (IEE) direcionado produz um valor decisório significativamente superior a alternativas mais simples, e esse valor adicional compensa a complexidade, as chamadas de modelo e os tokens adicionais?**

---

## 2. Parâmetros Experimentais Congelados

- **Ideia Humana Bruta (Idêntica para todas as condições):**
  > *"Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros."*
- **Provedor Primário:** `Groq`
- **Modelo:** `openai/gpt-oss-120b`
- **Política de Custo:** `FREE_ONLY` / Gasto Financeiro Adicional = `R$ 0,00` (Free Tier)
- **Fallback Automático:** `PROIBIDO` (Se Groq/modelo falhar, a execução é interrompida com `BLOCKED`, sem troca de modelo).
- **Temperatura de Geração:** `0.3` (onde configurável).

---

## 3. Condições Experimentais

### Condição A — Baseline Single Refine
- **Objetivo:** Baseline representativo do que um usuário obtém com 1 prompt direto de refinamento genérico em 1 modelo forte.
- **Chamadas de Modelo:** Exatamente 1.
- **Prompt Congelado:**
  > *"You are given a raw project idea. Refine it into a clearer and more useful project concept. Preserve the original intent. Explain the problem, intended users, core mechanism, important assumptions or risks, and a practical next step. Do not invent user requirements. Prefer clarity and decision usefulness over verbosity."*

### Condição B — IEE Simple Loop (Produção Pós-R5)
- **Objetivo:** Motor de 6 estágios dirigidos do IEE com validação determinística de autoridade (`AuthorityProofValidator`), inversão topológica pós-síntese (`RealityCheck` sobre o Core aceito), detecção de essence drift e hard gates soberanos.
- **Topologia:** `UNDERSTAND` $\to$ `ATTACK` $\to$ `ALTERNATIVES` $\to$ `SYNTHESIZE` $\to$ `REALITY_CHECK` $\to$ `FINAL_REVIEW`.
- **Chamadas de Modelo:** 6 chamadas nominais (ou até 10 em caso de 1 ciclo de reconstrução controlada).

### Condição C — Critique-Revision Loop (4 Etapas)
- **Objetivo:** Aproximação do fluxo manual iterativo do usuário (Ideia $\to$ Crítica 1 $\to$ Revisão 1 $\to$ Crítica 2 $\to$ Revisão 2).
- **Chamadas de Modelo:** Exatamente 4 chamadas sequenciais.
- **Prompts Congelados:**
  1. **C1 (Crítica 1):** *"Critique the following project idea rigorously. Identify ambiguity, weak assumptions, missing problem definition, unnecessary speculation, likely failure modes, and the most important questions that should be resolved. Preserve the user's original intent and do not invent requirements."*
  2. **C2 (Revisão 1):** *"Revise the original project idea using the critique below. Improve clarity, problem definition and practical usefulness while preserving the user's original intent. Do not introduce unsupported requirements. Clearly separate what follows from the original idea from what remains only a possibility."*
  3. **C3 (Crítica 2):** *"Critique this revised idea again. Focus on remaining ambiguity, unsupported assumptions, speculative feature accretion, contradictions and whether the revision has drifted from the original human intent. Recommend only changes that materially improve the idea."*
  4. **C4 (Revisão Final):** *"Produce the final revision using the original idea, the previous revision and the latest critique. Preserve the original human intent. Do not convert speculative possibilities into user requirements. State remaining uncertainties honestly and give the most useful next step."*

---

## 4. Protocolo de Blinding e Avaliação
- Os outputs finais das 3 condições serão normalizados e anonimizados como `RESULT 1`, `RESULT 2` e `RESULT 3`.
- O mapeamento real será registrado exclusivamente no artefato isolado `BLIND-REVEAL.json`.
- A avaliação será conduzida pelo operador humano através de uma rubrica de 13 dimensões (0 a 5).
