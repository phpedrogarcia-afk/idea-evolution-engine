# docs/experiments/M04-DONOR-HARVEST-SPEC.md — Especificação de Colheita de Doadores para a Missão 04

> **PREFLIGHT DECISÓRIO OBRIGATÓRIO ANTES DA IMPLEMENTAÇÃO DA MISSÃO 04.**
> *Resolve os 5 gaps centrais sem criar dependências desnecessárias nem adiar a construção.*

---

## 1. As 5 Decisões Pré-Construção da Missão 04

### 1.1 Estratégia de Structured Output (Gap A)
- **Doador Consultado:** PydanticAI / Instructor.
- **Mecanismo Colhido:** Validação estrita via Pydantic v2 com injeção de JSON Schema e no máximo 1 tentativa de correção semântica (*schema repair loop*).
- **Decisão de Engenharia:** `ADAPT` via camada fina nativa em Python (`src/idea_evolution/stages/contracts.py`). Não instalar frameworks complexos intermediários para evitar dependências transitivas e manter controle total sobre raw outputs.

### 1.2 Estratégia de Abstração de Provedores (Gap B)
- **Doador Consultado:** LiteLLM / Base Runner Patterns.
- **Mecanismo Colhido:** Interface desacoplada `ModelRunner` (`generate(stage_contract, context, prompt)`), suportando:
  - `FakeModelRunner`: Execução 100% determinística e offline para testes unitários, integração e simulação rápida.
  - `NativeModelRunner`: Integração HTTP/SDK nativa (Groq/OpenAI/Custom) com preservação de telemetria e saída bruta.
- **Decisão de Engenharia:** `ADAPT` simples. Zero frameworks de marketplace de modelos.

### 1.3 Topologias de Crítica e Revisão para Teste Experimental (Gap C)
- **Doador Primário:** MultiAgent Research Ideator & DCI.
- **Hipótese de Design M04-H1:**  
  > *"Depth of critique–revision is likely more valuable for the initial IEE than breadth of parallel critics."*
- **Topologias a Comparar Experimentalmente:**
  - **Condição A (Baseline):** Prompt único genérico de refinamento (*"Analyze and refine this idea"*).
  - **Condição B (Simple Loop Fixo):** `UNDERSTAND` $\to$ `ATTACK` $\to$ `ALTERNATIVES` $\to$ `REALITY_CHECK` $\to$ `SYNTHESIZE` $\to$ `FINAL_REVIEW`.
  - **Condição C (Iterative Critique-Revision):**  
    `UNDERSTAND` $\to$ `CRITIQUE_1 (Logical/Assumptions)` $\to$ `REVISION` $\to$ `CRITIQUE_2 (Feasibility/Real-World)` $\to$ `REVISION` $\to$ `REALITY_CHECK` $\to$ `SYNTHESIZE` $\to$ `FINAL_REVIEW`.

### 1.4 Estratégia de Avaliação e Red-Teaming (Gap D)
- **Doador Consultado:** Promptfoo.
- **Mecanismo Colhido:** Fixtures padronizadas de teste (`fixtures/`), métricas determinísticas e geração de pacote de comparação mascarado (`comparison-packet.md`) para avaliação humana cega.

### 1.5 Política de Dependências (Gap E)
- **Dependências Autorizadas:** `pydantic` (já instalada), `pytest` (já instalada), biblioteca padrão do Python (`json`, `pathlib`, `argparse`, `dataclasses`, `typing`), e `httpx`/`groq` (já instaladas para quando houver credencial).
- **Dependências Rejeitadas:** LangGraph, AutoGen, CrewAI, DSPy, Instructor (framework externo), LiteLLM (framework externo).

---

## 2. Condição de Parada do Preflight
Com as 5 decisões acima resolvidas e congeladas, o preflight está concluído:
$$\text{DONOR PREFLIGHT} \longrightarrow \text{FREEZE} \longrightarrow \mathbf{BUILD}$$
