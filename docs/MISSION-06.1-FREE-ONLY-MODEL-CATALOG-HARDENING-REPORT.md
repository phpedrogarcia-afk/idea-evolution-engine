# MISSION 06.1 — FREE-ONLY MODEL CATALOG HARDENING REPORT

> **RELATÓRIO DE ENDURECIMENTO DO CATÁLOGO DE MODELOS E GOVERNANÇA DE CUSTOS (IEE)**  
> **Data:** 26 de agosto de 2026 | **Agente:** Antigravity (Google DeepMind)  
> **Status:** `COMPLETE_OFFLINE` | **Veredito:** `MULTI_MODEL_READY_OFFLINE = TRUE` | `FREE_ONLY_POLICY = INSTITUTIONALIZED`  
> **Fase:** `FASE_1_SIMPLE_LOOP_MVP` | **Checkpoint:** [`CP-20260826-007`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/checkpoints/CP-20260826-007.md)

---

## 1. Stale Config Found & Models Replaced
- **Stale Models Detectados:**
  - `groq/llama-3.3-70b-versatile`: Encerrado pela Groq em 16 de agosto de 2026.
  - `gemini/gemini-2.0-flash`: Encerrado pelo Google em 1º de junho de 2026.
- **Modelos Ativos Adotados no Seed:**
  - **Groq:** `openai/gpt-oss-120b` e `qwen/qwen3.6-27b` (ambos ativos no Free Plan com limites publicados de 1.000 req/dia e 200k tokens/dia).
  - **Gemini:** `gemini-3.7-flash`, `gemini-3.6-flash`, `gemini-3.1-flash-lite` (ativos com input/output gratuitos no Free Tier).
  - **OpenRouter:** `openrouter/free` catalogado para futuras expansões (~50 req/dia).
  - **OpenAI / Anthropic:** Classificados como `PAID` e `PROMOTIONAL_CREDIT` (bloqueados sob política padrão `FREE_ONLY`).

---

