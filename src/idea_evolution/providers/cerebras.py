"""
src/idea_evolution/providers/cerebras.py
Adapter de transporte e executor ModelRunner para Cerebras Cloud Inference.

Invariantes estritas:
1. Endpoint fixo e gratuito: https://api.cerebras.ai/v1
2. Modelo científico alvo: openai/gpt-oss-120b
3. Identificador de transporte: gpt-oss-120b (TRANSPORT_ALIAS_ONLY, sem troca semântica)
4. Custo estrito: ZERO (fail-closed contra qualquer rota externa ou tarifada)
5. Structured Outputs: response_format com json_schema e strict=True
6. Sem retries ocultos: max_retries = 0
7. Sanitização completa de credenciais (CEREBRAS_API_KEY / csk-...)
8. Fail-closed se a credencial não estiver configurada no ambiente.
"""

from __future__ import annotations

import os
import sys
import re
import json
import hashlib
from typing import Any, Dict, List, Mapping, Optional, Type, TypeVar
import urllib.request
import urllib.error

from pydantic import BaseModel, ValidationError
from src.idea_evolution.providers.base import ModelRunner, ModelResponse, ModelUsage
from src.idea_evolution.providers.native import to_strict_json_schema

T = TypeVar("T", bound=BaseModel)

CEREBRAS_HOSTED_BASE_URL = "https://api.cerebras.ai/v1"
CEREBRAS_TRANSPORT_MODEL_ID = "gpt-oss-120b"
SCIENTIFIC_MODEL_ID = "openai/gpt-oss-120b"
EXPECTED_INFERENCE_PRICE = 0.0

MAX_SCHEMA_CHARS = 5000
MAX_NESTING_DEPTH = 10
MAX_OBJECT_PROPERTIES = 500
MAX_ENUM_VALUES = 500
UNSUPPORTED_KEYWORDS = frozenset({"pattern", "format", "minItems", "maxItems", "$anchor"})


def sanitize_cerebras_credential(text: str) -> str:
    """Sanitiza mensagens de erro e payloads, mascarando chaves da Cerebras e Bearer tokens."""
    if not text:
        return ""
    sanitized = re.sub(r"csk-[A-Za-z0-9_\-]+", "csk-***", text)
    sanitized = re.sub(r"Bearer\s+[A-Za-z0-9_\.\-]+", "Bearer ***", sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r"api[_\-]?key['\":\s=]+[A-Za-z0-9_\-]+", "api_key=***", sanitized, flags=re.IGNORECASE)
    return sanitized


def get_cerebras_api_key() -> Optional[str]:
    """Recupera a chave da Cerebras da variável de ambiente CEREBRAS_API_KEY ou do registro do usuário no Windows."""
    key = os.environ.get("CEREBRAS_API_KEY")
    if key and len(key.strip()) > 0:
        return key.strip()
    if sys.platform == "win32":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as k:
                val, _ = winreg.QueryValueEx(k, "CEREBRAS_API_KEY")
                if val and len(str(val).strip()) > 0:
                    os.environ["CEREBRAS_API_KEY"] = str(val).strip()
                    return str(val).strip()
        except Exception:
            pass
    return None


def is_cerebras_key_present() -> bool:
    """Verifica se a credencial da Cerebras está presente no ambiente."""
    key = get_cerebras_api_key()
    return bool(key and len(key.strip()) > 0)


