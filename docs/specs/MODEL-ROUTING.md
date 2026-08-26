# MODEL-ROUTING.md — Especificação de Roteamento Multi-Modelo & Governança de Custos

> **CASA CANÔNICA DA ESPECIFICAÇÃO DE ROTEAMENTO DE MODELOS E POLÍTICA FREE_ONLY (v1.1.0).**

---

## 1. Princípios Arquiteturais e Doutrinais
- **Functions are not Models:** Estágios cognitivos (`UNDERSTAND`, `ATTACK`, `CRITIQUE`, `REVISION`, `ALTERNATIVES`, `REALITY_CHECK`, `SYNTHESIZE`, `FINAL_REVIEW`) são funções e contratos estritos do kernel, independentes de fornecedores específicos.
- **The Kernel is the Mediator:** Modelos nunca dialogam diretamente entre si ("chat livre"). O IEE controla a ordem, valida esquemas JSON, preserva o estado intermediário e roteia o contexto estritamente necessário para o próximo modelo.
- **Cost Authority is Authority (Doutrina FioOS):** Nenhuma inferência comercial com custo direto não autorizado pode ser disparada. O IEE opera por padrão sob política `FREE_ONLY`.
- **Capability Request First; Provider Selection Second:** O estágio requisita capacidade cognitiva (ex: `reasoning`, `structured_output`); a governança de roteamento seleciona candidatos elegíveis sob a política de custo e privacidade.
- **Zero Fallback Silencioso (`NO_CROSS_PROVIDER_FALLBACK`):** Se um modelo ou provedor falha em validação de schema ou erro semântico, o sistema nunca troca de provedor silenciosamente para não mascarar bugs.
- **Fronteira com o FioOS:**
  - *IEE owns epistemic routing* (decide quais papéis epistêmicos e deliberações são necessários para maturar a ideia).
  - *FioOS owns governed execution routing* (quando a ponte estiver ativa, governa sandboxes, orçamentos, leases e auditoria de ferramentas).
  - O IEE não duplica o runtime, kernels ou gateways do FioOS.

---

## 2. Classificação de Custos (`CostClass`)
O catálogo categoriza o modelo em classes explícitas:
- `FREE_TIER`: Gratuito diretamente no provedor com limites de quota diária/minuto (ex: Groq, Google Gemini Free Tier).
- `FREE_ROUTER`: Router gratuito com rota dinâmica entre modelos abertos (ex: OpenRouter Free Pool).
- `LOCAL_ZERO_MARGINAL_API_COST`: Modelos locais ou fake determinísticos rodando em máquina própria com custo marginal de API zero.
- `PROMOTIONAL_CREDIT`: Saldo promocional inicial temporário (ex: Anthropic signup credit). Requer política `ALLOW_PROMOTIONAL`.
- `PAID`: Cobrança obrigatória por token (ex: OpenAI API comercial). Bloqueado sob `FREE_ONLY`.
- `UNKNOWN`: Provedor sem evidência verificada. Bloqueado sob `FREE_ONLY`.

---

## 3. Modos de Execução (`ExecutionMode`)
- **`EXPERIMENTAL_PINNED` (Modo Canário / M05):**
  - Modelo estritamente fixo (`PINNED_MODEL = TRUE`, `AUTO_FALLBACK = FALSE`).
  - Em caso de esgotamento de quota ou indisponibilidade, o experimento é interrompido com `EXPERIMENT_BLOCKED` para preservar a integridade científica do teste A/B/C.
- **`FREE_POOL_OPERATIONAL` (Modo Operacional Futuro):**
  - Permite transição apenas para o próximo candidato gratuito elegível (`MAY_TRY_NEXT_FREE`) se o erro for `FREE_QUOTA_EXHAUSTED` ou `MODEL_UNAVAILABLE`.
  - Proíbe transição se o erro for `SCHEMA_INVALID`, `PROMPT_FAILURE`, `SEMANTIC_FAILURE` ou `SAFETY_REJECTION`.

---

## 4. Schema de Configuração (`ModelRoutingConfig`)

```yaml
schema_version: "1.0.0"
description: "Mapeamento lógico de modelos e rotas por estágio"
cost_policy: FREE_ONLY                    # FREE_ONLY | ALLOW_PROMOTIONAL | ALLOW_PAID_WITH_BUDGET
execution_mode: EXPERIMENTAL_PINNED       # EXPERIMENTAL_PINNED | FREE_POOL_OPERATIONAL
exclude_product_improvement_use: false    # Se true, exclui provedores cujo free tier usa dados para treino

models:
  analyst:
    provider: groq
    model: openai/gpt-oss-120b
    credential_env: GROQ_API_KEY
    parameters:
      temperature: 0.2

  critic:
    provider: groq
    model: qwen/qwen3.6-27b
    credential_env: GROQ_API_KEY
    parameters:
      temperature: 0.3

routes:
  understand: analyst
  attack: critic

default_model_alias: analyst
```

---

## 5. Proveniência e Hash Determinístico
Cada execução grava deterministicamente:
- `logical_alias`, `provider`, `model`, `prompt_id`, `prompt_version`, `attempt`, `routing_config_hash`.
- O hash SHA-256 canônico inclui a versão do schema, política de custo, modo de execução, modelos e rotas ordenadas.
