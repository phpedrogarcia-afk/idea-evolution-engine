# Pacote de Maturação da Ideia — Run EXP-M05.5-REP-04-COND-B

**Status:** `FAILED` | **Ciclos de Reconstrução:** 0

---

## 1. Ideia Original (Imutável)

> Um organizador de documentos pessoais que funcione 100% local no computador, sem login, sem servidor e sem enviar conteúdo para a internet, permitindo exportar um único arquivo de backup.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Criar um organizador de documentos pessoais que funcione totalmente localmente, sem login nem conexão à internet, e que permita exportar tudo em um único arquivo de backup.
- **Problema Central:** Usuários precisam organizar documentos pessoais de forma segura sem depender de serviços online, login ou servidores, e desejam uma maneira simples de fazer backup local.
- **Atores / Usuários:** Usuário individual que gerencia seus documentos pessoais


## 3. Versão Refinada e Mecanismo Proposto

Um aplicativo de organização de documentos pessoais que opera totalmente offline no computador do usuário, sem necessidade de login ou conexão a servidores, e que permite exportar todos os documentos organizados em um único arquivo de backup.


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Lack of encryption for stored documents
   - *Impacto:* If documents are stored unencrypted on disk, a malicious actor with physical or remote access can read sensitive personal data.
   - *Parte Afetada:* Data storage layer
2. **[HIGH]** Single backup file is a single point of failure
   - *Impacto:* Corruption or loss of the backup file would result in total data loss, defeating the purpose of the organizer.
   - *Parte Afetada:* Backup/export functionality
3. **[MEDIUM]** No versioning or recovery for accidental deletions
   - *Impacto:* User may delete or overwrite documents; without version control, recovery is impossible.
   - *Parte Afetada:* Document management UI


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Armazenar todos os documentos dentro de um contêiner criptografado (AES‑256) local e manter snapshots incrementais em diretórios separados, permitindo restaurar versões anteriores a partir desses snapshots
   - *Tradeoffs:* O usuário deve definir e lembrar uma senha forte, Ocupa mais espaço em disco devido aos snapshots, Processo de criação de snapshots pode consumir recursos temporariamente
2. **Mecanismo:** Sincronizar o organizador via rede local (LAN) entre múltiplos dispositivos do usuário, armazenando cópias criptografadas em cada máquina e mantendo histórico de versões por meio de um log de alterações distribuído
   - *Tradeoffs:* Requer que o usuário possua mais de um dispositivo na mesma rede, Configuração inicial de sincronização pode ser complexa, Conflitos de edição simultânea podem precisar de resolução manual
3. **Mecanismo:** Utilizar um arquivo de log append‑only (estilo blockchain local) onde cada operação (criação, edição, exclusão) é registrada e criptografada; o backup consiste no log completo, permitindo reconstruir qualquer versão anterior
   - *Tradeoffs:* O log pode crescer significativamente ao longo do tempo, exigindo mais espaço de armazenamento, Operações de leitura podem ser mais lentas ao precisar percorrer o log, Implementação mais sofisticada pode aumentar a complexidade do código


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Aplicativo desktop
2. *[CANDIDATE]* Armazenamento em arquivos locais
3. *[CANDIDATE]* Exportação para arquivo compactado (ex.: ZIP)
4. *[CANDIDATE]* Possibilidade de criptografia dos dados
5. *[CANDIDATE]* Interface gráfica para gerenciamento de documentos


## 10. Próximo Passo Recomendado

Definir próximo experimento com usuários.
