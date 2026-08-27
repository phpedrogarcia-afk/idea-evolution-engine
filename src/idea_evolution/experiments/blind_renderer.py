"""
src/idea_evolution/experiments/blind_renderer.py
Renderizador determinístico de pacotes de avaliação cega para M05.4.
Remove metadados de execução, identificadores de condição, nomes de arquitetura
e padroniza o envelope de avaliação para evitar vazamento de identidade.
"""

from __future__ import annotations
import re
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


# Lista de tokens terminantemente proibidos no pacote de avaliação cega
FORBIDDEN_METADATA_PATTERNS = [
    r"\bCOND[-_][ABC]\b",
    r"\bCONDITION[-_][ABC]\b",
    r"\bBASELINE\b",
    r"\bSIMPLE[-_]?LOOP\b",
    r"\bLEAN[-_]?IEE\b",
    r"\bLEAN[-_]?L1\b",
    r"\bFIOED\b",
    r"\bRUN[-_]\d{8}[-_]\w+\b",
    r"\b0\d[-_][A-Z_]+\.json\b",
    r"\bprovider\b\s*:\s*[\"']?\w+[\"']?",
    r"\bmodel\b\s*:\s*[\"']?[\w/-]+[\"']?",
    r"\bcall_count\b\s*:\s*\d+",
    r"\btotal_tokens\b\s*:\s*\d+",
]


class BlindReviewItem(BaseModel):
    label: str  # RESULT_1, RESULT_2, RESULT_3
    content_text: str


class BlindReviewPacket(BaseModel):
    idea_id: str
    raw_idea: str
    items: List[BlindReviewItem] = Field(default_factory=list)


class BlindRenderer:
    """
    Renderizador de pacotes de avaliação cega.
    Higieniza e normaliza saídas sem alterar o conteúdo semântico substantivo.
    """

    @classmethod
    def sanitize_text(cls, text: str) -> str:
        sanitized = text
        # Remove eventuais metadados brutos que possam ter sido injetados
        for pattern in FORBIDDEN_METADATA_PATTERNS:
            sanitized = re.sub(pattern, "[REDACTED_METADATA]", sanitized, flags=re.IGNORECASE)
        return sanitized.strip()

    @classmethod
    def detect_leaks(cls, text: str) -> List[str]:
        leaks = []
        for pattern in FORBIDDEN_METADATA_PATTERNS:
            matches = re.findall(pattern, text, flags=re.IGNORECASE)
            if matches:
                leaks.extend(matches)
        return leaks

    @classmethod
    def render_markdown_packet(cls, packet: BlindReviewPacket) -> str:
        lines = [
            f"# PACOTE DE AVALIAÇÃO CEGA — {packet.idea_id}",
            "",
            f'> **IDEIA ORIGINAL:** "{packet.raw_idea}"',
            "",
        ]

        for item in packet.items:
            sanitized_content = cls.sanitize_text(item.content_text)
            lines.extend([
                "---",
                "",
                f"## {item.label}",
                "",
                sanitized_content,
                "",
            ])

        return "\n".join(lines)
