"""
src/idea_evolution/providers/native.py
Executor Nativo de Modelos via SDK/HTTP (Groq, OpenAI, etc.) com preservação de raw output e repair bounded.
"""

from typing import Type, TypeVar, Optional, Dict, Any
import os
import time
import json
from pydantic import BaseModel, ValidationError
from src.idea_evolution.providers.base import ModelRunner, ModelResponse, ModelUsage

T = TypeVar("T", bound=BaseModel)


from pathlib import Path

def _load_env_file_safe():
    """Carrega variáveis do .env no os.environ caso exista localmente ou no home."""
    candidates = [
        Path(__file__).resolve().parent.parent.parent.parent / ".env",
        Path.home() / ".env",
    ]
    for env_p in candidates:
        if env_p.exists():
            for line in env_p.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'").strip('"')
                    if k not in os.environ:
                        os.environ[k] = v

_load_env_file_safe()


class NativeModelRunner(ModelRunner):
    """
    Executor para provedores reais de LLM.
    Suporta Groq / OpenAI compatível com Structured Output JSON e 1 tentativa de repair.
    """

    def __init__(self, provider: str = "groq", api_key: Optional[str] = None, default_model: Optional[str] = None):
        self.provider = provider.lower()
        self.api_key = api_key or os.environ.get(f"{self.provider.upper()}_API_KEY")
        if self.provider == "groq":
            self.default_model = default_model or "llama-3.3-70b-versatile"
        elif self.provider == "openai":
            self.default_model = default_model or "gpt-4o-mini"
        elif self.provider == "gemini":
            self.default_model = default_model or "gemini-2.0-flash"
        else:
            self.default_model = default_model or "default-model"

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
                error=f"PROVIDER_CREDENTIAL_MISSING: Chave {self.provider.upper()}_API_KEY não encontrada no ambiente.",
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

        raise NotImplementedError(f"Provider {self.provider} não implementado no NativeModelRunner.")

    def _clean_and_parse_json(self, raw_text: str) -> dict:
        text = raw_text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())
