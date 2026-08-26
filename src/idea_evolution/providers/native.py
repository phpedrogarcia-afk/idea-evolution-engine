"""
src/idea_evolution/providers/native.py
Executor Nativo de Modelos via SDK/HTTP (Groq, OpenAI, Gemini, Anthropic) com preservação de raw output e repair bounded.
"""

from __future__ import annotations
from typing import Type, TypeVar, Optional, Dict, Any
import os
import time
import json
from pathlib import Path
from pydantic import BaseModel, ValidationError
from src.idea_evolution.providers.base import ModelRunner, ModelResponse, ModelUsage

T = TypeVar("T", bound=BaseModel)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent


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
            "structured_output_mode": "native_json_object",
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


class NativeModelRunner(ModelRunner):
    """
    Executor para provedores reais de LLM.
    Suporta Groq, OpenAI, Gemini e Anthropic com Structured Output JSON e 1 tentativa de repair.
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
        schema_json = json.dumps(output_schema.model_json_schema(), indent=2)
        system_instruction = (
            f"Você é um módulo cognitivo do Idea Evolution Engine para o estágio {stage_name}.\n"
            f"Sua resposta DEVE ser estritamente um objeto JSON válido correspondente ao seguinte JSON Schema:\n"
            f"{schema_json}\n"
            f"IMPORTANTE: Não inclua tags markdown (```json ... ```) ou texto antes/depois do JSON."
        )

        try:
            raw_text, usage = self._call_provider(system_instruction, prompt_text, model)
            latency = time.time() - start_time

            # Tentativa de Parse Direto
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
                    # Tentativa de Repair Bounded (1 tentativa)
                    repair_prompt = (
                        f"O JSON fornecido falhou na validação com o erro: {str(val_err)}\n"
                        f"Texto recebido anteriormente:\n{raw_text}\n\n"
                        f"Corrija o JSON para conformidade estrita com o schema:\n{schema_json}"
                    )
                    repair_raw, repair_usage = self._call_provider(system_instruction, repair_prompt, model)
                    total_usage = ModelUsage(
                        prompt_tokens=(usage.prompt_tokens or 0) + (repair_usage.prompt_tokens or 0),
                        completion_tokens=(usage.completion_tokens or 0) + (repair_usage.completion_tokens or 0),
                        total_tokens=(usage.total_tokens or 0) + (repair_usage.total_tokens or 0),
                    )
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

    def _call_provider(self, system_instruction: str, user_prompt: str, model: str) -> tuple[str, ModelUsage]:
        if self.provider == "groq":
            from groq import Groq

            client = Groq(api_key=self.api_key)
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
            )
            raw = completion.choices[0].message.content or ""
            usage = ModelUsage(
                prompt_tokens=completion.usage.prompt_tokens if completion.usage else 0,
                completion_tokens=completion.usage.completion_tokens if completion.usage else 0,
                total_tokens=completion.usage.total_tokens if completion.usage else 0,
            )
            return raw, usage

        if self.provider == "openai":
            import httpx

            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt},
                ],
                "response_format": {"type": "json_object"},
                "temperature": 0.3,
            }
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
            return raw, usage

        if self.provider == "gemini":
            import httpx

            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
            payload = {
                "contents": [{"role": "user", "parts": [{"text": f"{system_instruction}\n\n{user_prompt}"}]}],
                "generationConfig": {"response_mime_type": "application/json", "temperature": 0.3},
            }
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
            return raw, usage

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
            return raw, usage

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
