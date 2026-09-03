# Pacote de Maturação da Ideia — Run EXP-M05.5R2-H04-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Quero organizar meus registros pessoais de saúde e sintomas para perceber padrões antes das consultas, mas não quero enviar esses dados para aplicativos, contas online ou serviços de terceiros. Preciso conseguir usar isso no meu próprio computador.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Criar uma solução que permita registrar, armazenar e analisar dados de saúde no próprio computador, mantendo total privacidade e controle sobre as informações.
- **Problema Central:** O usuário precisa organizar seus registros pessoais de saúde e sintomas de forma local para identificar padrões antes das consultas, evitando o envio de dados a aplicativos, contas online ou serviços de terceiros.
- **Atores / Usuários:** usuário individual


## 3. Versão Refinada e Mecanismo Proposto

Um aplicativo desktop que permite ao usuário registrar, armazenar e analisar seus dados de saúde localmente, com criptografia forte e recursos de recuperação de dados integrados, garantindo total privacidade e controle sem depender de serviços externos.


- **Justificativa de Promoção ao Core:** Mantém todos os dados no computador do usuário, preservando privacidade, enquanto o versionamento fornece recuperação automática contra perda ou corrupção, atendendo à preocupação de data loss sem introduzir dependências externas. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Data loss due to lack of automated backup
   - *Impacto:* If the user stores health data only locally and the application does not implement robust backup or versioning, a hardware failure, accidental deletion, or corruption could permanently erase critical medical information, jeopardizing future care decisions.
   - *Parte Afetada:* Data storage and persistence


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Implementar um agendador interno que cria backups criptografados (AES‑256) dos dados de saúde para um dispositivo de armazenamento externo especificado pelo usuário, como um pendrive ou disco de rede, e permite restaurar a partir desses backups.
   - *Tradeoffs:* Requer que o usuário possua e mantenha um dispositivo de armazenamento externo conectado periodicamente, Configuração inicial pode ser complexa para usuários menos técnicos, Se o dispositivo externo for perdido ou danificado, os backups também podem ser perdidos
2. **Mecanismo:** Adicionar uma opção de sincronização ponto‑a‑ponto (P2P) que replica os arquivos de dados para nós confiáveis escolhidos pelo usuário (por exemplo, um servidor doméstico ou computadores de amigos) usando criptografia de ponta a ponta, garantindo que apenas o usuário possua as chaves de descriptografia.
   - *Tradeoffs:* Necessita de configuração de rede e de nós confiáveis, o que pode ser tecnicamente desafiador, Dependência da disponibilidade dos nós remotos para restaurar os dados, Possível aumento de latência ao sincronizar grandes volumes de dados
3. **Mecanismo:** Incorporar versionamento interno que gera snapshots diários imutáveis dos dados em um diretório oculto local, permitindo ao usuário reverter a versões anteriores caso ocorra corrupção ou exclusão acidental.
   - *Tradeoffs:* O armazenamento local pode crescer rapidamente, consumindo espaço em disco, Não protege contra falhas de hardware que afetam todo o computador, Restauração requer que o usuário saiba como acessar o diretório oculto


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Implementar um agendador interno que cria backups criptografados (AES‑256) dos dados de saúde para um dispositivo de armazenamento externo especificado pelo usuário, como um pendrive ou disco de rede


## 7. Propostas Rejeitadas (com Justificativa)

- **Rejeitado:** Adicionar uma opção de sincronização ponto‑a‑ponto (P2P) que replica os arquivos de dados para nós confiáveis escolhidos pelo usuário usando criptografia de ponta a ponta (Origem: ALTERNATIVES)
  *Motivo:* Requer configuração de rede e nós externos, violando a exigência de privacidade total e introduzindo dependências externas indesejadas


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Armazenamento local criptografado (AES‑256) com versionamento interno que gera snapshots diários imutáveis em um diretório oculto.)

**Dependências Externas do Core:**
- Biblioteca de criptografia que ofereça implementação auditada de AES‑256 (ex.: OpenSSL, libsodium).
- Acesso ao sistema de arquivos com permissões para criar e proteger um diretório oculto e armazenar arquivos de snapshot.
- Um mecanismo confiável de versionamento (ex.: sistema de arquivos que suporte snapshots ou camada de aplicação que registre versões).
- Gerenciamento seguro de chaves de criptografia (ex.: armazenamento em keystore protegido por senha do usuário).

**Testes Discriminativos do Core:**
- [ ] Verificar que dados criptografados com a biblioteca escolhida podem ser descriptografados corretamente usando a mesma chave e parâmetros (modo, IV).
- [ ] Simular a criação de um snapshot diário e tentar modificar o arquivo resultante; confirmar que a alteração é detectada ou que a versão original permanece intacta.
- [ ] Testar a invisibilidade do diretório oculto para processos não privilegiados em diferentes sistemas operacionais (ex.: listar arquivos sem atributos de ocultação).
- [ ] Medir o tempo de criação e recuperação de snapshots para garantir que o overhead seja aceitável em hardware de baixa potência.
- [ ] Avaliar a resistência a ataques de força bruta ao tentar derivar a chave a partir da senha do usuário usando parâmetros de KDF (ex.: PBKDF2, Argon2).


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Implementar um agendador que copie backups criptografados para um dispositivo externo (pendrive ou disco de rede) e validar a integridade dos arquivos após a transferência.
- [ ] *[EXPLORATÓRIO]* Testar a restauração de dados a partir de backups externos em diferentes sistemas operacionais para garantir compatibilidade.
- [ ] *[EXPLORATÓRIO]* Avaliar a eficácia de um mecanismo P2P de sincronização ponto‑a‑ponto, medindo latência e consistência dos dados replicados entre nós confiáveis.
- [ ] *[EXPLORATÓRIO]* Simular falhas de rede durante a sincronização P2P e observar a capacidade de recuperação e reconciliação de versões conflitantes.


## 10. Próximo Passo Recomendado

Desenvolver o mecanismo central de armazenamento criptografado com versionamento interno, criar protótipo de snapshots diários e validar a usabilidade do processo de restauração com usuários‑teste; depois, avaliar a necessidade de implementar o agendador de backups externos como funcionalidade opcional.
