# Baseline de Refinamento de Ideia — EXP-M05.4-IDEA-08-COND-A

## Ideia Original
> Um diário reflexivo que ajuda a capturar sensações sutis do dia a dia, medindo se o tempo de resposta do editor de texto abaixo de 16ms reduz a distração ao digitar.

## Resumo do Modelo
Um aplicativo de diário reflexivo que registra sensações sutis do cotidiano e, simultaneamente, monitora a latência do editor de texto usado, avaliando se tempos de resposta abaixo de 16 ms reduzem a distração durante a escrita.

## Versão Refinada
Desenvolver um aplicativo multiplataforma (desktop e mobile) chamado "MindLatency Journal". O app oferece um modo de escrita reflexiva com campos para registrar sensações físicas, emocionais e contextuais. Em paralelo, um módulo de monitoramento de latência mede o tempo de resposta do editor de texto (ou do campo de entrada) em milissegundos, exibindo um indicador simples (verde abaixo de 16 ms, amarelo entre 16‑30 ms, vermelho acima de 30 ms). O usuário pode ativar ou desativar o monitoramento, visualizar tendências ao longo do tempo e receber sugestões de ajustes (ex.: mudar de editor, usar hardware mais rápido). O design prioriza uma interface minimalista para não interromper a prática de escrita, e os dados são armazenados localmente com opção de exportação para análise posterior.

## Pontos Fortes e Fracos
- **Fortes:** Fomenta a atenção plena ao capturar detalhes sensoriais do dia a dia, Combina prática de escrita reflexiva com métrica objetiva de desempenho, Possibilidade de gerar insights sobre como a latência afeta a concentração, Pode ser integrado a editores populares, ampliando o alcance
- **Fracos:** A métrica de 16 ms pode ser muito específica e difícil de validar em diferentes hardware, Implementar medição precisa de latência exige acesso a APIs de baixo nível, o que pode limitar plataformas, Público-alvo pode ser pequeno – usuários que se importam simultaneamente com mindfulness e performance de teclado, Risco de sobrecarregar o usuário com dados técnicos, desviando o foco da reflexão

## Próximos Passos
Conduzir pesquisa de mercado para validar interesse em combinar mindfulness com métricas de latência, Definir requisitos técnicos para medição de latência em Windows, macOS, Linux e mobile, Criar wireframes de UI focados em simplicidade e baixa distração, Desenvolver um protótipo MVP que registre entradas de diário e mostre latência em tempo real, Realizar testes de usabilidade com usuários de diferentes perfens de hardware para calibrar o limiar de 16 ms, Iterar com base no feedback, adicionando recursos como exportação de dados e integração com editores externos
