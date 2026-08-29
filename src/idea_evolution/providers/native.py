"""
src/idea_evolution/providers/native.py
Executor Nativo de Modelos via SDK/HTTP (Groq, OpenAI, Gemini, Anthropic) com suporte a Groq Strict Mode, preservação de raw output / failed_generation e bounded repair.
"""

from dataclasses import dataclass
from typing import Type, TypeVar, Optional, Dict, Any, Tuple
import os
import time
import json
import re
from pathlib import Path
from pydantic import BaseModel, ValidationError
from src.idea_evolution.providers.base import ModelRunner, ModelResponse, ModelUsage

T = TypeVar("T", bound=BaseModel)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent


@dataclass
class ProviderErrorDetails:
    """Representação tipada e sanitizada de erros do provedor LLM."""
    provider: str
    http_status: Optional[int] = None
    error_type: str = "UNKNOWN_PROVIDER_ERROR"
    error_code: Optional[str] = None
    message_sanitized: str = ""
    failed_generation: Optional[str] = None
    retry_after_seconds: Optional[float] = None
    is_rate_limit: bool = False
    is_transient: bool = False
    is_schema_generation_failure: bool = False
    transport_attempts: int = 1
    transport_retries: int = 0


def sanitize_error_message(msg: str) -> str:
    """Remove credenciais, chaves de API e tokens Bearer de mensagens de erro."""
    if not msg:
        return ""
    # Mascarar chaves groq (gsk_...), bearer tokens, ou hexadecimais longos
    sanitized = re.sub(r"gsk_[A-Za-z0-9_\-]+", "gsk_***", msg)
    sanitized = re.sub(r"Bearer\s+[A-Za-z0-9_\.\-]+", "Bearer ***", sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r"api[_\-]?key['\":\s=]+[A-Za-z0-9_\-]+", "api_key=***", sanitized, flags=re.IGNORECASE)
    return sanitized


def parse_provider_exception(exc: Exception, provider: str = "groq", attempts: int = 1, retries: int = 0) -> ProviderErrorDetails:
    """Extrai campos tipados de uma exceção do SDK do Groq ou provedores HTTP."""
    raw_msg = str(exc)
    sanitized_msg = sanitize_error_message(raw_msg)

    http_status: Optional[int] = None
    error_code: Optional[str] = None
    error_type = "UNKNOWN_PROVIDER_ERROR"
    failed_gen: Optional[str] = None
    retry_after: Optional[float] = None
    is_rate_limit = False
    is_transient = False
    is_schema_gen_fail = False

    # Inspecionar atributos do SDK do Groq / OpenAI / httpx
    if hasattr(exc, "status_code") and isinstance(exc.status_code, int):
        http_status = exc.status_code
    elif hasattr(exc, "response") and hasattr(exc.response, "status_code"):
        http_status = exc.response.status_code

    # Inspecionar corpo da resposta JSON de erro
    body = getattr(exc, "body", None)
    if isinstance(body, dict):
        err_info = body.get("error", {})
        if isinstance(err_info, dict):
            error_code = err_info.get("code")
            # failed_generation genuíno da API (quando o modelo gerou algo que violou strict schema)
            raw_fg = err_info.get("failed_generation")
            if raw_fg and isinstance(raw_fg, str) and raw_fg.strip():
                failed_gen = raw_fg
                is_schema_gen_fail = True

    # Inspecionar headers para retry-after
    resp = getattr(exc, "response", None)
    if resp and hasattr(resp, "headers") and resp.headers:
        ra = resp.headers.get("retry-after") or resp.headers.get("Retry-After")
        if ra:
            try:
                retry_after = float(ra)
            except ValueError:
                pass

    # Classificação canônica por status HTTP / tipo
    cls_name = exc.__class__.__name__

    if http_status == 429 or "RateLimit" in cls_name or "rate limit" in raw_msg.lower():
        http_status = 429
        error_type = "RATE_LIMIT"
        is_rate_limit = True
        is_transient = True
    elif http_status == 400:
        error_type = "BAD_REQUEST"
        is_transient = False
    elif http_status == 401:
        error_type = "AUTHENTICATION"
        is_transient = False
    elif http_status == 403:
        error_type = "PERMISSION"
        is_transient = False
    elif http_status == 413:
        error_type = "REQUEST_TOO_LARGE"
        is_transient = False
    elif http_status == 422:
        error_type = "UNPROCESSABLE"
        is_transient = False
    elif http_status and 500 <= http_status <= 599:
        error_type = "PROVIDER_TRANSIENT"
        is_transient = True
    elif "Timeout" in cls_name or "Connection" in cls_name or "network" in raw_msg.lower():
        error_type = "NETWORK_TIMEOUT"
        is_transient = True

    return ProviderErrorDetails(
        provider=provider,
        http_status=http_status,
        error_type=error_type,
        error_code=error_code,
        message_sanitized=sanitized_msg,
        failed_generation=failed_gen,
        retry_after_seconds=retry_after,
        is_rate_limit=is_rate_limit,
        is_transient=is_transient,
        is_schema_generation_failure=is_schema_gen_fail,
        transport_attempts=attempts,
        transport_retries=retries,
    )


