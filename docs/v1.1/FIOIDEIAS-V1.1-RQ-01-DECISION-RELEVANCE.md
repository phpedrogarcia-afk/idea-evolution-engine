# FIOIDEIAS-V1.1-RQ-01: Relevância Decisória e Endurecimento da Qualidade de Resposta

**Data:** 2026-09-05  
**Baseline Release:** v1.0.1 (`a6d92905367b72ec0b5afebfed0e3c70603d9c21`)  
**Development Branch:** `fioideias/v1.1-decision-relevance`  
**Status:** IMPLEMENTADO & VERIFICADO (453/453 TESTES PASSANDO)  
**Governança Financeira:** `PAID_INFERENCE = 0`, `OUT_OF_POCKET_COST = ZERO`  

---

## 1. Falha Observada no v1.0.1 (Regressão Canônica)

Em uma ideia em estágio inicial de descoberta (SaaS para recuperação de orçamentos e cotações esquecidas no WhatsApp), o modelo no v1.0.1 identificou corretamente a intenção do usuário, premissas de mercado e o risco de adoção do vendedor em marcar mensagens manualmente.

Entretanto:
1. Um risco de privacidade/segurança (LGPD / armazenamento de mensagens) foi classificado com severidade `HIGH`.
2. O `EarlyEpistemicGate` continha uma regra cega: qualquer vulnerabilidade com severidade `HIGH` disparava automaticamente escalação focada (`ESCALATE_FOCUSED` com `MATERIAL_VULNERABILITY`).
3. O segundo passo (escalação focada) mutou a hipótese refinada do produto para uma arquitetura técnica de criptografia (`E2EE`, `AES-256`, `TLS 1.3`, `Certificate Pinning`).
4. Fabricou uma asserção numérica não suportada (`latência <200 ms`) sem qualquer base de medição.
5. Substituiu a recomendação de próximo passo (que deveria ser validar a dor e disposição a pagar com clientes reais) por "implementar criptografia de ponta a ponta no backend".

---

## 2. Causas-Raiz Confirmadas no Código

A auditoria forense do código v1.0.1 confirmou quatro causas-raiz estruturais:

- **Causa A (Precedência Incondicional de Severidade):** Em `src/idea_evolution/domain/early_epistemic_gate.py` (linhas 291–311), `severe_vulns = [v for v in first_pass.material_vulnerabilities if v.severity.upper() == "HIGH"]` disparava escalação imediata antes de avaliar o estágio da ideia, alternativas concorrentes ou a relevância imediata da decisão.
- **Causa B (Justificativa Rígida de Aluguel Epistêmico):** O registro de aluguel epistêmico assumia taxativamente que toda vulnerabilidade `HIGH` alterava diretamente o próximo passo humano.
- **Causa C (Sobrescrita Unilateral do Próximo Passo):** Em `src/idea_evolution/orchestration/lean_loop.py` e `src/idea_evolution/artifacts/mapper.py`, `escalation_output.updated_next_action` sobrescrevia incondicionalmente a proposta de falseamento da primeira passada (`FOCUSED_ESCALATION_CAN_UNILATERALLY_OVERRIDE_NEXT_ACTION = TRUE`).
- **Causa D (Ausência de Diretrizes de Estágio e Falsa Precisão nos Prompts):** Os prompts em linha do Lean Loop não distinguiam severidade de prioridade atual, não proibiam requisitos não-funcionais de mutar a hipótese de produto e não continham guardas contra asserções numéricas arbitrárias.

---

## 3. Novos Invariantes de Domínio e Arquitetura

1. **`SEVERITY != PRIORITY`:** Uma vulnerabilidade de segurança ou conformidade pode ter severidade `HIGH`, mas em estágios iniciais (`DISCOVERY`, `VALIDATION`) sua relevância para a próxima decisão humana é `LATER`, salvo solicitação explícita do usuário.
2. **`FOCUSED_ESCALATION_CAN_UNILATERALLY_OVERRIDE_NEXT_ACTION = FALSE`:** A arbitragem de próximo passo avalia o estágio evolutivo da ideia e impede que requisitos técnicos de implementação substituam experimentos de validação de problema/mercado.
3. **`PRODUCT_REFINEMENT != ENGINEERING_REQUIREMENT`:** Controles técnicos de infraestrutura e conformidade são registrados em críticas e requisitos de engenharia, sendo estritamente impedidos de sequestrar a hipótese refinada do produto.
4. **`FALSE_PRECISION_GUARD`:** Asserções numéricas não rastreáveis à fonte original ou a medições declaradas (ex: `<200 ms`) são detectadas e rebaixadas para `[MÉTRICA NÃO MEDIDA: medição necessária]`.
5. **`ALTERNATIVE_CLASSIFICATION`:** Reconhece explicitamente que o status quo gratuito (`STATUS_QUO`, como planilhas e etiquetas do WhatsApp) é a linha de base competitiva em descoberta.
6. **`LEAN_L1_MAX_MODEL_CALLS = 2`:** O teto inegociável de chamadas de inferência do Lean L1 permanece exatamente 2.

