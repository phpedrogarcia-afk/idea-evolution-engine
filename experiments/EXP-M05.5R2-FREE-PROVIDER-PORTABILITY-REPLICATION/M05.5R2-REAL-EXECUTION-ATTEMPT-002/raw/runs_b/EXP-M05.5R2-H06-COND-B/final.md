# Pacote de Maturação da Ideia — Run EXP-M05.5R2-H06-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> O nosso clube de leitura recebe poucos lugares para encontros presenciais e temos de decidir quem participa quando há mais interessados do que vagas. Não quero que vire uma disputa por rapidez de inscrição, mas também não sei qual critério seria justo para todos.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Find a fair criterion for selecting participants that does not turn into a race based on rapid sign‑up and is acceptable to all members.
- **Problema Central:** The reading club has limited in‑person meeting spots, leading to a situation where more members want to attend than there are available places, creating a need for a fair allocation method.
- **Atores / Usuários:** Reading club members, Club organizers or coordinators


## 3. Versão Refinada e Mecanismo Proposto

Implement a fixed rotating schedule with a shared calendar and limited sign‑up windows, complemented by a randomized weighted lottery per cycle to allocate spots fairly.


- **Justificativa de Promoção ao Core:** Ensures each member gets a predictable turn while preventing race conditions; aligns directly with the user's desire for a fair, non‑racing allocation. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Absence of a concrete allocation algorithm
   - *Impacto:* Without a defined mechanism (e.g., lottery, rotating schedule, points system) the club cannot implement the promised fairness, leading to ad‑hoc decisions that may be perceived as biased.
   - *Parte Afetada:* Allocation Process
2. **[MEDIUM]** Potential for perceived inequity in rotating attendance
   - *Impacto:* Rotating spots assumes equal interest over time, but members may have varying availability or desire to attend specific sessions, causing dissatisfaction and possible attrition.
   - *Parte Afetada:* Attendance Scheduling


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Randomized weighted lottery per cycle, where each member receives a number of tickets proportional to how many times they have attended recently; a computer draws the winners for each sign‑up window
   - *Tradeoffs:* Introduces randomness that some may view as less predictable, Requires tracking of past attendance and a fair random number generator, May be perceived as unfair by members who prefer deterministic order
2. **Mecanismo:** Points‑based credit system: members earn credits each time they attend a meeting and spend credits to secure a spot in upcoming sign‑up windows; the schedule still rotates but priority is given to those with higher credit balances
   - *Tradeoffs:* Adds administrative overhead to track and update credit balances, May incentivize over‑attendance, creating burnout risk, Potential for gaming the system if credits are not carefully managed
3. **Mecanismo:** Blockchain‑backed smart contract that enforces a deterministic round‑robin allocation with cryptographic timestamps; each sign‑up window is recorded immutably, and the contract automatically rejects entries that would break the rotation
   - *Tradeoffs:* Requires technical expertise and infrastructure to deploy and maintain the smart contract, Members must learn to interact with the blockchain interface, Potential latency or cost issues depending on the chosen platform


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Points‑based credit system: members earn credits for attendance and spend them to secure spots, with rotating schedule as fallback.
2. *[CANDIDATE]* Blockchain‑backed smart contract enforcing deterministic round‑robin allocation with cryptographic timestamps.


## 7. Propostas Rejeitadas (com Justificativa)

- **Rejeitado:** Blockchain‑backed smart contract that enforces deterministic round‑robin allocation with cryptographic timestamps. (Origem: ALTERNATIVES)
  *Motivo:* Requires technical expertise and infrastructure beyond the club's capacity, and introduces learning curve for members.


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Fixed rotating schedule with shared calendar and limited sign‑up windows)

**Dependências Externas do Core:**
- A shared digital calendar platform that all members can access and edit
- Automated notification system (email or push) to alert members when their sign‑up window opens and closes
- Agreement among members on the length of each sign‑up window and the rotation order
- Reliable time‑zone handling to ensure all members see the same window times
- Procedures for handling missed sign‑ups (e.g., automatic pass‑over to next member)

**Testes Discriminativos do Core:**
- [ ] Run a controlled simulation of two full rotation cycles with a representative group of members and record sign‑up timestamps to verify that no member signs up outside their allocated window
- [ ] Introduce a deliberate missed sign‑up and observe whether the system correctly passes the slot to the next member in the rotation
- [ ] Measure the distribution of sign‑up attempts before and after implementing limited windows to confirm a reduction in peak sign‑up traffic
- [ ] Survey participants after a trial period to assess perceived fairness versus the previous lottery approach


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Prototype a points‑based credit system layered on top of the rotating schedule and test whether credit accumulation influences spot allocation without breaking rotation integrity
- [ ] *[EXPLORATÓRIO]* Develop a blockchain smart‑contract prototype that records sign‑up windows and enforces round‑robin allocation; evaluate its performance and usability compared to the calendar‑based implementation


## 10. Próximo Passo Recomendado

Run a pilot cycle using the rotating schedule with limited sign‑up windows and the weighted lottery, monitor member feedback, and refine the ticket allocation rules before full rollout.