def _load_env_file_safe():
    """
    Carrega variáveis exclusivamente do arquivo .env da raiz do projeto, se existir.
    Não varre diretórios globais (~/.env) para evitar contaminação acidental de credenciais.
    """
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        try:
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'").strip('"')
                    if k not in os.environ:
                        os.environ[k] = v
        except Exception:
            pass


_load_env_file_safe()


def get_provider_capabilities() -> Dict[str, Dict[str, Any]]:
    """Retorna a matriz de capacidades dos provedores suportados no IEE."""
    return {
        "groq": {
            "name": "Groq",
            "implemented": True,
            "structured_output_mode": "native_json_schema_strict",
            "usage_reporting": True,
            "real_tested": False,
            "credential_env": "GROQ_API_KEY",
            "default_model": "openai/gpt-oss-120b",
        },
        "gemini": {
            "name": "Google Gemini",
            "implemented": True,
            "structured_output_mode": "native_response_mime_type",
            "usage_reporting": True,
            "real_tested": False,
            "credential_env": "GEMINI_API_KEY",
            "default_model": "gemini-3.7-flash",
        },
        "openai": {
            "name": "OpenAI",
            "implemented": True,
            "structured_output_mode": "native_json_object",
            "usage_reporting": True,
            "real_tested": False,
            "credential_env": "OPENAI_API_KEY",
            "default_model": "gpt-4o-mini",
        },
        "anthropic": {
            "name": "Anthropic Claude",
            "implemented": True,
            "structured_output_mode": "prompted_json_validation",
            "usage_reporting": True,
            "real_tested": False,
            "credential_env": "ANTHROPIC_API_KEY",
            "default_model": "claude-3-5-haiku-20241022",
        },
        "fake": {
            "name": "Deterministic Fake Runner",
            "implemented": True,
            "structured_output_mode": "local_pydantic_mock",
            "usage_reporting": True,
            "real_tested": True,
            "credential_env": None,
            "default_model": "default-model",
        },
    }


def check_providers_health(catalog: Optional[Any] = None) -> Dict[str, Dict[str, Any]]:
    """
    Verifica a saúde, credenciais e status de catálogo para todos os provedores.
    NUNCA expõe valores de chaves.
    """
    from src.idea_evolution.config.catalog import ModelCatalog, LifecycleStatus, CostClass, PrivacyClass
    cat = catalog or ModelCatalog()
    caps = get_provider_capabilities()
    status = {}
    for prov_id, info in caps.items():
        env_var = info.get("credential_env")
        has_key = bool(env_var and os.environ.get(env_var)) if env_var else True
        def_model = info["default_model"]
        cat_entry = cat.get_entry(prov_id, def_model)

        status[prov_id] = {
            "name": info["name"],
            "adapter_available": info["implemented"],
            "credential_env": env_var,
            "credential_present": has_key,
            "ready": info["implemented"] and has_key,
            "real_tested": info["real_tested"],
            "default_model": def_model,
            "catalog_status": cat_entry.status.value if cat_entry else "UNKNOWN",
            "cost_class": cat_entry.cost_class.value if cat_entry else "UNKNOWN",
            "free_eligible": cat_entry.cost_class in [CostClass.FREE_TIER, CostClass.FREE_ROUTER, CostClass.LOCAL_ZERO_MARGINAL_API_COST] if cat_entry else False,
            "privacy_class": cat_entry.privacy_class.value if cat_entry else "UNKNOWN",
            "replacement": cat_entry.replacement_if_deprecated if cat_entry else None,
        }
    return status


def to_strict_json_schema(model: Type[BaseModel]) -> Dict[str, Any]:
    """
    Converte um modelo Pydantic para um JSON Schema estritamente compatível com o modo Strict do Groq/OpenAI:
    - additionalProperties: false em todos os objetos
    - required contendo TODAS as chaves de properties
    - $defs e items processados recursivamente
    """
    schema = model.model_json_schema()

    def process_object(obj: Any):
        if not isinstance(obj, dict):
            return
        if obj.get("type") == "object" or "properties" in obj:
            obj["type"] = "object"
            obj["additionalProperties"] = False
            props = obj.get("properties", {})
            if props:
                obj["required"] = list(props.keys())
            for p in props.values():
                process_object(p)
        if "$defs" in obj:
            for d in obj["$defs"].values():
                process_object(d)
        if "items" in obj:
            process_object(obj["items"])

    process_object(schema)
    return schema


