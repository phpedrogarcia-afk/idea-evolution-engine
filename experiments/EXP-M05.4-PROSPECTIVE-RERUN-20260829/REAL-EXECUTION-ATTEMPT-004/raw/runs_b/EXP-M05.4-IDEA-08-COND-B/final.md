# Pacote de Maturação da Ideia — Run EXP-M05.4-IDEA-08-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Um diário reflexivo que ajuda a capturar sensações sutis do dia a dia, medindo se o tempo de resposta do editor de texto abaixo de 16ms reduz a distração ao digitar.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Criar um diário reflexivo que registre sensações cotidianas e avalie se um editor de texto com latência inferior a 16 ms reduz a distração durante a escrita.
- **Problema Central:** Os usuários se distraem ao digitar quando o editor de texto tem latência perceptível, e não há evidência de que reduzir o tempo de resposta abaixo de 16 ms diminua essa distração.
- **Atores / Usuários:** Usuário que escreve no diário


## 3. Versão Refinada e Mecanismo Proposto

Um diário digital reflexivo que registra sensações cotidianas e mede a latência do editor de texto usado, correlacionando latências <16 ms com níveis de distração durante a digitação.


- **Justificativa de Promoção ao Core:** Essa abordagem fornece a precisão de milissegundos requerida pela intenção humana e evita dependências de hardware externo ou modelos hipotéticos. (Base: `VALID_USER_DERIVATION`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Imprecisão na medição do tempo de resposta do editor com precisão de milissegundos em diferentes sistemas operacionais e hardware
   - *Impacto:* Dados de latência imprecisos invalidam a correlação entre latência e distração, comprometendo todo o estudo
   - *Parte Afetada:* Módulo de Medição de Performance
2. **[MEDIUM]** Suposição de que latências abaixo de 16 ms são percebidas como instantâneas pelos usuários não é suportada por evidência psicológica
   - *Impacto:* Se os usuários não percebem diferença, a redução de latência não terá efeito sobre a distração, tornando o objetivo da ideia irrealizável
   - *Parte Afetada:* Hipótese de Experiência do Usuário
3. **[HIGH]** Dependência de autorrelato de distração como métrica principal, que é altamente subjetiva e suscetível a viés
   - *Impacto:* Métricas subjetivas dificultam estabelecer causalidade clara entre latência e distração, enfraquecendo conclusões
   - *Parte Afetada:* Coleta e Análise de Dados


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Implementar medição de latência baseada em timestamps de alta resolução (Performance.now) combinada com calibração automática por hardware/OS usando benchmarks de microsegundos antes da sessão de escrita
   - *Tradeoffs:* Requer permissões de baixo nível ou extensões do navegador; aumento da complexidade de implementação; possível overhead de desempenho durante a calibração
2. **Mecanismo:** Substituir o limiar fixo de 16 ms por um limiar perceptual individual determinado por testes psicofísicos adaptativos e complementar a avaliação de distração com métricas fisiológicas (p. ex., variação de frequência cardíaca ou rastreamento ocular)
   - *Tradeoffs:* Necessita equipamento adicional (sensor de frequência cardíaca, eye‑tracker) e sessões de calibração mais longas; aumento da carga cognitiva para o usuário durante os testes
3. **Mecanismo:** Criar um modelo híbrido que combina autorrelato de distração com indicadores passivos de comportamento (variação de velocidade de digitação, frequência de pausas, erros de tecla) treinado por aprendizado de máquina para inferir níveis de distração
   - *Tradeoffs:* Requer coleta de dados extensiva para treinar o modelo; risco de viés algorítmico; necessidade de validação contínua


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Determinar limiar perceptual individual via testes psicofísicos baseados em autorrelato, sem necessidade de sensores adicionais
2. *[CANDIDATE]* Explorar modelo híbrido que combina autorrelato de distração com indicadores passivos de comportamento (velocidade de digitação, pausas, erros)


## 7. Propostas Rejeitadas (com Justificativa)

- **Rejeitado:** Substituir o limiar fixo de 16 ms por um limiar perceptual individual determinado por testes psicofísicos adaptativos e métricas fisiológicas (Origem: ALTERNATIVES)
  *Motivo:* Requer equipamento adicional (sensor de frequência cardíaca, eye‑tracker) que foge da intenção original do usuário
- **Rejeitado:** Criar um modelo híbrido que combina autorrelato de distração com indicadores passivos de comportamento treinado por aprendizado de máquina (Origem: ALTERNATIVES)
  *Motivo:* Complexidade alta, necessidade de grande volume de dados e risco de viés algorítmico, não suportado pela intenção explícita do usuário


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Medição precisa da latência do editor de texto usando timestamps de alta resolução (performance.now) com calibração automática por hardware/SO antes da sessão de escrita.)

**Dependências Externas do Core:**
- Acesso ao API performance.now no ambiente de execução (navegador ou app desktop)
- Permissão para executar código de benchmark de alta frequência antes da sessão
- Consistência do relógio de alta resolução do SO/hardware durante a medição
- Capacidade de registrar timestamps imediatamente antes da captura de entrada e imediatamente após a renderização do texto
- Mecanismo de sincronização entre thread de entrada e thread de renderização para evitar atrasos de software

**Testes Discriminativos do Core:**
- [ ] Comparar latência medida por performance.now com um equipamento externo de captura de vídeo de alta velocidade para validar a precisão
- [ ] Executar o benchmark de calibração em diferentes máquinas/OS e medir a variabilidade do offset estimado
- [ ] Realizar um estudo controlado onde participantes escrevem com latências medidas <16 ms e >16 ms e reportam níveis de distração
- [ ] Testar se a calibração automática reduz o erro médio da medição em pelo menos 50 % comparado a medições não calibradas
- [ ] Verificar a consistência das medições de latência ao longo de sessões prolongadas (ex.: 30 min)


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Desenvolver testes psicofísicos adaptativos para determinar o limiar perceptual individual de latência de teclado
- [ ] *[EXPLORATÓRIO]* Construir modelo híbrido que combina autorrelato de distração com métricas passivas (velocidade de digitação, pausas, taxa de erros) e validar sua capacidade preditiva
- [ ] *[EXPLORATÓRIO]* Incorporar sensores fisiológicos (ex.: frequência cardíaca, rastreamento ocular) para investigar correlações adicionais com distração
- [ ] *[EXPLORATÓRIO]* Explorar algoritmos de aprendizado de máquina que inferem níveis de distração a partir de padrões de digitação e latência medida


## 10. Próximo Passo Recomendado

Desenvolver um protótipo da medição de latência com performance.now, calibrar em diferentes dispositivos e conduzir um estudo piloto para correlacionar latência medida com autorrelatos de distração.
