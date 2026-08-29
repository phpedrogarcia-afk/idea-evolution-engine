# Pacote de Maturação da Ideia — Run EXP-M05.4-IDEA-03-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Um sistema para conectar leitores de livros raros: ou através de um mapa geográfico de proximidade física entre vizinhos, ou através de um feed assíncrono baseado em afinidade de temas obscuros.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Criar um sistema que conecte leitores de livros raros, oferecendo um mapa de proximidade física entre vizinhos e um feed assíncrono baseado em afinidade de temas obscuros.
- **Problema Central:** Os leitores de livros raros não têm um meio eficaz para encontrar outros leitores próximos geograficamente ou com interesses temáticos semelhantes, dificultando a troca de informações e possíveis empréstimos.
- **Atores / Usuários:** Leitores de livros raros, Proprietários de livros raros, Vizinhos que possuem livros raros


## 3. Versão Refinada e Mecanismo Proposto

Plataforma descentralizada que conecta leitores de livros raros mediante proximidade criptográfica baseada em provas de conhecimento zero e um feed de afinidade temática, preservando privacidade e respeitando direitos autorais.


- **Justificativa de Promoção ao Core:** Atende ao desejo explícito do usuário por privacidade total, elimina exposição de localização, e fornece recomendações temáticas, ao mesmo tempo que mantém a descentralização necessária para escalar a rede de leitores escassos. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Exposição da localização dos usuários sem garantias robustas de privacidade
   - *Impacto:* Usuários podem recusar o serviço ou sofrer riscos de segurança, comprometendo a adoção e violando regulamentos de proteção de dados
   - *Parte Afetada:* Privacidade dos usuários / camada de dados
2. **[HIGH]** Baixa densidade de leitores com livros raros impede a formação de uma rede útil
   - *Impacto:* Sem um número crítico de participantes, o mapa e o feed terão poucos resultados, tornando o produto inútil e levando ao abandono
   - *Parte Afetada:* Funcionalidade central / adoção de usuários
3. **[MEDIUM]** Riscos legais ao facilitar empréstimo ou troca de livros raros protegidos por direitos autorais ou com valor patrimonial
   - *Impacto:* A plataforma pode ser responsabilizada por violações de direitos autorais ou danos a bens valiosos, resultando em litígios e necessidade de compliance onerosa
   - *Parte Afetada:* Conformidade legal / responsabilidade da plataforma


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Rede P2P descentralizada que usa provas de conhecimento zero (zero‑knowledge proofs) para validar a proximidade criptográfica sem revelar coordenadas reais; o mapa de vizinhança é substituído por clusters virtuais baseados em afinidade temática e histórico de trocas
   - *Tradeoffs:* Complexidade de implementação e necessidade de clientes capazes de executar provas de conhecimento zero, Dependência de participação ativa para que os clusters virtuais atinjam densidade suficiente
2. **Mecanismo:** Hub centralizado que coleta metadados anonimizado dos usuários e aplica privacidade diferencial antes de gerar recomendações de afinidade; o empréstimo de livros ocorre via um serviço de escrow legalmente auditado que verifica direitos autorais e valor patrimonial antes de autorizar a troca
   - *Tradeoffs:* Requer confiança em um operador central e custos operacionais de auditoria legal, Possível perda de granularidade nas recomendações devido ao ruído introduzido pela privacidade diferencial
3. **Mecanismo:** Modelo federado onde bibliotecas, arquivos e coletivos locais atuam como nós de referência; o sistema só compartilha hashes anônimos dos livros e utiliza um sistema de reputação para conectar leitores a esses nós, permitindo encontros presenciais controlados sem divulgar endereços exatos
   - *Tradeoffs:* Dependência de instituições parceiras para manter nós ativos, Necessidade de acordos formais com as instituições para lidar com questões de direitos autorais


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Hub centralizado que coleta metadados anonimizado, aplica privacidade diferencial e utiliza um serviço de escrow legalmente auditado para empréstimo de livros.
2. *[CANDIDATE]* Modelo federado onde bibliotecas, arquivos e coletivos locais atuam como nós de referência, compartilhando hashes anônimos e usando reputação para conectar leitores a encontros presenciais controlados.


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Rede P2P descentralizada usando provas de conhecimento zero para validar proximidade criptográfica sem revelar coordenadas reais, formando clusters virtuais por afinidade temática.)

**Dependências Externas do Core:**
- Bibliotecas criptográficas maduras que implementem ZK proofs específicas para provas de proximidade física (ex.: zk-SNARKs/zk-STARKs adaptados).
- Rede de nós suficientemente densa em áreas com leitores de livros raros para que a proximidade criptográfica seja significativa.
- Infra‑estrutura de descoberta de pares (peer discovery) que funcione sem expor endereços IP reais.
- Regulamentações locais sobre anonimato e proteção de dados que permitam a coleta de hashes de livros sem violar direitos autorais.
- Mecanismos de mitigação de ataques Sybil e de controle de reputação dentro da rede P2P.

**Testes Discriminativos do Core:**
- [ ] Implementar um protótipo de ZK proof de proximidade e validar que dois dispositivos a até 10 km podem gerar uma prova verificável sem trocar coordenadas reais.
- [ ] Simular uma rede P2P com 500 nós distribuídos geograficamente e medir a taxa de sucesso na formação de clusters temáticos baseados em hashes de metadados.
- [ ] Benchmark de tempo de geração e verificação das ZK proofs de proximidade em hardware típico de leitores (Android, iOS).
- [ ] Executar testes de resistência a ataques Sybil inserindo nós maliciosos e avaliar a eficácia dos mecanismos de reputação.
- [ ] Analisar tráfego de rede durante a geração/verificação das provas para detectar possíveis vazamentos de informação por padrões de comunicação.


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Desenvolver um hub centralizado que agrega metadados anonimizado e aplicar privacidade diferencial; medir a utilidade das recomendações geradas comparado ao modelo P2P puro.
- [ ] *[EXPLORATÓRIO]* Implementar um modelo federado onde bibliotecas locais atuam como nós de referência, compartilhando apenas hashes anônimos; testar a eficácia na conexão de leitores a encontros presenciais controlados.
- [ ] *[EXPLORATÓRIO]* Criar um serviço de escrow legalmente auditado para empréstimo de livros; conduzir um piloto com parceiros jurídicos para validar conformidade regulatória e fluxo de autorização.


## 10. Próximo Passo Recomendado

Desenvolver um protótipo da rede P2P com ZK proofs, validar a privacidade em testes controlados e conduzir revisão jurídica sobre o fluxo de troca de livros antes de expandir a rede.
