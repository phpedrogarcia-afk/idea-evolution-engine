# UI-02B — verificação visual

final result: passed

## Referência e método

- Fonte visual: `C:\Users\phped\Documents\ProjetoFioIedeias\layoutFioIdeias` (944 × 1710 px).
- Implementação: `http://127.0.0.1:8765`, servida somente em loopback e exercitada com `FakeModelRunner`.
- Navegador: Chrome local via Playwright 1.63.0; `deviceScaleFactor=1`.
- O mock é um pôster ilustrativo que combina maturação, comparação e mapa, não uma captura do mesmo estado responsivo. A comparação abaixo verifica linguagem visual e organização; não reivindica fidelidade pixel a pixel.
- Para a comparação de página inteira, a fonte foi reduzida proporcionalmente de 944 × 1710 para 390 × 693 px. A captura de resultado móvel manteve 390 × 1562 px (390 CSS px de largura). As duas foram colocadas lado a lado, sem recorte, em `C:\Users\phped\Documents\FioIdeias_UI_Lab_EVIDENCE\UI-02B-20261003\comparison-source-vs-mobile-result.png` (812 × 1562 px). A diferença de altura reflete a composição do mock e o conteúdo progressivo da interface.

## Capturas

Todas estão fora do repositório em `C:\Users\phped\Documents\FioIdeias_UI_Lab_EVIDENCE\UI-02B-20261003`.

| Estado | Viewport CSS | Captura em pixels |
|---|---:|---:|
| Vazio desktop | 1440 × 1000 | `desktop-empty-1440x1000.png` — 1440 × 1000 |
| Processando | 1440 × 1000 | `desktop-processing-1440x1000.png` — 1440 × 1000 |
| Resultado desktop, detalhes/mapa | 1440 × 1000 | `desktop-result-1440x1000.png` — 1440 × 1153, página inteira |
| Decisão humana | 1440 × 1000 | `desktop-human-decision-1440x1000.png` — 1440 × 1174, página inteira |
| Erro seguro | 1440 × 1000 | `desktop-error-render-1440x1000.png` — 1440 × 1000 |
| Vazio móvel | 390 × 844 | `mobile-empty-390x844.png` — 390 × 894, página inteira |
| Resultado móvel, detalhes/mapa | 390 × 844 | `mobile-result-390x844-full.png` — 390 × 1562, página inteira |
| Resultado tablet | 768 × 1024 | `tablet-result-768x1024-full.png` — 768 × 1141, página inteira |

## Verificações e comparação

- Vazio: título, textarea rotulada, CTA e aviso de execução estão visíveis; em móvel a textarea e o botão permanecem utilizáveis e o botão cabe no viewport.
- Processamento: o frasco anima de forma discreta, o formulário fica desabilitado e não há porcentagem, ETA ou afirmação de fases reais.
- Resultado: comparação desktop em duas colunas e móvel empilhada; ideia original preservada; Forma Atual proeminente; detalhes recolhidos por padrão e expansíveis.
- Mapa: seis conceitos presentes. Nós sem conteúdo correspondente ficam desabilitados; clicar em nó disponível navega para seu conteúdo. Um realce transitório de toque/foco na captura móvel não representa conclusão nem progresso.
- Decisão humana: cartão separado mostra a justificativa retornada, sem escolher pelo usuário.
- Erro: texto contendo marcas HTML foi exibido literalmente, sem criar elementos HTML.
- Reenvio: o formulário ficou desabilitado durante a chamada fake; um segundo evento de submissão não produziu outra requisição. Não há retry automático.
- Responsividade: verificados 1440 × 1000, 768 × 1024 e 390 × 844. `scrollWidth` do documento e do body não excedeu a largura do viewport; cartões não colidiram; comparação móvel empilhou; mapa manteve três colunas em 390 px.
- Ativos: SVG do frasco e estilos/script carregaram; nenhuma imagem quebrada. Zero requisições a hosts externos.
- Erros de navegador: zero `pageerror` e zero erro JavaScript. O único registro de console foi o aviso de resposta HTTP 503 da fixture de erro provocada deliberadamente; não é falha de renderização.
- Tipografia/legibilidade: títulos manuscritos e texto de interface mantêm hierarquia; corpo permanece legível nos três tamanhos. Avisos auxiliares e rótulos do mapa são menores, mas legíveis nas capturas em resolução de viewport.
- Espaçamento/cores: papel quente, contorno escuro e acentos laranja/sálvia se mantêm consistentes. Cartões têm margens e separação suficientes em desktop, tablet e móvel.
- Ativos/imagens: frasco simples separado em SVG conforme o escopo. Menu/conta, mostrador de maturação e contadores ilustrados do mock não foram reproduzidos: a interface não deve sugerir funções, progresso ou métricas inexistentes.
- Conteúdo: o aviso esclarece que a interface é local, mas a inferência pode usar o provedor configurado e gerar registros locais.

## Achados e histórico de comparação

Nenhum achado acionável P0/P1/P2. Não foram necessários ajustes visuais; portanto, não houve iteração de correção. A diferença de riqueza gráfica entre o mock ilustrativo e a interface enxuta é intencional e limitada pelas regras do UI-02 (sem métricas fictícias ou controles fora do produto).

Comparação de página inteira suficiente para esta aceitação: títulos, comparação, mapa e hierarquia aparecem nas capturas em seus viewports reais; os estados de decisão e erro foram inspecionados separadamente em tela inteira. A captura da fonte e a implementação aparecem juntas no arquivo de comparação indicado acima.

## Execução e testes

- Um fluxo ponta a ponta local do servidor/serviço foi executado exclusivamente com `FakeModelRunner`; decisão humana, resposta de erro 503 e estado móvel foram exercitados com fixtures locais do navegador.
- Chamadas reais a provedores: 0. Sites externos acessados: 0.
- Testes UI: 17 aprovados.
- Suíte determinística completa: 559 aprovados, 0 falhas, 1 `PytestCollectionWarning` preexistente.
- Nenhum ajuste de código foi feito após a inspeção visual.
