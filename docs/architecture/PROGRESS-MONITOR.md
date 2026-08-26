# PROGRESS-MONITOR.md — Monitor de Progresso Epistêmico

> **STATUS: TARGET / DESIGN_HYPOTHESIS**

---

## 1. Papel do Progress Monitor
O **Progress Monitor** é o componente responsável por calcular e auditar o avanço real gerado por uma rodada de deliberação. Ele atua como um filtro determinístico para assegurar a vigência inegociável do princípio *Progress Over Prose*.

---

## 2. Três Artefatos Fundamentais de Medição

```text
               ┌──────────────────────────────┐
               │      UncertaintyRecord       │
               │   (Identifica a incerteza)   │
               └──────────────┬───────────────┘
                              │
                              ▼
               ┌──────────────────────────────┐
               │   DecisionRelevanceReport    │
               │    (Olha para FRENTE):       │
               │  Contrafactuais e Impactos   │
               └──────────────┬───────────────┘
                              │
                     [Execução do Teste]
                              │
                              ▼
               ┌──────────────────────────────┐
               │        DecisionDelta         │
               │     (Olha para TRÁS):        │
               │   O que de fato se alterou   │
               └──────────────────────────────┘
```

### 2.1 UncertaintyRecord (Registro de Incerteza)
Documenta a dúvida investigada, status (`OPEN`, `UNDER_INVESTIGATION`, `RESOLVED`, `DEFERRED`), claims vinculadas e tipo epistêmico.

### 2.2 DecisionRelevanceReport (Olhar Prospectivo)
Mapeia o impacto potencial através de raciocínio contrafactual explícito:
- `if_supported`: Qual ação, claim ou decisão é modificada?
- `if_refuted`: Qual ação, claim ou decisão é modificada?
- `if_uncertain`: Qual o custo de permanecer na ignorância?
- Se nenhuma ação, claim estrutural ou decisão for afetada, a incerteza é classificada como `NOT_DECISIVE`.

### 2.3 DecisionDelta (Olhar Retrospectivo)
Registra o impacto real pós-deliberação:
- Mudança efetiva de ações recomendadas.
- Transições de status de claims (`UNTESTED` $\to$ `SUPPORTED` / `REFUTED`).
- Resolução ou criação de tensões.
- Comparação entre o impacto previsto pelo `DecisionRelevanceReport` e o impacto realizado, calibrando a precisão do sistema ao longo do tempo.
