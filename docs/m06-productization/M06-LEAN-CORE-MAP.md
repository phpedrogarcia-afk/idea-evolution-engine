# M06-LEAN-CORE-MAP.md — Mapeamento e Congelamento do Núcleo Científico Lean L1

> **PROGRAMA:** M06 — Productization do Idea Evolution Engine  
> **BASE DO NÚCLEO CIENTÍFICO:** `LEAN_V1_CORE_BASELINE`  
> **HASH COMBINADO DO NÚCLEO (SHA-256):** `e6785bcaf5af291f438ab467386db640d4c0790e0f7012c40773dd25782e5600`  
> **STATUS:** `FROZEN_SCIENTIFIC_CORE`

---

## 1. Inventário de Arquivos do Núcleo Científico e Hashes SHA-256

Os componentes de software que definem formalmente a **Condição C (Lean Loop L1 + Early Epistemic Gate)** foram identificados, isolados e auditados criptograficamente:

| Módulo / Arquivo Canônico | Caminho no Repositório | SHA-256 (Normalizado LF) | Responsabilidade Epistêmica |
|---|---|---|---|
| **Orquestrador Lean** | [`src/idea_evolution/orchestration/lean_loop.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/src/idea_evolution/orchestration/lean_loop.py) | `8e3551f87dc9c1b9a6bf225f96d6b50fe6bb48441eaa94e569438918fa6056d0` | Orquestra a Chamada 1, consulta o Gate a custo zero e despacha no máximo 1 escalação focada. |
| **Portão Epistêmico Precoce** | [`src/idea_evolution/domain/early_epistemic_gate.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/src/idea_evolution/domain/early_epistemic_gate.py) | `2bc13fdff123964f7b1e103ab52d41d61d7ca130eed07bdc1b7a0583063ebb62` | Regras determinísticas de decisão (custo 0), aluguel epistêmico, delta decisório e contenção de desperdício. |
| **Bases de Estado e Autoridade** | [`src/idea_evolution/domain/state.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/src/idea_evolution/domain/state.py) | `9692daf65e3a4697b6847a1afb83a0231954cae564d726eae30c37b5dcfd0a83` | Define `PromotionAuthorityBasis`, `OntologyState` e imutabilidade de base humana. |
| **Contratos Epistêmicos** | [`src/idea_evolution/domain/epistemic_contracts.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/src/idea_evolution/domain/epistemic_contracts.py) | `639866dd801d8e60e93ce9ccb9d673c9df204a66a98c407c559a86adefc8e43b` | `SourceAnchor`, `NegativeKnowledgeRecord` e linhagem imutável de proposições. |
| **Validador de Ancoragem** | [`src/idea_evolution/domain/grounding.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/src/idea_evolution/domain/grounding.py) | `d68c0598fa31c256d0e2ca1a3d01b11c0810c4f1330304cb5316a5397803733d` | `AuthorityProofValidator` — detecta e bloqueia spoofing de autoridade `USER_EXPLICIT`. |
| **Fronteira de Evidência** | [`src/idea_evolution/domain/evidence_boundary.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/src/idea_evolution/domain/evidence_boundary.py) | `b75a369a0525dd2850b06d80d92add91a4acd71527f31ef8536328bced5e0a12` | `EvidencePassport`, canais de aquisição e separação rigorosa entre sintético e observado. |
| **Interface do Provedor** | [`src/idea_evolution/providers/base.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/src/idea_evolution/providers/base.py) | `24b49a58333d2ca9be8dc6dc01cf1749fecb91e9becd6e735bef4b61dc82ba02` | Contrato abstrato de execução de modelo (`ModelRunner`, `ModelResponse`). |

$$\mathbf{\text{LEAN\_V1\_CORE\_COMBINED\_SHA256} = \text{e6785bcaf5af291f438ab467386db640d4c0790e0f7012c40773dd25782e5600}}$$

---

## 2. Anatomia Semântica do Núcleo Lean L1

### 2.1 Invariante Inegociável de Custo
```python
LEAN_L1_MAX_MODEL_CALLS = 2
```
O sistema nunca executa mais de 2 chamadas de modelo por evolução de ideia:
- **Chamada 1 (Obrigatória):** `LEAN_FIRST_PASS`
- **Gate (Custo 0):** `EarlyEpistemicGate.evaluate()`
- **Chamada 2 (Condicional):** `FOCUSED_ESCALATION` (apenas se justificada por incerteza material)

### 2.2 Schemas de Entrada e Saída

1. **`LeanFirstPassOutput`:**
   - `interpreted_problem`: Problema formulado a partir da ideia.
   - `human_intent`: Intenção do usuário isolada e preservada.
   - `primary_mechanism`: Mecanismo primário com `claimed_basis` auditada.
   - `competing_alternatives`: Alternativas com tradeoffs identificados.
   - `key_assumptions`: Premissas críticas não verificadas.
   - `material_ambiguities`: Ambiguidades materiais a resolver.
   - `material_vulnerabilities`: Vulnerabilidades com severidade (`HIGH`, `MEDIUM`, `LOW`).
   - `remaining_uncertainties`: Incertezas residuais.
   - `requires_human_normative_choice`: Booleano para escolha de valor humano.
   - `proposed_next_action`: Próximo passo sugerido.

2. **`FocusedEscalationOutput`:**
   - `escalation_reason`: Razão tipada de escalação.
   - `target_hypothesis`: Hipótese ou incerteza focalizada.
   - `focused_critique_or_analysis`: Crítica aprofundada específica.
   - `resolved_tradeoffs`: Trade-offs esclarecidos.
   - `discriminating_tests`: Testes concretos sugeridos.
   - `decision_progress_made`: Indicador de avanço decisório.
   - `updated_next_action`: Atualização do próximo passo.

### 2.3 Regras de Decisão do Early Epistemic Gate (Custo = 0)

1. **Auditoria de Autoridade:** Verifica se o modelo alegou falsamente `USER_EXPLICIT` para conceitos inventados; caso positivo, rebaixa para `MODEL_HYPOTHESIS` e marca `authority_spoofing_detected = True`.
2. **Conhecimento Negativo:** Cruza propostas contra lições podadas prévias (`negative_knowledge_pool`).
3. **Parada por Autoridade Humana:** Se a dúvida for normativa/ética, retorna `REQUEST_HUMAN_DECISION` imediatamente (mais IA não substitui autoridade humana).
4. **Escalação por Vulnerabilidade Crítica:** Se houver risco `HIGH`, emite `ESCALATE_FOCUSED` com `MATERIAL_VULNERABILITY`.
5. **Escalação por Mecanismos Concorrentes:** Se houver alternativas com tradeoffs concorrentes reais, emite `ESCALATE_FOCUSED` com `COMPETING_MECHANISMS`.
6. **Escalação por Incerteza da Realidade:** Se houver dúvida factual profunda de hardware ou ambiente real, emite `ESCALATE_FOCUSED` com `REALITY_UNCERTAINTY`.
7. **Retorno Imediato (Regra de Contenção de Desperdício):** Em todos os demais casos, a ideia é considerada estruturada o suficiente e o sistema retorna imediatamente após 1 chamada (`RETURN_NOW`).

---

## 3. Classificação de Reuso vs. Componentes Faltantes

### Componentes Reutilizáveis Imediatamente (Zero Reescrever):
- `LeanLoopRunner`: Orquestrador completo, testado e imutável.
- `EarlyEpistemicGate`: Validador determinístico completo.
- `AuthorityProofValidator`: Guard contra spoofing de autoridade.
- `SourceAnchor`: Ancoragem criptográfica da entrada original.
- `RunTracer`: Gravação de eventos, chamadas e deltas em disco.

### Componentes que Devem ser Embalados (Product Shell):
- **`IdeaEvolutionService` (Novo):** Ponto de entrada de aplicação que orquestra a sessão do usuário, lida com configurações e isola a CLI do runner interno.
- **`EvolutionArtifact` (Novo/Refinado):** Artefato canônico tipado que consolida o resultado do Lean L1 sem misturar dados de experimento científico.
- **`HumanResultRenderer` (Novo/Refinado):** Gerador de Markdown limpo para o usuário, destacando O Que Mudou, Crítica, Premissas e Próximo Passo sem ruído técnico ou metadados de laboratório (A/B/C, RPL, tokens de provedor).
- **`ProviderAdapter` (Novo/Refinado):** Encapsulamento que desacopla o `LeanLoopRunner` de provedores físicos específicos, garantindo política de custo zero e erro tipado.
