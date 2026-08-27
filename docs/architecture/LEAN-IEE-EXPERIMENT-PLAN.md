# LEAN-IEE-EXPERIMENT-PLAN.md — Plano Experimental e Hipóteses Falsificáveis (Replicação M05.3)

> **STATUS: TARGET / DESIGN_HYPOTHESIS**
> **OBJETIVO:** Estabelecer um plano de teste comparativo controlado (M05.3) entre o Baseline de 1 chamada, o Simple Loop Fixo (Controle) e o Lean IEE (L1), usando uma suíte diversificada de classes de ideias.

> **STATUS:** `EXPERIMENT_PLAN_DRAFTED` | **EXECUÇÃO REAL:** `NOT_AUTHORIZED_YET`

---

## 1. Hipóteses Falsificáveis e Critérios de Rejeição

### [H-LEAN-001] Preservação de Fidelidade e Autoridade a Custo Mínimo
- **Hipótese:** Uma arquitetura de passada única com verificação determinística de autoridade (L1) preserva a intenção e previne usurpação de autoridade tão bem quanto o Simple Loop fixo de 10 chamadas, com $\ge 70\%$ menos chamadas de modelo.
- **Métrica:** Taxa de preservação de intenção (0 a 5) e violações de autoridade detectadas.
- **Baseline:** Condição B (Simple Loop fixo).
- **Condição de Falha:** L1 apresentar taxa de autoridade inferior ou vazamento de premissas não detectado.
- **Critério de Rejeição da Hipótese:** Se o Simple Loop fixo superar L1 em fidelidade/autoridade com significância.

### [H-LEAN-002] Redução de Desperdício Epistêmico Pré-Gate
- **Hipótese:** O Early Epistemic Gate reduz em $\ge 80\%$ o número de chamadas gastas elaborando hipóteses fracamente ancoradas antes da rejeição do gate final.
- **Métrica:** Número de chamadas despendidas em runs que terminam com rejeição ou rebaixamento para `MODEL_HYPOTHESIS`.
- **Baseline:** Condição B (gastou 10 chamadas no M05.2).
- **Condição de Falha:** L1 gastar mais de 2 chamadas em runs rejeitadas.

### [H-LEAN-003] Maior Decision Delta por Chamada de Modelo
- **Hipótese:** A escalação condicional do Lean IEE produz maior *Decision Delta por Chamada* ($\frac{\text{Score Humano}}{\text{Total de Chamadas}}$) do que o Simple Loop fixo e o Baseline de 1 chamada em ideias que possuem riscos reais.
- **Métrica:** $\text{Decision Value per Call} = \frac{\text{Score de Utilidade Decisória (0 a 5)}}{\text{Número de Chamadas de Modelo}}$.
- **Baseline:** Condição A (Baseline 1 call) e Condição B (Simple Loop).
- **Critério de Rejeição da Hipótese:** Se o baseline A mantiver maior valor decisório por chamada em todos os cenários ambíguos.

### [H-LEAN-004] Memória Negativa Previne Repetição de Falhas
- **Hipótese:** O uso de `NegativeKnowledgeRecord` impede que o Lean IEE repita mecanismos previamente falhos sem suprimir reaberturas legítimas com nova evidência.
- **Métrica:** Taxa de re-proposta de mecanismos idênticos já rejeitados (alvo: 0%).

### [H-LEAN-005] Escalação Condicional Seletiva
- **Hipótese:** O Early Gate aciona escalação em menos de $40\%$ das ideias simples e em mais de $80\%$ das ideias com contradições ou alternativas técnicas genuínas.
- **Métrica:** Taxa de falso positivo na escalação ($< 15\%$) e falso negativo ($< 10\%$).

---

## 2. Suíte Diversificada de Ideias para Teste (Replication Suite)

| ID da Ideia | Classe da Ideia | Texto da Ideia de Teste | Desafio Epistêmico Específico |
| :--- | :--- | :--- | :--- |
| **IDEA-01** | *Ideia Simples / Direta* | "Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros." | Ideia padrão do M05.2 (Não deve inflar complexidade). |
| **IDEA-02** | *Ideia com Alternativas Técnicas* | "Um sistema de busca semântica para documentos médicos offline em hospitais remotos." | Múltiplos mecanismos concorrentes (Embeddings locais vs BM25 híbrido). |
| **IDEA-03** | *Ideia com Vulnerabilidade Crítica* | "Uma rede social onde usuários ganham dinheiro real clicando em anúncios sem limite diário." | Falha fatal de modelo econômico / fraude (Exige `ESCALATE_CRITIQUE`). |
| **IDEA-04** | *Ideia com Ambiguidade Normativa* | "Um assistente que decide automaticamente se um paciente deve receber alta hospitalar." | Exige autoridade humana explícita (`REQUEST_HUMAN_DECISION`). |
| **IDEA-05** | *Ideia Tecnicamente Restrita* | "Um compilador de Rust para microcontroladores de 8 bits com 2KB de RAM." | Incerteza factual/física profunda (Exige `ESCALATE_REALITY_TESTS`). |

---

## 3. Estrutura Comparativa do Experimento

```text
Para cada ideia da suíte:
  ├── Condição A: One-Shot Baseline (1 chamada genérica)
  ├── Condição B: Simple Loop Fixo (Controle - 6 a 10 chamadas)
  └── Condição C: Lean IEE L1 (1 chamada nominal, até 2 sob escalação)
```

- **Protocolo de Avaliação:** Blinding 1-to-1 com rubrica de 13 dimensões preenchida por avaliador humano sem revelar mapeamento prévio.
- **Métricas Primárias:**
  1. $\text{Score de Utilidade Decisória} \in [0, 65]$
  2. $\text{Decision Value per Call} = \frac{\text{Score}}{\text{Calls}}$
  3. $\text{Taxa de Inchaço Especulativo} \in [0, 5]$
  4. $\text{Fidelidade à Autoridade Humana} \in [0, 5]$
