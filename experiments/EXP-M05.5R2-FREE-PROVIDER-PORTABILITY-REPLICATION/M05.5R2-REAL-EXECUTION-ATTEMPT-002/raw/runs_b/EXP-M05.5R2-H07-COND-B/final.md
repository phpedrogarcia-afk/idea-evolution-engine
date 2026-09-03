# Pacote de Maturação da Ideia — Run EXP-M05.5R2-H07-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Quero uma ferramenta de linha de comando pequena que leia uma lista de tarefas do projeto e mostre apenas as que estão marcadas como bloqueadas, junto com a pessoa ou dependência indicada na própria lista.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Desenvolver uma ferramenta de linha de comando pequena que leia a lista de tarefas do projeto e mostre apenas as tarefas bloqueadas com a pessoa ou dependência associada.
- **Problema Central:** Identificar e exibir as tarefas do projeto que estão marcadas como bloqueadas, incluindo a pessoa responsável ou a dependência indicada para cada tarefa.
- **Atores / Usuários:** Desenvolvedor que criará a ferramenta, Membros da equipe que usarão a lista de tarefas


## 3. Versão Refinada e Mecanismo Proposto

Criar uma ferramenta de linha de comando pequena que lê um arquivo JSON contendo a lista de tarefas do projeto, filtra as tarefas marcadas como bloqueadas e exibe, para cada uma, a pessoa responsável ou a dependência indicada na própria lista.


- **Justificativa de Promoção ao Core:** O Python está amplamente disponível, não requer dependências externas e permite implementar a lógica de filtragem de forma clara e extensível, atendendo ao desejo do usuário por uma ferramenta CLI simples e portátil. (Base: `VALID_USER_DERIVATION`)


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Implementar um script shell que utiliza o utilitário jq para ler o arquivo JSON, filtrar as tarefas com o campo "blocked": true e imprimir o nome da pessoa ou a dependência associada.
   - *Tradeoffs:* Depende de que o usuário tenha jq instalado","Menos flexível para lógica complexa de filtragem","Saída limitada a formatação simples de texto
2. **Mecanismo:** Desenvolver um pequeno programa Python que usa argparse para receber o caminho do arquivo, carrega o JSON com a biblioteca padrão json, filtra as tarefas bloqueadas e exibe a pessoa ou dependência em formato tabular.
   - *Tradeoffs:* Requer que o usuário tenha Python 3 instalado","A dependência de bibliotecas externas pode ser evitada, mas aumenta o tamanho do script","Execução ligeiramente mais lenta que um binário nativo
3. **Mecanismo:** Compilar um binário Go autônomo que aceita o caminho do arquivo JSON como argumento, processa o conteúdo usando structs tipados e exibe as tarefas bloqueadas com seus responsáveis ou dependências.
   - *Tradeoffs:* Necessita do ambiente de compilação Go para gerar o binário","O binário pode ser maior que um script simples","Menos familiar para usuários que não trabalham com Go


## 7. Propostas Rejeitadas (com Justificativa)

- **Rejeitado:** Implementar um script shell que utiliza o utilitário jq para ler o arquivo JSON, filtrar as tarefas com o campo "blocked": true e imprimir o nome da pessoa ou a dependência associada. (Origem: ALTERNATIVES)
  *Motivo:* Depende de que o usuário tenha jq instalado, limitando a portabilidade e a flexibilidade da ferramenta.
- **Rejeitado:** Compilar um binário Go autônomo que aceita o caminho do arquivo JSON como argumento, processa o conteúdo usando structs tipados e exibe as tarefas bloqueadas com seus responsáveis ou dependências. (Origem: ALTERNATIVES)
  *Motivo:* Requer ambiente de compilação Go e gera um binário maior, o que contraria o objetivo de uma ferramenta CLI pequena e simples de distribuir.


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Desenvolver um script Python que usa argparse para receber o caminho do arquivo JSON, carrega o conteúdo com a biblioteca padrão json, filtra as tarefas onde "blocked": true e imprime a pessoa ou dependência em formato tabular.)

**Dependências Externas do Core:**
- Python 3.x runtime (versão >=3.6)
- Acesso de leitura ao arquivo JSON especificado
- Estrutura do JSON contendo, ao menos, os campos "blocked" (boolean) e "person" ou "dependency" para cada tarefa
- Permissões de arquivo adequadas para leitura

**Testes Discriminativos do Core:**
- [ ] Teste unitário com um arquivo JSON de exemplo contendo três tarefas, duas marcadas como "blocked": true, verificando que a saída lista exatamente essas duas tarefas com as informações corretas de pessoa/dependência.
- [ ] Teste de erro ao fornecer um caminho de arquivo inexistente, confirmando que o script exibe uma mensagem de erro clara e encerra com código de saída não‑zero.
- [ ] Teste de entrada JSON onde uma tarefa bloqueada carece do campo "person" e tem apenas "dependency", garantindo que a saída mostre a dependência correta.
- [ ] Teste de desempenho com um arquivo JSON grande (10.000 tarefas) para validar que o script completa a filtragem e impressão em tempo aceitável.
- [ ] Teste de compatibilidade passando o caminho do arquivo usando aspas e espaços, assegurando que argparse interpreta corretamente o argumento.


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Comparar a implementação Python com um script shell que utiliza jq para filtrar tarefas bloqueadas, medindo tempo de execução e consumo de memória.
- [ ] *[EXPLORATÓRIO]* Avaliar a viabilidade de portar a funcionalidade para um binário Go autônomo, incluindo análise de complexidade de desenvolvimento versus benefício de distribuição.
- [ ] *[EXPLORATÓRIO]* Investigar a possibilidade de gerar a saída em formatos alternativos (CSV, Markdown) e testar a aceitação pelos usuários finais.


## 10. Próximo Passo Recomendado

Implementar o script Python descrito, criar um conjunto de testes com arquivos JSON de exemplo (incluindo casos de erro) e validar a saída em ambientes onde Python 3 está disponível.
