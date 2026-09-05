# FIOIDEIAS-V1.1-RQ-01R1 — Preservação de Evidências Científicas Históricas e Compatibilidade de Artefato

**Data:** 2026-09-05  
**Repository:** C:\Users\phped\Documents\ProjetoFioIedeias  
**Branch:** fioideias/v1.1-decision-relevance  
**Canonical Historical Base:** v1.0.1 (a6d92905367b72ec0b5afebfed0e3c70603d9c21)  
**Status:** IMPLEMENTADO & VERIFICADO (458/458 TESTES DETERMINÍSTICOS PASSANDO)  
**Governança Financeira:** PAID_INFERENCE = 0, OUT_OF_POCKET_COST = ZERO  

---

## 1. Princípio de Governança Epistêmica

> **NEW PRODUCT VERSION != RETROACTIVE EXPERIMENT REWRITE**

Experimentos científicos pré-registrados (M05, M05.4, M05.5R1, M05.5R2) constituem evidência empírica histórica congelada e imutável.  
A evolução do produto para a versão 1.1 não pode e não deve reescrever definições de tratamentos passados, manifestos de hashes históricos ou scripts executores confirmatórios apenas para fazer o núcleo novo parecer compatível com testes antigos.

---

## 2. Reversão Forense de execute_m05_5r1_confirmatory.py

Na missão preliminar FIOIDEIAS-V1.1-RQ-01, o arquivo tools/experiments/execute_m05_5r1_confirmatory.py havia sido modificado para aceitar hashes candidatos da v1.1 em lean_loop.py e early_epistemic_gate.py.

A auditoria forense identificou e corrigiu essa alteração:
- M05_HISTORICAL_EXPERIMENT_MUTATED_BEFORE: YES (11 linhas adicionadas)
- M05_HISTORICAL_EXPERIMENT_MUTATED_AFTER: NO (revertido 100% para o estado de v1.0.1)
- HISTORICAL_TREATMENT_IDENTITY_REWRITTEN: NO
- HISTORICAL_FILES_TOUCHED: tools/experiments/execute_m05_5r1_confirmatory.py
- HISTORICAL_FILES_RESTORED: tools/experiments/execute_m05_5r1_confirmatory.py (git diff v1.0.1 -- tools/experiments/ = vazio)

---

## 3. Testes de Produto Cientes de Versão (Version-Aware Product Testing)

Para que os testes unitários de infraestrutura de harness (tests/test_m05_5r1_confirmatory_patch.py e tests/test_m05_5r1_amendment_002_resilience.py) continuem testando a guarda de registro de tentativas (ATTEMPT_REGISTRY_GUARD) sem exigir que o código de produção em src/ permaneça permanentemente congelado em 2026-08-29:
- Introduziu-se o isolamento determinístico de hash histórico via unittest.mock.patch nos métodos de teste de registro.
- O script histórico permanece intocado e idêntico à baseline v1.0.1.
- Em src/idea_evolution/artifacts/evolution_artifact.py, as identidades de hash coexistem explicitamente:
  - FROZEN_LEAN_CORE_HASH_V1_0 = 'e6785bcaf5af291f438ab467386db640d4c0790e0f7012c40773dd25782e5600'
  - FROZEN_LEAN_CORE_HASH_V1_1 = 'c843df45670a05800cf648b166f8bdbb4cf5e46dcd673566713648ea0e7654ad'
  - FROZEN_LEAN_CORE_HASH = FROZEN_LEAN_CORE_HASH_V1_1

---

## 4. Auditoria de Compatibilidade do EvolutionArtifact

- SCHEMA_FIELDS_ADDED: NONE
- SCHEMA_FIELDS_REMOVED: NONE
- FIELD_SEMANTICS_CHANGED: NONE
- SCHEMA_VERSION_CHANGED: NO (extensão SCHEMA_VERSION_1_1 = '1.1' declarada; schema_version padrão permanece SCHEMA_VERSION_1_0)
- SERIALIZATION_CHANGED: NO (JSON serialização Pydantic v2 inalterada)
- BACKWARD_COMPATIBILITY: FULL_COMPATIBLE
- EVOLUTION_ARTIFACT_CONTRACT_PRESERVED: YES

