"""
src/idea_evolution/providers/nvidia_nim.py
Transport Adapter para NVIDIA NIM Hosted API (https://integrate.api.nvidia.com/v1).

Garante:
1. Zero custo de inferência com verificação estrita de fail-closed (bloqueia endpoints pagos).
2. Preservação exata dos schemas lógicos Pydantic através de guided_json e response_format json_schema.
3. Sanitização absoluta de credenciais (NVIDIA_API_KEY / NGC_API_KEY).
4. Suporte aos parâmetros científicos congelados (model: openai/gpt-oss-120b, temp: 0.3, max_tokens: 2048).
"""

import os
import json
import re
import hashlib
from typing import Type, TypeVar, Optional, Dict, Any, Tuple
from pydantic import BaseModel, ValidationError
from src.idea_evolution.providers.base import ModelRunner, ModelResponse, ModelUsage

T = TypeVar("T", bound=BaseModel)

NVIDIA_HOSTED_BASE_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_MODEL_ID = "openai/gpt-oss-120b"
EXPECTED_INFERENCE_PRICE = 0.0


def sanitize_nvidia_credential(text: str) -> str:
    """Sanitiza chaves de API da NVIDIA (nvapi-...) e tokens Bearer de strings e logs."""
    if not text:
        return ""
    sanitized = re.sub(r"nvapi-[A-Za-z0-9_\-]+", "nvapi-***", text)
    sanitized = re.sub(r"Bearer\s+[A-Za-z0-9_\.\-]+", "Bearer ***", sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r"api[_\-]?key['\":\s=]+[A-Za-z0-9_\-]+", "api_key=***", sanitized, flags=re.IGNORECASE)
    return sanitized


def get_nvidia_api_key() -> Optional[str]:
    """Recupera a chave de API da NVIDIA do ambiente sem nunca expor ou registrar seu valor."""
    return os.environ.get("NVIDIA_API_KEY") or os.environ.get("NGC_API_KEY")


def is_nvidia_key_present() -> bool:
    """Retorna True se NVIDIA_API_KEY ou NGC_API_KEY estiver configurada no ambiente."""
    return bool(get_nvidia_api_key())


class NvidiaNimTransportBuilder:
    """Construtor determinístico de requisições de transporte para NVIDIA NIM."""

    def __init__(
        self,
        base_url: str = NVIDIA_HOSTED_BASE_URL,
        model: str = NVIDIA_MODEL_ID,
    ):
        if base_url != NVIDIA_HOSTED_BASE_URL:
            raise ValueError(f"FAIL_CLOSED_PAID_ROUTING_GUARD: Base URL must be {NVIDIA_HOSTED_BASE_URL}, got {base_url}")
        if model != NVIDIA_MODEL_ID:
            raise ValueError(f"FAIL_CLOSED_MODEL_GUARD: Model must be {NVIDIA_MODEL_ID}, got {model}")

        self.base_url = base_url
        self.model = model

    def build_request_payload(
        self,
        messages: list,
        schema_cls: Optional[Type[BaseModel]] = None,
        temperature: float = 0.3,
        max_tokens: int = 2048,
        top_p: float = 0.7,
        use_guided_json: bool = True,
        use_response_format: bool = True,
    ) -> Dict[str, Any]:
        """
        Constrói o payload JSON exato para o endpoint /chat/completions da NVIDIA NIM.
        Preserva 100% o schema lógico Pydantic através de guided_json e/ou response_format.
        """
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "stream": False,
        }

        if schema_cls is not None:
            raw_schema = schema_cls.model_json_schema()
            schema_name = getattr(schema_cls, "__name__", "OutputSchema")

            # Envelope guided_json recomendado pelo NVIDIA NIM (xgrammar)
            if use_guided_json:
                payload["guided_json"] = raw_schema
                payload["extra_body"] = {
                    "nvext": {
                        "guided_json": raw_schema
                    }
                }

            # Envelope padrão OpenAI json_schema com strict=true
            if use_response_format:
                payload["response_format"] = {
                    "type": "json_schema",
                    "json_schema": {
                        "name": schema_name,
                        "strict": True,
                        "schema": raw_schema,
                    }
                }

        return payload

    def compute_sanitized_payload_sha256(self, payload: Dict[str, Any]) -> str:
        """Gera hash SHA-256 canônico determinístico do payload de transporte."""
        norm_json = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(norm_json.encode("utf-8")).hexdigest()

    def build_headers(self, api_key: Optional[str] = None) -> Dict[str, str]:
        """Constrói os cabeçalhos HTTP necessários para o NVIDIA NIM."""
        key = api_key or get_nvidia_api_key()
        if not key:
            raise RuntimeError("NVIDIA_API_KEY_ABSENT: Chave de API da NVIDIA não configurada no ambiente.")
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {key}",
            "User-Agent": "IdeaEvolutionEngine-M05.5R2/1.0",
        }


class NvidiaNimRunner(ModelRunner):
    """
    Executor ModelRunner compatível com a arquitetura IEE para NVIDIA NIM.
    """

    def __init__(
        self,
        model_name: str = NVIDIA_MODEL_ID,
        temperature: float = 0.3,
        max_output_tokens: int = 2048,
        base_url: str = NVIDIA_HOSTED_BASE_URL,
        transport_callable: Optional[Any] = None,
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.builder = NvidiaNimTransportBuilder(base_url=base_url, model=model_name)
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
        """Executa a chamada contra o endpoint da NVIDIA NIM."""
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
            # Em testes ou harness controlado, delegar ao transport
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
                        provider="nvidia_nim",
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
                provider="nvidia_nim",
                model=self.model_name,
                usage=ModelUsage(
                    prompt_tokens=usage_dict.get("prompt_tokens", 0),
                    completion_tokens=usage_dict.get("completion_tokens", 0),
                    total_tokens=usage_dict.get("total_tokens", 0),
                ),
            )

        # Sem transport mockado: verificar chave antes de chamada real
        if not is_nvidia_key_present():
            raise RuntimeError("NVIDIA_API_KEY_ABSENT: Chave NVIDIA_API_KEY não configurada no ambiente.")

        # Importar urllib e despachar
        import urllib.request
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
                    provider="nvidia_nim",
                    model=self.model_name,
                    usage=ModelUsage(
                        prompt_tokens=usage_info.get("prompt_tokens", 0),
                        completion_tokens=usage_info.get("completion_tokens", 0),
                        total_tokens=usage_info.get("total_tokens", 0),
                    ),
                )
        except Exception as e:
            sanitized = sanitize_nvidia_credential(str(e))
            return ModelResponse(
                raw_text="",
                parsed=None,
                provider="nvidia_nim",
                model=self.model_name,
                error=f"NVIDIA_TRANSPORT_ERROR: {sanitized}",
            )
