# M06-P3-PROVENANCE-ONTOLOGY-COMPLETION-RECORD.md — Registro de Conclusão da Fase P3

> **PROGRAMA:** M06 — Productization  
> **FASE:** P3 — Product Provenance & Ontology Enforcement  
> **STATUS:** `COMPLETE`  
> **DATA:** 2026-09-04  
> **INTEGRIDADE DO NÚCLEO CIENTÍFICO:** `LEAN_CORE_HASH_MATCH = YES` (`e6785bcaf5af291f438ab467386db640d4c0790e0f7012c40773dd25782e5600`)

---

## 1. Escopo e Objetivo da Fase P3

Endurecer a fronteira de produto do `EvolutionArtifact` para garantir deterministicamente que nenhuma inferência ou hipótese gerada por IA possa usurpar a autoridade do usuário humano, preservando sem ambiguidade a distinção ontológica:

$$\mathbf{USER\_EXPLICIT \neq VALID\_USER\_DERIVATION \neq MODEL\_CANDIDATE \neq UNKNOWN}$$

A Fase P3 assegura que:
- O produto pode reformular ou aprofundar uma ideia, mas **nunca reescrever o histórico**.
- Hipótese de modelo não é fato de usuário.
- Derivação lógica do sistema não é declaração explícita humana.
- Refinamento de produto não é decisão aprovada.
- Repetição de um conceito em múltiplos estágios não cria autoridade.
- Seleção de uma proposta como "próximo passo" não cria autoridade.
- A serialização/desserialização JSON não apaga estados epistêmicos.
- O desconhecido (UNKNOWN) permanece representável e não é descartado para cosmética.
- O sistema falha fechado (*fail closed*) para `UNKNOWN`/rejeitado, nunca para `USER_EXPLICIT`.
- Nenhum modelo pode autocertificar sua própria autoridade.

---

## 2. Inventário de Arquivos e Modificações

### Arquivos Criados:
- [`src/idea_evolution/artifacts/provenance.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/src/idea_evolution/artifacts/provenance.py): Modelo `ProvenanceReceipt` e função determinística `audit_artifact_provenance(artifact)` com custo $= 0$ chamadas de IA.
- [`tests/test_fioideias_v1_provenance_guard.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/tests/test_fioideias_v1_provenance_guard.py): Suíte de 20 testes adversariais e de conformidade epistêmica.
- [`docs/m06-productization/M06-P3-PROVENANCE-ONTOLOGY-COMPLETION-RECORD.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/m06-productization/M06-P3-PROVENANCE-ONTOLOGY-COMPLETION-RECORD.md): Este registro formal de conclusão.

### Arquivos Modificados:
- [`src/idea_evolution/artifacts/evolution_artifact.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/src/idea_evolution/artifacts/evolution_artifact.py):
  - Adicionados campos tipados: `original_idea_authority`, `refined_idea_authority`, `assumptions_authority`.
  - Adicionado `ontology_state` em `CandidatePossibility` com bloqueio determinístico a spoofing de `CORE`.
  - Adicionados validadores estritos de autoridade e integridade criptográfica de `SourceAnchor` (detecção de adulteração de hash e conteúdo).
  - Adicionado método `audit_provenance()` gerando `ProvenanceReceipt`.
