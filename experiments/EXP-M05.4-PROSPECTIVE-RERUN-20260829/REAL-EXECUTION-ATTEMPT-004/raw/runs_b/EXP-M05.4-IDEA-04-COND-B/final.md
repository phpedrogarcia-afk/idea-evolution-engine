# Pacote de Maturação da Ideia — Run EXP-M05.4-IDEA-04-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Um gerador de relatórios financeiros pessoais que precisa funcionar 100% offline, em um único arquivo HTML local, sem banco de dados externo e sem login.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Permitir que o usuário gere seus próprios relatórios financeiros de forma totalmente offline, mantendo a privacidade e simplicidade.
- **Problema Central:** Necessidade de criar relatórios financeiros pessoais sem depender de conexão à internet, bancos de dados externos ou autenticação, usando apenas um arquivo local.
- **Atores / Usuários:** Usuário individual que deseja gerar relatórios financeiros


## 3. Versão Refinada e Mecanismo Proposto

Gerador de relatórios financeiros pessoais totalmente offline que produz um único arquivo HTML contendo os dados financeiros criptografados com senha fornecida pelo usuário, garantindo privacidade e simplicidade.


- **Justificativa de Promoção ao Core:** Atende diretamente à intenção do usuário de manter os dados totalmente offline e privados, usando criptografia cliente‑side para proteger o conteúdo dentro do próprio HTML. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Sensitive financial data stored in plain text within the HTML file
   - *Impacto:* If the file is accessed by unauthorized parties, personal financial information is exposed, violating privacy priorities
   - *Parte Afetada:* Data storage / privacy
2. **[MEDIUM]** Performance degradation with large datasets
   - *Impacto:* Browsers may become unresponsive or crash when processing extensive financial records in a single HTML file, rendering the tool unusable
   - *Parte Afetada:* Rendering engine / JavaScript execution


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Encrypt the financial data client‑side with a user‑provided password and embed the ciphertext in the HTML; the browser decrypts it on‑the‑fly for rendering.
   - *Tradeoffs:* Requires the user to remember a password, Encryption/decryption adds CPU overhead, If password is lost data is unrecoverable
2. **Mecanismo:** Store the raw dataset in a compressed binary blob (e.g., gzip‑compressed JSON) alongside the HTML and render reports by streaming only the needed portions into memory.
   - *Tradeoffs:* Data is not human‑readable without decompression, Adds a step to decompress before viewing, Compression may slightly increase file size for very small datasets
3. **Mecanismo:** Leverage the browser’s IndexedDB to store the dataset encrypted, and generate the HTML report dynamically by querying only the rows needed for the current view.
   - *Tradeoffs:* Requires modern browser support for IndexedDB, Adds complexity to the client‑side code, Initial load may be slower as data is indexed


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Store the raw dataset in a compressed binary blob (e.g., gzip‑compressed JSON) alongside the HTML and render reports by streaming only the needed portions into memory.
2. *[CANDIDATE]* Leverage the browser’s IndexedDB to store the dataset encrypted, and generate the HTML report dynamically by querying only the rows needed for the current view.


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Gerar um arquivo HTML único que incorpora os dados financeiros criptografados com uma senha fornecida pelo usuário; o navegador descriptografa o conteúdo em tempo real para renderizar o relatório.)

**Dependências Externas do Core:**
- Disponibilidade e compatibilidade do Web Crypto API nos navegadores alvo (Chrome, Firefox, Safari, Edge)
- Suporte ao File API/Blob para leitura do HTML local
- Capacidade de executar JavaScript de forma segura em arquivos HTML abertos localmente
- Gerador de salt e KDF (ex.: PBKDF2, scrypt) implementado em JavaScript
- Mecanismo de derivação de chave a partir da senha do usuário

**Testes Discriminativos do Core:**
- [ ] Teste de round‑trip: criptografar um dataset de exemplo, embutir no HTML, abrir offline e verificar se a saída renderizada corresponde ao original
- [ ] Medição de tempo de descriptografia para diferentes tamanhos de dataset (1 MB, 5 MB, 10 MB) em Chrome, Firefox e Safari
- [ ] Teste de senha incorreta: garantir que o relatório não seja renderizado e que mensagens de erro não vazem dados
- [ ] Verificação de funcionamento offline: abrir o HTML em modo avião e confirmar que todas as funcionalidades permanecem operacionais


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Implementar armazenamento de blob gzip‑compressado ao lado do HTML e medir tempo de streaming e descriptografia parcial
- [ ] *[EXPLORATÓRIO]* Usar IndexedDB para armazenar o dataset criptografado e gerar relatórios dinamicamente, avaliando latência de consultas
- [ ] *[EXPLORATÓRIO]* Testar fallback para browsers sem Web Crypto usando bibliotecas JavaScript puras (ex.: CryptoJS)
- [ ] *[EXPLORATÓRIO]* Avaliar impacto de diferentes KDFs (PBKDF2 vs scrypt) sobre tempo de derivação de chave e segurança


## 10. Próximo Passo Recomendado

Develop a prototype implementing the encrypted‑HTML generator, then test password handling, decryption performance, and compatibility across major browsers with realistic dataset sizes.