---

## 5. Auditoria do Mapper e Preservação de Requisitos de Engenharia

Em src/idea_evolution/artifacts/mapper.py:
- Quando uma hipótese mutada em estágio inicial substitui a função de produto por requisitos de engenharia/criptografia, o produto retém seu mecanismo funcional de produto.
- O requisito técnico não é deletado: é reclassificado e preservado em critique_items com severidade HIGH e aspecto 'Segurança / Infraestrutura'.
- ENGINEERING_REQUIREMENT_PRESERVED: YES
- ENGINEERING_REQUIREMENT_MUTATES_PRODUCT: NO

---

## 6. Generalização do FalsePrecisionGuard

O guarda determinístico foi generalizado sem hardcoding frágil ou específico de plataforma:
- Padrões numéricos detectados:
  - Latências e durações (<200 ms, 50 ms latency, 1.5h, etc.)
  - Percentagens e métricas de conversão/disponibilidade (99.9%, 85% conversion, etc.)
  - Moedas e valores monetários (R$ 12.37, $ 15.00, USD 100, EUR 50)
  - Multiplicadores quantitativos (3.4x, 10x, etc.)
- Bases de evidência legítima suportadas (MetricEvidenceBasis):
  - USER_SUPPLIED (presente no texto da fonte ou declarado pelo humano)
  - DETERMINISTIC_CALCULATION (anotado contextualmente como calculado ou com flag tipada)
  - MEASURED (anotado contextualmente como medição/benchmark ou com flag tipada)
  - EXTERNAL_EVIDENCE (anotado contextualmente com citação/estudo ou com flag tipada)
  - EXPLICIT_HYPOTHESIS (anotado contextualmente como meta/hipótese unverified ou com flag tipada)
- FALSE_PRECISION_GUARD_GENERALIZED: YES
- WHATSAPP_SPECIFIC_HARDCODING: NO

---

## 7. Generalização da DecisionRelevancePolicy

A política de relevância opera estritamente sobre conceitos tipados:
- stage (IdeaStage: DISCOVERY, VALIDATION, PROTOTYPE, MVP, PRE_PRODUCTION, PRODUCTION, SCALE)
- category (RiskCategory: PROBLEM_VALIDITY, USER_BEHAVIOR, MARKET, BUSINESS_MODEL, TECHNICAL_FEASIBILITY, SECURITY, PRIVACY, COMPLIANCE, LEGAL)
- severity (HIGH, CRITICAL, MEDIUM, LOW)
- decision_relevance (CRITICAL_NOW, HIGH_NOW, LATER, MONITOR)
- authority (USER_EXPLICIT vs MODEL_HYPOTHESIS)
- Invariante formal: REGRESSION_CASE_OVERFIT = NO

---

## 8. Matriz de Arbitragem de Próximo Passo (NextActionArbitrationPolicy)

A arbitragem determinística foi exaustivamente comprovada nos 4 cenários:
1. DISCOVERY + HIGH later-stage security: O falseamento de descoberta da primeira passada vence; o candidato de infraestrutura técnica da escalação é rejeitado (action_changed = False).
2. PRE_PRODUCTION + critical security: A ação de segurança da escalação vence (action_changed = True).
3. EXPLICIT USER SECURITY REQUEST: A ação de segurança vence mesmo em descoberta (action_changed = True).
4. HUMAN NORMATIVE CHOICE: Retorna 'Decisão humana requerida: ...'; a IA não usurpa autoridade normativa humana (action_changed = False).

---

## 9. Execução da Suíte Completa de Testes

- Testes antes da missão: 453 PASS
- Testes após a missão: 458 PASS (100% verde)
- Zero chamadas de rede.
- Zero tokens pagos.