- [`src/idea_evolution/artifacts/mapper.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/src/idea_evolution/artifacts/mapper.py):
  - Mapeamento explícito das classes de autoridade para Lean L1, Fast Fallback (Condição A) e Simple Loop (Condição B).
  - Preservação do status `REJECTED` em candidatos descartados.
  - Contenção determinística de spoofing em propostas da Condição B via `AuthorityProofValidator`.
- [`src/idea_evolution/artifacts/__init__.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/src/idea_evolution/artifacts/__init__.py): Exportação de `ProvenanceReceipt` e `audit_artifact_provenance`.
- [`src/idea_evolution/service/evolution_service.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/src/idea_evolution/service/evolution_service.py): Ajuste na leitura do status do `SimpleIdeaState` no caminho isolado de pesquisa da Condição B.
- Documentos de governança atualizados: `M06-V1-EXECUTION-PLAN.md`, `CURRENT-STATE.md`, `ACTIVE-QUEUE.md`.

---

## 3. Mapeamento Ontológico Canônico

| Conceito Científico | Classe Canônica Existente | Representação no `EvolutionArtifact` | Regra de Autoridade / Proveniência |
|---|---|---|---|
| Entrada Bruta Humana | `SourceAnchor` / `HUMAN_INPUT` | `original_idea` + `source_anchor` | `original_idea_authority = USER_EXPLICIT` (Imutável, Ancorado) |
| Intenção Inferida | `LeanFirstPassOutput.human_intent` | `human_intent` | `intent_provenance = VALID_USER_DERIVATION` (Não explícito) |
| Ideia Refinada Proposta | Mutação ou Mecanismo Primário | `refined_idea` | `refined_idea_authority = MODEL_HYPOTHESIS` (Proposta de sistema) |
| Possibilidades / Alternativas | `competing_alternatives` | `candidate_possibilities` | `authority_basis = MODEL_HYPOTHESIS`, `ontology_state = CANDIDATE/REJECTED` |
| Crítica e Fragilidades | `material_vulnerabilities` | `critique` | `authority_basis = MODEL_HYPOTHESIS` |
| Premissas Identificadas | `key_assumptions` | `assumptions` | `assumptions_authority = MODEL_HYPOTHESIS` (Nunca fato do usuário) |
| Incertezas e Lacunas | `remaining_uncertainties` / `material_ambiguities` | `uncertainties` | `unknown_count` (Preservado, nunca descartado por conveniência) |
| Escolha Normativa Humana | `requires_human_normative_choice` | `human_decision_required` | Exige decisão soberana do usuário; IA não decide |

$$\mathbf{\text{PARALLEL\_PRODUCT\_ONTOLOGY\_CREATED} = NO}$$

---

## 4. Auditoria das Rotas de Refinamento (`refined_idea`)

| Rota no Runtime | Campo Fonte | Classe de Autoridade na Fonte | Campo no Produto | Classe de Autoridade no Produto | Upgrade de Autoridade? |
|---|---|---|---|---|---|
| Lean L1 com Escalação | `escalation.mutated_hypothesis_description` | `MODEL_HYPOTHESIS` | `refined_idea` | `MODEL_HYPOTHESIS` | **NÃO** |
| Lean L1 Direto (1 passada) | `first_pass.primary_mechanism.mechanism` | `MODEL_HYPOTHESIS` | `refined_idea` | `MODEL_HYPOTHESIS` | **NÃO** |
| Fallback Condição A | `parsed_output.refined_version` | `MODEL_HYPOTHESIS` | `refined_idea` | `MODEL_HYPOTHESIS` | **NÃO** |
| Pesquisa Condição B | `state.current_idea` | `MODEL_HYPOTHESIS` | `refined_idea` | `MODEL_HYPOTHESIS` | **NÃO** |

$$\mathbf{\text{REFINED\_IDEA\_AUTHORITY\_UPGRADE} = NO}$$

---

## 5. Recibo de Completude de Proveniência (`ProvenanceReceipt`)

A função determinística `audit_artifact_provenance(artifact)` audita todos os itens semânticos do artefato sem invocar modelos:
- Conta itens com autoridade: `USER_EXPLICIT`, `VALID_USER_DERIVATION`, `MODEL_CANDIDATE`, `UNKNOWN`, `REJECTED`, `DEFERRED`.
- Garante conformidade:
  $$\mathbf{\text{UNLABELED\_SEMANTIC\_ITEM\_COUNT} = 0}$$
- Metadados técnicos (`run_id`, `schema_version`, etc.) são excluídos da contagem semântica.

---

## 6. Verificação Criptográfica do Núcleo Científico

```
LEAN_CORE_HASH_BEFORE = e6785bcaf5af291f438ab467386db640d4c0790e0f7012c40773dd25782e5600
LEAN_CORE_HASH_AFTER  = e6785bcaf5af291f438ab467386db640d4c0790e0f7012c40773dd25782e5600
STATUS                = STRICT_MATCH (ZERO MUTATION IN SCIENTIFIC CORE)
```

---

## 7. Resultados de Testes

- **Testes Adversariais da Fase P3 (`test_fioideias_v1_provenance_guard.py`):** 20/20 aprovados.
- **Testes da Fase P2 (`test_evolution_artifact.py`):** 20/20 aprovados.
- **Testes da Fase P1 (`test_fioideias_v1_service_boundary.py`):** 11/11 aprovados.
- **Testes de Continuidade (`test_continuity.py`):** 7/7 aprovados.
- **Suíte Global de Regressão:** 383/383 aprovados (0 falhas).
- **Consumo de Tokens na Auditoria:** 0 tokens gastos ($0 custo, 100% determinístico).
