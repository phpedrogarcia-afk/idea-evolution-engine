# docs/intelligence/BASELINE-POLICY.md — Política de Medição de Baseline

> **SEM BASELINE, NENHUMA ALEGAÇÃO DE MELHORIA É VÁLIDA.**
> *Sem medição anterior, um resultado é no máximo uma observação isolada.*

---

## 1. Princípio da Medição Prévia
> **BASELINE_REQUIRED:** Nenhuma IA ou colaborador pode alegar que uma nova solução, prompt, topologia ou arquitetura "melhorou" o sistema sem apresentar a medição do baseline correspondente.

---

## 2. Dimensões que Exigem Baseline Obrigatório
1. **Custo de Contexto e Tokens:** "Este router economiza tokens" $\to$ Exige medir o consumo de tokens antes e depois na mesma tarefa.
2. **Taxa de Redundância:** "Reduziu repetições" $\to$ Exige contagem de paráfrases antes e depois.
3. **Precisão de Classificação:** "Classifica melhor" $\to$ Exige acurácia no dataset de teste padronizado.
4. **Detecção de Falhas:** "Encontra mais problemas" $\to$ Exige benchmark comparativo sob o mesmo conjunto de premissas.
5. **Tempo e Latência:** "Mais rápido" $\to$ Exige medição de tempo de resposta em hardware e condições equivalentes.

---

## 3. Classificação de Alegações sem Baseline
Se uma medição for apresentada sem comparação com baseline:
- O sistema classifica o resultado como `OBSERVATION` isolada.
- O resultado **NÃO** pode ser registrado como `IMPROVEMENT_CONFIRMED`.
- O relatório deve registrar: `"Baseline ausente; ganho comparativo não comprovado"`.
