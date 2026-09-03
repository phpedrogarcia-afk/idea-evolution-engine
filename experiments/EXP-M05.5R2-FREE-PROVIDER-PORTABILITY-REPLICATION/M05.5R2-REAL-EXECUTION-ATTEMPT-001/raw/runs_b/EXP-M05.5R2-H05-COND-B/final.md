# Pacote de Maturação da Ideia — Run EXP-M05.5R2-H05-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> No galpão onde fazemos reparos de bicicletas, perdemos muito tempo procurando ferramentas que foram usadas em outro canto ou ficaram em bicicletas prontas. Pensei em criar um jeito físico e prático de saber onde as ferramentas importantes estão durante o dia.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Criar um método físico e prático que permita saber, a qualquer momento durante o dia, onde estão as ferramentas importantes usadas no reparo de bicicletas.
- **Problema Central:** Tempo excessivo gasto pelos mecânicos ao procurar ferramentas que foram usadas em outro local ou deixadas em bicicletas concluídas, indicando falta de um método claro de localização das ferramentas no galpão.
- **Atores / Usuários:** Mecânicos de bicicletas, Assistentes do galpão, Gerente da oficina


## 3. Versão Refinada e Mecanismo Proposto

Sistema físico simples usando um painel magnético vertical com suportes coloridos designados para cada ferramenta essencial, permitindo visualização imediata da localização das ferramentas durante o dia.


- **Justificativa de Promoção ao Core:** Fornece localização visual imediata, baixo custo, não depende de energia ou dispositivos eletrônicos, atendendo diretamente à intenção humana de um método físico e prático para saber onde estão as ferramentas importantes. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Dependência de atualização manual da localização das ferramentas
   - *Impacto:* Se os mecânicos não registrarem imediatamente onde deixaram cada ferramenta, o sistema exibirá informações incorretas, anulando o benefício esperado de economia de tempo
   - *Parte Afetada:* Procedimento de registro manual
2. **[MEDIUM]** Identificação visual insuficiente para ferramentas semelhantes
   - *Impacto:* Ferramentas com aparência similar podem ser confundidas, levando a colocações errôneas e à necessidade de nova busca, aumentando o tempo gasto
   - *Parte Afetada:* Design de marcação/etiquetagem
3. **[MEDIUM]** Espaço físico limitado impede a instalação de suportes ou quadros adicionais
   - *Impacto:* A falta de espaço pode tornar o sistema impraticável ou criar obstruções que atrapalham o fluxo de trabalho dos mecânicos
   - *Parte Afetada:* Layout do galpão


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Integrar etiquetas RFID em cada ferramenta e instalar um leitor RFID fixo na parede do galpão que acende um LED de cor correspondente quando a ferramenta está fora de sua posição designada.
   - *Tradeoffs:* Custo inicial dos tags RFID e do leitor, Necessidade de alimentação elétrica contínua, Possível interferência em ambientes com metal pesado
2. **Mecanismo:** Instalar um painel magnético vertical com perfis em forma de silhueta (shadow board) que inclui recortes de diferentes formas e cores para cada ferramenta, combinado com sensores de peso discretos sob cada recorte que acionam um pequeno display de LED indicando a ausência da ferramenta.
   - *Tradeoffs:* Complexidade de calibrar sensores de peso para ferramentas de tamanho similar, Necessidade de manutenção dos sensores ao longo do tempo, Limitação ao tipo de ferramenta que pode ser acomodada no painel
3. **Mecanismo:** Aplicativo móvel que utiliza códigos QR adesivos nas ferramentas; ao escanear o QR, o app registra a posição atual e exibe um mapa em tempo real das ferramentas, permitindo buscas rápidas mesmo em áreas com espaço restrito.
   - *Tradeoffs:* Dependência de smartphones e conexão à internet ou rede local, Necessidade de imprimir e aplicar QR codes resistentes ao desgaste, Curva de aprendizado para a equipe usar o aplicativo


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Aplicativo móvel com códigos QR nas ferramentas para registro de posição em tempo real


## 7. Propostas Rejeitadas (com Justificativa)

- **Rejeitado:** Integrar etiquetas RFID em cada ferramenta e instalar um leitor RFID fixo na parede do galpão (Origem: ALTERNATIVES)
  *Motivo:* Requer alimentação elétrica contínua e aumenta significativamente o custo inicial, além de potencial interferência em ambientes metálicos
- **Rejeitado:** Instalar painel magnético com sensores de peso discretos sob cada recorte que acionam um display LED indicando ausência da ferramenta (Origem: ALTERNATIVES)
  *Motivo:* Complexidade de calibrar sensores de peso, necessidade de manutenção constante e limitação ao tipo de ferramenta que pode ser acomodada


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Painel magnético vertical com suportes coloridos designados para cada ferramenta essencial.)

**Dependências Externas do Core:**
- Painel magnético de aço ou material ferromagnético com força de retenção suficiente
- Ímãs de neodímio ou outro tipo de ímã de alta potência para garantir a fixação das ferramentas
- Suportes coloridos (plástico, alumínio pintado ou outro material) projetados para acomodar as formas das ferramentas
- Método de fixação do painel à parede (parafusos, buchas, suportes)
- Ferramentas que contenham componentes ferromagnéticos ou a adição de inserções magnéticas quando necessário

**Testes Discriminativos do Core:**
- [ ] Teste de carga: pendurar cada ferramenta no suporte correspondente e medir a força necessária para removê‑la
- [ ] Teste de resistência ao impacto: simular vibrações e batidas típicas do ambiente e observar se as ferramentas permanecem fixas
- [ ] Teste de visibilidade: avaliar a rapidez com que um operador identifica a ferramenta correta sob diferentes níveis de iluminação
- [ ] Teste de durabilidade: expor o painel a ciclos de uso diário por 30 dias e verificar perda de magnetismo ou desgaste dos suportes
- [ ] Teste de instalação: medir o tempo e a facilidade de fixação do painel na parede usando os métodos de montagem previstos


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Desenvolver um aplicativo móvel que lê códigos QR colados nas ferramentas e registra a posição em tempo real; testar a precisão da localização via QR em diferentes ângulos de leitura
- [ ] *[EXPLORATÓRIO]* Implementar etiquetas RFID em cada ferramenta e instalar um leitor RFID fixo; medir a latência e a taxa de detecção quando a ferramenta está fora de sua posição designada
- [ ] *[EXPLORATÓRIO]* Criar um shadow board com recortes de silhueta e sensores de peso discretos; validar se o display LED indica corretamente a ausência da ferramenta
- [ ] *[EXPLORATÓRIO]* Avaliar a combinação de QR code + RFID para redundância de rastreamento; comparar custos e complexidade de integração


## 10. Próximo Passo Recomendado

Construir um protótipo do painel magnético com suportes coloridos, testar no galpão com a equipe, medir a redução no tempo de busca e coletar feedback para ajustes antes da produção final.
