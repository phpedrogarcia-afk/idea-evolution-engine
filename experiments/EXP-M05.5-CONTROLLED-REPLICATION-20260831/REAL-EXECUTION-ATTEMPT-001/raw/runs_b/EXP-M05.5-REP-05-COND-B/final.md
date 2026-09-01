# Pacote de Maturação da Ideia — Run EXP-M05.5-REP-05-COND-B

**Status:** `FAILED` | **Ciclos de Reconstrução:** 0

---

## 1. Ideia Original (Imutável)

> Um serviço de pequenos reparos de roupas por bairro: coleta na portaria, conserto e devolução em até 48 horas, sem exigir que o cliente esteja em casa.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Oferecer um serviço de reparos de roupas de pequeno porte por bairro que coleta na portaria, conserta e devolve em até 48h, eliminando a necessidade de presença do cliente.
- **Problema Central:** Clientes precisam de reparos rápidos em roupas sem precisar estar em casa para entrega ou coleta.
- **Atores / Usuários:** Clientes residentes, Costureiros/técnicos de reparo, Funcionários de coleta/entrega, Equipe da portaria


## 3. Versão Refinada e Mecanismo Proposto

Um serviço local que coleta roupas na portaria do condomínio, realiza pequenos reparos e devolve ao cliente em até 48 horas, sem necessidade de o cliente estar presente.


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Risco de perda, dano ou furto das roupas durante coleta, transporte ou reparo
   - *Impacto:* Os clientes confiam itens pessoais ao serviço; incidentes geram reclamações, responsabilidade civil e perda de confiança, comprometendo a viabilidade do negócio
   - *Parte Afetada:* Logística de coleta/entrega
2. **[MEDIUM]** Incapacidade de cumprir o prazo de 48 horas para todos os tipos de reparos pequenos
   - *Impacto:* A promessa de devolução em até 48h é central para a proposta de valor; atrasos frequentes reduzem a satisfação do cliente e podem gerar penalidades contratuais
   - *Parte Afetada:* Operações de reparo


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Utilizar sacolas seladas com RFID e seguro integrado para coleta, transporte e reparo, permitindo rastreamento em tempo real e cobertura contra perdas ou danos
   - *Tradeoffs:* Custo adicional para sacolas inteligentes e seguro, Necessidade de infraestrutura de leitura RFID, Possível preocupação dos clientes com privacidade dos dados
2. **Mecanismo:** Criar uma rede de costureiros locais parceiros com contrato de garantia de 48h e um sistema digital de fila que prioriza reparos por complexidade e tempo estimado
   - *Tradeoffs:* Dependência de qualidade e disponibilidade dos parceiros, Necessidade de gerenciamento de contratos e monitoramento de desempenho, Possível variação na qualidade do serviço
3. **Mecanismo:** Instalar lockers seguros nas portarias dos condomínios onde os clientes depositam as roupas; a equipe recolhe, repara e devolve os itens ao mesmo locker
   - *Tradeoffs:* Investimento em hardware de lockers e manutenção, Limitações de espaço nas áreas comuns, Necessidade de treinamento da equipe para operar os lockers


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Aplicativo móvel para agendamento
2. *[CANDIDATE]* Parcerias com costureiros locais
3. *[CANDIDATE]* Rede logística de coleta e entrega por bairro


## 10. Próximo Passo Recomendado

Definir próximo experimento com usuários.
