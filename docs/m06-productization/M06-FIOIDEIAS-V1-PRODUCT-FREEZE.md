# M06-FIOIDEIAS-V1-PRODUCT-FREEZE.md — Congelamento da Transição Ciência → Produto

> **PROGRAMA:** M06 — Productization do Idea Evolution Engine  
> **SISTEMA:** FioIdeias V1 (FioIdeias V1 — Lean L1 Default)  
> **DATA DE CONGELAMENTO:** 2026-09-03  
> **STATUS:** `FROZEN_FOR_PRODUCTIZATION`  
> **BASE CIENTÍFICA:** M05.5 Concluído (Commit [`adc3e8a`](https://github.com/phpedrogarcia-afk/idea-evolution-engine/commit/adc3e8a))

---

## 0. Linha de Base Científica

O programa experimental M05.5 encerrou formalmente suas atividades:
- **`M05.5_STATUS = COMPLETE`**
- **Commit Final Científico:** [`adc3e8a`](https://github.com/phpedrogarcia-afk/idea-evolution-engine/commit/adc3e8a)
- **Tentativa Confirmatória Válida:** `M05.5R2-REAL-EXECUTION-ATTEMPT-002` (Cerebras Cloud, `openai/gpt-oss-120b`)
- **Desfecho Primário:** **`PRIMARY_REPLICATION_RESULT = PASS`** (Condição C: 22 pts > Condição A: 18 pts > Condição B: 8 pts)
- **Status do Lean L1:** **`REPLICATED_PRIMARY_WITH_PARTIAL_PATTERN_SUPPORT`**
- **Convergências:**
  - Continuidade (CONTINUE): C = 6/8 ($75\%$) vs A = 2/8 vs B = 0/8 (`PASS`)
  - Dimensional Secundário: C = 362 / 400 ($90,5\%$, média 4.525) vs A = 282 vs B = 143 (`PASS`)
  - Eficiência de Chamadas: C utilizou 11 chamadas lógicas contra 80 de B ($13,75\% \le 25\%$, `PASS`)
- **Lista de Padrões de Replicação (RPL):** 6/7 itens aprovados (`FULL_PATTERN = FAIL` devido à não retenção de crítica/novidade isolada por B)
- **Salvaguarda Causal:** **`CAUSAL_MECHANISM_STATUS = UNRESOLVED`** (o ganho pertence ao pacote de tratamento da Condição C; ablações de componentes individuais pertencem a pesquisas futuras).

---

## 1. Decisão Estratégica de Produto

Com base na superioridade empírica replicada e na disciplina de custos:

```yaml
FIOIDEIAS_V1_DEFAULT_TREATMENT: CONDITION_C_LEAN_L1
FIOIDEIAS_V1_DEFAULT_PATH: LEAN_L1_PLUS_EARLY_EPISTEMIC_GATE
CONDITION_A_PRODUCT_ROLE: FAST_MINIMAL_REFINEMENT_FALLBACK
CONDITION_B_PRODUCT_ROLE: SUSPENDED_FROM_DEFAULT_PATH
```

1. **Adoção do Lean L1 como Padrão:**  
   O motor de inferência padrão do FioIdeias V1 é a **Condição C (Lean Loop L1 + Early Epistemic Gate)**.
2. **Papel da Condição A:**  
   A Condição A (Single Refine) assume exclusivamente o papel de **Fallback de Contingência Rápido / Sanity Baseline** para cenários de altíssima restrição de latência ou depuração operacional.
3. **Suspensão da Condição B:**  
   A Condição B (Simple Loop com 10 estágios) está **suspensa do caminho de produto V1**. Sob modelos abertos (`gpt-oss-120b`), ela demonstrou alta taxa de spoofing de autoridade e contaminação ontológica por vazamento de alarmes determinísticos. Não fará parte de qualquer fluxo automático de produção.

---

## 2. Correção Terminológica Canônica

Para evitar confusão ontológica no repositório:
- **NÃO** chamar o produto V1 de "Simple Idea Evolution Loop", pois *Simple Loop* é o identificador histórico da **Condição B**, que foi expressamente preterida.
- **Nomenclatura Canônica Oficial:**  
  $$\mathbf{\text{FioIdeias V1 — Lean L1 Default}}$$  
  Identificador de configuração interno: `LEAN_DEFAULT` ou `CONDITION_C_LEAN_L1`.

---

## 3. Fronteira Ciência vs. Produto

Estabelece-se uma barreira explícita entre o **Núcleo Científico** e a **Casca de Produto**:

$$\mathbf{\text{EXPERIMENTAL\_RESULT } \ne \text{ PRODUCT\_POLICY}}$$

```
┌──────────────────────────────────────────────────────────────┐
│                    PRODUCT SHELL (M06)                       │
│  - Ergonomia de CLI (iee evolve ...)                         │
│  - Formatação e renderização humana limpa (sem ruído debug)  │
│  - Persistência e catálogo de artefatos (EvolutionArtifact)   │
│  - Observabilidade e auditoria estruturada                   │
│  - Gestão tipada de erros e cotas ($0 out-of-pocket)         │
│  - Service Boundary (IdeaEvolutionService)                   │
├──────────────────────────────────────────────────────────────┤
│               SCIENTIFIC TREATMENT CORE (M05)                │
│  - Lean First Pass (Chamada 1)                               │
│  - Early Epistemic Gate (Custo 0, Determinístico)            │
│  - Focused Escalation (Chamada 2, Condicional)               │
│  - Teto inviolável de chamadas: MAX CALLS = 2               │
│  - Schemas Pydantic validados                                │
│  - Proibição de spoofing de autoridade e promoções indevidas │
└──────────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> A casca de produto pode melhorar usabilidade, renderização, persistência e interfaces, mas **jamais** alterará silenciosamente a semântica do núcleo científico validado.

---

## 4. Política de Provedores e Custo Zero

1. **Desacoplamento do Provedor:**  
   O ambiente Cerebras Cloud (`openai/gpt-oss-120b`) foi suficiente para a comprovação científica em M05.5R2. Ele **não** é uma dependência arquitetural permanente. A arquitetura de produto V1 deve isolar a camada de transporte via `ProviderAdapter`.
2. **Custo de Bolso Zero (`OUT_OF_POCKET_COST = ZERO`):**  
   O sistema opera sob princípio *fail-closed* contra inferência paga acidental. Se as cotas gratuitas se esgotarem, o sistema transiciona para o estado tipado explícito `PROVIDER_QUOTA_EXHAUSTED`, sem chaveamento para rotas pagas.

---

## 5. Fronteira com o FioOS

Preserva-se a separação estrita de domínios:
- **FioIdeias:** Serviço cognitivo de maturação, crítica, contextualização e redução de incerteza de ideias.
- **FioOS:** Sistema operacional governado de autoridade, execução de ferramentas, leases e budgets.
- **Modo Futuro de Integração:** `FIOIDEIAS_MODE = ADVISORY_SHADOW`, com `FIOIDEIAS_AUTHORITY = NONE`.
- **Invariante Fundamental:** `IDEA != REQUIREMENT`, `IDEA != TRUTH`, `IDEA != AUTHORITY`.
