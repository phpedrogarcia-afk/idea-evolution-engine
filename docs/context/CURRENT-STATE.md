# docs/context/CURRENT-STATE.md — Snapshot Operacional Dinâmico

> **ESTE DOCUMENTO É A DECLARAÇÃO OPERACIONAL VIVA DO ESTADO DO REPOSITÓRIO.**
> Atualizado em: 2026-08-26 | Checkpoint: CP-20260826-006

---

## 1. Identificação Operacional

- **Projeto:** Idea Evolution Engine (IEE)
- **Fase Ativa:** FASE 1 — SIMPLE IDEA EVOLUTION LOOP MVP (MOTOR EXECUTÁVEL MULTI-MODELO PREPARADO OFFLINE)
- **Status da Fundação:** `COMPLETE_AND_LOCKED` (`FOUNDATION_READY = TRUE`)
- **Status do Produto:** `SIMPLE IDEA EVOLUTION LOOP` implementado com Condição B e Condição C, CLI, suíte de 49 testes verdes e camada de roteamento multi-modelo (`ModelRoutingConfig` + `RunnerRouter`).
- **Status da Missão 05:** `REAL_MODEL_CANARY = BLOCKED_PROVIDER_CREDENTIAL_OR_COST` (Incerteza real mantida honestamente bloqueada por ausência de chaves de API).
- **Status da Missão 06:** `MULTI_MODEL_INTEGRATION_READINESS = COMPLETE_OFFLINE` (`MULTI_MODEL_READY_OFFLINE = TRUE`).
- **Reconciliação do Repositório Remoto:**
  - `DEFAULT_BRANCH`: `main`
  - `REMOTE_REPOSITORY`: `https://github.com/phpedrogarcia-afk/idea-evolution-engine.git`
  - `SECRET_SCAN`: `PASS` (0 credenciais ou segredos rastreados no Git)
- **Status do Executor de Modelos Reais:**
  - `REAL_SINGLE_MODEL_EXECUTION`: `BLOCKED_PROVIDER_CREDENTIAL_OR_COST` (Aguardando configuração de API key).
  - `REAL_CROSS_PROVIDER_VALIDATED`: `FALSE`
  - `REAL_MULTI_MODEL_DELIBERATION`: `NOT_EXECUTED`
  - `OFFLINE_SIMULATION_RUN`: 100% operacional com múltiplos fake runners (49/49 testes verdes).
- **Último Checkpoint Imutável:** [`CP-20260826-006`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/checkpoints/CP-20260826-006.md)
- **Último Estado Seguro (Last Known Good):** `CP-20260826-006`
- **Git Branch:** `main`
- **Worktree Status:** CLEAN

---

## 2. Matriz de Adaptadores de Provedor (Provider Capability Matrix)

| Provedor | Adaptador Implementado | Modo Structured Output | Credential Env | Testado Real? |
| :--- | :---: | :--- | :--- | :---: |
| **Groq** | `Sim (NativeModelRunner)` | `native_json_object` | `GROQ_API_KEY` | `NÃO (Aguardando chave)` |
| **OpenAI** | `Sim (NativeModelRunner)` | `native_json_object` | `OPENAI_API_KEY` | `NÃO (Aguardando chave)` |
| **Google Gemini** | `Sim (NativeModelRunner)` | `native_response_mime_type` | `GEMINI_API_KEY` | `NÃO (Aguardando chave)` |
| **Anthropic** | `Sim (NativeModelRunner)` | `prompted_json_validation` | `ANTHROPIC_API_KEY` | `NÃO (Aguardando chave)` |
| **Fake Runners** | `Sim (FakeModelRunner)` | `local_pydantic_mock` | Nenhuma | `SIM (100% offline)` |

---

## 3. Status do Trabalho

- **Último Trabalho Concluído:**
  - Missão 06: Implementação completa da infraestrutura de roteamento multi-modelo por estágio (`src/idea_evolution/config/routing.py`, `src/idea_evolution/providers/router.py`), suporte nativo ao Anthropic, comando `iee providers doctor`, comando `iee routes show`, flag `--dry-run`, exemplos em `config/` e 49 testes automatizados aprovados.
- **Tarefa Ativa Atual:**
  - `TASK-000`: Gate de Governança — Apresentação do relatório da Missão 06 e parada mandatória (*STOP*).
- **Próximo Passo Exato:**
  - Configuração da chave de API pelo operador humano no arquivo local `.env` para desbloqueio do primeiro *Real Model Canary* (M05-B) e, subsequentemente, da primeira deliberação multi-modelo real (M07).

---

## 4. O Que Explicitamente NÃO Fazer (DO-NOT-DO)
1. ❌ **NÃO** fazer chamadas reais a APIs ou gastar sem autorização/credencial explícita.
2. ❌ **NÃO** declarar que multi-modelos conversando livremente é superior antes de experimentos empíricos.
3. ❌ **NÃO** introduzir frameworks de agentes pesados (LangGraph, AutoGen, CrewAI).
4. ❌ **NÃO** permitir fallback silencioso entre provedores (`NO_CROSS_PROVIDER_FALLBACK`).
