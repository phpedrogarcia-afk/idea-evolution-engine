# Baseline de Refinamento de Ideia — EXP-M05.4-IDEA-07-COND-A

## Ideia Original
> Um bloco de notas em linha de comando simples para salvar trechos rápidos de texto em arquivos markdown na pasta pessoal.

## Resumo do Modelo
Um utilitário de linha de comando que permite ao usuário capturar rapidamente trechos de texto e armazená‑los como arquivos Markdown organizados em uma pasta pessoal, facilitando a criação de um bloco de notas digital leve e portátil.

## Versão Refinada
Um CLI avançado chamado **md‑snip** que permite criar, listar, buscar e organizar snippets em arquivos Markdown. Cada snippet é salvo com metadados (data, tags, título) em um diretório configurável. O programa oferece sub‑comandos para: add (captura rápida via stdin ou argumento), list (exibe resumo com filtros por tag ou data), view (mostra conteúdo formatado), edit (abre em editor padrão), export (gera um único documento consolidado) e sync (opcional, via Git ou serviços cloud). Opcionalmente, pode criptografar o diretório de snippets e manter um histórico de versões usando Git interno. Configurações são armazenadas em um arquivo YAML na home do usuário, permitindo personalização de caminho, editor, e políticas de backup.

## Pontos Fortes e Fracos
- **Fortes:** Simplicidade de uso via terminal, Baixo consumo de recursos, Armazenamento em formato Markdown legível e portátil, Facilidade de integração com scripts e automações, Organização automática por data ou tags
- **Fracos:** Falta de interface gráfica para usuários menos técnicos, Gerenciamento limitado de buscas avançadas, Nenhum mecanismo de sincronização entre dispositivos, Ausência de controle de versões ou histórico de edições, Segurança dos dados (criptografia) não contemplada

## Próximos Passos
Definir requisitos funcionais detalhados (sub‑comandos, metadados, opções de criptografia), Escolher linguagem de implementação (ex.: Python com Click ou Rust com Clap), Criar protótipo mínimo: comando `mdsnip add` que salva texto em um arquivo Markdown datado