class NativeModelRunner(ModelRunner):
    """
    Executor para provedores reais de LLM.
    Suporta Groq, OpenAI, Gemini e Anthropic com Structured Output JSON e bounded repair governado.
    """

    def __init__(self, provider: str = "groq", api_key: Optional[str] = None, default_model: Optional[str] = None):
        self.provider = provider.lower()
        caps = get_provider_capabilities()
        if self.provider not in caps and not self.provider.startswith("fake"):
            raise ValueError(f"UNSUPPORTED_PROVIDER: Provedor '{self.provider}' não reconhecido.")

        env_name = caps.get(self.provider, {}).get("credential_env")
        self.api_key = api_key or (os.environ.get(env_name) if env_name else None)

        def_model = caps.get(self.provider, {}).get("default_model", "default-model")
        self.default_model = default_model or def_model

    def generate(
        self,
        prompt_text: str,
        output_schema: Type[T],
        stage_name: str,
        model_name: Optional[str] = None,
        max_repairs: int = 1,
    ) -> ModelResponse:
        model = model_name or self.default_model

        if not self.api_key:
            return ModelResponse(
                parsed=None,
                raw_text="",
                provider=self.provider,
                model=model,
                error=f"PROVIDER_CREDENTIAL_MISSING: Chave para provedor '{self.provider}' não configurada.",
            )

        start_time = time.time()
        strict_schema = to_strict_json_schema(output_schema)
        schema_json = json.dumps(strict_schema, indent=2)
        system_instruction = (
            f"Você é um módulo cognitivo do Idea Evolution Engine para o estágio {stage_name}.\n"
            f"Sua resposta DEVE ser estritamente um objeto JSON válido correspondente ao seguinte JSON Schema:\n"
            f"{schema_json}\n"
            f"IMPORTANTE: Não inclua tags markdown (```json ... ```) ou texto antes/depois do JSON."
        )

        try:
            raw_text, usage, error_details = self._call_provider(
                system_instruction, prompt_text, model, output_schema, stage_name
            )
            latency = time.time() - start_time

            # Se houve falha de transporte/API sem texto retornado
            if error_details and not raw_text:
                # Reparo semântico só ocorre se houver failed_generation GENUÍNA do modelo
                if error_details.is_schema_generation_failure and error_details.failed_generation and max_repairs > 0:
                    repair_prompt = (
                        f"A geração anterior falhou na validação estruturada do provedor.\n"
                        f"Conteúdo rejeitado (failed_generation):\n{error_details.failed_generation}\n\n"
                        f"Gere um JSON válido em estrita conformidade com o schema:\n{schema_json}"
                    )
                    repair_raw, repair_usage, repair_err = self._call_provider(
                        system_instruction, repair_prompt, model, output_schema, stage_name
                    )
                    total_usage = ModelUsage(
                        prompt_tokens=(usage.prompt_tokens or 0) + (repair_usage.prompt_tokens or 0),
                        completion_tokens=(usage.completion_tokens or 0) + (repair_usage.completion_tokens or 0),
                        total_tokens=(usage.total_tokens or 0) + (repair_usage.total_tokens or 0),
                    )
                    if repair_raw:
                        try:
                            repaired_data = self._clean_and_parse_json(repair_raw)
                            repaired_obj = output_schema.model_validate(repaired_data)
                            return ModelResponse(
                                parsed=repaired_obj,
                                raw_text=repair_raw,
                                provider=self.provider,
                                model=model,
                                usage=total_usage,
                                latency_seconds=time.time() - start_time,
                                retry_count=1,
                                failed_generation=error_details.failed_generation,
                            )
                        except (json.JSONDecodeError, ValidationError) as re_val_err:
                            return ModelResponse(
                                parsed=None,
                                raw_text=repair_raw,
                                provider=self.provider,
                                model=model,
                                usage=total_usage,
                                latency_seconds=time.time() - start_time,
                                retry_count=1,
                                error=f"SCHEMA_VALIDATION_FAILED: {str(re_val_err)}",
                                failed_generation=repair_raw,
                            )
                    else:
                        return ModelResponse(
                            parsed=None,
                            raw_text="",
                            provider=self.provider,
                            model=model,
                            usage=total_usage,
                            latency_seconds=time.time() - start_time,
                            retry_count=1,
                            error=f"PROVIDER_STRUCTURED_OUTPUT_REPAIR_FAILED: {repair_err.message_sanitized if repair_err else 'Sem resposta'}",
                            failed_generation=error_details.failed_generation,
                        )
                else:
                    # Falha de transporte/API pura (429, 400, 401, 5xx, etc.) -> FAIL CLOSED SEM REPARO SEMÂNTICO
                    err_msg = f"PROVIDER_TRANSPORT_ERROR: {error_details.error_type}"
                    if error_details.http_status:
                        err_msg += f" (HTTP {error_details.http_status})"
                    if error_details.message_sanitized:
                        err_msg += f": {error_details.message_sanitized}"
                    return ModelResponse(
                        parsed=None,
                        raw_text="",
                        provider=self.provider,
                        model=model,
                        usage=usage,
                        latency_seconds=latency,
                        retry_count=0,
                        error=err_msg,
                        failed_generation=None,
                    )

            # Tentativa de Parse Direto quando raw_text existe
            try:
                parsed_data = self._clean_and_parse_json(raw_text)
                parsed_obj = output_schema.model_validate(parsed_data)
                return ModelResponse(
                    parsed=parsed_obj,
                    raw_text=raw_text,
                    provider=self.provider,
                    model=model,
                    usage=usage,
                    latency_seconds=latency,
                    retry_count=0,
                )
            except (json.JSONDecodeError, ValidationError) as val_err:
                if max_repairs > 0:
                    # Tentativa de Repair Bounded Local (1 tentativa)
                    repair_prompt = (
                        f"O JSON fornecido falhou na validação com o erro: {str(val_err)}\n"
                        f"Texto recebido anteriormente:\n{raw_text}\n\n"
                        f"Corrija o JSON para conformidade estrita com o schema:\n{schema_json}"
                    )
                    repair_raw, repair_usage, repair_err = self._call_provider(
                        system_instruction, repair_prompt, model, output_schema, stage_name
                    )
                    total_usage = ModelUsage(
                        prompt_tokens=(usage.prompt_tokens or 0) + (repair_usage.prompt_tokens or 0),
                        completion_tokens=(usage.completion_tokens or 0) + (repair_usage.completion_tokens or 0),
                        total_tokens=(usage.total_tokens or 0) + (repair_usage.total_tokens or 0),
                    )
                    if repair_raw:
                        try:
                            repaired_data = self._clean_and_parse_json(repair_raw)
                            repaired_obj = output_schema.model_validate(repaired_data)
                            return ModelResponse(
                                parsed=repaired_obj,
                                raw_text=repair_raw,
                                provider=self.provider,
                                model=model,
                                usage=total_usage,
                                latency_seconds=time.time() - start_time,
                                retry_count=1,
                                failed_generation=raw_text,
                            )
                        except (json.JSONDecodeError, ValidationError) as re_err:
                            return ModelResponse(
                                parsed=None,
                                raw_text=repair_raw,
                                provider=self.provider,
                                model=model,
                                usage=total_usage,
                                latency_seconds=time.time() - start_time,
                                retry_count=1,
                                error=f"SCHEMA_VALIDATION_FAILED: {str(re_err)}",
                                failed_generation=repair_raw,
                            )
                    else:
                        return ModelResponse(
                            parsed=None,
                            raw_text="",
                            provider=self.provider,
                            model=model,
                            usage=total_usage,
                            latency_seconds=time.time() - start_time,
                            retry_count=1,
                            error=f"PROVIDER_STRUCTURED_OUTPUT_REPAIR_FAILED: {repair_err.message_sanitized if repair_err else 'Sem resposta'}",
                            failed_generation=raw_text,
                        )
                else:
                    return ModelResponse(
                        parsed=None,
                        raw_text=raw_text,
                        provider=self.provider,
                        model=model,
                        usage=usage,
                        latency_seconds=latency,
                        error=f"SCHEMA_VALIDATION_FAILED: {str(val_err)}",
                        failed_generation=raw_text,
                    )

        except Exception as e:
            return ModelResponse(
                parsed=None,
                raw_text="",
                provider=self.provider,
                model=model,
                latency_seconds=time.time() - start_time,
                error=f"PROVIDER_EXECUTION_ERROR: {str(e)}",
            )

    def _call_provider(
        self,
        system_instruction: str,
        user_prompt: str,
        model: str,
        output_schema: Type[BaseModel],
        stage_name: str,
    ) -> Tuple[str, ModelUsage, Optional[ProviderErrorDetails]]:
        """
        Invoca o provedor com retries de transporte limitados. Retorna (raw_text, usage, error_details).
        """
        if self.provider == "groq":
            from groq import Groq

            client = Groq(api_key=self.api_key)
            strict_schema = to_strict_json_schema(output_schema)
            response_format = {
                "type": "json_schema",
                "json_schema": {
                    "name": f"{stage_name.lower()}_output",
                    "strict": True,
                    "schema": strict_schema,
                },
            }

            max_transport_attempts = 3
            last_err_details: Optional[ProviderErrorDetails] = None

            for attempt_idx in range(max_transport_attempts):
                try:
                    completion = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": user_prompt},
                        ],
                        response_format=response_format,
                        temperature=0.3,
                    )
                    raw = completion.choices[0].message.content or ""
                    usage = ModelUsage(
                        prompt_tokens=completion.usage.prompt_tokens if completion.usage else 0,
                        completion_tokens=completion.usage.completion_tokens if completion.usage else 0,
                        total_tokens=completion.usage.total_tokens if completion.usage else 0,
                    )
                    return raw, usage, None
                except Exception as groq_err:
                    err_details = parse_provider_exception(
                        groq_err, provider="groq", attempts=attempt_idx + 1, retries=attempt_idx
                    )
                    last_err_details = err_details

                    # Apenas retentar erros comprovadamente transientes (429 ou 5xx/timeout)
                    if err_details.is_transient and attempt_idx < max_transport_attempts - 1:
                        wait_sec = err_details.retry_after_seconds or min(10.0, 2.0 * (attempt_idx + 1))
                        time.sleep(wait_sec)
                        continue
                    else:
                        break

            return "", ModelUsage(), last_err_details

        if self.provider == "openai":
            import httpx

            strict_schema = to_strict_json_schema(output_schema)
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt},
                ],
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        "name": f"{stage_name.lower()}_output",
                        "strict": True,
                        "schema": strict_schema,
                    },
                },
                "temperature": 0.3,
            }
            try:
                resp = httpx.post(url, headers=headers, json=payload, timeout=60.0)
                resp.raise_for_status()
                data = resp.json()
                raw = data["choices"][0]["message"]["content"] or ""
                u = data.get("usage", {})
                usage = ModelUsage(
                    prompt_tokens=u.get("prompt_tokens", 0),
                    completion_tokens=u.get("completion_tokens", 0),
                    total_tokens=u.get("total_tokens", 0),
                )
                return raw, usage, None
            except Exception as openai_err:
                err_details = parse_provider_exception(openai_err, provider="openai", attempts=1, retries=0)
                return "", ModelUsage(), err_details

        if self.provider == "gemini":
            import httpx

            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
            payload = {
                "contents": [{"role": "user", "parts": [{"text": f"{system_instruction}\n\n{user_prompt}"}]}],
                "generationConfig": {"response_mime_type": "application/json", "temperature": 0.3},
            }
            try:
                resp = httpx.post(url, json=payload, timeout=60.0)
                resp.raise_for_status()
                data = resp.json()
                raw = data["candidates"][0]["content"]["parts"][0]["text"]
                u = data.get("usageMetadata", {})
                usage = ModelUsage(
                    prompt_tokens=u.get("promptTokenCount", 0),
                    completion_tokens=u.get("candidatesTokenCount", 0),
                    total_tokens=u.get("totalTokenCount", 0),
                )
                return raw, usage, None
            except Exception as gemini_err:
                err_details = parse_provider_exception(gemini_err, provider="gemini", attempts=1, retries=0)
                return "", ModelUsage(), err_details

        if self.provider == "anthropic":
            import httpx

            url = "https://api.anthropic.com/v1/messages"
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            }
            payload = {
                "model": model,
                "max_tokens": 4096,
                "system": system_instruction,
                "messages": [{"role": "user", "content": user_prompt}],
                "temperature": 0.3,
            }
            try:
                resp = httpx.post(url, headers=headers, json=payload, timeout=60.0)
                resp.raise_for_status()
                data = resp.json()
                raw = data["content"][0]["text"]
                u = data.get("usage", {})
                usage = ModelUsage(
                    prompt_tokens=u.get("input_tokens", 0),
                    completion_tokens=u.get("output_tokens", 0),
                    total_tokens=(u.get("input_tokens", 0) + u.get("output_tokens", 0)),
                )
                return raw, usage, None
            except Exception as anth_err:
                err_details = parse_provider_exception(anth_err, provider="anthropic", attempts=1, retries=0)
                return "", ModelUsage(), err_details

        raise NotImplementedError(f"UNSUPPORTED_PROVIDER: Provider '{self.provider}' não implementado.")

    def _clean_and_parse_json(self, raw_text: str) -> dict:
        text = raw_text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())
