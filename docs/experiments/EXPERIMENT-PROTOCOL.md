# EXPERIMENT-PROTOCOL.md — Protocolo Metodológico de Experimentação

> **Protocolo Científico para Testes Empíricos do Idea Evolution Engine**

---

## 1. Princípios Experimentais Obrigatórios
1. **Falsificabilidade Estrita:** Todo experimento deve declarar formalmente as condições sob as quais a hipótese testada será considerada refutada.
2. **Isolamento de Variáveis e Baseline Obrigatório:** Nenhum ganho de inteligência ou deliberação pode ser alegado sem comparação controlada com um baseline explícito (ex: modelo individual forte sem orquestração).
3. **Custo como Variável de Controle:** Todo experimento deve contabilizar tokens de entrada/saída, latência e custo financeiro. O progresso deve ser medido como *Progresso Decisório por Unidade de Custo*.
4. **Reprodutibilidade:** Fixtures, prompts, sementes aleatórias (quando aplicável) e versões de modelos devem ser congelados e registrados.

---

## 2. Estrutura Padrão de um Protocolo de Teste

```text
ExperimentPlan
├── experiment_id: EXP-XXX
├── hypothesis: H1, H2... (vinculada a SCIENTIFIC-HYPOTHESES.md)
├── target_idea_fixtures: Conjunto de ideias-teste padronizadas (esparsas, ricas, contraditórias)
├── baselines:
│   ├── Baseline A: Prompt único direto (Single-Shot Strong Model)
│   └── Baseline B: Chat multiagente livre não-estruturado
├── treatment: Deliberação governada sob DeliberationContract (IEE)
├── independent_variables: Topologia, papéis epistemológicos, limites de budget
├── dependent_metrics:
│   ├── Decision Delta por 1k tokens
│   ├── Taxa de detecção de premissas ocultas
│   ├── Taxa de identificação de falhas materiais reais
│   └── Aderência a critérios de parada (ausência de loops infinitos)
└── falsification_criteria: Condições para rejeitar a superioridade do IEE
```
