# Pacote de Maturação da Ideia — Run EXP-M05.4-IDEA-07-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Um bloco de notas em linha de comando simples para salvar trechos rápidos de texto em arquivos markdown na pasta pessoal.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Criar um bloco de notas operado via linha de comando que permita salvar de forma rápida e direta trechos de texto em arquivos markdown dentro de um diretório pessoal.
- **Problema Central:** O usuário carece de uma ferramenta simples de linha de comando para capturar rapidamente trechos de texto e armazená‑los como arquivos markdown em sua pasta pessoal, evitando a necessidade de abrir editores ou gerenciar manualmente arquivos individuais.
- **Atores / Usuários:** usuário final que precisa capturar notas rápidas, desenvolvedor que utiliza o terminal para organizar snippets


## 3. Versão Refinada e Mecanismo Proposto

Utilitário de linha de comando que captura trechos de texto, salva cada um como arquivo markdown individual com nome único e mantém um índice estruturado para busca rápida.


- **Justificativa de Promoção ao Core:** UUID elimina colisões de nomes; SQLite oferece consultas eficientes e evita limitações do índice JSON plano. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** File name collisions can overwrite existing notes, causing irreversible data loss
   - *Impacto:* Without a robust naming or deduplication strategy, two different snippets may generate the same filename, erasing the first entry
   - *Parte Afetada:* filename generation / storage logic
2. **[MEDIUM]** Absence of search or indexing makes saved notes hard to retrieve
   - *Impacto:* Capturing notes is only valuable if the user can later locate them; lacking retrieval mechanisms renders the tool ineffective
   - *Parte Afetada:* overall utility / user workflow
3. **[MEDIUM]** Improper handling of special characters and Unicode can cause filesystem errors
   - *Impacto:* Users may paste text containing symbols, emojis, or non‑ASCII characters; if these are used directly in filenames the command may fail on many OSes
   - *Parte Afetada:* input sanitization / filename creation


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Gerar nomes de arquivos baseados em UUIDs (versão 4) e armazenar notas em subdiretórios por data, mantendo um índice SQLite que registra caminho, timestamp, tags e conteúdo para busca rápida
   - *Tradeoffs:* Dependência de SQLite aumenta o tamanho do binário e requer migrações de esquema, Estrutura de diretórios mais profunda pode complicar backups manuais
2. **Mecanismo:** Salvar todas as anotações de um dia em um único arquivo markdown diário com cabeçalhos delimitados por front‑matter, usando codificação URL‑safe para nomes de seções e permitindo busca via grep ou ferramenta integrada de regex
   - *Tradeoffs:* O arquivo diário pode crescer muito grande, tornando a edição manual lenta, Requer parsing adicional para extrair notas individuais
3. **Mecanismo:** Integrar o diretório de notas a um repositório Git local; cada captura cria um commit com mensagem contendo metadados e o conteúdo salvo em um arquivo markdown cujo nome é sanitizado (slug) e, se necessário, numerado para evitar colisões; busca feita via git grep e histórico de versões protege contra perdas
   - *Tradeoffs:* Requer que o usuário tenha Git instalado e compreenda seu fluxo básico, Operações de commit podem introduzir latência em ambientes de baixa performance


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Permitir escolha entre backend JSON ou SQLite via flag
2. *[CANDIDATE]* Adicionar suporte opcional para criptografia de notas
3. *[CANDIDATE]* Implementar modo de operação offline sem dependência de SQLite


## 7. Propostas Rejeitadas (com Justificativa)

- **Rejeitado:** Salvar todas as anotações de um dia em um único arquivo markdown diário com front‑matter. (Origem: ALTERNATIVES)
  *Motivo:* Aumenta o tamanho do arquivo diário, dificultando edição e busca; contraria objetivo de acesso rápido a notas individuais.
- **Rejeitado:** Integrar diretório de notas a um repositório Git local, criando commit por captura. (Origem: ALTERNATIVES)
  *Motivo:* Exige que usuário tenha Git instalado e compreenda fluxo, adicionando complexidade desnecessária ao utilitário simples.


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Salvar cada trecho como arquivo markdown com nome único baseado em UUID v4, armazenar metadados (timestamp, hash, tags) em um banco SQLite que serve como índice de busca.)

**Dependências Externas do Core:**
- Acesso de leitura/escrita ao sistema de arquivos do usuário
- Biblioteca para geração de UUID v4 (ex.: uuid em Python, uuid npm)
- Biblioteca SQLite compatível com a linguagem escolhida
- Função de hash criptográfico (ex.: SHA‑256) para gerar o hash do conteúdo
- Permissões de execução para criar arquivos e abrir o banco SQLite

**Testes Discriminativos do Core:**
- [ ] Criar 10.000 notas de teste e verificar que cada arquivo possui nome UUID v4 válido e único
- [ ] Confirmar que para cada nota existe um registro correspondente no banco SQLite com timestamp, hash e tags corretos
- [ ] Executar consultas de busca por tag e por intervalo de timestamps e medir tempo de resposta (<100 ms)
- [ ] Alterar o conteúdo de um arquivo e validar que o hash armazenado no SQLite não corresponde, detectando a corrupção
- [ ] Simular falha de energia durante gravação e garantir que o banco SQLite permanece consistente ao reiniciar


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Testar a flag de escolha entre backend JSON vs SQLite e validar que ambos mantêm a mesma consistência de metadados
- [ ] *[EXPLORATÓRIO]* Implementar criptografia opcional das notas e medir impacto de desempenho na gravação e leitura
- [ ] *[EXPLORATÓRIO]* Avaliar modo offline que usa apenas arquivos markdown sem SQLite, verificando se buscas por metadados ainda são possíveis via parsing de cabeçalhos


## 10. Próximo Passo Recomendado

Implementar o core mechanism com geração de UUID v4 e backend SQLite, escrever testes de colisão de nomes e consultas de busca, e validar com usuários que relataram problemas de colisão.