---

## 4. Comportamento Alterado e Componentes Implementados

### 4.1. Módulo `src/idea_evolution/domain/decision_relevance.py`
- Enums tipados: `IdeaStage`, `RiskCategory`, `DecisionRelevance`, `AlternativeCategory`, `NumericBasis`.
- Contrato Pydantic: `FalsificationCriterion` (hipótese, observação destrutiva, teste de menor custo).
- `DecisionRelevancePolicy`: Avaliação determinística baseada no estágio, categoria do risco, severidade e intenção explícita do usuário.
- `FalsePrecisionGuard`: Detecção e sanitização regex de alegações quantitativas não ancoradas.
- `NextActionArbitrationPolicy`: Arbitragem de próximo passo impedindo substituição indevida por requisitos técnicos em descoberta.

### 4.2. Endurecimento do `EarlyEpistemicGate`
- Etapa 5 reformulada: avalia `DecisionRelevancePolicy.evaluate_vulnerability_relevance`.
- Em `DISCOVERY`/`VALIDATION`: Riscos de segurança HIGH recebem relevância `LATER` e não acionam escalação desnecessária, permitindo que a atenção foque em bloqueadores de usabilidade ou comportamento.
- Em `PRE_PRODUCTION`: Riscos de segurança HIGH tornam-se `CRITICAL_NOW` e acionam escalação legítima.
- Solicitação explícita do usuário por segurança é honrada imediatamente como `CRITICAL_NOW`.

### 4.3. Endurecimento do `LeanLoopRunner` e `EvolutionArtifactMapper`
- Prompts refinados com diretrizes de qualidade, estágio e falseamento empírico.
- Sanitização de precisão numérica nas saídas de ambos os passos.
- Arbitragem de próximo passo impedindo que a escalação técnica imponha "implementar criptografia".
- Desacoplamento entre hipótese de produto e requisitos de engenharia na montagem do `EvolutionArtifact`.
- Otimização do schema JSON estrito de `LeanFirstPassOutput` para respeitar o limite de 5000 caracteres da Cerebras Cloud (comprimento atual: 4707 caracteres).

---

## 5. Matriz de Testes e Evidências

Todos os 445 testes anteriores continuam 100% verdes, acrescidos de 8 novos testes adversariais rigorosos:

| Teste | Cenário | Resultado |
|---|---|---|
| `test_whatsapp_saas_discovery_regression_case` | Regressão WhatsApp SaaS: segurança HIGH gravada, mas prioridade imediata mantida no falseamento de descoberta; hipótese não mutada para E2EE; `<200 ms` sanitizado | **PASS** |
| `test_preproduction_security_countercase` | Pré-produção com falha crítica de segurança: segurança torna-se `CRITICAL_NOW` e escala | **PASS** |
| `test_explicit_user_security_request_case` | Usuário solicita auditoria de segurança expressamente: segurança escala mesmo em descoberta | **PASS** |
| `test_technical_feasibility_blocker_case` | Inviabilidade técnica fatal em descoberta (banimento de API): escala como `CRITICAL_NOW` | **PASS** |
| `test_human_normative_choice_control_case` | Escolha normativa humana: retorna `REQUEST_HUMAN_DECISION` com exatamente 1 chamada | **PASS** |
| `test_false_precision_guard_detection_and_downgrade` | Detecção e rebaixamento de métricas numéricas arbitrárias | **PASS** |
| `test_falsification_criteria_structure_and_preservation` | Preservação estruturada de critérios de falseamento empírico | **PASS** |
| `test_authority_and_provenance_invariants` | Preservação de `USER_EXPLICIT`, `VALID_USER_DERIVATION`, `MODEL_HYPOTHESIS` e `SourceAnchor` | **PASS** |

Total da suíte: **453 passed, 1 warning (pytest collection) em 14.96s**.

---

## 6. Limitações Conhecidas & Próximos Passos

1. **Classificação de Estágio:** Em ausência de modelo externo de categorização ou declaração explícita do usuário, o sistema assume conservadoramente `DISCOVERY` para ideias conceituais novas.
2. **Revisão de Supervisor:** Esta missão produz a branch candidata `fioideias/v1.1-decision-relevance`. Nenhuma tag `v1.1.0` foi criada e a branch `main` (v1.0.1) permanece intocada.
3. **Próxima Missão Recomendada:** `SUPERVISOR_REVIEWS_V1_1_RESPONSE_QUALITY_BEFORE_RELEASE`.
