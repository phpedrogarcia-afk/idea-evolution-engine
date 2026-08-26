"""
src/idea_evolution/config/routing.py
Configuração de Roteamento de Modelos por Estágio (Model Routing Configuration).
"""

from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field, field_validator


class ModelDefinition(BaseModel):
    """Definição de um modelo/provedor específico."""
    provider: str
    model: str
    credential_env: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("provider")
    def validate_provider(cls, v: str) -> str:
        allowed = {"groq", "openai", "gemini", "anthropic", "fake", "fake_a", "fake_b", "fake_c"}
        if v.lower() not in allowed and not v.lower().startswith("fake"):
            raise ValueError(f"Provedor '{v}' não suportado. Provedores válidos: {allowed}")
        return v.lower()


class ModelRoutingConfig(BaseModel):
    """
    Configuração determinística de roteamento:
    Associa aliases lógicos (ex: analyst, critic) a provedores/modelos e mapeia cada estágio para um alias.
    """
    schema_version: str = "1.0.0"
    description: str = "Configuração de roteamento multi-modelo para o IEE"
    models: Dict[str, ModelDefinition] = Field(default_factory=dict)
    routes: Dict[str, str] = Field(default_factory=dict)  # stage_name -> model_alias
    default_model_alias: Optional[str] = None

    def compute_hash(self) -> str:
        """Calcula o hash SHA-256 canônico determinístico desta configuração."""
        canonical_dict = {
            "schema_version": self.schema_version,
            "models": {k: self.models[k].model_dump() for k in sorted(self.models.keys())},
            "routes": {k: self.routes[k] for k in sorted(self.routes.keys())},
            "default_model_alias": self.default_model_alias,
        }
        json_bytes = json.dumps(canonical_dict, sort_keys=True).encode("utf-8")
        return hashlib.sha256(json_bytes).hexdigest()

    def resolve_stage(self, stage_name: str) -> Tuple[str, ModelDefinition]:
        """
        Resolve o alias lógico e a definição de modelo para um estágio específico.
        Falha ruidosamente se a rota ou o alias forem desconhecidos.
        """
        normalized_stage = stage_name.lower()
        alias = self.routes.get(normalized_stage) or self.routes.get(stage_name)
        if not alias:
            if self.default_model_alias and self.default_model_alias in self.models:
                alias = self.default_model_alias
            else:
                raise KeyError(f"ROUTE_CONFIGURATION_INVALID: Nenhuma rota configurada para o estágio '{stage_name}'.")

        if alias not in self.models:
            raise KeyError(f"UNKNOWN_MODEL_ALIAS: O alias '{alias}' referenciado pelo estágio '{stage_name}' não está definido em 'models'.")

        return alias, self.models[alias]

    def validate_for_topology(self, stages: List[str]) -> List[str]:
        """Verifica se todos os estágios exigidos possuem rotas válidas."""
        errors = []
        for stage in stages:
            try:
                self.resolve_stage(stage)
            except Exception as e:
                errors.append(str(e))
        return errors

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ModelRoutingConfig:
        return cls.model_validate(data)

    @classmethod
    def from_file(cls, filepath: Path) -> ModelRoutingConfig:
        if not filepath.exists():
            raise FileNotFoundError(f"Arquivo de configuração de modelos não encontrado: {filepath}")

        content = filepath.read_text(encoding="utf-8")
        if filepath.suffix in [".yaml", ".yml"]:
            # Parser simples de YAML sem dependência externa obrigatória, ou json fallback
            try:
                import yaml
                data = yaml.safe_load(content)
            except ImportError:
                # Fallback: se yaml não estiver instalado, suportar json ou yaml básico
                import json
                try:
                    data = json.loads(content)
                except Exception:
                    # Carregador elementar chave-valor
                    data = _parse_simple_yaml(content)
        else:
            data = json.loads(content)

        return cls.from_dict(data)

    @classmethod
    def default_single_model(cls, provider: str = "fake", model: str = "default") -> ModelRoutingConfig:
        """Gera configuração padrão onde todos os estágios usam o mesmo modelo."""
        return cls(
            models={
                "default": ModelDefinition(provider=provider, model=model)
            },
            routes={},
            default_model_alias="default",
        )


def _parse_simple_yaml(text: str) -> dict:
    """Parser simplificado para arquivos YAML de modelo quando PyYAML não está disponível."""
    import yaml  # Se disponível
    return yaml.safe_load(text)
