# STATE-MACHINE.md — Máquina de Estados e Ciclo de Vida do Genoma

> **STATUS: TARGET / DESIGN_HYPOTHESIS**

---

## 1. Grafo de Estados Epistêmicos

```text
               ┌──────────────┐
               │   RAW_IDEA   │
               └──────┬───────┘
                      │ Início do Processamento
                      ▼
           ┌──────────────────────┐
           │ STRUCTURE_BOOTSTRAP  │◄────────────────────┐
           └──────────┬───────────┘                     │
                      │ BootstrapExitPolicy satisfeita  │
                      ▼                                 │
         ┌─────────────────────────┐                    │
   ┌────►│ DECISIONAL_INVESTIGATION│                    │
   │     └────────────┬────────────┘                    │
   │                  │                                 │
   │   ┌──────────────┼──────────────┬──────────────┐   │
   │   │              │              │              │   │
   │   ▼              ▼              ▼              ▼   │
   │ [READY_      [HUMAN_        [PIVOT_        [STALLED│
   │ TO_TEST]    DECISION_      CANDIDATE]         /    │
   │   │         REQUIRED]           │          REPLAN] │
   │   │              │              │              │   │
   │   │ Teste        │ Decisão      │ Branch       │   │
   │   │ executado    │ humana       │ criada       │   │
   │   └──────────────┼──────────────┴──────────────┘   │
   │                  │                                 │
   │                  ▼                                 │
   │         [Branch / Pivot / Reabertura]──────────────┘
   │                  │
   │                  ▼
   │          ┌───────────────┐
   └──────────┤   ARCHIVED    │
              │  / NOT_VIABLE │
              └───────────────┘
```

---

## 2. Descrição dos Estados

| Estado | Descrição |
| :--- | :--- |
| **RAW_IDEA** | Entrada da ideia humana bruta sem estruturação formal. |
| **STRUCTURE_BOOTSTRAP** | Regime de estruturação focado em `StructureGain` (claims, premissas, atores). |
| **DECISIONAL_INVESTIGATION** | Investigação governada pelo DCE focada em incertezas decisivas. |
| **READY_TO_TEST** | Transição onde a deliberação cessa e formula-se o `TestContract` empírico. |
| **HUMAN_DECISION_REQUIRED** | Pausa de deliberação para consulta soberana sobre valores, propósito ou trade-offs. |
| **PIVOT_CANDIDATE** | Proposta de mudança fundamental de rumo que requer criação de branch de linhagem. |
| **STALLED** | Detecção de estagnação ou saturação que exige replanejamento de estratégia. |
| **REPLAN_REQUIRED** | Necessidade de reorganização das prioridades de investigação pelo DCE. |
| **RESOURCE_LIMIT_REACHED** | Esgotamento do orçamento computacional/financeiro alocado à ideia. |
| **NOT_CURRENTLY_VIABLE** | Registro fundamentado de inviabilidade técnica, lógica ou de mercado. |
| **ARCHIVED** | Congelamento da ideia por decisão humana soberana. |

---

## 3. Regras de Transição Determinísticas
- Nenhuma transição ocorre por mera "declaração de texto" de uma IA.
- Toda transição requer uma política formal satisfeita (`BootstrapExitPolicy`, `ReadyToTestPolicy`, `StallPolicy`, etc.).
- Transições para `ARCHIVED`, `PIVOT` e alterações de *Protected Core* exigem `HUMAN_AUTHORITY`.
