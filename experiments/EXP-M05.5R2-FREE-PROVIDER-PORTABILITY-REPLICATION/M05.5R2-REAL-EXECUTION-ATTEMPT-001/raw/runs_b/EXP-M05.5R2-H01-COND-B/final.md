# Pacote de Maturação da Ideia — Run EXP-M05.5R2-H01-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Quero uma forma simples de dividir as tarefas de fechamento da minha pequena cafeteria entre três pessoas, sem precisar instalar um sistema de gestão. As tarefas mudam um pouco de dia para dia e ninguém deve ficar sempre com a parte mais chata.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Encontrar um método simples para repartir as tarefas de fechamento entre três colaboradores, garantindo rotatividade e evitando que a mesma pessoa execute sempre a tarefa menos desejada, sem necessidade de software ou sistema de gestão.
- **Problema Central:** Dividir de forma simples e justa as tarefas de fechamento da cafeteria entre três pessoas, sem usar um sistema de gestão, considerando que as tarefas variam diariamente e ninguém deve ficar sempre com a parte mais chata.
- **Atores / Usuários:** três funcionários da cafeteria


## 3. Versão Refinada e Mecanismo Proposto

Método manual simples para rotacionar as tarefas de fechamento entre três colaboradores, garantindo variação diária e evitando que a mesma pessoa execute sempre a tarefa menos desejada.


- **Justificativa de Promoção ao Core:** Atende ao desejo explícito do usuário de usar um método manual, sem necessidade de software, e permite planejamento prévio com flexibilidade para ajustes diários. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Ausência de um mecanismo formal de registro das rotações
   - *Impacto:* Sem um registro claro, é fácil que a mesma pessoa receba repetidamente a tarefa mais desagradável, gerando percepção de injustiça e desmotivação
   - *Parte Afetada:* Processo de atribuição de tarefas
2. **[HIGH]** A suposição de que a rotatividade diária garante justiça ignora a variabilidade de dificuldade das tarefas
   - *Impacto:* Algumas tarefas são intrinsecamente mais pesadas ou indesejáveis; rotacionar diariamente pode ainda resultar em carga desigual, comprometendo a equidade
   - *Parte Afetada:* Mecanismo de justiça/fairness
3. **[MEDIUM]** Falta de plano de contingência para ausências ou atrasos dos colaboradores
   - *Impacto:* Se um colaborador falta, a rotação quebra e pode deixar tarefas críticas sem responsável, impactando o fechamento da cafeteria
   - *Parte Afetada:* Continuidade operacional


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Quadro branco dividido em três colunas, uma para cada colaborador, com cartões de data que são movidos diariamente para indicar quem realiza a tarefa de fechamento; um registro de rotação é mantido em um caderno ao lado.
   - *Tradeoffs:* Requer atualização manual diária, Necessita de espaço físico dedicado, Dependente da disciplina de quem move os cartões
2. **Mecanismo:** Sistema de fichas coloridas: cada colaborador tem uma ficha; ao final de cada dia, as fichas são embaralhadas em um pote e a ficha tirada determina quem assume a tarefa de fechamento no próximo dia; as escolhas são anotadas em um registro de papel.
   - *Tradeoffs:* Aleatoriedade pode gerar sequências desfavoráveis, Fichas podem ser perdidas ou confundidas, Não controla a dificuldade específica das tarefas
3. **Mecanismo:** Calendário impresso mensal com linhas para cada dia e colunas para os três colaboradores; antes do mês começar, preenche-se a rotação considerando a carga de trabalho estimada; uma coluna extra indica o colaborador de reserva para cobrir ausências.
   - *Tradeoffs:* Precisa de planejamento prévio que pode não refletir mudanças inesperadas, Impressão e atualização manual, Reserva fixa pode não ser ideal para todas as ausências


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Quadro branco dividido em três colunas, com cartões de data movidos diariamente para indicar quem realiza a tarefa de fechamento; registro da rotação mantido em um caderno ao lado.


## 7. Propostas Rejeitadas (com Justificativa)

- **Rejeitado:** Sistema de fichas coloridas: fichas embaralhadas em um pote para determinar quem assume a tarefa de fechamento no próximo dia. (Origem: ALTERNATIVES)
  *Motivo:* Introduz aleatoriedade que pode gerar sequências desfavoráveis e risco de perda ou confusão das fichas, contrariando a necessidade de previsibilidade do usuário.


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Calendário impresso mensal com linhas para cada dia e colunas para os três colaboradores; antes do mês começar, preenche‑se a rotação considerando a carga de trabalho estimada e inclui‑se uma coluna reserva para cobrir ausências.)

**Dependências Externas do Core:**
- Disponibilidade de um calendário impresso com espaço suficiente para linhas de dias e colunas de colaboradores
- Precisão na estimativa da carga de trabalho antes do início do mês
- Compromisso dos colaboradores em seguir a rotação predefinida
- Um colaborador reserva identificado e disponível para cobrir ausências

**Testes Discriminativos do Core:**
- [ ] Conduzir um piloto de 30 dias com três colaboradores usando o calendário impresso e registrar quem realiza a tarefa de fechamento a cada dia; analisar a distribuição para verificar se há equilíbrio
- [ ] Simular ausências inesperadas (ex.: 2 dias de falta) e observar se a coluna reserva cobre adequadamente sem necessidade de replanejamento adicional
- [ ] Comparar a percepção de justiça dos colaboradores antes e depois da implementação do calendário para validar a aceitação do método


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Implementar um quadro branco dividido em três colunas com cartões de data movidos diariamente para indicar quem realiza a tarefa de fechamento; avaliar a flexibilidade e aceitação da equipe
- [ ] *[EXPLORATÓRIO]* Utilizar um sistema de fichas coloridas onde as fichas são embaralhadas diariamente em um pote e a ficha tirada determina o responsável; monitorar a aleatoriedade e a percepção de justiça


## 10. Próximo Passo Recomendado

Imprimir o calendário mensal, definir a rotação inicial baseada na carga estimada, treinar a equipe para atualização diária e estabelecer um plano de contingência simples (ex.: colaborador reserva) para ausências inesperadas.
