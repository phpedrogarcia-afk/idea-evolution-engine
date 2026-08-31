# Pacote de Maturação da Ideia — Run EXP-M05.4-IDEA-03-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Um sistema para conectar leitores de livros raros: ou através de um mapa geográfico de proximidade física entre vizinhos, ou através de um feed assíncrono baseado em afinidade de temas obscuros.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Criar um sistema que conecte leitores de livros raros, oferecendo opções de conexão por proximidade geográfica ou por afinidade temática de assuntos obscuros.
- **Problema Central:** Leitores de livros raros têm dificuldade em encontrar outros leitores com interesses semelhantes ou em localizar livros raros próximos fisicamente.
- **Atores / Usuários:** Leitores de livros raros, Vizinhos físicos, Usuários interessados em temas obscuros


## 3. Versão Refinada e Mecanismo Proposto

Um sistema que conecta leitores de livros raros usando geohashing difuso e matching temático baseado em embeddings, preservando privacidade e permitindo encontros presenciais opcionais.


- **Justificativa de Promoção ao Core:** Atende ao desejo do usuário de conectar leitores por proximidade geográfica sem expor localização exata e por afinidade temática de assuntos obscuros, mitigando riscos de privacidade e inconsistências de categorização. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Privacy risk from precise location sharing
   - *Impacto:* Exposing users' exact whereabouts can lead to stalking, theft, or legal liability, undermining trust and adoption
   - *Parte Afetada:* Location sharing module
2. **[HIGH]** Sparse user density makes geographic matching ineffective
   - *Impacto:* Rare books are, by definition, scarce; most users will have no nearby matches, resulting in a dead‑end feature and user churn
   - *Parte Afetada:* Map matching algorithm
3. **[MEDIUM]** Inconsistent categorization of obscure themes
   - *Impacto:* If themes cannot be reliably classified, the asynchronous feed will surface irrelevant connections, reducing perceived value
   - *Parte Afetada:* Recommendation engine


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Rede P2P descentralizada com consultas de proximidade criptografadas (ex.: homomorphic encryption) e grade de localização difusa (grid cells) que permite aos usuários compartilhar apenas a célula geográfica em vez de coordenadas exatas
   - *Tradeoffs:* Maior consumo computacional e latência nas consultas criptográficas, Necessita de usuários mais familiarizados com tecnologia P2P, Complexidade de implementação da criptografia homomórfica
2. **Mecanismo:** Ontologia temática curada por comunidade + clustering assistido por IA, com encontros virtuais (salas de vídeo temáticas) como alternativa principal ao encontro presencial
   - *Tradeoffs:* Depende da participação ativa da comunidade para manter a ontologia atualizada, Risco de viés nos clusters gerados pela IA, Menor ênfase em encontros presenciais espontâneos
3. **Mecanismo:** Sistema de incentivos baseado em tokens onde usuários recebem créditos por compartilhar localização aproximada (ex.: raio de 5 km) e metadados temáticos de alta qualidade; matching usa filtros Bloom probabilísticos para ocultar a localização exata
   - *Tradeoffs:* Complexidade de gerenciar a economia de tokens e prevenir fraudes, Possível curva de aprendizado para usuários sobre como ganhar e gastar tokens, Requer backend para gerar e validar filtros Bloom


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Incentivo baseado em tokens com filtros Bloom para ocultar localização exata
2. *[CANDIDATE]* Criptografia homomórfica para consultas de proximidade criptografadas
3. *[CANDIDATE]* Encontros virtuais temáticos como alternativa principal ao encontro presencial


## 7. Propostas Rejeitadas (com Justificativa)

- **Rejeitado:** Uso de criptografia homomórfica para consultas de proximidade (Origem: ALTERNATIVES)
  *Motivo:* Alto consumo computacional e latência incompatíveis com o MVP inicial
- **Rejeitado:** Incentivo baseado em tokens com filtros Bloom (Origem: ALTERNATIVES)
  *Motivo:* Complexidade de gerenciamento econômico e risco de fraude excedem o escopo inicial


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Geohashing difuso (grade de células geográficas) combinado com matching temático baseado em embeddings e ontologia temática curada pela comunidade)

**Dependências Externas do Core:**
- Serviço de geolocalização que forneça coordenadas de usuários (ex.: GPS ou IP)
- Infraestrutura de armazenamento e consulta de grades de geohash (banco de dados geoespacial)
- Modelo de embeddings temáticos treinado ou fine‑tuned para literatura rara
- Plataforma colaborativa para criação e manutenção da ontologia temática
- Mecanismo de anonimização que limite a divulgação da célula ao tamanho de grade adequado

**Testes Discriminativos do Core:**
- [ ] Medir o nível de anonimato fornecido por diferentes resoluções de geohash (ex.: 5km vs 10km) usando ataques de re‑identificação simulados
- [ ] Comparar a precisão de matching temático baseado em embeddings contra um baseline de keyword matching em um conjunto de usuários piloto
- [ ] Avaliar a latência e throughput de consultas que combinam filtro de célula geohash + busca vetorial de embeddings em um ambiente de carga realista
- [ ] Conduzir um estudo de usabilidade onde usuários avaliam a relevância das recomendações geradas pelo mecanismo core
- [ ] Testar a robustez da ontologia temática ao inserir novos termos e verificar consistência automática via validação de regras


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Implementar e medir o impacto de um sistema de incentivos baseado em tokens com filtros Bloom para ocultar localização exata
- [ ] *[EXPLORATÓRIO]* Avaliar a viabilidade prática de consultas de proximidade criptografadas usando criptografia homomórfica em um protótipo de baixa escala
- [ ] *[EXPLORATÓRIO]* Testar a aceitação de encontros virtuais temáticos como alternativa principal ao presencial, medindo engajamento e satisfação


## 10. Próximo Passo Recomendado

Desenvolver um protótipo da grade de localização difusa e do mecanismo de matching temático baseado em embeddings, testar com um grupo piloto de leitores de livros raros, coletar métricas de privacidade e qualidade de correspondência e refinar a ontologia temática com o feedback dos usuários.