## 2. Model Catalog & Verification Sources
O IEE passa a manter um catálogo versionado e auditável em [`config/model_catalog.json`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/config/model_catalog.json) e gerenciado por [`src/idea_evolution/config/catalog.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/src/idea_evolution/config/catalog.py):

| Provedor | Modelo | Status | Classe de Custo | Free Capacity Type | Privacy Class | Fonte de Verificação |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Groq** | `openai/gpt-oss-120b` | `ACTIVE` | `FREE_TIER` | `1000_req_day_200k_tokens` | `STANDARD_PRIVACY` | GroqCloud Models API & Free Docs |
| **Groq** | `qwen/qwen3.6-27b` | `ACTIVE` | `FREE_TIER` | `1000_req_day_200k_tokens` | `STANDARD_PRIVACY` | GroqCloud Models API & Free Docs |
| **Groq** | `llama-3.3-70b-versatile` | `SHUT_DOWN` | `FREE_TIER` | `none` | `STANDARD_PRIVACY` | Groq Deprecations Notice (16/08/2026) |
| **Gemini** | `gemini-3.7-flash` | `ACTIVE` | `FREE_TIER` | `15_rpm_1500_rpd` | `PROVIDER_MAY_USE_FOR_PRODUCT_IMPROVEMENT` | Google AI Studio Pricing Docs |
| **Gemini** | `gemini-3.6-flash` | `ACTIVE` | `FREE_TIER` | `15_rpm_1500_rpd` | `PROVIDER_MAY_USE_FOR_PRODUCT_IMPROVEMENT` | Google AI Studio Pricing Docs |
| **Gemini** | `gemini-2.0-flash` | `SHUT_DOWN` | `FREE_TIER` | `none` | `PROVIDER_MAY_USE_FOR_PRODUCT_IMPROVEMENT` | Google AI Deprecations Notice (01/06/2026) |
| **OpenAI** | `gpt-4o-mini` | `ACTIVE` | `PAID` | `none` | `STANDARD_PRIVACY` | OpenAI Platform Pricing |
| **Anthropic** | `claude-3-5-haiku-20241022`| `ACTIVE` | `PROMOTIONAL_CREDIT` | `signup_credit_only` | `STANDARD_PRIVACY` | Anthropic Platform Pricing |
| **OpenRouter**| `openrouter/free` | `ACTIVE` | `FREE_ROUTER` | `50_req_day` | `STANDARD_PRIVACY` | OpenRouter FAQ Docs |
| **Fake Local**| `default-model` | `ACTIVE` | `LOCAL_ZERO_MARGINAL_API_COST` | `unlimited` | `AIR_GAPPED_LOCAL` | Internal Deterministic Mock |

---

## 3. Cost Classes & FREE_ONLY Policy
- **Taxonomia de Custo:** `FREE_TIER`, `FREE_ROUTER`, `LOCAL_ZERO_MARGINAL_API_COST`, `PROMOTIONAL_CREDIT`, `PAID`, `UNKNOWN`.
- **Regras sob `FREE_ONLY` (Padrão Constitucional):**
  - Modelos `PAID` são rejeitados antes da inferência com `COST_POLICY_VIOLATION`.
  - Modelos `PROMOTIONAL_CREDIT` são rejeitados sob `FREE_ONLY` e requerem declaração explícita de `ALLOW_PROMOTIONAL`.
  - `PAID_FALLBACK: FORBIDDEN`: Falha de cota em modelo gratuito nunca transiciona para um modelo pago.

---

## 4. Privacy Policy Metadata
- O catálogo mapeia `privacy_class: PROVIDER_MAY_USE_FOR_PRODUCT_IMPROVEMENT` para o Free Tier do Gemini.
- A flag `exclude_product_improvement_use: true` permite bloquear provedores com essa cláusula para processamento de ideias sensíveis ou proprietárias.

---

## 5. Regras de Fallback e Modos de Execução

```text
┌────────────────────────────────────────────────────────┐
│               GOVERNANÇA DE FALLBACK                   │
└──────────────────────────┬─────────────────────────────┘
                           │
         ┌─────────────────┴─────────────────┐
         ▼                                   ▼
  [EXPERIMENTAL_PINNED]             [FREE_POOL_OPERATIONAL]
  (Modo Canário / M05)              (Modo Operacional Futuro)
  - PINNED_MODEL = TRUE             - FREE_QUOTA_EXHAUSTED ──► Tenta próximo Free elegível
  - AUTO_FALLBACK = FALSE           - MODEL_UNAVAILABLE ─────► Tenta próximo Free elegível
  - Quota falhou? ──► BLOCKED       - SCHEMA_INVALID ────────► NÃO troca provedor (Preserva Bug)
  (Sem troca de modelo)             - SEMANTIC_FAILURE ──────► NÃO troca provedor
```

---

## 6. Saída do `iee providers doctor`

```text
================================================================================
          IDEA EVOLUTION ENGINE — PROVIDERS DOCTOR & CATALOG HEALTH
================================================================================
PROVEDOR         ADAPTADOR    MODELO PADRÃO            STATUS     COST CLASS     FREE_ONLY 
--------------------------------------------------------------------------------
Groq             [OK] Sim     openai/gpt-oss-120b      ACTIVE     FREE_TIER      [OK] Sim  
Google Gemini    [OK] Sim     gemini-3.7-flash         ACTIVE     FREE_TIER      [OK] Sim  
OpenAI           [OK] Sim     gpt-4o-mini              ACTIVE     PAID           [X] Nao   
Anthropic Claude [OK] Sim     claude-3-5-haiku-20241022 ACTIVE     PROMOTIONAL_CREDIT [X] Nao   
Deterministic Fake Runner [OK] Sim     default-model            ACTIVE     LOCAL_ZERO_MARGINAL_API_COST [OK] Sim  
--------------------------------------------------------------------------------
NOTAS DE GOVERNANÇA E PRIVACIDADE:
  * [Google Gemini]: Termos do Free Tier permitem uso de dados pelo provedor para melhoria de produto.
  * [OpenAI]: Provedor classificado como PAID. Bloqueado sob política padrão FREE_ONLY.
  * [Anthropic Claude]: Provedor classificado como PROMOTIONAL_CREDIT. Bloqueado sob política padrão FREE_ONLY.
--------------------------------------------------------------------------------
Nenhum valor secreto é exibido ou gravado. Zero chamadas de inferência realizadas.
================================================================================
```

---

## 7. Resultados dos Testes Automatizados (61 / 61 Aprovados — 100% OK)

```text
=================================================================
       SUÍTE TOTAL DE TESTES: 61 / 61 APROVADOS (100% OK)
=================================================================
  1. Continuidade (test_continuity.py):                       7 passed
  2. Inteligência (test_intelligence.py):                    10 passed
  3. Doutrina Constitucional (test_constitutional_doctrine):  7 passed
  4. Domínio e Estado (test_domain_state.py):                 4 passed
  5. Contratos e Prompts (test_stage_contracts.py):           2 passed
  6. Roteamento de Modelos (test_model_routing.py):           5 passed
  7. Catálogo de Modelos (test_model_catalog.py):             8 passed
  8. Loop E2E Padrão (test_simple_loop_e2e.py):               1 passed
  9. Reconstrução Bounded (test_reconstruction_path.py):      2 passed
 10. Critique-Revision Loop (test_critique_revision_loop.py): 1 passed
 11. Multi-Model E2E (test_multi_model_e2e.py):               2 passed
 12. Adversarial MVP (test_adversarial_mvp.py):               3 passed
 13. Adversarial Multi-Model (test_adversarial_multi_model):  4 passed
 14. Adversarial Catálogo & Custo (test_adversarial_catalog): 4 passed
 15. Pacote de Comparação (test_comparison_packet.py):        1 passed
=================================================================
  - Context Validator:        [OK] 100% VÁLIDO (Zero Drift)
  - Intelligence Validator:   [OK] 100% VÁLIDO (Foundation Ready = True)
=================================================================
```

---

## 8. M05 Blocker Status & FioOS Future Boundary
- **Status do Canário Real (M05):** Mantido como `BLOCKED_PROVIDER_CREDENTIAL_OR_COST`.
- **FioOS Boundary Formalizada:**
  - *IEE owns epistemic routing* (qualidade, crítica, deliberação, redução de incerteza).
  - *FioOS owns governed execution routing* (budgets, sandboxes, leases, auditoria).
  - O IEE não duplica o kernel ou gateway do FioOS.

---

## 9. Decision Delta
- `CLOSED_STALE_MODEL_RISK`: Modelos descontinuados eliminados das configurações ativas.
- `INSTITUTIONALIZED_FREE_ONLY_EXECUTION_POLICY`: Bloqueio estrito e preventivo de custos diretos.
- `PREPARED_FUTURE_FIOOS_BOUNDARY`: Arquitetura orientada a capacidades cognitivas sem dependência de IDs proprietários fixos.

---

## 🚦 Status Operacional do Repositório

```text
=================================================================
        IDEA EVOLUTION ENGINE — OPERATIONAL STATUS
=================================================================
  Project:           Idea Evolution Engine (IEE)
  Current Phase:     FASE_1_SIMPLE_LOOP_MVP
  Next Product:      SIMPLE_IDEA_EVOLUTION_LOOP
  Git State:         branch=main | worktree=CLEAN
  Latest Checkpoint: CP-20260826-007
  Active Task:       TASK-000
  Next Action:       Configuração de API key pelo operador para M05-B e M07
=================================================================
```

---

## 🛑 Ponto de Parada Mandatório (STOP)
A Missão 06.1 está **100% concluída**. O catálogo de modelos e a governança de custos gratuita estão endurecidos e testados offline.
