# Baseline de Refinamento de Ideia — EXP-M05.5R2-H04-COND-A

## Ideia Original
> Quero organizar meus registros pessoais de saúde e sintomas para perceber padrões antes das consultas, mas não quero enviar esses dados para aplicativos, contas online ou serviços de terceiros. Preciso conseguir usar isso no meu próprio computador.

## Resumo do Modelo
O usuário deseja organizar registros pessoais de saúde e sintomas localmente, sem depender de serviços online, para identificar padrões antes das consultas médicas.

## Versão Refinada
Desenvolver um aplicativo desktop (ou script) de código aberto que permita ao usuário inserir, categorizar e visualizar seus registros de saúde e sintomas. O software deve armazenar os dados em um formato criptografado local (por exemplo, um banco de dados SQLite cifrado) e oferecer ferramentas de visualização como gráficos de frequência, linhas de tempo e filtros por período ou tipo de sintoma. Opcionalmente, incluir módulos de exportação para CSV ou PDF para facilitar a revisão durante consultas médicas, mantendo tudo offline e sob controle do usuário.

## Pontos Fortes e Fracos
- **Fortes:** Privacidade total dos dados pessoais, Controle total sobre o armazenamento e acesso, Possibilidade de personalizar a estrutura de registro conforme necessidades individuais
- **Fracos:** Responsabilidade total de backup e segurança recai sobre o usuário, Falta de recursos avançados de análise automática que serviços online podem oferecer, Possível dificuldade de integração com dispositivos ou aplicativos de saúde existentes

## Próximos Passos
Definir os requisitos funcionais (tipos de dados, campos, visualizações), Escolher a tecnologia (ex.: Python + PyQt, Electron, ou .NET) e a forma de criptografia local, Desenvolver um protótipo mínimo viável com entrada de dados e visualização básica, Implementar backup automático local (ex.: cópia em pasta segura) e testes de segurança, Documentar o uso e disponibilizar o código em um repositório público para colaboração
