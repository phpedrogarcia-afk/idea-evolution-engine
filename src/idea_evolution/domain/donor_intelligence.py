"""
src/idea_evolution/domain/donor_intelligence.py
Mecanismo determinístico de visualização e consulta ao conhecimento de doadores (Donor Intelligence Context View).
DONOR CONTEXT IS DATA, NOT AUTHORITY.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from src.idea_evolution.domain.epistemic_contracts import ClaimStatus


class DonorContextView(BaseModel):
    """Visão delimitada determinística do conhecimento de doadores para um determinado gap receptor."""
    receiver_gap: str
    matched_donors: List[str] = Field(default_factory=list)
    relevant_mechanisms: List[str] = Field(default_factory=list)
    relevant_scars: List[str] = Field(default_factory=list)
    paid_uncertainties: List[str] = Field(default_factory=list)
    claim_status: ClaimStatus = ClaimStatus.BORROWED_MODEL
    current_receiver_decisions: List[str] = Field(default_factory=list)
    do_not_copy: List[str] = Field(default_factory=list)
    source_refs: List[str] = Field(default_factory=list)
    freshness: str = "2026-08-27"


class DonorIntelligenceCatalog:
    """Catálogo e visualizador determinístico de inteligência de doadores."""

    def __init__(self, manifest_path: Optional[Path] = None):
        self.manifest_path = manifest_path or (Path("docs") / "research" / "donor-manifest.json")
        self._data: Dict[str, Any] = {}
        self._load()

    def _load(self):
        if self.manifest_path.exists():
            self._data = json.loads(self.manifest_path.read_text(encoding="utf-8"))

    def get_context_view_for_gap(self, receiver_gap: str) -> DonorContextView:
        """
        Retorna uma visualização delimitada e determinística baseada em tags/gaps no manifesto de doadores.
        Sem RAG, sem embeddings e sem oráculo de LLM.
        """
        gap_index = self._data.get("gap_index", {})
        donor_keys = gap_index.get(receiver_gap, [])
        all_donors = self._data.get("donors", {})

        matched_donors = []
        mechanisms = []
        scars = []
        decisions = []
        sources = []

        for k in donor_keys:
            d_info = all_donors.get(k, {})
            d_name = d_info.get("name", k)
            matched_donors.append(d_name)
            if "primary_mechanism" in d_info:
                mechanisms.append(f"{d_name}: {d_info['primary_mechanism']}")
            for sc in d_info.get("scars", []):
                scars.append(f"{d_name}: {sc}")
            if "decision" in d_info:
                decisions.append(f"{d_name}: {d_info['decision']}")
            if "donor_id" in d_info:
                sources.append(f"docs/research/donors/{d_info['donor_id']}.md")

        return DonorContextView(
            receiver_gap=receiver_gap,
            matched_donors=matched_donors,
            relevant_mechanisms=mechanisms,
            relevant_scars=scars,
            paid_uncertainties=[],
            claim_status=ClaimStatus.BORROWED_MODEL,
            current_receiver_decisions=decisions,
            do_not_copy=["Literal framework runtime", "Unverified claims as receiver truth"],
            source_refs=sources,
            freshness=self._data.get("updated_at", "2026-08-27"),
        )
