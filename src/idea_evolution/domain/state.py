"""
src/idea_evolution/domain/state.py
Domínio e Estado Mínimo Compartilhado (SimpleIdeaState) do IEE MVP.
"""

from __future__ import annotations
import json
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator


class RunStatus(str, Enum):
    INITIALIZED = "INITIALIZED"
    RUNNING = "RUNNING"
    REFINED_IDEA_READY = "REFINED_IDEA_READY"
    RECONSTRUCTING = "RECONSTRUCTING"
    REFINEMENT_INCOMPLETE = "REFINEMENT_INCOMPLETE"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


class CriticalIssue(BaseModel):
    issue: str
    why_it_matters: str
    severity: str = "MEDIUM"  # HIGH | MEDIUM | LOW
    affected_part: str = ""


class AlternativeMechanism(BaseModel):
    mechanism: str
    addresses_issues: List[str] = Field(default_factory=list)
    preserves_intent: bool = True
    tradeoffs: List[str] = Field(default_factory=list)
    novelty_or_difference: str = ""


class RejectedProposal(BaseModel):
    proposal: str
    reason_rejected: str
    source_stage: str = ""


class StageHistoryEntry(BaseModel):
    stage_id: str
    stage_version: str
    executed_at: str
    provider: str
    model: str
    success: bool
    retry_count: int = 0
    delta_summary: str = ""


class SimpleIdeaState(BaseModel):
    schema_version: str = "0.1.0"
    run_id: str
    status: RunStatus = RunStatus.INITIALIZED
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    # Imutável por constituição
    original_idea: str

    # Evolução semântica
    current_idea: str = ""
    human_intent: str = ""
    problem_statement: str = ""
    actors_or_users: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    ambiguities: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)

    # Críticas e modo de falha
    critical_issues: List[CriticalIssue] = Field(default_factory=list)
    fragile_assumptions: List[str] = Field(default_factory=list)
    contradictions: List[str] = Field(default_factory=list)
    failure_modes: List[str] = Field(default_factory=list)

    # Exploração e Realidade
    alternatives: List[AlternativeMechanism] = Field(default_factory=list)
    reality_dependencies: List[str] = Field(default_factory=list)
    claims_needing_evidence: List[str] = Field(default_factory=list)
    candidate_tests: List[str] = Field(default_factory=list)

    # Síntese e Revisão
    accepted_changes: List[str] = Field(default_factory=list)
    rejected_changes: List[RejectedProposal] = Field(default_factory=list)
    remaining_uncertainties: List[str] = Field(default_factory=list)
    known_risks: List[str] = Field(default_factory=list)
    recommended_next_step: str = ""

    # Governança do Loop
    reconstruction_count: int = 0
    max_reconstructions: int = 1
    essence_drift_detected: bool = False
    human_intervention: bool = False
    stage_history: List[StageHistoryEntry] = Field(default_factory=list)

    def record_stage_execution(
        self,
        stage_id: str,
        stage_version: str,
        provider: str,
        model: str,
        success: bool,
        retry_count: int = 0,
        delta_summary: str = "",
    ):
        self.stage_history.append(
            StageHistoryEntry(
                stage_id=stage_id,
                stage_version=stage_version,
                executed_at=datetime.now().isoformat(),
                provider=provider,
                model=model,
                success=success,
                retry_count=retry_count,
                delta_summary=delta_summary,
            )
        )
        self.updated_at = datetime.now().isoformat()

    def to_human_markdown(self) -> str:
        """Gera a apresentação estruturada limpa em Markdown para o usuário humano."""
        md = []
        md.append(f"# Pacote de Maturação da Ideia — Run {self.run_id}\n")
        md.append(f"**Status:** `{self.status.value}` | **Ciclos de Reconstrução:** {self.reconstruction_count}\n")
        md.append("---\n")
        md.append("## 1. Ideia Original (Imutável)\n")
        md.append(f"> {self.original_idea.strip()}\n\n")

        md.append("## 2. Intenção Humana & Problema Definido\n")
        md.append(f"- **Intenção Preservada:** {self.human_intent or 'N/D'}")
        md.append(f"- **Problema Central:** {self.problem_statement or 'N/D'}")
        if self.actors_or_users:
            md.append(f"- **Atores / Usuários:** {', '.join(self.actors_or_users)}")
        md.append("\n")

        md.append("## 3. Versão Refinada e Mecanismo Proposto\n")
        md.append(f"{self.current_idea or 'Em desenvolvimento'}\n\n")

        if self.critical_issues:
            md.append("## 4. Vulnerabilidades e Críticas Severas Encontradas\n")
            for idx, item in enumerate(self.critical_issues, 1):
                md.append(f"{idx}. **[{item.severity}]** {item.issue}")
                md.append(f"   - *Impacto:* {item.why_it_matters}")
                if item.affected_part:
                    md.append(f"   - *Parte Afetada:* {item.affected_part}")
            md.append("\n")

        if self.alternatives:
            md.append("## 5. Mecanismos Alternativos Considerados\n")
            for idx, alt in enumerate(self.alternatives, 1):
                md.append(f"{idx}. **Mecanismo:** {alt.mechanism}")
                if alt.tradeoffs:
                    md.append(f"   - *Tradeoffs:* {', '.join(alt.tradeoffs)}")
            md.append("\n")

        if self.rejected_changes:
            md.append("## 6. Propostas Rejeitadas (com Justificativa)\n")
            for rej in self.rejected_changes:
                md.append(f"- **Rejeitado:** {rej.proposal} (Origem: {rej.source_stage})")
                md.append(f"  *Motivo:* {rej.reason_rejected}")
            md.append("\n")

        if self.reality_dependencies or self.candidate_tests:
            md.append("## 7. Dependências da Realidade & Testes Empíricos Necessários\n")
            if self.reality_dependencies:
                md.append("**Dependências Externas:**")
                for dep in self.reality_dependencies:
                    md.append(f"- {dep}")
            if self.candidate_tests:
                md.append("\n**Testes Discriminativos Sugeridos:**")
                for tst in self.candidate_tests:
                    md.append(f"- [ ] {tst}")
            md.append("\n")

        md.append("## 8. Próximo Passo Recomendado\n")
        md.append(f"{self.recommended_next_step or 'Definir próximo experimento com usuários.'}\n")

        return "\n".join(md)
