# Pacote de Maturação da Ideia — Run EXP-M05.5R2-H08-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Acho que pessoas que cozinham para uma ou duas pessoas desperdiçam menos alimentos se receberem sugestões de refeições baseadas no que já têm em casa e no prazo de validade aproximado. Gostaria de testar se isso realmente muda o comportamento delas.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** To test whether providing meal suggestions based on the user's current pantry items and their approximate expiry dates changes the cooking behavior of small‑household cooks and reduces food waste.
- **Problema Central:** People cooking for one or two individuals may waste food because they lack meal suggestions that consider the ingredients they already have and the approximate expiration dates of those ingredients.
- **Atores / Usuários:** Individuals who cook for one or two people, Small‑household families, Researchers conducting the behavior test


## 3. Versão Refinada e Mecanismo Proposto

Develop a lightweight application for small‑household cooks to manually record pantry ingredients and their approximate expiry dates, generate tailored meal suggestions, and track self‑reported food waste to evaluate behavioral change.


- **Justificativa de Promoção ao Core:** This mechanism directly reflects the user's explicit intent to test whether pantry‑based suggestions influence cooking behavior and reduce waste, without relying on model‑generated data or automated capture methods. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** User-provided pantry and expiration data may be inaccurate or incomplete
   - *Impacto:* Inaccurate inputs lead to irrelevant or unsafe meal suggestions, undermining trust and potentially increasing waste
   - *Parte Afetada:* User Input / Data Collection
2. **[MEDIUM]** Generated meal suggestions may not be appealing or practical for users
   - *Impacto:* If users reject the suggestions, the system fails to influence behavior, rendering the intervention ineffective
   - *Parte Afetada:* Suggestion Engine
3. **[MEDIUM]** Measuring food waste before and after the intervention is challenging
   - *Impacto:* Without reliable measurement, any claimed reduction in waste cannot be validated, compromising the study's conclusions
   - *Parte Afetada:* Evaluation Methodology


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Integrar reconhecimento de imagem e leitura de código‑de‑barras via câmera do smartphone para capturar automaticamente os itens da despensa e estimar datas de validade a partir de bases de dados de validade padrão
   - *Tradeoffs:* Requer processamento local ou conexão constante à nuvem, aumentando consumo de energia e necessidade de conexão de internet, Possíveis falhas de reconhecimento em ambientes de iluminação pobre ou com embalagens não padronizadas, Privacidade dos dados de imagem deve ser gerenciada cuidadosamente
2. **Mecanismo:** Oferecer uma lista pré‑carregada de itens comuns com estimativas de validade baseadas em pesquisas de consumo, permitindo que o usuário selecione rapidamente itens e ajuste manualmente quando necessário
   - *Tradeoffs:* As estimativas padrão podem não refletir a realidade de cada usuário, gerando imprecisão nas sugestões, Depende da manutenção da base de dados para permanecer atualizada
3. **Mecanismo:** Implementar um sistema de recomendações adaptativas que apresenta múltiplas opções de receitas e coleta feedback (gostou/não gostou, praticidade) para refinar o algoritmo de sugestão ao longo do tempo
   - *Tradeoffs:* Exige mais interações do usuário inicialmente, o que pode aumentar a carga cognitiva, O algoritmo pode precisar de um período de coleta de dados antes de gerar sugestões de alta qualidade
4. **Mecanismo:** Adicionar um módulo de registro visual de desperdício onde o usuário fotografa restos de alimentos; a IA analisa a imagem para estimar quantidade e tipo de desperdício, automatizando a coleta de métricas antes e depois da intervenção
   - *Tradeoffs:* Requer que o usuário tire fotos dos resíduos, o que pode ser percebido como incômodo, Precisão da estimativa depende da qualidade da imagem e do modelo de reconhecimento


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Integrate optional image capture via smartphone camera to auto‑populate pantry items and estimate expiry dates
2. *[CANDIDATE]* Add a visual waste‑logging module where users photograph leftovers for automated waste estimation


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Manual entry of pantry items with expiry dates, generation of meal suggestions based on that data, and collection of self-reported food-waste metrics for pre- and post-intervention analysis.)

**Dependências Externas do Core:**
- Recruitment of a representative sample of small‑household cooks willing to use the app for the study duration
- Baseline measurement of participants' typical cooking habits and food‑waste levels
- Reliable self‑reporting mechanisms (e.g., daily logs or prompts) to capture waste before and after intervention
- Stable internet connectivity only for optional data backup; core functions work offline
- Ethical approval and informed consent for collecting behavioral data

**Testes Discriminativos do Core:**
- [ ] Run a randomized controlled trial where one group uses the app and a control group follows usual habits; compare pre‑ and post‑intervention waste reports
- [ ] Measure entry compliance rates by tracking frequency and completeness of pantry logs over a 4‑week period
- [ ] Conduct a usability survey to assess perceived usefulness and ease of use of the meal‑suggestion feature
- [ ] Validate self‑reported waste by spot‑checking a subset of participants with actual waste audits


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Evaluate an image‑capture prototype that auto‑populates pantry items against manual entry for accuracy and speed
- [ ] *[EXPLORATÓRIO]* Test an AI‑based visual waste‑logging module by comparing estimated waste from photos to manual weight measurements
- [ ] *[EXPLORATÓRIO]* Assess user acceptance of a pre‑loaded common‑item list with default expiry estimates versus fully manual entry
- [ ] *[EXPLORATÓRIO]* Prototype an adaptive recommendation system that learns from user feedback and compare its suggestion relevance to the rule‑based core engine


## 10. Próximo Passo Recomendado

Conduct a pilot study with a small group of target users to validate the manual entry core mechanism, assess suggestion relevance, and evaluate the feasibility of self‑reported waste tracking.
