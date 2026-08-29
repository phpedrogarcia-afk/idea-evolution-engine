# Pacote de Maturação da Ideia — Run EXP-M05.4-IDEA-04-COND-B

**Status:** `FAILED` | **Ciclos de Reconstrução:** 0

---

## 1. Ideia Original (Imutável)

> Um gerador de relatórios financeiros pessoais que precisa funcionar 100% offline, em um único arquivo HTML local, sem banco de dados externo e sem login.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Fornecer uma ferramenta simples e privada para criar relatórios financeiros pessoais que funcione totalmente offline e não exija login ou infraestrutura externa.
- **Problema Central:** O usuário precisa gerar relatórios financeiros pessoais sem depender de conexão à internet, bancos de dados externos ou processos de autenticação, utilizando apenas um arquivo HTML local.
- **Atores / Usuários:** Usuário individual que deseja acompanhar suas finanças pessoais


## 3. Versão Refinada e Mecanismo Proposto

Ferramenta offline que gera relatório financeiro pessoal em um único arquivo HTML, com dados criptografados por senha fornecida pelo usuário, garantindo privacidade e simplicidade.


- **Justificativa de Promoção ao Core:** Atende ao requisito de funcionamento 100% offline e em um único arquivo, resolve a vulnerabilidade de dados em texto plano e mantém a simplicidade de uso sem necessidade de login ou infraestrutura externa. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Data stored in plain HTML file is unencrypted and easily accessible
   - *Impacto:* Financial data is sensitive; exposure can lead to identity theft or fraud
   - *Parte Afetada:* Data storage
2. **[MEDIUM]** Manual data entry is error‑prone and no validation is defined
   - *Impacto:* Incorrect entries produce inaccurate reports, undermining trust in the tool
   - *Parte Afetada:* User input handling


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Gerar um relatório em um arquivo HTML que contém os dados criptografados com uma senha fornecida pelo usuário; ao abrir o arquivo, um script JavaScript solicita a senha, descriptografa os dados em memória e renderiza o relatório dinamicamente
   - *Tradeoffs:* Usuário precisa lembrar e gerenciar a senha, Processamento de criptografia pode ser mais lento em dispositivos antigos, Complexidade do código JavaScript aumenta risco de bugs
2. **Mecanismo:** Utilizar um banco de dados SQLite embutido (por exemplo, SQLCipher) para armazenar os dados; a aplicação desktop lê/escreve no banco com validação de esquema e, ao final, exporta um relatório HTML a partir dos dados armazenados
   - *Tradeoffs:* Requer distribuição de executável ou script adicional, Arquivo de banco de dados aumenta o tamanho da solução, Usuário lida com dois arquivos (banco + relatório)
3. **Mecanismo:** Criar uma planilha (LibreOffice Calc) com campos predefinidos, validação de dados e proteção por senha; o usuário preenche a planilha offline e, ao salvar, a própria planilha gera o relatório HTML via macro incorporada
   - *Tradeoffs:* Depende de aplicativo de planilha compatível, Macros podem ser desativadas por questões de segurança, Proteção por senha da planilha pode ser menos robusta que criptografia dedicada


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Utilizar um banco de dados SQLite embutido (ex.: SQLCipher) para armazenar os dados e exportar o relatório HTML a partir dele.


## 7. Propostas Rejeitadas (com Justificativa)

- **Rejeitado:** Utilizar um banco de dados SQLite embutido (SQLCipher) para armazenar os dados e exportar o relatório HTML a partir dele. (Origem: ALTERNATIVES)
  *Motivo:* Introduz múltiplos arquivos e requer distribuição de executável ou script adicional, violando o requisito de solução em um único arquivo HTML offline.
- **Rejeitado:** Criar uma planilha LibreOffice Calc com validação de dados e proteção por senha, gerando o relatório HTML via macro incorporada. (Origem: ALTERNATIVES)
  *Motivo:* Depende de aplicativo de planilha externo e de macros, aumentando a complexidade e risco de incompatibilidade, contrariando o objetivo de simplicidade e independência de software externo.


## 10. Próximo Passo Recomendado

Desenvolver um protótipo funcional do relatório HTML criptografado usando uma biblioteca JavaScript de criptografia comprovada (ex.: CryptoJS), testar a usabilidade da entrada de senha e validar a segurança e desempenho em navegadores alvo.
