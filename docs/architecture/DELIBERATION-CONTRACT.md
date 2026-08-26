# DELIBERATION-CONTRACT.md — O Contrato de Deliberação

> **STATUS: TARGET / DESIGN_HYPOTHESIS**

---

## 1. O Princípio do Contrato Pré-Execução
> **Conversa sem contrato não é unidade válida de investigação.**

Para impedir que a deliberação degenere em chat prolixo, *moving goalposts* ou consenso artificial, toda rodada investigativa deve operar sob um **`DeliberationContract`** formalmente emitido antes do início da execução.

---

## 2. Estrutura Canônica do DeliberationContract

```text
DeliberationContract
├── contract_id: UUID
├── round_id: Identificador da rodada
├── investigation_target: Descrição do objetivo epistemológico
├── target_claims: Lista de IDs de claims investigadas
├── question_type: EMPIRICAL | NORMATIVE | MIXED | STRUCTURAL
├── epistemic_operation: Operação a realizar (ex: falsificação, busca de evidência, crítica de mecanismo)
├── coordination_mode: SINGLE_AGENT_MODE | STRUCTURED_MULTI_AGENT_MODE
├── team:
│   └── Lista de papéis e funções epistemológicas convocadas
├── topology: SEQUENTIAL | PARALLEL | CRITIQUE_LOOP | TREE | SYNTHESIS_LOOP
├── allowed_epistemic_acts: Lista de atos autorizados (ex: FRAME, PROPOSE, CHALLENGE, GROUND)
├── required_epistemic_acts: Atos obrigatórios durante a rodada
├── required_artifacts: Artefatos esperados (ex: UncertaintyRecord, TensionRecord, GenomePatch)
├── progress_criteria: Lista explícita do que configurará progresso válido
├── non_progress_criteria: O que será explicitamente ignorado (ex: reformulações, concordâncias sem base)
├── candidate_admission_policy: Critérios para aceitar novos elementos no genoma
├── tension_handling_policy: Regra para lidar com divergências (ex: registrar TensionRecord sem forçar síntese)
├── stop_condition: Critério de término normal da rodada
├── failure_condition: Critério que caracteriza falha da rodada
├── interpretation_of_failure: Significado epistemológico caso a rodada falhe
├── budget: Limite estrito de tokens, tempo e chamadas de modelo
├── safety_bounds: Limites operacionais e restrições de segurança
└── reopen_policy: Condições para reabrir este contrato no futuro
```

---

## 3. Avaliação Relativa ao Contrato (Contract-Relative Progress)
O `ProgressMonitor` avalia o resultado da rodada estritamente contra os `progress_criteria` fixados no contrato antes da execução. Não é permitido inspecionar o texto final e inventar *a posteriori* motivos pelos quais a rodada teria sido útil.
