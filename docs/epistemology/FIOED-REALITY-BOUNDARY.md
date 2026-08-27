# FIOED-REALITY-BOUNDARY.md — Fronteira da Realidade, Proveniência e Admissão de Evidência

> **DOCUMENTO DOUTRINÁRIO E DE ESPECIFICAÇÃO DE DOMÍNIO**
> **STATUS:** `EXPERIMENTAL_ARCHITECTURAL_CONTRACT` | `FORMALIZED_OFFLINE`
> **OBJETIVO:** Estabelecer uma separação inquebrável entre raciocínio generativo interno e contato empírico com o mundo real, garantindo que modelos de IA jamais fabriquem ou autoatestem evidência externa.

---

## 1. As Três Fronteiras Independentes da Realidade

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                          REALITY BOUNDARY MODEL                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [1] CAPABILITY BOUNDARY                                                    │
│      O modelo gera hipóteses, perguntas e requisições;                      │
│      O modelo NÃO POSSUI a capacidade de emitir EvidenceArtifacts reais.   │
│                                                                             │
│  [2] PROVENANCE BOUNDARY                                                    │
│      ArtifactClass = f(Canal de Aquisição Físico/Lógico)                    │
│      NÃO = f(Alegações do Modelo em JSON/Texto)                             │
│                                                                             │
│  [3] TRANSITION BOUNDARY                                                    │
│      Evidência externa admitida passa por avaliação determinística;        │
│      O modelo NÃO POSSUI autoridade unilateral para promover claims.        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. O Estado Rígido `WAITING_FOR_REALITY`

Quando uma hipótese formula uma questão discriminativa ($Q^*$) e emite um `EvidenceRequest`, ela entra obrigatoriamente no estado formal **`WAITING_FOR_REALITY`**:

```text
    ┌──────────────────────┐
    │  READY_TO_TEST (Q*)  │
    └──────────┬───────────┘
               │ Emit EvidenceRequest
               ▼
    ┌──────────────────────┐
    │ WAITING_FOR_REALITY  │ ──▶ [Ramo aguarda em repouso estrito]
    └──────────┬───────────┘
               │
   ┌───────────┴───────────────────────────┐
   │ REGRAS INEGOCIÁVEIS EM WAITING:       │
   │ 1. Nenhuma promoção empírica          │
   │ 2. Proibido inventar observações      │
   │ 3. Proibido auto-completar com LLM    │
   │ 4. Outros ramos seguros continuam     │
   └───────────────────────────────────────┘
```

> **MANDATO CANÔNICO:** *Quando a realidade estiver ausente, espere. Não invente o chão.*

---

## 3. Taxonomia Relativa de Interfaces e Classes de Evidência

A "Realidade" não é um oráculo universal único; a interface adequada é estritamente **relativa à classe da afirmação**:

| Tipo de Afirmação / Claim | Interface da Realidade Exigida | Classe de Evidência Adequada | Canal de Aquisição Legítimo |
| :--- | :--- | :--- | :--- |
| *"O usuário deseja a funcionalidade X"* | `HUMAN_SOURCE` | `HUMAN_OBSERVATION` | `HUMAN_INTERVENTION_CHANNEL` |
| *"O portão Lean L1 executa em no máximo 2 chamadas"* | `RUNTIME_OBSERVATION` | `DETERMINISTIC_RUNTIME_OBSERVATION` | `DETERMINISTIC_RUNNER_CHANNEL` |
| *"Usuários sentem menor fadiga mental com layout A"* | `HUMAN_OBSERVATION` | `HUMAN_OBSERVATION` | `EXTERNAL_INGESTION_CHANNEL` |
| *"A API externa da biblioteca Y suporta streaming"* | `PRIMARY_EXTERNAL_SOURCE` | `PRIMARY_EXTERNAL_SOURCE` | `EXTERNAL_INGESTION_CHANNEL` |
| *"O modelo de simulação Z converge em 100 épocas"* | `SIMULATION_ONLY` | `SIMULATION` | `DETERMINISTIC_RUNNER_CHANNEL` |

---

## 4. Regra Fundamental da Evidência Sintética

1. Personas sintéticas, votos de múltiplos LLMs e simulações generativas **podem**:
   - Propor hipóteses criativas;
   - Identificar possíveis objeções conceituais;
   - Sugerir perguntas de teste ($Q^*$).
2. Personas sintéticas e modelos generativos **NÃO PODEM**:
   - Fechar claims empíricas sobre o comportamento humano real;
   - Substituir observações do mundo exterior;
   - Atuar como evidência independente de suas próprias afirmações.

$$\mathbf{SYNTHETIC\_EVIDENCE \text{ pode ABRIR uma pergunta empírica; JAMAIS pode FECHÁ-LA.}}$$

---

## 5. Passaporte Epistêmico (`EvidencePassport`) e Portão de Admissão

O `EvidencePassport` é um objeto de metadados emitido exclusivamente pelo runtime:

```python
class EvidencePassport:
    passport_id: str
    acquisition_channel: ArtifactAcquisitionChannel  # MODEL, RUNNER, EXTERNAL, HUMAN
    collector_identity: str
    binding_id: str
    experiment_id: str
    nature: ArtifactNature                          # SYNTHETIC vs OBSERVED
    evidence_class: EvidenceClass
    independence_class: IndependenceClass
```

### 5.1 Portão Determinístico de Admissão (`EvidenceAdmissionGate`)
O portão rejeita deterministicamente qualquer tentativa de **`EVIDENCE_SPOOFING`**:
- **`REJECTED_SYNTHETIC_NOT_ADMISSIBLE`:** Se o modelo tentar fechar claim empírica com payload gerado;
- **`REJECTED_BINDING_MISMATCH`:** Se o passaporte pertencer a outro teste;
- **`REJECTED_WRONG_EVIDENCE_CLASS`:** Se a classe de evidência não corresponder à exigida no `TestabilityBinding`;
- **`REJECTED_REPLAY_DETECTED`:** Se um resultado antigo for reaproveitado fora de escopo.

---

## 6. Predeclaração e Imutabilidade de Bindings

1. Antes da coleta de evidências, o `TestabilityBinding` pré-declara o mapeamento:
   - Desfecho $O_1 \implies \text{Transição } T_1$
   - Desfecho $O_2 \implies \text{Transição } T_2$
   - Desfecho $\text{INCONCLUSIVE} \implies \text{Preservar } U_g$
2. Uma vez emitido o `EvidenceRequest` ou anexada a observação, o binding é **congelado** (`is_frozen = True`).
3. É expressamente proibido alterar regras de interpretação após a observação dos dados (*"pintar o alvo ao redor da flecha"*). Qualquer alteração metodológica exige um novo binding e um novo experimento.
