# Baseline de Refinamento de Ideia — EXP-M05.4-IDEA-07-COND-A

## Ideia Original
> Um bloco de notas em linha de comando simples para salvar trechos rápidos de texto em arquivos markdown na pasta pessoal.

## Resumo do Modelo
Um aplicativo de linha de comando leve que permite capturar, organizar e armazenar trechos de texto como notas em arquivos Markdown, com recursos avançados de etiquetagem, busca, sincronização e segurança, mantendo a simplicidade de uso.

## Versão Refinada
CLI Notebook 2.0 – Um utilitário Python (ou Go) distribuído via pip/npm que cria notas rápidas em Markdown dentro de um diretório configurável. Cada nota recebe um título, tags opcionais e timestamp. O comando "list" permite filtrar por tags ou data, "search" realiza busca full‑text usando ripgrep integrado, e "sync" pode conectar a um repositório Git ou serviço de nuvem (Dropbox, Google Drive). Opcionalmente, o usuário pode habilitar criptografia AES para notas confidenciais. O programa inclui um arquivo de configuração (~/.clinotebookrc) para definir pasta padrão, editor preferido e opções de sincronização.

## Pontos Fortes e Fracos
- **Fortes:** Instalação e uso extremamente simples via terminal, Armazenamento em formato Markdown, facilitando leitura e exportação, Baixo consumo de recursos e sem dependências pesadas, Ideal para captura rápida de ideias e trechos de código
- **Fracos:** Organização limitada se apenas pastas forem usadas, Falta de busca textual nativa nos arquivos, Nenhum mecanismo de sincronização entre dispositivos, Ausência de criptografia ou controle de acesso para notas sensíveis

## Próximos Passos
Definir a estrutura de diretórios e formato de arquivo (ex.: YYYY-MM-DD_title.md), Especificar a interface de linha de comando (sub‑comandos: add, list, search, sync, encrypt), Implementar suporte a tags e metadados no cabeçalho YAML de cada nota, Integrar busca rápida usando ripgrep ou biblioteca similar, Adicionar opção de criptografia com chave fornecida pelo usuário, Criar script de instalação via pip e documentação no README, Testar em diferentes sistemas operacionais (Linux, macOS, Windows), Coletar feedback de usuários beta e iterar funcionalidades
