# Pacote de Maturação da Ideia — Run EXP-M05.5-REP-02-COND-B

**Status:** `FAILED` | **Ciclos de Reconstrução:** 0

---

## 1. Ideia Original (Imutável)

> Um lugar digital para guardar perguntas que ainda não têm resposta, deixando-as reaparecer ocasionalmente sem categorias, metas ou obrigação de concluí-las.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Criar um espaço digital para guardar perguntas ainda não respondidas, permitindo que reapareçam ocasionalmente, sem necessidade de categorização, metas ou obrigação de concluí‑las.
- **Problema Central:** Falta de um local digital onde perguntas sem resposta possam ser armazenadas e revisitadas, evitando que se percam e sem imposição de categorias ou metas.
- **Atores / Usuários:** usuários que têm perguntas não respondidas, pessoas curiosas que desejam revisitar questões, qualquer pessoa interessada em guardar dúvidas


## 3. Versão Refinada e Mecanismo Proposto

Um serviço digital que permite aos usuários salvar perguntas sem resposta em um repositório sem categorias nem metas, apresentando-as novamente de forma esporádica, sem exigir que sejam respondidas.


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Lack of categorization makes retrieval inefficient
   - *Impacto:* Users cannot locate specific unanswered questions later, reducing utility
   - *Parte Afetada:* User experience / Retrieval system
2. **[MEDIUM]** Random resurfacing may annoy users
   - *Impacto:* Frequent irrelevant prompts can cause disengagement and churn
   - *Parte Afetada:* Notification system
3. **[MEDIUM]** No incentive to answer leads to accumulation of stale questions
   - *Impacto:* Repository becomes cluttered, diminishing perceived value
   - *Parte Afetada:* Content quality
4. **[HIGH]** Potential privacy concerns with storing personal questions
   - *Impacto:* Sensitive data could be exposed if security is insufficient
   - *Parte Afetada:* Data storage


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Permitir que usuários adicionem tags opcionais livres ao salvar a pergunta, usando correspondência difusa para agrupar perguntas semelhantes sem impor categorias rígidas
   - *Tradeoffs:* Introduz leve complexidade na interface de salvamento, Risco de que usuários criem tags excessivas que se aproximem de categorização tradicional
2. **Mecanismo:** Algoritmo de resurfacing personalizado que prioriza perguntas com base no histórico de engajamento do usuário e intervalos de tempo ajustáveis pelo próprio usuário
   - *Tradeoffs:* Requer processamento adicional para analisar padrões de uso, Pode criar viés se o algoritmo favorecer certos tipos de perguntas
3. **Mecanismo:** Sistema de recompensas anônimas onde perguntas podem receber 'bounties' de pontos virtuais que são concedidos ao primeiro usuário que responder, com opção de criptografar o conteúdo da pergunta para privacidade
   - *Tradeoffs:* Pode atrair respostas de baixa qualidade motivadas apenas por pontos, Implementação de criptografia aumenta a complexidade técnica


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* aplicativo móvel
2. *[CANDIDATE]* site web
3. *[CANDIDATE]* extensão de navegador
4. *[CANDIDATE]* serviço online


## 10. Próximo Passo Recomendado

Definir próximo experimento com usuários.
