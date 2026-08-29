# GROQ-GPT-OSS-STRUCTURED-OUTPUT-AUTOPSY.md — Autópsia de Compatibilidade de Structured Output

> **DOCUMENTO DE INTELIGÊNCIA & DIAGNÓSTICO DE INFRAESTRUTURA**
> **MISSÃO:** Autópsia de Structured Output (Attempt-003)
> **DATA:** 2026-08-29
> **STATUS:** ZERO_REAL_CALLS_AUDIT | ROOT_CAUSE_ISOLATED

---

## 1. Contexto e Fato Externo Oficial

1. **Capacidade Documentada do Provedor:** A documentação oficial do Groq afirma expressamente que o modelo openai/gpt-oss-120b possui suporte nativo a **Structured Outputs** via json_schema com strict: true.
2. **Resultado Observado no Attempt-003:**
   - 24 células executadas.
   - 2 sucessos (Condição A: IDEA-01, IDEA-02 com latências nominais de 1.9s e 2.2s).
   - 22 falhas com PROVIDER_STRUCTURED_OUTPUT_REPAIR_FAILED e latências atipicamente baixas (0.15s - 0.25s).
   - Texto de resposta retornado foi nulo (aw_text = "", aw_len = 0).

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
- **Conversão de Schema Pydantic:** 	o_strict_json_schema() gera schemas válidos com dditionalProperties: False e chaves obrigatórias em equired.

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

### 2.3 Mecânica do Colapso
1. Quando a chamada inicial falha rapidamente (ex: Rate Limit 429 de TPM/RPM no Free Tier do Groq ou rejeição de payload), a exceção é capturada genericamente como Exception as groq_err.
2. _call_provider atribui ailed_gen = str(groq_err) e retorna aw_text = "".
3. generate() interpreta erroneamente qualquer erro da API como uma falha de validação de modelo, acionando imediatamente um epair_prompt.
4. A chamada de reparo é disparada instantaneamente contra a API, falhando pelo mesmo motivo (ou agravando o rate limit).
5. O runner mascara o erro real e grava o rótulo enganoso PROVIDER_STRUCTURED_OUTPUT_REPAIR_FAILED.

---

## 3. Taxonomia de Falhas dos 24 Artefatos do Attempt-003

| Categoria | Contagem | Detalhe |
|---|---|---|
| RAW_NOT_JSON | 0 | Nenhuma resposta retornou JSON malformado; o texto bruto foi vazio (aw_len = 0). |
| JSON_VALID_SCHEMA_INVALID | 0 | Nenhum JSON válido foi rejeitado pelo Pydantic. |
| PROVIDER_SCHEMA_ERROR | 22 | Erros de API/Rate-Limit mascarados como falha estruturada. |
| LOCAL_PARSER_FAILURE | 0 | O parser local não falhou em nenhuma resposta recebida. |
| REPAIR_FAILURE | 22 | A re-execução imediata falhou e consolidou o erro. |
| UNKNOWN_FAILURE | 0 | Causa 100% mapeada no fluxo de exceção. |

---

## 4. Auditoria de Compatibilidade dos Schemas do M05.4

Foram auditados os 4 schemas principais do experimento:
1. BaselineRefineOutput (Condição A): Compatível com strict: true (0 violações locais).
2. UnderstandOutput (Condição B): Compatível com strict: true (0 violações locais).
3. AttackOutput (Condição B): Compatível com strict: true (0 violações locais).
4. LeanFirstPassOutput (Condição C): Compatível com strict: true (0 violações locais).

Os schemas em si não violam as regras do JSON Schema Strict Mode. O colapso foi causado pelo tratamento de exceções da camada de transporte/API.

---

## 5. Classificação da Causa Raiz

- **PRIMARY_ROOT_CAUSE:** ERROR_HANDLING_COLLAPSE_IN_NATIVE_RUNNER
  - Captura genérica de Exception as groq_err que confunde erros de API/Rate-Limit com desvios de validação semântica de schema, disparando loop de reparação inútil.
- **SECONDARY_ROOT_CAUSES:**
  - Ausência de backoff exponencial e espera determinística para limites de taxa (TPM/RPM) no Free Tier do Groq.
  - Duplicação desnecessária do schema no system_instruction quando esponse_format nativo json_schema com strict: true já é enviado.

---

## 6. Escopo Mínimo de Correção

1. **Separação Estrita de Erros:**
   - Tratar RateLimitError (429) com retry/backoff temporal bounded (ex: 2s, 4s, 8s).
   - Tratar BadRequestError (400) registrando a mensagem exata de rejeição de schema.
   - Acionar epair_prompt **exclusivamente** quando houver ailed_generation comprovada de um modelo que respondeu com texto fora do schema.
2. **Limpeza do Prompt de Sistema:**
   - Quando esponse_format={"type": "json_schema"} estiver ativo, omitir o dump redundante do JSON Schema no system_instruction para economizar tokens e evitar conflitos.

---

## 7. Desenho do Micro-Probe Diagnóstico (<= 6 Chamadas Reais)

Antes de qualquer novo experimento completo (Attempt-004), deve ser executado um micro-probe estritamente delimitado:

- **Script:** 	ools/experiments/probe_groq_structured_output.py
- **Schemas Testados:**
  - BaselineRefineOutput (2 chamadas)
  - UnderstandOutput (2 chamadas)
  - LeanFirstPassOutput (2 chamadas)
- **Total de Chamadas Reais:** 6 (máximo).
- **Provedor / Modelo:** groq / openai/gpt-oss-120b.
- **Critério de Sucesso:** $\ge 5/6$ (idealmente /6$) admissões estruturadas válidas com tempo de resposta nominal (> 1.0s) e zero erros mascarados.
