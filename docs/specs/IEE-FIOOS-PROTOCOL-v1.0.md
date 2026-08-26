# IEE/FioOS Protocol Specification & Architectural Boundary (v1.0)

> **ESPECIFICAÇÃO CANÔNICA DE FRONTEIRA E CONTRATOS ENTRE IDEA EVOLUTION ENGINE E FioOS**  
> **Status:** `CANONICAL_SPECIFICATION_LOCKED`  
> **Modo de Implementação:** `CONTRACT_SPECIFICATION_ONLY` (Sem runtime bridge, sem mutação no FioOS)  
> **Princípio Central:** *"Architecture may prepare for FioOS. Evidence must earn the integration."*

---

## 1. Regra Constitucional Suprema de Fronteira

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        CONSTITUIÇÃO DE FRONTEIRA                       │
├────────────────────────────────────────────────────────────────────────┤
│  1. HUMAN OWNS INTENT.                                                 │
│  2. IEE OWNS EPISTEMIC STATE AND INVESTIGATION RECOMMENDATION.         │
│  3. FioOS OWNS OPERATIONAL GOVERNANCE AND EXECUTION.                   │
│  4. NO LAYER MAY SILENTLY INHERIT THE AUTHORITY OF ANOTHER.            │
└────────────────────────────────────────────────────────────────────────┘
```

Nenhuma camada pode agir em nome da outra sem passagem formal de contrato tipado e validação de autoridade correspondente.

---

## 2. Divisão Estrita de Responsabilidades e Soberania

### 2.1 Soberania Humana (Human Authority)
O ser humano detém com exclusividade:
- **Intenção Original (`original_intent`)**: O propósito fundacional da ideia.
- **Valores e Critérios Normativos (`values`)**: Julgamentos éticos, estéticos e de valor.
- **Núcleos Protegidos (`protected_cores`)**: Invariantes conceituais invioláveis por agentes.
- **Decisões Normativas e Pivots Fundamentais**: Mudanças de rumo que alteram a essência.
- **Autoridade Final de Aceitação**: Nenhuma mutação que altere o `CORE` pode ocorrer sem autorização humana expressa.

> **Regra:** O IEE **não** é dono da intenção humana; o IEE apenas *representa, preserva, estrutura e investiga* a intenção formulada pelo ser humano.

### 2.2 Responsabilidades do Idea Evolution Engine (IEE)
O IEE governa com exclusividade a **esfera epistemológica**:
- Representação estruturada da ideia (`IdeaGenome`).
- Estado epistêmico (`EpistemicState`: claims, suposições, tensões, contradições, incertezas).
- Cálculo de Relevância Decisória (`DecisionRelevance`) e `DecisionDelta`.
- Planejamento de investigação e formulação de requisitos cognitivos.
- Lógica de terminação epistêmica (`MORE_INVESTIGATION_REQUIRED`, `STALLED`, `HUMAN_DECISION_REQUIRED`, `READY_TO_TEST`).

### 2.3 Responsabilidades do FioOS
O FioOS governa com exclusividade a **esfera operacional e de execução**:
- Planejamento e agendamento operacional de missões (`FioOSMissionPlan`).
- Concessão de autoridade operacional, leases e sandboxing.
- Seleção concreta de provedores, modelos, ferramentas e credenciais.
- Vínculo temporal de identidade de execução (`ExecutionIdentityBinding`).
- Imposição de orçamento financeiro (`OperationalBudgetAuthority`), controle de custos e limites de taxa.
- Isolamento de execução (*territory*), auditoria, proveniência e produção de envelopes de evidência (`EvidenceEnvelope`).

---

## 3. Estados Epistêmicos e a Invariante READY_TO_TEST

O IEE pode classificar uma ideia ou hipótese nos seguintes estados epistêmicos determinísticos:
- `MORE_INVESTIGATION_REQUIRED`: O raciocínio deliberativo abstrato ainda possui retornos marginais positivos.
- `STALLED`: O motor detectou circularidade sem redução de incerteza e requer nova hipótese ou encerramento.
- `HUMAN_DECISION_REQUIRED`: Incerteza normativa ou tensão de valores que exige julgamento humano soberano.
- `READY_TO_TEST`: A deliberação abstrata esgotou sua utilidade; o próximo salto de conhecimento exige evidência empírica.

### Invariante Fundamental:
> **`READY_TO_TEST != EXECUTION_AUTHORITY`**

Declarar `READY_TO_TEST` significa estritamente:  
*"O progresso epistêmico adicional requer evidência do mundo real."*

O IEE emite uma requisição (`REALITY_TEST_REQUESTED`), e a autoridade operacional do FioOS decide e responde com um status governado:
- `AUTHORIZED`: Missão agendada e lease de execução concedido no sandbox.
- `BLOCKED`: Violação de invariante de segurança ou política operacional.
- `DEFERRED`: Repriorizado para execução posterior.
- `BUDGET_DENIED`: Excede o orçamento operacional autorizado.
- `AUTHORITY_REQUIRED`: Exige autorização humana expressa antes do disparo.
- `UNAVAILABLE`: Recursos, ferramentas ou conectividade indisponíveis.

---

## 4. IEE/FioOS Protocol V1 — Contratos Formais

O protocolo de comunicação entre IEE e FioOS opera através de 4 contratos conceituais desacoplados e uma etapa temporal de vinculação de execução:

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                           IEE / FioOS PROTOCOL V1                        │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  [IEE: Epistemic Layer]                                                  │
│           │                                                              │
│           ▼ (1) Emite Intenção Epistêmica                                │
│   InvestigationIntent (Requisitos Cognitivos, Stop Condition, Sem Segredos)│
│           │                                                              │
│  ═════════╪════════════════════════════════════════════════════════════  │
│  [FioOS: Governance & Planning Layer]                                    │
│           │                                                              │
│           ▼ (2) Planeja Operação                                         │
│   FioOSMissionPlan (Modelo Concreto, Ferramentas, Budget Operacional)     │
│           │                                                              │
│           ▼ (3) Autorização & Vinculação Temporal (Separada)             │
│   ExecutionIdentityBinding (Lease, Workload Token, Sandbox Target)       │
│           │                                                              │
│           ▼ (4) Execução no Runtime Gateway                              │
│   Execution / Tool Dispatch                                              │
│           │                                                              │
│           ▼ (5) Retorno de Observações e Proveniência                    │
│   EvidenceEnvelope (Dados Brutos, Hashes, Custos, Intervenções)          │
│           │                                                              │
│  ═════════╪════════════════════════════════════════════════════════════  │
│  [IEE: Epistemic Interpretation Layer]                                   │
│           │                                                              │
│           ▼ (6) Avaliação Semântica e Proposta Atômica                   │
│   EpistemicUpdate (ProposedGenomePatch, Claims Atualizadas, Delta)       │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

### 4.1 Contrato 1: `InvestigationIntent` (IEE $\to$ FioOS)
Representa a solicitação pura de investigação epistêmica gerada pelo IEE.

```json
{
  "idea_id": "string",
  "genome_version": "string",
  "uncertainty_id": "string",
  "target_claims": ["string"],
  "question": "string",
  "epistemic_operation": "CRITIQUE | DISCRIMINATE | EVIDENCE_GATHERING | REALITY_TEST",
  "decision_relevance": "string",
  "evidence_required": "string",
  "preferred_topology": "SINGLE_AGENT | SEQUENTIAL_PIPELINE | CRITIQUE_REVISION",
  "cognitive_requirements": [
    "ADVERSARIAL_REASONING_HIGH | SEMANTIC_SYNTHESIS_MEDIUM | RESEARCH_FAST | MECHANICAL_NO_MODEL"
  ],
  "protected_cores": ["string"],
  "epistemic_budget_hint": {
    "max_rounds": 3,
    "cost_sensitivity": "ZERO_INCREMENTAL_PREFERRED | LOW_COST | UNCONSTRAINED"
  },
  "stop_condition": "string",
  "provenance": {
    "created_by": "IEE_COORDINATOR",
    "created_at": "ISO-8601"
  }
}
```

> **Invariantes do `InvestigationIntent`:**
> 1. É terminantemente **PROIBIDO** conter credenciais, chaves de API ou segredos.
> 2. É terminantemente **PROIBIDO** conter objetos de `ToolRequest`, comandos de terminal/shell ou código de execução direta.
> 3. É terminantemente **PROIBIDO** conter declarações de autoridade operacional concedida.
> 4. É terminantemente **PROIBIDO** exigir modelos concretos por nome comercial (ex: "GPT-4o", "Gemini Pro"); expressa apenas **Requisitos Cognitivos** (`cognitive_requirements`).

---

### 4.2 Contrato 2: `FioOSMissionPlan` (Produzido pelo FioOS)
Plano formal de resolução operacional elaborado pelo planejador do FioOS.

```json
{
  "investigation_intent_hash": "SHA-256",
  "mission_id": "string",
  "source_identity": "string",
  "lane": "INTERACTIVE | BATCH | SECURE_ENCLAVE",
  "concrete_model": "string",
  "provider": "string",
  "reasoning_effort": "LOW | MEDIUM | HIGH",
  "context_allocation_bytes": 65536,
  "tools": ["string"],
  "requested_authority": "READ_ONLY | NETWORK_ACCESS | WORKSPACE_WRITE",
  "budget": {
    "max_cost_usd": 0.0,
    "max_tokens": 100000
  },
  "territory": "SANDBOX_EPHEMERAL",
  "test_budget": "1_EXECUTION",
  "stop_condition": "string"
}
```

> **Invariante do `FioOSMissionPlan`:**
> `MISSION_PLAN != AUTHORIZATION`. Ter um plano de missão não confere permissão de execução. A autorização é um gate posterior e independente.

---

### 4.3 Contrato 3: `ExecutionIdentityBinding` (Vinculação Temporal Separada)
Emitido exclusivamente no momento em que o agendador e o motor de autorização do FioOS concedem o *lease* de execução.

```json
{
  "binding_id": "string",
  "mission_id": "string",
  "authorized_identity": "string",
  "workload_token": "TOKEN_REDACTED",
  "granted_authority": "READ_ONLY",
  "lease_expires_at": "ISO-8601",
  "sandbox_container_id": "string"
}
```

> **Invariante Temporal:** `ExecutionIdentityBinding` não existe durante o planejamento. É gerado downstream da autorização formal.

---

### 4.4 Contrato 4: `EvidenceEnvelope` (FioOS $\to$ IEE)
Transporta observações brutas, telemetria de execução e metadados de proveniência de volta ao IEE.

```json
{
  "evidence_id": "string",
  "mission_id": "string",
  "investigation_intent_hash": "SHA-256",
  "source_identity": "string",
  "execution_identity": "string",
  "artifact_pointer": "string",
  "artifact_sha256": "SHA-256",
  "observation_type": "EXECUTION_OUTPUT | CRITIQUE_BUNDLE | EMPIRICAL_DATA | FAILURE_LOG",
  "raw_verdict": "PASS | FAIL | INCONCLUSIVE",
  "occurred_at": "ISO-8601",
  "operational_cost": {
    "total_tokens": 1250,
    "cost_usd": 0.0,
    "latency_seconds": 1.2
  },
  "intervention_record": [],
  "provenance": {
    "runner": "FioOS_RUNTIME_GATEWAY",
    "signature": "VALIDATED"
  },
  "source_metadata": {}
}
```

> **Invariantes do `EvidenceEnvelope`:**
> 1. *"EvidenceEnvelope carries observations and provenance, not accepted truth."*
> 2. `ToolResult != Truth` | `EvidenceEnvelope != Truth` | `Memory != Evidence`.
> 3. O `EvidenceEnvelope` é imutável e **não pode** aplicar mutações diretas no `IdeaGenome`.

---

### 4.5 Contrato 5: `EpistemicUpdate` (Processamento Interno do IEE)
Consolidação semântica após interpretação epistemológica do conjunto de evidências.

```json
{
  "proposed_genome_patch": {
    "patch_id": "string",
    "target_version": "string",
    "operations": []
  },
  "claims_changed": [
    {
      "claim_id": "string",
      "previous_status": "UNTESTED",
      "new_status": "SUPPORTED | REFUTED | UNCERTAIN | CONTRADICTED"
    }
  ],
  "evidence_links": ["string"],
  "contradictions": [],
  "uncertainties_resolved": ["string"],
  "uncertainties_created": ["string"],
  "decision_delta": "CONFIRMED_EXISTING_DECISION | FOUND_COUNTEREXAMPLE | CREATED_NEW_BLOCKER",
  "next_recommendation": "MORE_INVESTIGATION_REQUIRED | READY_TO_TEST | STALLED",
  "termination_state": "ACTIVE | TERMINATED"
}
```

> **Invariante:** `PROPOSED_GENOME_PATCH != APPLIED_GENOME_PATCH`. A proposta de patch só é aplicada se passar integralmente pelo `GenomeValidator` determinístico.

---

## 5. Ontologia em Três Camadas e Regras de Transição de Estado

Toda proposição no IEE pertence estritamente a uma das 5 categorias ontológicas:

```text
┌─────────────────────────────────────────────────────────────┐
│                      ONTOLOGIA DO IEE                       │
├─────────────────────────────────────────────────────────────┤
│  1. CORE:       Invariantes essenciais da ideia humana      │
│  2. DERIVED:    Implicações e refinamentos lógicos diretos  │
│  3. CANDIDATE:  Possibilidades/extensões propostas por IA   │
│  4. DEFERRED:   Hipóteses adiadas por falta de condições    │
│  5. REJECTED:   Propostas avaliadas e descartadas           │
└─────────────────────────────────────────────────────────────┘
```

### Regras Estritas de Transição:
1. `CANDIDATE → DERIVED`: Exige justificativa formal de resolução de problema sem aumento desnecessário de complexidade.
2. `CANDIDATE → CORE`: Exige **autorização humana soberana expressa** se alterar ou expandir a essência da ideia.
3. `CORE Mutation`: Exige **autoridade humana soberana** sempre que a alteração for normativa ou essencial.
4. `REJECTED → ACTIVE`: Exige nova evidência empírica substantiva OU justificativa explícita de reabertura (`reopen_reason`).
5. `DEFERRED → ACTIVE`: Exige mudança comprovada nas condições externas OU justificativa explícita de reabertura.

---

## 6. Modos Operacionais do IEE

### 6.1 Modo Autônomo Standalone (`IEE_MODE = STANDALONE`)
- O IEE opera de forma independente do FioOS.
- Utiliza provedores locais, adaptadores diretos ou modelos do `ModelCatalog` sob a política `FREE_ONLY` / `ZERO_INCREMENTAL_SPEND`.
- Executa apenas transformações cognitivas puras e seguras sem ferramentas externas de alto efeito.

### 6.2 Modo Governado por FioOS (`IEE_MODE = FIOOS_GOVERNED`)
- O IEE renuncia a qualquer pretensão de autoridade operacional e de execução direta.
- O IEE despacha `InvestigationIntent` para o gateway do FioOS.
- O FioOS assume todo o agendamento, governança financeira, sandboxing, concessão de credenciais e produção de evidências.

---

## 7. Nomenclatura e Vocabulário de Governança

- **Coordenação Epistêmica:** O componente orquestrador do IEE é denominado formalmente **`InvestigationCoordinator`**, evitando confusão com o `RuntimeGateway` ou `ExecutionOrchestrator` do FioOS.
- **Autoridade sobre o Genoma:** A autoridade de aceitar ou rejeitar alterações no `IdeaGenome` é denominada **`EPISTEMIC_MUTATION_AUTHORITY`** (ou `GENOME_MUTATION_AUTHORITY`), diferenciando-se da `OPERATIONAL_EXECUTION_AUTHORITY` do FioOS.
- **Diferenciação de Orçamentos:** `EPISTEMIC_BUDGET_HINT != OPERATIONAL_BUDGET_AUTHORITY`. O IEE apenas sinaliza sua sensibilidade a custos; o FioOS impõe limites financeiros executáveis.

---

## 8. Status de Implementação e Fronteira Segura

```text
================================================================================
                    IEE / FioOS BOUNDARY STATUS
================================================================================
  IEE_FIOOS_BOUNDARY:                 CANONICAL_AND_LOCKED
  IEE_FIOOS_PROTOCOL_V1:              SPECIFIED
  INVESTIGATION_INTENT:               SPECIFIED (Zero Credentials / Pure Intent)
  FIOOS_MISSION_PLAN:                 SPECIFIED (Planning != Authority)
  EXECUTION_IDENTITY_BINDING:         SPECIFIED (Temporal Separation Enforced)
  EVIDENCE_ENVELOPE:                  SPECIFIED (Observations != Truth)
  EPISTEMIC_UPDATE:                   SPECIFIED (Proposal != Mutation)
  CORE_TRANSITION_RULES:              SPECIFIED (3 Layers + 2 Parking States)
  STANDALONE_MODE:                    PRESERVED
  FIOOS_GOVERNED_MODE:                DEFINED
  REAL_FIOOS_BRIDGE:                  NOT_IMPLEMENTED
  FIOOS_RUNTIME_TOUCHED:              NO
================================================================================
```
