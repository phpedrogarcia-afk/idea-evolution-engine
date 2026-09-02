# Baseline de Refinamento de Ideia — EXP-M05.5R1-H08-COND-A

## Ideia Original
> Acho que pessoas que cozinham para uma ou duas pessoas desperdiçam menos alimentos se receberem sugestões de refeições baseadas no que já têm em casa e no prazo de validade aproximado. Gostaria de testar se isso realmente muda o comportamento delas.

## Resumo do Modelo
A proposta visa reduzir o desperdício de alimentos em domicílios de uma ou duas pessoas ao oferecer sugestões de refeições personalizadas com base nos itens já disponíveis em casa e nas datas de validade aproximadas, testando se essa intervenção altera o comportamento de compra e consumo.

## Versão Refinada
Desenvolver um aplicativo móvel que permita ao usuário registrar seu estoque doméstico via escaneamento de código de barras ou inserção manual, atribua datas de validade estimadas e, usando um algoritmo de IA, gere planos de refeição para 1‑2 porções priorizando ingredientes próximos da expiração. O app inclui porções ajustáveis, lista de compras para itens faltantes, feedback gamificado sobre a redução de desperdício e um painel de métricas. Para validar a eficácia, conduzir um estudo controlado randomizado comparando usuários do app com um grupo de controle que não recebe sugestões, medindo mudanças no volume de resíduos alimentares e nos padrões de compra ao longo de 8‑12 semanas.

## Pontos Fortes e Fracos
- **Fortes:** Aborda um problema ambiental relevante (desperdício de alimentos), Foco em pequenos domicílios, nicho muitas vezes negligenciado, Personalização aumenta relevância e engajamento do usuário, Uso de dados de estoque e validade permite otimização de consumo, Potencial para integração com tecnologias existentes (scanners de código de barras, IA de receitas), Métricas de impacto claras (redução de resíduos, mudança de comportamento)
- **Fracos:** Necessidade de que o usuário registre manualmente ou escaneie itens, o que pode ser percebido como esforço extra, Precisão das datas de validade pode ser limitada sem integração direta com embalagens inteligentes, Privacidade e segurança dos dados de inventário doméstico, Possível resistência à mudança de hábitos alimentares mesmo com sugestões, Desafio de criar receitas atrativas para porções pequenas sem desperdiçar ingredientes, Escalabilidade e manutenção de um banco de receitas atualizado

## Próximos Passos
Realizar entrevistas e pesquisas com consumidores de 1‑2 pessoas para validar a necessidade e identificar barreiras de adoção, Definir requisitos de funcionalidade mínima (registro de estoque, sugestão de receitas, alerta de validade) e escolher a stack tecnológica (ex.: React Native + backend serverless), Desenvolver um MVP focado em registro de itens e geração de receitas simples baseadas em validade, Estabelecer parceria com nutricionistas ou organizações de combate ao desperdício para curadoria de receitas e métricas de impacto, Elaborar protocolo de estudo controlado (RCT) incluindo critérios de inclusão, métricas de coleta (peso de resíduos, frequência de uso) e plano de análise estatística, Recrutar participantes piloto e conduzir o teste de campo por 8‑12 semanas, Analisar os dados, identificar melhorias de usabilidade e eficácia, e iterar o produto com base nos resultados
