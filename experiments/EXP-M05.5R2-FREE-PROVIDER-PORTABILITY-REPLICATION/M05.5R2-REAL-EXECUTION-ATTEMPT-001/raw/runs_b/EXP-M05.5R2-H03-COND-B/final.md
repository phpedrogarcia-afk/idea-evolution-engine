# Pacote de Maturação da Ideia — Run EXP-M05.5R2-H03-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Na minha cidade, muita gente deixa de usar a praça perto da estação depois do fim da tarde. Acho que pode ser porque ela parece insegura, mas também pode ser porque não há nada que convide as pessoas a permanecer ali. Queria explorar uma ideia para mudar isso.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Explorar ideias que tornem a praça mais segura e atrativa, incentivando seu uso pelos moradores e usuários da estação.
- **Problema Central:** A praça próxima à estação tem baixa frequência de uso após o fim da tarde, possivelmente devido à percepção de insegurança e à falta de elementos que incentivem as pessoas a permanecerem lá.
- **Atores / Usuários:** Moradores da cidade, Usuários da estação de transporte, Visitantes da região, Autoridades municipais responsáveis por espaços públicos, Organizadores comunitários


## 3. Versão Refinada e Mecanismo Proposto

Implementar um programa de eventos comunitários ao entardecer na praça, utilizando iluminação portátil e voluntários locais, com presença policial limitada, para gerar vigilância natural e tornar o espaço mais seguro e atrativo após o fim da tarde.


- **Justificativa de Promoção ao Core:** Alinha‑se diretamente com a intenção humana de melhorar a percepção de segurança e atratividade da praça, promovendo a ocupação do espaço por moradores e usuários da estação. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** A percepção de insegurança é tratada como a causa principal da baixa frequência, sem evidência empírica que confirme essa relação.
   - *Impacto:* Se a insegurança não for o fator dominante, investimentos em iluminação, vigilância ou policiamento podem não gerar aumento de uso, desperdiçando recursos públicos.
   - *Parte Afetada:* Análise de percepção dos usuários
2. **[MEDIUM]** Suposição de que há recursos ou vontade política suficiente para implementar mudanças.
   - *Impacto:* Sem apoio financeiro ou político, quaisquer propostas de melhoria podem ficar estagnadas, tornando a ideia inviável a longo prazo.
   - *Parte Afetada:* Viabilidade de implementação


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Instalar iluminação LED de baixa energia com sensores de movimento que se ativam ao detectar presença, integrando um sistema de coleta de dados de fluxo de pessoas e incidentes para validar a relação entre percepção de insegurança e uso da praça
   - *Tradeoffs:* Custo inicial de hardware e manutenção tecnológica, Dependência de conectividade e possíveis falhas de sensores, Necessidade de treinamento para análise dos dados coletados
2. **Mecanismo:** Organizar dias mensais de mercado pop‑up com vendedores locais e atividades culturais, usando espaços já existentes e patrocinadores privados, acompanhados de pesquisas de percepção de segurança antes e depois dos eventos
   - *Tradeoffs:* Dependência da disponibilidade de vendedores e patrocinadores, Impacto temporário que pode não gerar mudança de longo prazo, Necessidade de logística para montagem e desmontagem dos eventos
3. **Mecanismo:** Desenvolver um aplicativo comunitário de vigilância colaborativa, onde moradores registram observações e relatam incidentes em tempo real, com recompensas gamificadas e integração a um painel público de segurança na praça
   - *Tradeoffs:* Risco de privacidade e necessidade de moderação de conteúdo, Possível baixa adesão inicial sem incentivos claros, Manutenção da plataforma tecnológica e suporte técnico


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Instalar iluminação LED de baixa energia com sensores de movimento que se ativam ao detectar presença, integrando coleta de dados de fluxo de pessoas e incidentes
2. *[CANDIDATE]* Organizar dias mensais de mercado pop‑up com vendedores locais e atividades culturais, patrocinados por empresas privadas


## 7. Propostas Rejeitadas (com Justificativa)

- **Rejeitado:** Desenvolver um aplicativo comunitário de vigilância colaborativa com recompensas gamificadas (Origem: ALTERNATIVES)
  *Motivo:* Apresenta riscos de privacidade, necessidade de moderação intensiva e baixa adesão inicial, não sendo prioritário para o objetivo imediato de melhorar a segurança percebida


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Programa de eventos comunitários ao entardecer com iluminação portátil, voluntários locais e presença policial limitada)

**Dependências Externas do Core:**
- Disponibilidade e quantidade suficiente de iluminação portátil (ex.: lanternas, refletores)
- Base de voluntários comprometidos a permanecer durante o evento
- Aprovação da polícia para reduzir a presença oficial durante o horário do evento
- Permissão da prefeitura para ocupação da praça à noite
- Condições meteorológicas favoráveis no dia do evento

**Testes Discriminativos do Core:**
- [ ] Realizar um piloto de evento em uma sexta‑feira ao entardecer e registrar o número de pessoas presentes (contagem manual ou via sensores temporários)
- [ ] Aplicar questionário de percepção de segurança antes e depois do piloto para comparar mudanças
- [ ] Coletar dados de incidentes policiais reportados na praça durante o dia do piloto e compará‑los com dias sem evento
- [ ] Variar a intensidade da iluminação portátil (ex.: 2 lux vs 5 lux) e medir o efeito na percepção de segurança dos participantes
- [ ] Testar diferentes esquemas de turnos de voluntários (ex.: 2 h vs 4 h) e avaliar a continuidade da vigilância


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Instalar iluminação LED de baixa energia com sensores de movimento e comparar a coleta de dados de fluxo de pessoas e incidentes com o modelo de iluminação portátil tradicional
- [ ] *[EXPLORATÓRIO]* Organizar um dia mensal de mercado pop‑up com vendedores locais e atividades culturais, medindo o impacto na segurança percebida e no uso da praça
- [ ] *[EXPLORATÓRIO]* Desenvolver um aplicativo de vigilância colaborativa onde moradores registram observações em tempo real, avaliando sua adoção e efeito sobre a taxa de incidentes


## 10. Próximo Passo Recomendado

Planejar e executar um piloto de um evento comunitário ao entardecer na praça, definindo data, recrutando voluntários, garantindo iluminação portátil e coordenando apoio policial; coletar feedback dos participantes sobre sensação de segurança e número de presentes para validar a eficácia da abordagem.
