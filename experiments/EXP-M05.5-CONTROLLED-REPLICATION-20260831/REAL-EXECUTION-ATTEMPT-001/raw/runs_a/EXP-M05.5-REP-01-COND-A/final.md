# Baseline de Refinamento de Ideia — EXP-M05.5-REP-01-COND-A

## Ideia Original
> Uma pequena ferramenta desktop que cola um texto e remove toda a formatação, salvando o resultado somente se o usuário clicar em confirmar; sem conta, sem nuvem e sem histórico automático.

## Resumo do Modelo
Ferramenta desktop simples que permite colar texto, remover toda a formatação e salvar o resultado apenas após confirmação, operando totalmente offline, sem necessidade de conta, nuvem ou histórico automático.

## Versão Refinada
Uma aplicação desktop multiplataforma (por exemplo, baseada em Electron ou Qt) que mantém a simplicidade de colar e limpar formatação, mas adiciona recursos opcionais como desfazer/redo, histórico temporário, suporte a arrastar e soltar arquivos de texto, escolha de salvar em arquivo ou copiar para a área de transferência, e atalhos de teclado configuráveis. Todas as opções avançadas são desativáveis por padrão, preservando a experiência minimalista e a privacidade total.

## Pontos Fortes e Fracos
- **Fortes:** Privacidade total – nenhum dado é enviado para a nuvem, Uso offline – funciona sem conexão à internet, Interface mínima e direta, fácil de aprender, Sem necessidade de cadastro ou login, Leve e rápido, baixa demanda de recursos
- **Fracos:** Funcionalidade limitada a um único caso de uso, Ausência de histórico ou desfazer impede correções rápidas, Nenhum suporte a processamento em lote ou múltiplos arquivos, Falta de integração com outros aplicativos (clipboard avançado, editores), Possível incompatibilidade entre sistemas operacionais se não for multiplataforma

## Próximos Passos
Definir as plataformas alvo (Windows, macOS, Linux) e escolher a tecnologia (Electron, Qt, .NET), Criar wireframes da interface focando na simplicidade e nos atalhos de teclado, Implementar o motor de limpeza de formatação usando bibliotecas confiáveis (ex.: html2text, pandoc), Adicionar funcionalidades opcionais de desfazer, histórico temporário e arrastar‑soltar, Realizar testes com diferentes tipos de documentos (Word, HTML, PDFs) para garantir remoção completa da formatação, Coletar feedback de usuários beta e iterar no design, Empacotar instaladores e preparar documentação mínima de uso