def validate_cerebras_strict_schema_compatibility(schema: Dict[str, Any], depth: int = 1) -> Tuple[bool, List[str]]:
    """
    Valida se um schema JSON está em total conformidade com as restrições de strict mode da Cerebras:
    - Raiz deve ser type object
    - additionalProperties: false em todos os objetos
    - Comprimento serializado <= 5000 chars
    - Profundidade de aninhamento <= 10
    - Quantidade de propriedades <= 500
    - Ausência de palavras-chave não suportadas (pattern, format, minItems, etc.)
    """
    errors: List[str] = []
    s_json = json.dumps(schema, separators=(",", ":"))
    if len(s_json) > MAX_SCHEMA_CHARS:
        errors.append(f"SCHEMA_LENGTH_EXCEEDED: {len(s_json)} > {MAX_SCHEMA_CHARS}")

    if schema.get("type") != "object":
        errors.append("ROOT_MUST_BE_OBJECT")

    def _traverse(node: Any, current_depth: int):
        if current_depth > MAX_NESTING_DEPTH:
            errors.append(f"NESTING_DEPTH_EXCEEDED: {current_depth} > {MAX_NESTING_DEPTH}")
        if isinstance(node, dict):
            for bad_kw in UNSUPPORTED_KEYWORDS:
                if bad_kw in node:
                    errors.append(f"UNSUPPORTED_KEYWORD: {bad_kw}")
            if node.get("type") == "object":
                if node.get("additionalProperties") is not False:
                    errors.append("MISSING_ADDITIONAL_PROPERTIES_FALSE")
                props = node.get("properties", {})
                if len(props) > MAX_OBJECT_PROPERTIES:
                    errors.append(f"TOO_MANY_PROPERTIES: {len(props)} > {MAX_OBJECT_PROPERTIES}")
                for pk, pv in props.items():
                    _traverse(pv, current_depth + 1)
            elif node.get("type") == "array":
                _traverse(node.get("items", {}), current_depth + 1)
            for def_k in ["$defs", "definitions"]:
                if def_k in node:
                    for dk, dv in node[def_k].items():
                        _traverse(dv, current_depth + 1)

    _traverse(schema, depth)
    return len(errors) == 0, errors


