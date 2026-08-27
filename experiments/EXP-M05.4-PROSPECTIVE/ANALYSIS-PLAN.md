# ANALYSIS-PLAN.md — Plano de Análise Estatística e Epistêmica M05.4

> **PLANO DE ANÁLISE PRÉ-REGISTRADO**
> **STATUS:** `FROZEN_BEFORE_EXECUTION`

---

## 1. Análise do Desfecho Primário

Após o congelamento da avaliação humana e a abertura do `BLIND-REVEAL.json`, serão computados:

1. **Tabela de Rankings por Ideia (N=8):**
   - Frequência de 1º Lugar para Condição A, Condição B e Condição C;
   - Frequência de 2º Lugar;
   - Frequência de 3º (Último) Lugar;
   - Frequência de Escolha de Processo ("Com qual processo você continuaria?").

*Aviso Metodológico:* Devido ao tamanho amostral $N=8$, não serão feitas alegações de significância estatística assintótica ($p$-values). Os resultados serão reportados como sinal de replicação empírica direta.

---

## 2. Análise de Eficiência e Rendimento Epistêmico

Para cada condição, serão consolidadas as métricas objetivas:

| Métrica de Custo / Eficiência | Condição A | Condição B | Condição C |
| :--- | :--- | :--- | :--- |
| **Total de Chamadas de Modelo** | $8$ ($1$ por ideia) | $\approx 48-80$ ($6-10$ por ideia) | $\le 16$ ($1-2$ por ideia) |
| **Média de Tokens Consumidos** | Medido via API | Medido via API | Medido via API |
| **Latência Média por Ideia** | Medido via API | Medido via API | Medido via API |
| **Razão de Preferência / Chamada** | $\text{Vitórias}_A / 8$ | $\text{Vitórias}_B / \text{Calls}_B$ | $\text{Vitórias}_C / \text{Calls}_C$ |

---

## 3. Teste das Predições Pré-registradas do FioED

Cada uma das 10 predições congeladas (PRED-01 a PRED-10) será avaliada categoricamente:
- **`CONFIRMED`:** O sinal observável e a preferência humana corroboraram a hipótese;
- **`REFUTED`:** O resultado contradiz a previsão teórica;
- **`INCONCLUSIVE`:** Ambiguidade nos dados ou falha de observação.

Qualquer descoberta exploratória que não conste em PRED-01 a PRED-10 será formalmente rotulada no relatório final como **`POST_HOC_OBSERVATION`**.
