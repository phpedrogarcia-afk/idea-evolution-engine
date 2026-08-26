# docs/context/CURRENT-STATE.md — Snapshot Operacional Dinâmico

> **ESTE DOCUMENTO É A DECLARAÇÃO OPERACIONAL VIVA DO ESTADO DO REPOSITÓRIO.**
> Atualizado em: 2026-08-26 | Checkpoint: CP-20260826-005

---

## 1. Identificação Operacional

- **Projeto:** Idea Evolution Engine (IEE)
- **Fase Ativa:** FASE 1 — SIMPLE IDEA EVOLUTION LOOP MVP (MOTOR EXECUTÁVEL COMPLETO & PRONTO PARA INFERÊNCIA REAL)
- **Status da Fundação:** `COMPLETE_AND_LOCKED` (`FOUNDATION_READY = TRUE`)
- **Status do Produto:** `SIMPLE IDEA EVOLUTION LOOP` implementado com Condição B e Condição C, CLI, suíte de 38 testes verdes e pacote de comparação experimental.
- **Status da Missão 05:** `PREFLIGHT_AND_SECURITY_SCAN_COMPLETE`
- **Reconciliação do Repositório Remoto:**
  - `DEFAULT_BRANCH`: `main`
  - `REMOTE_REPOSITORY`: `https://github.com/phpedrogarcia-afk/idea-evolution-engine.git`
  - `SECRET_SCAN`: `PASS` (0 credenciais ou segredos rastreados no Git)
- **Status do Executor de Modelos Reais:**
  - `REAL_MODEL_RUN`: `BLOCKED_PROVIDER_CREDENTIAL_OR_COST` (Nenhuma chave `GROQ_API_KEY`, `OPENAI_API_KEY` ou `GEMINI_API_KEY` configurada no ambiente local).
  - `OFFLINE_SIMULATION_RUN`: 100% operacional via `FakeModelRunner` (38/38 testes verdes).
- **Último Checkpoint Imutável:** [`CP-20260826-005`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/checkpoints/CP-20260826-005.md)
- **Último Estado Seguro (Last Known Good):** `CP-20260826-005`
- **Git Branch:** `main`
- **Git Commit:** `48c766b` $\to$ Próximo commit pós-M05
- **Worktree Status:** CLEAN

---

## 2. Status do Trabalho

- **Último Trabalho Concluído:**
  - Missão 04: Implementação completa do Simple Loop MVP, fixtures, experiment packet e 38 testes verdes.
  - Missão 05 (Preflight & Security): Reconciliação do branch `main`, verificação de remote GitHub, varredura de segurança contra vazamento de segredos (`SECRET_SCAN: PASS`), expansão do `NativeModelRunner` para suporte seguro a `.env` (Groq/OpenAI/Gemini).
- **Tarefa Ativa Atual:**
  - `TASK-000`: Gate de Governança — Apresentação do relatório da Missão 05 e instruções seguras para configuração de credencial de provedor real.
- **Próximo Passo Exato (Aguardando Configuração Humana de Credencial):**
  - Configuração da chave de API pelo operador humano via protocolo seguro para desbloqueio do primeiro *Real Model Canary* e execução do experimento A/B/C com inferência real.

---

## 3. Bloqueadores e Contradições Abertas

- **Bloqueadores Ativos:** 
  - `REAL_CANARY = BLOCKED_PROVIDER_CREDENTIAL_OR_COST`: Ausência de chave de API no ambiente local. Conforme regra #7 da Missão 05, o sistema não gasta silenciosamente nem finge determinismo via mocks para responder a qualidade semântica real.
- **Contradições Abertas Registradas:** 0 contradições críticas ([`docs/context/CONTRADICTIONS.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/CONTRADICTIONS.md)).
- **Dúvidas em Aberto Registradas:** 4 questões mapeadas em [`docs/context/OPEN-QUESTIONS.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/OPEN-QUESTIONS.md).

---

## 4. O Que Explicitamente NÃO Fazer (DO-NOT-DO)
1. ❌ **NÃO** usar o `FakeModelRunner` como evidência para responder sobre a qualidade semântica da IA real.
2. ❌ **NÃO** fazer commit de arquivos `.env` ou expor chaves de API nos logs ou no chat.
3. ❌ **NÃO** inventar provedores complexos ou frameworks intermediários (LiteLLM, LangGraph).
4. ❌ **NÃO** alterar os prompts versionados após inspecionar saídas (anti-moving goalposts).
