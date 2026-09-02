# Pacote de Maturação da Ideia — Run EXP-M05.5R1-H08-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Acho que pessoas que cozinham para uma ou duas pessoas desperdiçam menos alimentos se receberem sugestões de refeições baseadas no que já têm em casa e no prazo de validade aproximado. Gostaria de testar se isso realmente muda o comportamento delas.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** To test whether giving such tailored meal suggestions changes users' behavior and reduces food waste.
- **Problema Central:** People cooking for one or two persons may waste food because they lack meal suggestions that utilize the ingredients they already have and consider the approximate expiration dates of those ingredients.
- **Atores / Usuários:** Individuals cooking for one or two people, Researchers conducting the test


## 3. Versão Refinada e Mecanismo Proposto

Test whether providing personalized meal suggestions based on users' manually entered pantry items and their approximate expiration dates reduces food waste among individuals cooking for one or two people.


- **Justificativa de Promoção ao Core:** This mechanism directly follows the user's expressed desire for a low‑effort solution that relies on user‑provided data, avoiding complex hardware or AI image processing while still enabling targeted suggestions to reduce waste. (Base: `VALID_USER_DERIVATION`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Reliance on user‑provided pantry data that may be incomplete or inaccurate
   - *Impacto:* Incorrect ingredient lists can lead to unsuitable meal suggestions, causing increased waste or even health risks
   - *Parte Afetada:* Data collection & suggestion engine
2. **[HIGH]** Difficulty measuring food waste accurately
   - *Impacto:* Self‑reported waste is prone to bias, making it impossible to validate the core hypothesis of waste reduction
   - *Parte Afetada:* Metrics & evaluation
3. **[MEDIUM]** User willingness to follow suggested meals is uncertain
   - *Impacto:* If users ignore suggestions due to taste, time, or habit, the system cannot achieve its intended impact
   - *Parte Afetada:* User behavior
4. **[MEDIUM]** Privacy concerns around sharing pantry inventories
   - *Impacto:* Reluctance to provide detailed ingredient data may limit data availability, undermining the system’s functionality
   - *Parte Afetada:* Privacy & data access


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Implement a smartphone‑based image capture system that uses AI to recognize pantry items and estimate expiration dates from photos taken by the user
   - *Tradeoffs:* Requires users to take photos regularly, increasing effort, AI recognition may misidentify items or miss small packages, Images are stored or processed, raising additional privacy considerations
2. **Mecanismo:** Partner with grocery store loyalty programs and smart‑container IoT devices to automatically import purchase data and monitor weight/temperature changes that infer consumption and expiration
   - *Tradeoffs:* Requires commercial partnerships and user consent for data sharing, IoT hardware adds cost and may have adoption barriers, Potential technical failures in weight/temperature sensing could produce inaccurate data
3. **Mecanismo:** Introduce a gamified suggestion platform that offers points, badges, or discounts for following meal plans and for users to log leftover quantities via quick taps, using statistical models to estimate overall waste reduction
   - *Tradeoffs:* Self‑reported data can be biased or incomplete, Gamification may attract users primarily for rewards rather than genuine behavior change, Incentive costs need to be covered by sponsors or ads


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Smartphone image capture with AI to automatically recognize pantry items and estimate expiration dates
2. *[CANDIDATE]* Integration with grocery loyalty programs and IoT smart containers to auto‑import purchase and consumption data
3. *[CANDIDATE]* Gamified platform offering points, badges, or discounts for following meal plans and logging leftovers


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: A web/mobile app that lets users manually input the items they have at home and their estimated expiration dates, then generates personalized meal suggestions that use those items before they spoil.)

**Dependências Externas do Core:**
- Consistent user input of pantry items and expiration dates
- Accurate mapping of entered items to recipes that use them before spoilage
- Access to a comprehensive recipe database with ingredient quantities
- Ability to track food waste (e.g., self‑reported waste logs) for measurement
- Internet connectivity for data sync and app updates

**Testes Discriminativos do Core:**
- [ ] Conduct a 4‑week randomized controlled trial where one group uses the app and a control group does not; measure food waste via weekly waste logs
- [ ] Perform usability testing on the manual entry flow with 20 participants; assess time taken and error rate
- [ ] Run an algorithm validation study comparing suggested meals to actual pantry contents to ensure ingredient match before expiry
- [ ] Survey participants after app use to evaluate satisfaction with meal suggestions and perceived waste reduction


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Prototype AI‑based image capture to auto‑populate pantry items and compare entry time versus manual entry
- [ ] *[EXPLORATÓRIO]* Pilot integration with a grocery loyalty program to auto‑import purchase data and assess impact on inventory accuracy
- [ ] *[EXPLORATÓRIO]* Implement a gamified points system and test its effect on user engagement and frequency of waste reporting


## 10. Próximo Passo Recomendado

Build a minimal viable product of the manual‑entry suggestion app, recruit a small pilot group of 20‑30 individuals cooking for one or two people, collect baseline waste data, run the intervention for 4 weeks, and evaluate changes in reported food waste.
