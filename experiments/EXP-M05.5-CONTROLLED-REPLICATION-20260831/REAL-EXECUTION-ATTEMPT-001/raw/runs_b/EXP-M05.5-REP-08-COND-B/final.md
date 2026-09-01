# Pacote de Maturação da Ideia — Run EXP-M05.5-REP-08-COND-B

**Status:** `FAILED` | **Ciclos de Reconstrução:** 0

---

## 1. Ideia Original (Imutável)

> Um leitor digital que quer testar se reduzir animações de interface durante a leitura melhora a concentração; a hipótese deve ser avaliada antes de transformar isso em um produto cheio de recursos.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Testar a hipótese de que menos animações aumentam a concentração antes de desenvolver um produto completo.
- **Problema Central:** Avaliar se a redução de animações na interface de um leitor digital melhora a concentração durante a leitura.
- **Atores / Usuários:** leitores digitais, usuários que leem em dispositivos digitais


## 3. Versão Refinada e Mecanismo Proposto

Um leitor digital que pretende avaliar, por meio de teste, se a diminuição das animações da interface durante a leitura aumenta a concentração do usuário, antes de desenvolver um produto completo.


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Concentration is difficult to measure objectively, leading to unreliable results.
   - *Impacto:* If the metric does not accurately reflect true concentration, the test cannot validate the hypothesis, rendering the entire study inconclusive.
   - *Parte Afetada:* Measurement methodology
2. **[MEDIUM]** Potential confounding variables (e.g., lighting, text difficulty, user fatigue) are not controlled.
   - *Impacto:* These factors can influence concentration independently of animation changes, biasing the outcome.
   - *Parte Afetada:* Experimental design
3. **[MEDIUM]** Reducing animations may decrease user engagement or perceived responsiveness.
   - *Impacto:* A less engaging interface could offset any concentration gains, leading to negative user experience.
   - *Parte Afetada:* User experience


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Integrar sensores de rastreamento ocular e EEG para medir concentração de forma objetiva enquanto o usuário lê com diferentes níveis de animação
   - *Tradeoffs:* Equipamento caro e necessidade de ambiente controlado, Baixa escalabilidade para testes em grande escala, Curva de aprendizado para análise dos dados fisiológicos
2. **Mecanismo:** Realizar testes A/B controlados combinando escalas de autorrelato validadas com randomização de iluminação, dificuldade do texto e intervalos de descanso para mitigar variáveis de confusão
   - *Tradeoffs:* Dependência de medidas subjetivas que podem ser enviesadas, Necessidade de maior número de participantes para obter significância estatística, Tempo prolongado para coleta e análise dos dados
3. **Mecanismo:** Substituir a leitura por micro‑tarefas de foco (ex.: encontrar palavras‑chave ou responder perguntas de compreensão) e usar desempenho (acurácia e tempo de resposta) como proxy de concentração, alternando a presença de animações
   - *Tradeoffs:* O desempenho nas tarefas pode não refletir a concentração real durante leitura prolongada, Possível aumento da carga cognitiva que interfere no objetivo original, Necessidade de projetar tarefas que sejam suficientemente representativas


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* modo de leitura sem animações
2. *[CANDIDATE]* configuração para desativar animações
3. *[CANDIDATE]* estudo de usabilidade com medição de concentração


## 10. Próximo Passo Recomendado

Definir próximo experimento com usuários.
