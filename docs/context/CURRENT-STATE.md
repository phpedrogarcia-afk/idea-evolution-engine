# docs/context/CURRENT-STATE.md — Snapshot Operacional Dinâmico

> **ESTE DOCUMENTO É A DECLARAÇÃO OPERACIONAL VIVA DO ESTADO DO REPOSITÓRIO.**
> Atualizado em: 2026-08-26 | Checkpoint: CP-20260826-007

---

## 1. Identificação Operacional

- **Projeto:** Idea Evolution Engine (IEE)
- **Fase Ativa:** FASE 1 — SIMPLE IDEA EVOLUTION LOOP MVP (FREE-ONLY MODEL CATALOG & COST GOVERNANCE HARDENING)
- **Status da Fundação:** `COMPLETE_AND_LOCKED` (`FOUNDATION_READY = TRUE`)
- **Status do Produto:** `SIMPLE IDEA EVOLUTION LOOP` com governança de custo `FREE_ONLY`, catálogo vivo `ModelCatalog`, 61 testes verdes e proteção estrita contra fallbacks pagos.
- **Status da Missão 05:** `REAL_MODEL_CANARY = BLOCKED_PROVIDER_CREDENTIAL_OR_COST` (Incerteza real mantida honestamente bloqueada por ausência de chaves de API).
- **Status da Missão 06.1:** `FREE_ONLY_MODEL_CATALOG_HARDENING = COMPLETE_OFFLINE` (`MULTI_MODEL_READY_OFFLINE = TRUE`, `FREE_ONLY_POLICY = INSTITUTIONALIZED`).
- **Reconciliação do Repositório Remoto:**
  - `DEFAULT_BRANCH`: `main`
  - `REMOTE_REPOSITORY`: `https://github.com/phpedrogarcia-afk/idea-evolution-engine.git`
  - `SECRET_SCAN`: `PASS` (0 credenciais ou segredos rastreados no Git)
- **Status do Executor de Modelos Reais:**
  - `REAL_SINGLE_MODEL_EXECUTION`: `BLOCKED_PROVIDER_CREDENTIAL_OR_COST` (Aguardando configuração de API key).
  - `REAL_CROSS_PROVIDER_VALIDATED`: `FALSE`
  - `REAL_MULTI_MODEL_DELIBERATION`: `NOT_EXECUTED`
  - `OFFLINE_SIMULATION_RUN`: 100% operacional com múltiplos fake runners (61/61 testes verdes).
- **Último Checkpoint Imutável:** [`CP-20260826-007`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/checkpoints/CP-20260826-007.md)
- **Último Estado Seguro (Last Known Good):** `CP-20260826-007`
- **Git Branch:** `main`
- **Worktree Status:** CLEAN

---

## 2. Matriz de Adaptadores e Catálogo de Modelos (Seed Ativo)

| Provedor | Modelo Ativo Padrão | Status Catálogo | Classe de Custo | Elegível sob FREE_ONLY? | Nota de Privacidade |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Groq** | `openai/gpt-oss-120b` | `ACTIVE` | `FREE_TIER` | `SIM` | Standard Privacy |
| **Google Gemini** | `gemini-3.7-flash` | `ACTIVE` | `FREE_TIER` | `SIM` | Free tier permite melhoria de produto pelo provedor |
| **OpenAI** | `gpt-4o-mini` | `ACTIVE` | `PAID` | `NÃO` | Bloqueado sob FREE_ONLY |
| **Anthropic** | `claude-3-5-haiku-20241022`| `ACTIVE` | `PROMOTIONAL_CREDIT` | `NÃO` | Permitido apenas sob ALLOW_PROMOTIONAL |
| **Fake Local** | `default-model` | `ACTIVE` | `LOCAL_ZERO_MARGINAL_API_COST` | `SIM` | Air-gapped local |

---

## 3. Status do Trabalho

- **Último Trabalho Concluído:**
  - Missão 06.1: Resolução de model-catalog drift (remoção de `llama-3.3-70b-versatile` e `gemini-2.0-flash`), criação do `ModelCatalog` (`src/idea_evolution/config/catalog.py`, `config/model_catalog.json`), política `FREE_ONLY`, regras de fallback diferenciadas (`EXPERIMENTAL_PINNED` vs `FREE_POOL_OPERATIONAL`), expansão do `iee providers doctor` e aprovação de 61 testes automatizados.
- **Tarefa Ativa Atual:**
  - `TASK-000`: Gate de Governança — Apresentação do relatório da Missão 06.1 e parada mandatória (*STOP*).
- **Próximo Passo Exato:**
  - Configuração da chave de API pelo operador humano no arquivo local `.env` para desbloqueio do primeiro *Real Model Canary* (M05-B) com modelo gratuito ativo (`openai/gpt-oss-120b`).

---

## 4. O Que Explicitamente NÃO Fazer (DO-NOT-DO)
1. ❌ **NÃO** fazer chamadas reais a APIs ou gastar sem autorização/credencial explícita.
2. ❌ **NÃO** permitir fallback silencioso para modelos pagos (`PAID_FALLBACK: FORBIDDEN`).
3. ❌ **NÃO** alterar modelos no meio de experimentos científicos controlados (M05).
4. ❌ **NÃO** clonar ou implementar o runtime complexo do FioOS no IEE.
