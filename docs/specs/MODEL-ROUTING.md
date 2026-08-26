# MODEL-ROUTING.md — Especificação de Roteamento Multi-Modelo por Estágio

> **CASA CANÔNICA DA ESPECIFICAÇÃO DE ROTEAMENTO DE MODELOS (v1.0.0).**

---

## 1. Princípio Arquitetural
- **Functions are not Models:** Estágios cognitivos (`UNDERSTAND`, `ATTACK`, `CRITIQUE`, `REVISION`, `ALTERNATIVES`, `REALITY_CHECK`, `SYNTHESIZE`, `FINAL_REVIEW`) são funções e contratos estritos do kernel, independentes de fornecedores específicos.
- **The Kernel is the Mediator:** Modelos nunca dialogam diretamente entre si ("chat livre"). O IEE controla a ordem, valida esquemas JSON, preserva o estado intermediário e roteia o contexto estritamente necessário para o próximo modelo.
- **Zero Fallback Silencioso (`NO_CROSS_PROVIDER_FALLBACK`):** Se um modelo ou provedor falha, a execução é interrompida com status `FAILED_AT_STAGE` e erro explícito. O sistema nunca substitui silenciosamente um modelo por outro para não contaminar o experimento ou o custo.

---

## 2. Schema de Configuração (`ModelRoutingConfig`)
A configuração é descrita em formato YAML ou JSON estruturado com os seguintes blocos:

```yaml
schema_version: "1.0.0"
description: "Mapeamento lógico de modelos e rotas por estágio"

models:
  <alias_logico>:
    provider: <groq | openai | gemini | anthropic | fake>
    model: <nome_do_modelo>
    credential_env: <NOME_DA_VARIAVEL_DE_AMBIENTE>
    parameters:
      temperature: 0.2

routes:
  <nome_do_estagio>: <alias_logico>

default_model_alias: <alias_logico_padrao>
```

---

## 3. Proveniência Gravada por Estágio
Cada execução de estágio grava deterministicamente:
- `logical_alias`: Alias lógico configurado (ex: `analyst`, `critic`, `synthesizer`).
- `provider`: Provedor real (ex: `groq`, `anthropic`, `openai`, `gemini`, `fake`).
- `model`: Identificador exato do modelo (ex: `llama-3.3-70b-versatile`, `claude-3-5-haiku-20241022`).
- `prompt_id` & `prompt_version`: Arquivo e versão do prompt utilizado.
- `attempt`: Número da tentativa no ciclo de reconstrução (1 ou 2).
- `latency_seconds` e `retry_count`.

---

## 4. Hash Determinístico de Roteamento
Cada arquivo de configuração gera um hash SHA-256 canônico (`routing_config_hash`) gravado em `input.json` e `trace.json`, permitindo comparar runs com precisão forense.
