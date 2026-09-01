# Pacote de Maturação da Ideia — Run EXP-M05.5-REP-01-COND-B

**Status:** `FAILED` | **Ciclos de Reconstrução:** 0

---

## 1. Ideia Original (Imutável)

> Uma pequena ferramenta desktop que cola um texto e remove toda a formatação, salvando o resultado somente se o usuário clicar em confirmar; sem conta, sem nuvem e sem histórico automático.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Criar uma ferramenta desktop leve que permita colar texto, limpar sua formatação e salvar o texto limpo somente após confirmação explícita, mantendo a privacidade e evitando histórico automático.
- **Problema Central:** Usuários precisam remover rapidamente a formatação de textos copiados e desejam salvar o resultado apenas quando decidirem, sem armazenamento automático, contas ou uso de nuvem.
- **Atores / Usuários:** usuário final


## 3. Versão Refinada e Mecanismo Proposto

Uma ferramenta desktop simples que permite ao usuário colar texto, remover toda a formatação e, após confirmação explícita, salvar o texto limpo; não requer conta, não usa nuvem e não mantém histórico automático.


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Irreversible loss of text if user forgets to click confirm before closing the app
   - *Impacto:* Without any history or undo, accidental closure or crash results in permanent loss of the cleaned text, defeating the tool's purpose
   - *Parte Afetada:* Save/Confirm workflow
2. **[MEDIUM]** Formatting removal may not handle complex rich‑text elements such as tables, embedded images or custom styles
   - *Impacto:* Residual markup can corrupt the output or leave hidden data, breaking the claim of "remove all formatting" and confusing users
   - *Parte Afetada:* Formatting removal engine
3. **[HIGH]** Application crash or power loss before confirmation leads to loss of clipboard content with no recovery mechanism
   - *Impacto:* The tool relies entirely on volatile memory; any instability causes data loss, which is unacceptable for a productivity utility
   - *Parte Afetada:* Application stability
4. **[MEDIUM]** Saving overwrites existing files without explicit warning
   - *Impacto:* Users may unintentionally replace important documents, creating a new source of data loss that the tool promises to avoid
   - *Parte Afetada:* File saving module


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Implement a temporary session buffer that stores the cleaned text in a hidden draft file and maintains an undo stack; on app close or crash the app prompts the user to recover the draft before exiting
   - *Tradeoffs:* Consumes additional disk space for draft files, Adds complexity to the shutdown logic, Potentially slower exit due to recovery prompt
2. **Mecanismo:** Integrar um motor de renderização rico (ex.: WebView ou biblioteca de parsing RTF) que analisa o conteúdo colado e remove formatação de forma granular, preservando tabelas, imagens embutidas e estilos customizados quando possível, ou convertendo‑os para texto plano equivalente
   - *Tradeoffs:* Aumenta o tamanho do executável devido a dependências externas, Maior carga de processamento ao colar textos complexos, Alguns elementos podem ainda ser perdidos se não houver mapeamento adequado
3. **Mecanismo:** Antes de salvar, exibir um diálogo de confirmação que verifica se o arquivo de destino já existe e oferece opções de sobrescrita, renomeação automática ou criação de versão de backup com timestamp
   - *Tradeoffs:* Passo extra para o usuário que pode ser visto como atritivo, Armazena cópias de backup que ocupam espaço em disco


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* opção de salvar em arquivo local
2. *[CANDIDATE]* cópia automática para a área de transferência
3. *[CANDIDATE]* interface gráfica simples


## 10. Próximo Passo Recomendado

Definir próximo experimento com usuários.
