# docs/context/DECISIONS-SUMMARY.md — Sumário Executivo de Decisões de Arquitetura

> **ÍNDICE RÁPIDO DE TODAS AS DECISÕES ARQUITETURAIS (ADRs).**
> Para o registro canônico completo com justificativas e tradeoffs, consulte [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).

---

| ID | Data | Título / Decisão Central | Status | Impacto Principal |
| :--- | :---: | :--- | :---: | :--- |
| [**ADR-001**](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-001) | 2026-08-26 | **Separação Estrita de Fases e Proibição de Código Prematuro** | `ACCEPTED` | Zero código de produto ou frameworks na Fase 0/1. |
| [**ADR-002**](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-002) | 2026-08-26 | **IdeaGenome como Grafo Versionado Imutável em vez de Chat Log** | `ACCEPTED` | Estado epistêmico persistente ($v_N \to v_{N+1}$). |
| [**ADR-003**](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-003) | 2026-08-26 | **Validação Determinística do Kernel e Mutação Exclusiva via GenomePatch** | `ACCEPTED` | Validação em 5 camadas (*all-or-nothing*). |
| [**ADR-004**](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-004) | 2026-08-26 | **Soberania Humana Irrestrita e Governança de Protected Cores** | `ACCEPTED` | Monopólio humano sobre intenção e valores. |
| [**ADR-005**](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-005) | 2026-08-26 | **Deliberação Baseada em Contratos Formais Pré-Execução** | `ACCEPTED` | Critérios de progresso fixados antes da rodada. |
| [**ADR-006**](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-006) | 2026-08-26 | **Multiagente Não-Default e Avaliação de Coordination Value** | `ACCEPTED` | Single Agent Mode como default para baixo overhead. |
| [**ADR-007**](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-007) | 2026-08-26 | **Separação Rígida entre Idea Evolution Engine e FioOS** | `ACCEPTED` | IEE é epistemologia; FioOS é runtime de segurança. |
| [**ADR-008**](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-008) | 2026-08-26 | **Adoção de Doadores Orientada a Gaps Receptores** | `ACCEPTED` | Sem turismo tecnológico; transplante apenas com gap. |
| [**ADR-009**](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-009) | 2026-08-26 | **READY_TO_TEST como Veredito de Próxima Fonte de Conhecimento** | `ACCEPTED` | Transição quando o mundo real supera deliberação. |
| [**ADR-010**](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-010) | 2026-08-26 | **Separação entre Regimes de Bootstrap e Investigação Decisional** | `ACCEPTED` | Bootstrap maximiza StructureGain, não decisões. |
| [**ADR-011**](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-011) | 2026-08-26 | **Sistema de Continuidade Cognitiva, Checkpoints e Validação Determinística** | `ACCEPTED` | Context Manifest e scripts determinísticos de validação. |
