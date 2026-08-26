# TARGET-ARCHITECTURE.md — Panorama da Arquitetura Alvo do IEE

> **STATUS: TARGET / DESIGN_HYPOTHESIS**
> Este documento apresenta a visão arquitetural completa de longo prazo. Nenhum destes componentes deve ser considerado implementado em código na Fase 0.

---

## 1. Visão Geral em Camadas

```text
┌─────────────────────────────────────────────────────────────┐
│                     CAMADA DE SOBERANIA                     │
│    Humano Criador • Protected Cores • Julgamento Normativo  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│             DELIBERATION CONTROL ENGINE (DCE)               │
│  Epistemic Assessor ──► Gap Detector ──► Selector           │
│  Team Composer ───────► Topology Planner ──► Contract Build │
│  Execution Orch ──────► Progress Monitor ──► Termination    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    NÚCLEO CONSTITUCIONAL                    │
│   GenomePatch Builder ──► GenomeValidator (Determinístico)  │
│   State Machine       ──► Authority Matrix & Invariants     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    MEMÓRIA EPISTÊMICA                       │
│     IdeaGenome (Grafo Versionado Imutável: v1 → v2 → vN)    │
│  Claims • Evidence • Assumptions • Tensions • Lineage       │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Componentes Fundamentais

### 2.1 IdeaGenome (Memória Durável)
Substitui históricos efêmeros de chat por um grafo de conhecimento imutável e versionado.
👉 Detalhes: [`docs/architecture/IDEA-GENOME.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/architecture/IDEA-GENOME.md)

### 2.2 Deliberation Control Engine (DCE)
O "sistema nervoso" do IEE. Responsável por decidir *o que investigar, quando investigar, se é necessário mais de um agente, como coordenar a deliberação e quando parar*.
👉 Detalhes: [`docs/architecture/DCE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/architecture/DCE.md)

### 2.3 Regimes Cognitivos: Bootstrap e Investigação Decisional
- **Bootstrap:** Estruturação inicial da ideia para atingir legibilidade formal (`StructureGain`).
  👉 Detalhes: [`docs/architecture/BOOTSTRAP.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/architecture/BOOTSTRAP.md)
- **Investigação Decisional:** Redução de incertezas decisivas orientada a impacto em ações e claims.

### 2.4 DeliberationContract e ProgressMonitor
Governa a execução de cada rodada de investigação com orçamento, participantes, topologia e critérios estritos de progresso.
👉 Detalhes: [`docs/architecture/DELIBERATION-CONTRACT.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/architecture/DELIBERATION-CONTRACT.md) e [`docs/architecture/PROGRESS-MONITOR.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/architecture/PROGRESS-MONITOR.md)

### 2.5 GenomePatch e GenomeValidator
Garante que nenhuma IA altere o estado diretamente. As propostas de mutação passam por 5 camadas de validação determinística (*all-or-nothing*).
👉 Detalhes: [`docs/architecture/GENOME-PATCH.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/architecture/GENOME-PATCH.md)

### 2.6 READY_TO_TEST e TestContract
Mecanismo que encerra a deliberação quando o maior valor epistêmico deve vir de um teste empírico no mundo real.
👉 Detalhes: [`docs/architecture/READY-TO-TEST.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/architecture/READY-TO-TEST.md)

### 2.7 Máquina de Estados Epistêmica
Ciclo de vida formal da ideia, com transições auditáveis e protegidas contra bypass.
👉 Detalhes: [`docs/architecture/STATE-MACHINE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/architecture/STATE-MACHINE.md)
