# GROQ-GPT-OSS-STRUCTURED-OUTPUT-AUTOPSY.md — Autópsia de Compatibilidade de Structured Output

> **DOCUMENTO DE INTELIGÊNCIA & DIAGNÓSTICO DE INFRAESTRUTURA**
> **MISSÃO:** Autópsia de Structured Output (Attempt-003)
> **DATA:** 2026-08-29 (Atualizado com correção epistêmica)
> **STATUS:** ZERO_REAL_CALLS_AUDIT | ROOT_CAUSE_ISOLATED

---

## 1. Contexto e Fato Externo Oficial

1. **Capacidade Documentada do Provedor:** A documentação oficial do Groq afirma expressamente que o modelo openai/gpt-oss-120b possui suporte nativo a **Structured Outputs** via json_schema com strict: true.
2. **Resultado Observado no Attempt-003:**
   - 24 células executadas.
   - 2 sucessos (Condição A: IDEA-01, IDEA-02 com latências nominais de 1.9s e 2.2s).
   - 22 falhas com PROVIDER_STRUCTURED_OUTPUT_REPAIR_FAILED e latências atipicamente baixas (0.15s - 0.25s).
   - Texto de resposta retornado foi nulo (
aw_text = "",
aw_len = 0).

---

## 2. Auditoria da Implementação do NativeModelRunner

A inspeção detalhada de src/idea_evolution/providers/native.py revelou:

### 2.1 Requisição Enviada ao Groq
- **API Surface:** Groq Python SDK client.chat.completions.create.
- **Response Format:**
  `python
  response_format = {
      "type": "json_schema",
      "json_schema": {
          "name": f"{stage_name.lower()}_output",
          "strict": True,
          "schema": strict_schema,
      },
  }
  `
- **Conversão de Schema Pydantic:** 	o_strict_json_schema() gera schemas válidos com dditionalProperties: False e chaves obrigatórias em
equired.

### 2.2 Falha Estrutural no Tratamento de Erros e Pipeline de Reparação
Em NativeModelRunner._call_provider() (linhas 367-374):
`python
except Exception as groq_err:
    failed_gen = None
    if hasattr(groq_err, "body") and isinstance(groq_err.body, dict):
        err_info = groq_err.body.get("error", {})
        failed_gen = err_info.get("failed_generation")
    return "", ModelUsage(), (failed_gen or str(groq_err))
`
E em NativeModelRunner.generate() (linhas 209-249):
`python
if failed_gen and not raw_text:
    if max_repairs > 0:
        # Envia chamada de reparação imediata (repair_prompt) sem backoff!
        repair_raw, repair_usage, repair_failed = self._call_provider(...)
        if not repair_raw:
            return ModelResponse(..., error="PROVIDER_STRUCTURED_OUTPUT_REPAIR_FAILED")
`

### 2.3 Mecânica do Colapso (Fatos Comprovados vs Hipóteses)
1. **FATO COMPROVADO:** O runner capturou genericamente qualquer Exception as groq_err, transformou o erro em string (
ailed_gen = str(groq_err)), apagou o status code HTTP / tipo da exceção e tratou a exceção como se fosse uma saída textual rejeitada por schema.
2. **FATO COMPROVADO:** generate() acionou imediatamente uma chamada de reparo semântico (
epair_prompt), que também falhou e foi mascarada sob o rótulo PROVIDER_STRUCTURED_OUTPUT_REPAIR_FAILED.
3. **STATUS DO ERRO UPSTREAM:** UPSTREAM_HTTP_STATUS = UNKNOWN_FROM_ATTEMPT_003_EVIDENCE (apagado pelo runner histórico).
4. **STATUS DA HIPÓTESE 429:** RATE_LIMIT_429 = PLAUSIBLE_BUT_NOT_PROVEN (não foi medido nem registrado pelo runner histórico).

---

## 3. Taxonomia de Falhas dos 24 Artefatos do Attempt-003

| Categoria | Contagem | Detalhe |
|---|---|---|
| RAW_NOT_JSON | 0 | Nenhuma resposta retornou JSON malformado; o texto bruto foi vazio (
aw_len = 0). |
| JSON_VALID_SCHEMA_INVALID | 0 | Nenhum JSON válido foi rejeitado pelo Pydantic. |
| PROVIDER_API_EXCEPTION_MASKED_BY_RUNNER | 22 | Exceções de API do provedor mascaradas como falha de schema pelo runner. |
| LOCAL_PARSER_FAILURE | 0 | O parser local não falhou em nenhuma resposta recebida. |
| REPAIR_FAILURE | 22 | A re-execução imediata de reparo falhou e consolidou o erro. |
| UNKNOWN_FAILURE | 0 | Fluxo de erro 100% mapeado no código. |

---

## 4. Auditoria de Compatibilidade dos Schemas do M05.4

Foram auditados os 4 schemas principais do experimento:
1. BaselineRefineOutput (Condição A): Compatível com strict: true (0 violações locais).
2. UnderstandOutput (Condição B): Compatível com strict: true (0 violações locais).
3. AttackOutput (Condição B): Compatível com strict: true (0 violações locais).
4. LeanFirstPassOutput (Condição C): Compatível com strict: true (0 violações locais).

Os schemas em si não violam as regras do JSON Schema Strict Mode. O colapso foi causado pela perda de observabilidade e classificação de erros no adaptador do provedor.

---

## 5. Classificação da Causa Raiz

- **PRIMARY_ROOT_CAUSE:** ERROR_HANDLING_COLLAPSE_IN_NATIVE_RUNNER
  - Captura genérica de Exception as groq_err que confunde erros de API/transporte com desvios de validação semântica de schema, disparando loop de reparação inútil e apagando a evidência do erro HTTP original.
- **SECONDARY_ROOT_CAUSES:**
  - Ausência de separação explícita entre retries de transporte (429/5xx) e reparação semântica de output.
  - Duplicação do schema no system_instruction (P2_EFFICIENCY_CANDIDATE).

---

## 6. Escopo Mínimo de Correção

1. **Estrutura Tipada de Erro:**
   - Criar ProviderErrorDetails preservando http_status, rror_type, rror_code, is_rate_limit, is_transient,
etry_after_seconds.
   -
ailed_generation é preenchido **estritamente** quando fornecido pelo corpo da resposta do provedor.
2. **Separação de Retries de Transporte vs Reparo Semântico:**
   - Erros 429/5xx recebem retries de transporte limitados com backoff / respeito a
etry-after.
   -
epair_prompt só é chamado quando houve geração de texto real pelo modelo fora do schema.
3. **Manutenção do Prompt:**
   - Manter prompt intacto nesta etapa (DUPLICATE_SCHEMA_PROMPT_CHANGED = NO).

---

## 7. Desenho do Micro-Probe Diagnóstico (<= 6 Chamadas Reais)

- **Script:** 	ools/experiments/probe_groq_structured_output.py
- **Schemas Testados:**
  - BaselineRefineOutput (1 chamada inicial, até 2)
  - UnderstandOutput (1 chamada inicial, até 2)
  - LeanFirstPassOutput (1 chamada inicial, até 2)
- **Orçamento Adaptativo:** 3 chamadas iniciais. Se todas passarem: STOP (3 chamadas).
- **Provedor / Modelo:** groq / openai/gpt-oss-120b.
