# Pacote de Maturação da Ideia — Run EXP-M05.5R2-H01-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Quero uma forma simples de dividir as tarefas de fechamento da minha pequena cafeteria entre três pessoas, sem precisar instalar um sistema de gestão. As tarefas mudam um pouco de dia para dia e ninguém deve ficar sempre com a parte mais chata.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Encontrar um método simples e manual para distribuir as tarefas de fechamento entre três funcionários, com rotação ou variação diária, sem necessidade de instalar software ou ferramentas digitais.
- **Problema Central:** Dividir de forma simples e justa as tarefas de fechamento da cafeteria entre três pessoas, evitando que a mesma pessoa execute sempre a tarefa mais desagradável, sem usar um sistema de gestão formal.
- **Atores / Usuários:** Proprietário da cafeteria, Funcionário 1, Funcionário 2, Funcionário 3


## 3. Versão Refinada e Mecanismo Proposto

Método manual simples usando um quadro de tarefas com tokens coloridos que indicam o grau de desagradabilidade da tarefa de fechamento, rotacionado diariamente entre os três funcionários, garantindo que a carga percebida seja considerada na rotação.


- **Justificativa de Promoção ao Core:** Esta solução atende diretamente à intenção humana de um processo manual, visual e sem necessidade de software, ao mesmo tempo que tenta equilibrar a distribuição das tarefas mais desagradáveis. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** A rotação manual pode falhar em garantir justiça quando as tarefas variam em grau de desagradabilidade
   - *Impacto:* Sem um mecanismo objetivo para classificar a dificuldade de cada tarefa, a percepção dos funcionários pode divergir, gerando ressentimento e diminuição da moral
   - *Parte Afetada:* Mecanismo de distribuição de tarefas
2. **[MEDIUM]** Dependência de atualização diária manual aumenta risco de erro humano
   - *Impacto:* Se a lista não for atualizada corretamente, a pessoa designada pode acabar recebendo a tarefa mais chata repetidamente, contrariando o objetivo principal
   - *Parte Afetada:* Processo de manutenção da lista
3. **[MEDIUM]** Ausência de um mecanismo de verificação ou penalidade para não‑conformidade
   - *Impacto:* Funcionários podem simplesmente ignorar a rotação se acharem conveniente, pois não há controle nem consequência, comprometendo a eficácia do método
   - *Parte Afetada:* Compliance do esquema de rotação


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Quadro de tarefas com tokens coloridos que indicam o grau de desagradabilidade da tarefa; ao final do dia, o token é passado para o próximo funcionário, garantindo que a rotação leve em conta a carga percebida
   - *Tradeoffs:* Requer a criação e manutenção de tokens coloridos e um pequeno esforço de registro diário, Ainda depende de disciplina humana para mover o token corretamente, Pode gerar confusão se os funcionários não concordarem sobre a classificação de desagradabilidade
2. **Mecanismo:** Sistema de rolagem de dados: cada manhã os três funcionários rolam um dado de seis faces; o número mais alto recebe a tarefa de fechamento, com a regra de que nenhum funcionário pode ter mais de duas atribuições de fechamento em uma semana, anotado em um registro simples de papel
   - *Tradeoffs:* A aleatoriedade pode ainda gerar distribuições ligeiramente desiguais em semanas curtas, Exige um registro semanal para monitorar o limite de duas atribuições, Necessita de um dado físico e de um local para registrar as rolagens
3. **Mecanismo:** Quadro magnético semanal com cartões pré‑definidos de rotação; inclui cartões de "troca" que permitem que um funcionário troque a tarefa de fechamento com outro colega, desde que a troca seja registrada em uma folha de controle
   - *Tradeoffs:* Requer impressão ou criação dos cartões e a folha de controle de trocas, Depende da boa-fé dos funcionários para registrar trocas corretamente, Pode introduzir atrasos se as trocas precisarem de aprovação


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Checklist diário impresso para verificação de conformidade após a troca de token
2. *[CANDIDATE]* Uso de um registro semanal em papel para monitorar a distribuição das tarefas e ajustar manualmente as rotações


## 7. Propostas Rejeitadas (com Justificativa)

- **Rejeitado:** Sistema de rolagem de dados diário, onde o número mais alto recebe a tarefa de fechamento, com limite de duas atribuições por semana (Origem: ALTERNATIVES)
  *Motivo:* Requer uso de dado físico e registro semanal adicional, aumentando a complexidade e o risco de erro humano
- **Rejeitado:** Quadro magnético semanal com cartões pré‑definidos de rotação e cartões de troca para ajustes manuais (Origem: ALTERNATIVES)
  *Motivo:* Exige produção de cartões e depende de boa‑fé para registrar trocas, introduzindo atrasos e potencial confusão


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Quadro de tarefas com tokens coloridos que indicam o grau de desagradabilidade da tarefa; ao final do dia o token é passado para o próximo funcionário, assegurando rotação diária baseada na carga percebida.)

**Dependências Externas do Core:**
- Um quadro de tarefas fixo em local visível para todos os funcionários.
- Um conjunto de tokens coloridos (ex.: verde, amarelo, vermelho) cujas cores estejam previamente definidas como indicadores de carga percebida.
- Procedimento escrito que descreva como atribuir cores aos tokens antes do início da rotação.
- Compromisso dos três funcionários de trocar o token ao final de cada dia de trabalho.
- Um local de armazenamento seguro para o token durante a troca para evitar perda ou dano.

**Testes Discriminativos do Core:**
- [ ] Conduzir um piloto de 2 semanas com os três funcionários, registrando diariamente quem recebeu o token e coletando uma pesquisa de percepção de justiça ao final da semana.
- [ ] Medir a taxa de cumprimento da troca do token (percentual de dias em que a troca ocorreu corretamente) durante o piloto.
- [ ] Comparar o número de vezes que cada funcionário realizou a tarefa de fechamento antes e depois da implementação do sistema para verificar equilíbrio de carga.


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Testar a inclusão de um checklist impresso diário para verificação de conformidade após a troca do token, avaliando se melhora a aderência ao processo.
- [ ] *[EXPLORATÓRIO]* Implementar um registro semanal em papel para monitorar a distribuição das tarefas e ajustar manualmente as rotações, observando se isso aumenta a percepção de equidade.
- [ ] *[EXPLORATÓRIO]* Experimentar um conjunto alternativo de tokens (ex.: formas diferentes em vez de cores) para avaliar se a representação visual afeta a clareza e a aceitação do método.


## 10. Próximo Passo Recomendado

Criar o quadro de tarefas e os tokens coloridos, definir claramente o significado de cada cor, treinar a equipe sobre o uso diário, iniciar um período piloto de uma semana e coletar feedback para ajustar o processo se necessário
