# Pacote de Maturação da Ideia — Run EXP-M05.4-IDEA-03-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Um sistema para conectar leitores de livros raros: ou através de um mapa geográfico de proximidade física entre vizinhos, ou através de um feed assíncrono baseado em afinidade de temas obscuros.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Criar um sistema que conecte leitores de livros raros, permitindo que encontrem outros leitores tanto por proximidade física quanto por afinidade em temas obscuros.
- **Problema Central:** Os leitores de livros raros não têm um meio eficaz de encontrar outros leitores com interesses semelhantes ou que estejam geograficamente próximos para trocar ou discutir esses livros.
- **Atores / Usuários:** leitores de livros raros, vizinhos, comunidade de colecionadores


## 3. Versão Refinada e Mecanismo Proposto

Um sistema privado de matchmaking para leitores de livros raros que conecta usuários próximos ou com afinidades temáticas sem revelar localização exata nem listas completas de interesses.


- **Justificativa de Promoção ao Core:** Atende ao requisito de privacidade explícito do usuário, elimina a necessidade de um servidor central e permite matchmaking seguro baseada em criptografia avançada. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Privacy leakage due to mandatory sharing of location and reading interests
   - *Impacto:* Exposes users to stalking, legal liability, and reduces willingness to join, threatening adoption
   - *Parte Afetada:* User Data Handling
2. **[MEDIUM]** Insufficient user density in niche rare‑book community
   - *Impacto:* Map may show no nearby peers and feed may lack relevant matches, rendering core functionality ineffective
   - *Parte Afetada:* Matching & Map Feature
3. **[MEDIUM]** Inaccurate categorization of obscure themes
   - *Impacto:* Poor recommendations lower perceived value and increase churn, undermining the feed's purpose
   - *Parte Afetada:* Recommendation Engine


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Rede P2P descentralizada que utiliza provas de conhecimento zero (zero‑knowledge proofs) para comparar hashes de interesses e geohash aproximado sem jamais revelar os valores reais nem a localização exata
   - *Tradeoffs:* Maior complexidade de implementação e necessidade de dispositivos capazes de executar provas criptográficas, Latência potencialmente maior nas correspondências devido ao roteamento P2P
2. **Mecanismo:** Sistema de taxonomia colaborativa baseada em reputação, onde usuários curam e validam tags de temas obscuros; o matchmaking usa correspondência difusa (fuzzy matching) sobre essas tags e permite que a localização seja compartilhada apenas a nível de cidade ou bairro
   - *Tradeoffs:* Dependência de contribuição inicial da comunidade para construir a ontologia, o que pode ser lento, Risco de spam ou manipulação de tags sem mecanismos de reputação robustos
3. **Mecanismo:** Modelo híbrido com servidor central anonimizado que armazena vetores de interesse hashados e aplica diferencial privacy ao gerar sugestões; as conexões podem ser físicas (via geohash coarse) ou virtuais em salas de leitura online
   - *Tradeoffs:* Requer confiança em um servidor central, ainda que anonimizado, A aplicação de diferencial privacy pode reduzir a precisão das recomendações


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Sistema de taxonomia colaborativa baseada em reputação com matchmaking difuso e compartilhamento de localização a nível de cidade ou bairro
2. *[CANDIDATE]* Modelo híbrido com servidor central anonimizado que armazena vetores de interesse hashados e aplica diferencial privacy nas sugestões


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Rede P2P descentralizada que utiliza provas de conhecimento zero para comparar hashes de interesses e geohash aproximado sem revelar valores reais nem localização exata)

**Dependências Externas do Core:**
- Bibliotecas maduras de provas de conhecimento zero (ex.: libsnark, zkSNARKs) prontas para uso em dispositivos cliente
- Implementação de algoritmo de interseção de conjuntos via ZKP com latência aceitável
- Infraestrutura P2P confiável (DHT, NAT traversal) para conectar leitores dispersos
- Mecanismo seguro de gerenciamento de chaves públicas/privadas entre pares
- Adoção de padrões de hash criptográfico para representar interesses

**Testes Discriminativos do Core:**
- [ ] Implementar protótipo de matchmaking entre dois nós usando ZKP de interseção de conjuntos e medir tempo de execução
- [ ] Avaliar precisão e privacidade do geohash coarse comparando pares reais vs. falsos positivos
- [ ] Medir consumo de banda e CPU em rede P2P com 100, 500 e 1000 nós simulados
- [ ] Realizar auditoria de segurança da implementação ZKP contra ataques de replay e vazamento de dados
- [ ] Testar resiliência da rede a churn simulando desconexões aleatórias de 20 % dos nós


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Prototipar sistema de taxonomia colaborativa com reputação e medir qualidade de tags fuzzy sobre hashes
- [ ] *[EXPLORATÓRIO]* Desenvolver modelo híbrido com servidor central anonimizado aplicando diferencial privacy nas sugestões e comparar desempenho com P2P puro
- [ ] *[EXPLORATÓRIO]* Testar integração de fuzzy matching sobre vetores de interesse hashados para melhorar correspondência temática
- [ ] *[EXPLORATÓRIO]* Avaliar aceitação do usuário ao compartilhar localização ao nível de cidade/bairro em vez de coordenadas exatas
- [ ] *[EXPLORATÓRIO]* Investigar viabilidade de usar redes de gossip para disseminar reputação de tags sem revelar identidade


## 10. Próximo Passo Recomendado

Desenvolver um protótipo da rede P2P com zero‑knowledge proofs focado na comparação de hashes de interesses e geohash coarse, e conduzir testes de privacidade e desempenho com um grupo piloto de usuários.
