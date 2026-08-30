# Pacote de Maturação da Ideia — Run PILOT-CAL-01-COND-B_v2

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Um aplicativo de lista de compras compartilhada que aprende quais itens uma família costuma comprar e sugere automaticamente o que pode estar faltando, sem adicionar itens sem confirmação.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Criar um aplicativo de lista de compras compartilhada que aprenda os itens habituais da família e sugira automaticamente o que está faltando, adicionando apenas após confirmação do usuário.
- **Problema Central:** Famílias precisam coordenar compras, evitando itens esquecidos e duplicados, sem que o aplicativo adicione itens automaticamente sem sua aprovação.
- **Atores / Usuários:** pais, filhos, outros membros da família que participam das compras


## 3. Versão Refinada e Mecanismo Proposto

Aplicativo de lista de compras compartilhada que aprende localmente os itens habituais da família, sincroniza de forma ponto‑a‑ponto entre dispositivos usando criptografia de grupo e apresenta sugestões resumidas diárias que exigem confirmação manual antes de serem adicionadas.


- **Justificativa de Promoção ao Core:** Preserva privacidade ao manter dados e aprendizado local, elimina dependência de servidor central e atende ao desejo explícito do usuário por controle e segurança. (Base: `VALID_USER_DERIVATION`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Dependência de uma única conta compartilhada pode falhar quando membros usam contas distintas.
   - *Impacto:* Fragmenta os dados de compra, impede a aprendizagem correta e gera sugestões incompletas ou errôneas.
   - *Parte Afetada:* Autenticação e modelo de compartilhamento
2. **[HIGH]** Armazenamento de padrões de compra pode violar privacidade ou regulamentos de dados.
   - *Impacto:* Risco legal e perda de confiança do usuário, podendo levar à remoção do app das lojas.
   - *Parte Afetada:* Camada de armazenamento de dados
3. **[MEDIUM]** Confirmação manual de cada sugestão pode gerar fadiga do usuário.
   - *Impacto:* Reduz a taxa de adoção e pode levar os usuários a desativar a funcionalidade.
   - *Parte Afetada:* Interface do usuário


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Implementar sincronização ponto‑a‑ponto (peer‑to‑peer) entre os dispositivos dos membros da família, usando chaves de grupo criptografadas; cada usuário mantém seu histórico localmente e o modelo de aprendizado roda no dispositivo, compartilhando apenas atualizações resumidas criptografadas.
   - *Tradeoffs:* Maior complexidade de implementação e necessidade de conectividade entre dispositivos., Possíveis conflitos de sincronização quando dispositivos estão offline simultaneamente.
2. **Mecanismo:** Utilizar aprendizado federado com privacidade diferencial no servidor: cada dispositivo treina um modelo localmente e envia apenas gradientes ruidosos; o servidor agrega esses gradientes para gerar sugestões globais, aplicando um limiar de confiança que aceita automaticamente sugestões acima de 90% de certeza, reduzindo a necessidade de confirmação manual.
   - *Tradeoffs:* Sugestões podem ser menos personalizadas devido ao ruído introduzido., Requer infraestrutura de aprendizado federado e monitoramento de limites de privacidade.
3. **Mecanismo:** Criar um grupo familiar com contas individuais vinculadas por um token de família; armazenar apenas hashes dos itens frequentes no servidor e permitir que o usuário configure regras de auto‑adição para itens que aparecem em >80% das listas, enquanto itens menos recorrentes ainda requerem confirmação.
   - *Tradeoffs:* Necessita de configuração inicial de regras e de um administrador familiar., Hashes limitam a capacidade de análises avançadas e podem gerar colisões raras.


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Explorar opção híbrida: sincronização ponto‑a‑ponto com backup opcional em nuvem criptografada.
2. *[CANDIDATE]* Implementar modo offline com sincronização diferida quando a conexão for restabelecida.


## 7. Propostas Rejeitadas (com Justificativa)

- **Rejeitado:** Utilizar aprendizado federado com privacidade diferencial no servidor, aceitando automaticamente sugestões acima de 90% de certeza. (Origem: ALTERNATIVES)
  *Motivo:* Contraria a necessidade de confirmação manual e depende de hipótese de modelo, violando a diretriz de não circularidade.
- **Rejeitado:** Criar grupo familiar com contas individuais vinculadas por token, armazenar hashes e permitir regras de auto‑adição para itens >80% das listas. (Origem: ALTERNATIVES)
  *Motivo:* Reduz confirmação manual, introduz risco de colisões de hash e adiciona lógica de auto‑adição não explicitamente desejada pelo usuário.


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Sincronização ponto‑a‑ponto (peer‑to‑peer) entre dispositivos familiares com chaves de grupo criptografadas; cada dispositivo mantém histórico local e executa modelo de aprendizado local, compartilhando apenas atualizações resumidas criptografadas.)

**Dependências Externas do Core:**
- Capacidade de descoberta e conexão P2P entre dispositivos iOS, Android e desktops (Wi‑Fi Direct, Bluetooth LE, LAN multicast ou WebRTC).
- Mecanismo robusto de NAT traversal (STUN/TURN) para cenários onde dispositivos estão em redes diferentes dentro da mesma casa.
- Bibliotecas criptográficas que suportem geração e rotação segura de chaves de grupo em cada dispositivo.
- Armazenamento persistente local confiável para histórico de compras e modelo de aprendizado.
- Permissões de sistema operacional para execução de sincronização em segundo plano sem interrupções do usuário.

**Testes Discriminativos do Core:**
- [ ] Desenvolver um protótipo mínimo de sincronização P2P usando libp2p/WebRTC e medir taxa de sucesso de conexão em diferentes topologias de rede doméstica.
- [ ] Implementar troca de chaves de grupo (Diffie‑Hellman grupal) e validar a confidencialidade e integridade das mensagens trocadas.
- [ ] Executar o modelo de aprendizado local em um conjunto de dados sintético de compras e avaliar a taxa de acerto das sugestões geradas a partir de atualizações resumidas.
- [ ] Realizar teste de consumo de bateria comparando sincronização P2P ativa vs. sincronização baseada em nuvem tradicional.
- [ ] Conduzir um estudo de usabilidade com 10 famílias para medir a taxa de aceitação da confirmação manual das sugestões diárias.


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Avaliar a viabilidade de um backup opcional em nuvem criptografado que armazene snapshots periódicos do histórico local.
- [ ] *[EXPLORATÓRIO]* Testar modo offline com fila de atualizações diferidas que são enviadas quando a conexão P2P for restabelecida.
- [ ] *[EXPLORATÓRIO]* Prototipar aprendizado federado com privacidade diferencial em um servidor central como alternativa ao modelo totalmente local.
- [ ] *[EXPLORATÓRIO]* Implementar regras de auto‑adição baseadas em frequência (>80%) armazenadas como hashes no servidor e comparar a precisão com a abordagem P2P.


## 10. Próximo Passo Recomendado

Prototipar a sincronização ponto‑a‑ponto com criptografia de grupo, integrar o modelo de aprendizado local e conduzir testes de usabilidade focados na confirmação manual das sugestões.
