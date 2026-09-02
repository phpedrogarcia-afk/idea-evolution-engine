# Pacote de Maturação da Ideia — Run EXP-M05.5R1-H08-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Acho que pessoas que cozinham para uma ou duas pessoas desperdiçam menos alimentos se receberem sugestões de refeições baseadas no que já têm em casa e no prazo de validade aproximado. Gostaria de testar se isso realmente muda o comportamento delas.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Test whether providing meal suggestions based on existing pantry items and their approximate expiration dates changes cooking behavior and reduces food waste.
- **Problema Central:** People who cook for one or two individuals tend to waste food because they lack meal suggestions that take into account the ingredients they already have at home and the approximate expiration dates of those ingredients.
- **Atores / Usuários:** Home cooks preparing meals for one or two people, Researchers conducting the behavior test


## 3. Versão Refinada e Mecanismo Proposto

For individuals cooking for one or two people, provide personalized meal suggestions based on manually entered pantry items and their approximate expiration dates, and test whether this reduces food waste and changes cooking behavior.


- **Justificativa de Promoção ao Core:** This mechanism directly reflects the user's explicit intent to evaluate how manual pantry‑based suggestions influence cooking habits and food waste, without adding speculative hardware or algorithmic components. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Dependência de relatórios precisos dos usuários sobre ingredientes e datas de validade
   - *Impacto:* Dados imprecisos comprometem a qualidade das sugestões de refeições, resultando em recomendações inadequadas que podem aumentar, em vez de reduzir, o desperdício de alimentos.
   - *Parte Afetada:* Coleta de dados do usuário / Entrada de inventário
2. **[MEDIUM]** Medição inadequada da redução de desperdício de alimentos
   - *Impacto:* Sem métricas confiáveis, não será possível validar se a solução realmente diminui o desperdício, tornando os resultados do teste inconclusivos.
   - *Parte Afetada:* Metodologia de avaliação / Métricas de desperdício
3. **[MEDIUM]** Baixa adesão dos usuários às sugestões de refeições geradas
   - *Impacto:* Mesmo com sugestões relevantes, fatores como preferências pessoais, tempo de preparo e hábitos alimentares podem impedir que os usuários sigam as recomendações, limitando o impacto da solução.
   - *Parte Afetada:* Comportamento do usuário / Interface de recomendação


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Integrar sensores de peso e RFID/barcode nas despensas para capturar automaticamente os itens e suas datas de validade, eliminando a necessidade de relatórios manuais dos usuários.
   - *Tradeoffs:* Custo adicional de hardware e instalação, Necessidade de manutenção dos sensores, Possíveis preocupações de privacidade com coleta automática de dados
2. **Mecanismo:** Adicionar elementos de gamificação (pontos, badges, desafios semanais) e integração com redes sociais para incentivar o uso das sugestões, além de instalar balanças inteligentes nas lixeiras para medir quantitativamente o desperdício de alimentos.
   - *Tradeoffs:* Complexidade de desenvolvimento da camada de gamificação, Dependência de hardware adicional nas lixeiras, Risco de foco excessivo em recompensas ao invés de comportamento sustentável
3. **Mecanismo:** Empregar aprendizado de máquina para prever datas de validade com base em histórico de compras e tipos de alimentos, reduzindo a necessidade de entrada manual, e conduzir um experimento A/B rigoroso (grupo controle vs. intervenção) para medir a mudança de comportamento e a redução de desperdício.
   - *Tradeoffs:* Precisão das previsões pode ser inferior à informação fornecida pelo usuário, Necessidade de grandes volumes de dados de compra para treinar os modelos, Possível viés algorítmico que afete recomendações


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Integrar sensores de peso e RFID/barcode nas despensas para capturar automaticamente os itens e suas datas de validade, eliminando a necessidade de relatórios manuais dos usuários.
2. *[CANDIDATE]* Adicionar elementos de gamificação (pontos, badges, desafios semanais) e integração com redes sociais para incentivar o uso das sugestões, além de instalar balanças inteligentes nas lixeiras para medir quantitativamente o desperdício de alimentos.
3. *[CANDIDATE]* Empregar aprendizado de máquina para prever datas de validade com base em histórico de compras e tipos de alimentos, reduzindo a necessidade de entrada manual, e conduzir um experimento A/B rigoroso (grupo controle vs. intervenção) para medir a mudança de comportamento e a redução de desperdício.


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Provide personalized meal suggestions based on manually entered pantry items and their approximate expiration dates for individuals cooking for one or two people.)

**Dependências Externas do Core:**
- Recruit participants who cook for one or two people and are willing to log pantry items daily
- Develop a mobile/web interface for manual entry of items and expiration dates
- Implement a method to capture cooking behavior (e.g., meal logs, recipe selections)
- Establish a baseline measurement of food waste (self‑report, weight of trash, or photo diary)
- Access to statistical analysis tools for comparing intervention vs control groups

**Testes Discriminativos do Core:**
- [ ] Run a randomized controlled trial (2‑week pilot) where the intervention group receives personalized meal suggestions and the control group receives generic suggestions; measure changes in cooking frequency, recipe diversity, and self‑reported food waste
- [ ] Conduct a usability study of the manual entry interface to assess time per entry, error rate, and user satisfaction
- [ ] Perform a validation study comparing user‑entered expiration dates with actual product dates (e.g., by scanning barcodes for a subset of items)
- [ ] Implement a waste‑tracking protocol (kitchen trash weight before/after meals) to quantify waste reduction attributable to the suggestions


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Prototype RFID/weight‑sensor equipped pantry shelves and evaluate detection accuracy and latency for automatic item capture
- [ ] *[EXPLORATÓRIO]* Add gamification elements (points, badges, weekly challenges) to the suggestion app and run an A/B test measuring engagement metrics and repeat usage
- [ ] *[EXPLORATÓRIO]* Develop a machine‑learning model that predicts expiration dates from purchase history; test its prediction error against manually entered dates in a controlled dataset


## 10. Próximo Passo Recomendado

Realizar um estudo piloto com um pequeno grupo de usuários, utilizando o mecanismo manual de sugestões e o desenho experimental A/B, coletando dados de uso e de desperdício para validar a hipótese central.
