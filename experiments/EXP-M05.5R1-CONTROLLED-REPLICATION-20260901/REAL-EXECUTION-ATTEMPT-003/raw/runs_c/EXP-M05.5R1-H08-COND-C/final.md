# Pacote Lean de Maturação — Run EXP-M05.5R1-H08-COND-C

**Status:** `COMPLETED_WITH_FOCUSED_ESCALATION` | **Chamadas de Modelo Utilizadas:** 2 (Max: 2)

---

## 1. Fonte Humana Imutável (SourceAnchor)

> Acho que pessoas que cozinham para uma ou duas pessoas desperdiçam menos alimentos se receberem sugestões de refeições baseadas no que já têm em casa e no prazo de validade aproximado. Gostaria de testar se isso realmente muda o comportamento delas.


## 2. Intenção & Problema Estruturado (Lean First Pass)

- **Intenção do Usuário:** Testar se sugestões de refeições baseadas no estoque doméstico e na validade aproximada reduzem o desperdício de alimentos para quem cozinha para 1‑2 pessoas.
- **Problema Interpretado:** Pessoas que cozinham para uma ou duas pessoas desperdiçam alimentos porque não recebem sugestões de refeições alinhadas ao que já têm em casa e ao prazo de validade dos ingredientes.

## 3. Mecanismo Primário Proposto

**Mecanismo:** Algoritmo que gera sugestões de refeições a partir do inventário de alimentos disponíveis em casa e das datas de validade aproximadas, apresentando opções que utilizem itens próximos ao vencimento.
- **Base de Autoridade Auditada:** `MODEL_HYPOTHESIS`
- **Justificativa:** Hipótese de que recomendações personalizadas aumentam a probabilidade de usar alimentos antes que expirem, diminuindo o desperdício.


## 4. Alternativas Concorrentes Identificadas

1. **Aplicativos genéricos de receitas que não consideram o estoque ou validade dos alimentos** (Base: `MODEL_HYPOTHESIS`)
   - *Tradeoffs:* Baixa relevância para redução de desperdício, Requer que o usuário compre novos ingredientes
2. **Planilhas manuais de planejamento de refeições onde o usuário decide o que cozinhar** (Base: `MODEL_HYPOTHESIS`)
   - *Tradeoffs:* Alto custo de tempo para o usuário, Risco de erro humano ao estimar validade


## 5. Avaliação do Early Epistemic Gate (Custo = 0 chamadas)

- **Veredito do Gate:** `ESCALATE_FOCUSED`
- **Motivo de Escalação:** `COMPETING_MECHANISMS`
- **Explicação:** Escalação justificada para comparação focada entre mecanismos concorrentes.
- **Autoridade Usurpada Detectada:** `False`
- **Candidatos Não Ancorados:** 3

## 6. Resultado da Escalação Focada (Chamada 2)

**Incerteza Alvo:** Um algoritmo que, dado o inventário doméstico e datas de validade aproximadas, gera sugestões de refeições priorizando itens próximos ao vencimento.
- **Análise / Crítica:** A incerteza gira em torno de qual mecanismo de priorização produz o melhor equilíbrio entre redução de desperdício e satisfação do usuário. Dois mecanismos concorrentes são considerados: (1) priorizar estritamente alimentos com menor tempo restante até o vencimento (mecanismo de minimização de desperdício) e (2) combinar a proximidade do vencimento com preferências de sabor e valor nutricional (mecanismo de otimização de satisfação). Avaliamos como cada abordagem impacta métricas de desperdício, aceitação da sugestão e complexidade computacional, identificando pontos críticos onde um pode superar o outro.
- **Trade-offs Resolvidos:** Definimos que a redução de desperdício tem peso maior que a variedade quando o tempo até o vencimento é inferior a 3 dias., Aceitação do usuário será medida como critério secundário, permitindo ajustes dinâmicos se a taxa de rejeição ultrapassar 20%.
- **Testes Discriminativos Sugeridos:**
  - [ ] Teste A/B com 100 usuários: grupo 1 recebe sugestões baseadas apenas no vencimento, grupo 2 recebe sugestões que equilibram vencimento e preferências.
  - [ ] Medição de quantidade de alimentos descartados após 7 dias de uso das sugestões.
  - [ ] Survey de satisfação do usuário após cada refeição sugerida.
- **Progresso Decisório:** `True`

## 7. Próximo Passo Recomendado

Implementar o motor de priorização dual, configurar o experimento A/B descrito e coletar métricas de desperdício e satisfação durante duas semanas.