class CerebrasTransportBuilder:
    """
    Construtor de payloads e requisições HTTP para a API da Cerebras Cloud.
    Garante mapeamento de alias de transporte para gpt-oss-120b e preservação
    exata dos schemas Pydantic lógicos sob strict JSON Schema.
    """

    def __init__(
        self,
        base_url: str = CEREBRAS_HOSTED_BASE_URL,
        scientific_model: str = SCIENTIFIC_MODEL_ID,
        transport_model: str = CEREBRAS_TRANSPORT_MODEL_ID,
    ):
        if base_url != CEREBRAS_HOSTED_BASE_URL:
            raise RuntimeError(f"FAIL_CLOSED_PAID_ROUTING_GUARD: Tentativa de desvio de base_url para '{base_url}'")
        if transport_model != CEREBRAS_TRANSPORT_MODEL_ID:
            raise RuntimeError(f"FAIL_CLOSED_MODEL_GUARD: Modelo de transporte '{transport_model}' inválido")
        self.base_url = base_url
        self.scientific_model = scientific_model
        self.transport_model = transport_model

    def build_request_payload(
        self,
        messages: List[Dict[str, str]],
        schema_cls: Optional[Type[BaseModel]] = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> Dict[str, Any]:
        """Constrói o payload JSON estrito compatível com a API da Cerebras."""
        payload: Dict[str, Any] = {
            "model": self.transport_model,
            "messages": messages,
            "temperature": temperature,
            "max_completion_tokens": max_tokens,
            "stream": False,
        }

        if schema_cls is not None:
            strict_schema = to_strict_json_schema(schema_cls)
            is_compat, errs = validate_cerebras_strict_schema_compatibility(strict_schema)
            if not is_compat:
                raise ValueError(f"CEREBRAS_STRICT_SCHEMA_INCOMPATIBLE: {errs}")

            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": schema_cls.__name__,
                    "strict": True,
                    "schema": strict_schema,
                },
            }

        return payload

    def build_headers(self) -> Dict[str, str]:
        """Gera cabeçalhos HTTP necessários com autenticação Bearer da Cerebras."""
        key = get_cerebras_api_key()
        if not key:
            raise RuntimeError("CEREBRAS_API_KEY_ABSENT: Chave CEREBRAS_API_KEY não configurada no ambiente.")
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {key.strip()}",
            "User-Agent": "IdeaEvolutionEngine-M05.5R2-Cerebras/1.0",
        }

    def compute_sanitized_payload_sha256(self, payload: Dict[str, Any]) -> str:
        """Calcula o hash canônico do payload sanitizado (sem expor segredos)."""
        clean_copy = dict(payload)
        canonical = json.dumps(clean_copy, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class CerebrasRunner(ModelRunner):
    """
    Executor ModelRunner compatível com a arquitetura IEE para Cerebras Cloud.
    Opera com max_retries = 0 (sem retries ocultos de SDK) e guarda de custo zero.
    """

    def __init__(
        self,
        model_name: str = SCIENTIFIC_MODEL_ID,
        temperature: float = 0.3,
        max_output_tokens: int = 4096,
        base_url: str = CEREBRAS_HOSTED_BASE_URL,
        transport_callable: Optional[Any] = None,
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.base_url = base_url
        self.builder = CerebrasTransportBuilder(
            base_url=base_url,
            scientific_model=model_name,
            transport_model=CEREBRAS_TRANSPORT_MODEL_ID,
        )
        self.transport = transport_callable

    def generate(
        self,
        prompt_text: str,
        output_schema: Optional[Type[T]] = None,
        stage_name: Optional[str] = None,
        model_name: Optional[str] = None,
        max_repairs: int = 1,
        system_prompt: Optional[str] = None,
    ) -> ModelResponse:
        """Executa a chamada contra o endpoint da Cerebras Cloud com max_retries=0."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt_text})

        payload = self.builder.build_request_payload(
            messages=messages,
            schema_cls=output_schema,
            temperature=self.temperature,
            max_tokens=self.max_output_tokens,
        )

        if self.transport:
            raw_result = self.transport(payload)
            content = raw_result.get("content", "")
            usage_dict = raw_result.get("usage", {})
            parsed = None
            if output_schema:
                try:
                    parsed = output_schema.model_validate_json(content)
                except ValidationError as ve:
                    return ModelResponse(
                        raw_text=content,
                        parsed=None,
                        provider="cerebras",
                        model=self.model_name,
                        usage=ModelUsage(
                            prompt_tokens=usage_dict.get("prompt_tokens", 0),
                            completion_tokens=usage_dict.get("completion_tokens", 0),
                            total_tokens=usage_dict.get("total_tokens", 0),
                        ),
                        error=f"VALIDATION_ERROR: {str(ve)}",
                    )

            return ModelResponse(
                raw_text=content,
                parsed=parsed,
                provider="cerebras",
                model=self.model_name,
                usage=ModelUsage(
                    prompt_tokens=usage_dict.get("prompt_tokens", 0),
                    completion_tokens=usage_dict.get("completion_tokens", 0),
                    total_tokens=usage_dict.get("total_tokens", 0),
                ),
            )

        # Sem transport mockado: verificar chave antes de chamada real
        if not is_cerebras_key_present():
            raise RuntimeError("CEREBRAS_API_KEY_ABSENT: Chave CEREBRAS_API_KEY não configurada no ambiente.")

        headers = self.builder.build_headers()
        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.builder.base_url}/chat/completions",
            data=req_data,
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                resp_bytes = resp.read()
                resp_json = json.loads(resp_bytes.decode("utf-8"))
                choice = resp_json.get("choices", [{}])[0]
                message = choice.get("message", {})
                content = message.get("content", "")
                usage_info = resp_json.get("usage", {})

                parsed_data = None
                if output_schema:
                    parsed_data = output_schema.model_validate_json(content)

                return ModelResponse(
                    raw_text=content,
                    parsed=parsed_data,
                    provider="cerebras",
                    model=self.model_name,
                    usage=ModelUsage(
                        prompt_tokens=usage_info.get("prompt_tokens", 0),
                        completion_tokens=usage_info.get("completion_tokens", 0),
                        total_tokens=usage_info.get("total_tokens", 0),
                    ),
                )
        except Exception as e:
            sanitized = sanitize_cerebras_credential(str(e))
            return ModelResponse(
                raw_text="",
                parsed=None,
                provider="cerebras",
                model=self.model_name,
                error=f"CEREBRAS_TRANSPORT_ERROR: {sanitized}",
            )
