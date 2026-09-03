# Pacote Lean de Maturação — Run EXP-M05.5R2-H08-COND-C

**Status:** `HUMAN_DECISION_REQUIRED` | **Chamadas de Modelo Utilizadas:** 1 (Max: 2)

---

## 1. Fonte Humana Imutável (SourceAnchor)

> Acho que pessoas que cozinham para uma ou duas pessoas desperdiçam menos alimentos se receberem sugestões de refeições baseadas no que já têm em casa e no prazo de validade aproximado. Gostaria de testar se isso realmente muda o comportamento delas.


## 2. Intenção & Problema Estruturado (Lean First Pass)

- **Intenção do Usuário:** Test whether providing meal suggestions based on current pantry contents and near‑expiry items changes cooking behavior and reduces food waste.
- **Problema Interpretado:** Food waste among individuals cooking for one or two people, caused by lack of awareness of existing ingredients and their approximate expiration dates.

## 3. Mecanismo Primário Proposto

**Mecanismo:** A recommendation engine that generates meal ideas using ingredients already present at home, weighted by their proximity to expiration dates.
- **Base de Autoridade Auditada:** `MODEL_HYPOTHESIS`
- **Justificativa:** By surfacing meals that use soon‑to‑expire items, users are nudged to consume them before they spoil, thereby reducing waste.


## 4. Alternativas Concorrentes Identificadas

1. **Generic recipe recommendation system that suggests meals based on user preferences without considering pantry inventory or expiry dates.** (Base: `MODEL_HYPOTHESIS`)
   - *Tradeoffs:* Does not address waste issue, May increase grocery shopping
2. **Manual meal‑planning calendar where users schedule meals and manually track ingredient usage and expiration.** (Base: `MODEL_HYPOTHESIS`)
   - *Tradeoffs:* Higher user effort, Potential for missed expiry items


## 5. Avaliação do Early Epistemic Gate (Custo = 0 chamadas)

- **Veredito do Gate:** `REQUEST_HUMAN_DECISION`
- **Motivo de Escalação:** `NONE`
- **Explicação:** A transição exige escolha normativa/humana protegida. Mais raciocínio de IA não substitui autoridade humana.
- **Autoridade Usurpada Detectada:** `False`
- **Candidatos Não Ancorados:** 3

## 7. Próximo Passo Recomendado

Develop a minimal viable recommendation prototype, recruit a small pilot group of solo/dual‑cook households, and measure food waste before and after exposure to the system.
