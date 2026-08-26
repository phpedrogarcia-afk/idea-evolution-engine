# EXPERIMENT-BACKLOG.md — Backlog de Experimentos Científicos

> **Planejamento de Testes Empíricos do IEE**

---

## 🧪 Backlog de Experimentos Planejados

### [EXP-001] Baseline de Bootstrap: Contratos Estruturados vs Prompt Único
- **Fase de Execução:** Fase 3 (Single Model)
- **Hipótese:** A condução do bootstrap estrutural via regras determinísticas gera maior diversidade de claims atômicas e expõe mais premissas tácitas do que um único prompt pedindo "analise esta ideia".
- **Fixtures:** 5 ideias em estado bruto (software, hardware, modelo de negócio, pesquisa científica, produto social).
- **Métricas:** Contagem de claims falsificáveis únicas, número de premissas ocultas expostas, custo total de tokens.

### [EXP-002] Multiagente Adversarial vs Agente Único (Validação de Coordination Value)
- **Fase de Execução:** Fase 4 / Fase 5 (Controlled Experiments)
- **Hipótese:** A deliberação multiagente sob topologia `CRITIQUE_LOOP` detecta falhas materiais que passam despercebidas por um único agente atuando como autocrítico, justificando o custo de coordenação em claims de alta incerteza.
- **Tratamentos:**
  - Grupo 1: Single Model atuando como proponente e crítico.
  - Grupo 2: Multi-Model com funções especializadas sob `DeliberationContract`.
- **Métricas:** Quantidade de falhas críticas reais identificadas, taxa de falsos positivos, custo por falha detectada.

### [EXP-003] Validação da Política de Parada (READY_TO_TEST vs Deliberação Adicional)
- **Fase de Execução:** Fase 5 (Controlled Experiments)
- **Hipótese:** Forçar rodadas adicionais de deliberação após o disparo de `READY_TO_TEST` produz estagnação epistêmica (zero alteração em claims centrais) com aumento inútil de custo financeiro.
- **Métricas:** Delta em claims após ponto de saturação, custo de tokens excedente.
