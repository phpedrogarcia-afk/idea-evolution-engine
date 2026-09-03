# Pacote de Maturação da Ideia — Run EXP-M05.5R2-H08-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Acho que pessoas que cozinham para uma ou duas pessoas desperdiçam menos alimentos se receberem sugestões de refeições baseadas no que já têm em casa e no prazo de validade aproximado. Gostaria de testar se isso realmente muda o comportamento delas.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Testar se oferecer sugestões de refeições baseadas nos ingredientes disponíveis e na validade aproximada reduz o desperdício de alimentos e altera o comportamento de compra/cozinha desses usuários.
- **Problema Central:** Pessoas que cozinham para uma ou duas pessoas desperdiçam alimentos porque não utilizam de forma otimizada os ingredientes que já têm em casa e não consideram o prazo de validade dos mesmos.
- **Atores / Usuários:** pessoas que cozinham para uma ou duas pessoas, usuários domésticos que desejam reduzir desperdício de alimentos


## 3. Versão Refinada e Mecanismo Proposto

Oferecer sugestões de refeições personalizadas para quem cozinha para uma ou duas pessoas, usando os ingredientes que já possui em casa e a validade aproximada, com o objetivo de reduzir o desperdício de alimentos e avaliar mudanças de comportamento.


- **Justificativa de Promoção ao Core:** Baseia‑se na intenção explícita do usuário de usar dados que ele mesmo fornece, evitando dependências de hardware ou modelos de visão que não foram solicitados. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Dependência de conhecimento preciso dos usuários sobre os itens que possuem em casa
   - *Impacto:* Se os usuários não souberem ou não registrarem corretamente o que têm, as sugestões serão imprecisas, reduzindo a eficácia da solução e possivelmente aumentando o desperdício
   - *Parte Afetada:* User Input
2. **[HIGH]** Estimativa de datas de validade pelos usuários
   - *Impacto:* Datas de validade incorretas podem levar a recomendações que utilizam alimentos já estragados ou, ao contrário, descartam alimentos ainda consumíveis, comprometendo a confiança no sistema
   - *Parte Afetada:* Ingredient Metadata
3. **[MEDIUM]** Aderência dos usuários às sugestões de refeição
   - *Impacto:* A proposta assume que os usuários seguirão as recomendações; baixa aderência anulará o objetivo de reduzir desperdício e invalidará a medição de mudança de comportamento
   - *Parte Afetada:* Recommendation Engine
4. **[MEDIUM]** Medição confiável da mudança de comportamento e do desperdício
   - *Impacto:* Sem um método robusto para quantificar o desperdício antes e depois, não será possível validar a hipótese central, tornando os resultados inconclusivos
   - *Parte Afetada:* Behavior Measurement
5. **[LOW]** Privacidade e segurança dos dados de inventário doméstico
   - *Impacto:* Coletar informações detalhadas sobre alimentos em casa pode gerar preocupações de privacidade, levando a baixa participação ou a requisitos regulatórios que dificultam a implementação
   - *Parte Afetada:* Data Collection


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Integração de câmera do smartphone com reconhecimento de imagem para escanear automaticamente os itens na despensa e estimar a data de validade usando aprendizado de máquina sobre rótulos e condições de armazenamento
   - *Tradeoffs:* Necessita de acesso à câmera e permissão para processar imagens, o que pode gerar resistência por questões de privacidade, Requer treinamento de modelo de visão computacional e pode falhar com embalagens danificadas ou iluminação ruim, Custo de desenvolvimento e necessidade de dispositivos com boa capacidade de processamento
2. **Mecanismo:** Conexão com eletrodomésticos inteligentes (geladeira, armário) via APIs abertas que enviam automaticamente dados de estoque e datas de validade estimadas com base de sensores internos
   - *Tradeoffs:* Requer que o usuário possua eletrodomésticos compatíveis, limitando a adoção inicial, Dependência de terceiros (fabricantes) para manutenção das APIs e possíveis vulnerabilidades de segurança, Custo adicional para o usuário adquirir hardware inteligente
3. **Mecanismo:** Plataforma de gamificação que recompensa usuários por registrar manualmente seus ingredientes e validade, combinada com desafios semanais de receitas que utilizam itens próximos da expiração, e coleta de métricas de comportamento via consentimento explícito
   - *Tradeoffs:* Depende de motivação do usuário para registrar itens, podendo ainda haver imprecisão nas datas, Requer design de recompensas e monitoramento de métricas, aumentando complexidade de produto, Possível viés nos dados se apenas usuários altamente engajados participarem


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Conexão com eletrodomésticos inteligentes (geladeira, armário) via APIs abertas que enviam automaticamente dados de estoque e datas de validade estimadas


## 7. Propostas Rejeitadas (com Justificativa)

- **Rejeitado:** Integração de câmera do smartphone com reconhecimento de imagem para escanear automaticamente os itens na despensa e estimar a data de validade usando aprendizado de máquina (Origem: ALTERNATIVES)
  *Motivo:* Depende de modelo de visão computacional e coleta automática de imagens, o que constitui hipótese de modelo não autorizada para promoção ao núcleo
- **Rejeitado:** Conexão com eletrodomésticos inteligentes via APIs abertas que enviam automaticamente dados de estoque e datas de validade estimadas (Origem: ALTERNATIVES)
  *Motivo:* Requer hardware inteligente e APIs de terceiros, introduzindo dependências externas que não foram explicitamente solicitadas pelo usuário


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Algoritmo que gera sugestões de refeições a partir do inventário de ingredientes inserido manualmente pelo usuário e das datas de validade aproximadas fornecidas por ele.)

**Dependências Externas do Core:**
- Disponibilidade de usuários dispostos a inserir manualmente seu inventário e datas de validade aproximadas.
- Precisão razoável das datas de validade fornecidas pelos usuários (até ±3 dias).
- Acesso a uma base de dados de receitas que cubra a maioria dos ingredientes domésticos comuns.
- Infraestrutura de armazenamento segura para manter o inventário do usuário de forma persistente.

**Testes Discriminativos do Core:**
- [ ] Realizar um estudo piloto de 4‑6 semanas com 30‑50 usuários domésticos e medir a quantidade de alimentos descartados antes e depois do uso da aplicação.
- [ ] A/B test: grupo controle usando apenas lista de compras vs. grupo experimental recebendo sugestões baseadas em validade; comparar mudanças no volume de compras de itens perecíveis.
- [ ] Coletar métricas de engajamento (número de entradas de inventário por semana, taxa de aceitação das sugestões) e correlacionar com relatos de redução de desperdício.
- [ ] Entrevistas qualitativas pós‑uso para validar a percepção de utilidade das receitas sugeridas e identificar pontos de fricção na entrada manual.


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Teste de integração com geladeira inteligente via API aberta para captura automática de estoque e datas de validade estimadas; comparar precisão e engajamento contra entrada manual.
- [ ] *[EXPLORATÓRIO]* Prototipar reconhecimento de imagem usando a câmera do smartphone para escanear itens da despensa; avaliar acurácia da extração de validade e impacto na adoção.
- [ ] *[EXPLORATÓRIO]* Implementar um módulo de gamificação que recompensa usuários por registrar ingredientes; medir se a pontuação aumenta a frequência de entrada de dados e reduz o desperdício comparado ao fluxo básico.


## 10. Próximo Passo Recomendado

Desenvolver um protótipo MVP que permita ao usuário cadastrar manualmente seus ingredientes e datas de validade, gerar sugestões de refeições e conduzir um estudo piloto com um grupo pequeno de usuários para medir a redução de desperdício e a aceitação das recomendações
