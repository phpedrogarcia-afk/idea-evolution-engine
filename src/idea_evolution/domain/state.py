"""
src/idea_evolution/domain/state.py
Domínio e Estado Mínimo Compartilhado (SimpleIdeaState) do IEE MVP com ontologia tipada, proveniência de autoridade e linhagem referencial.
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


class OntologyState(str, Enum):
    CORE = "CORE"
    DERIVED = "DERIVED"
    CANDIDATE = "CANDIDATE"
    DEFERRED = "DEFERRED"
    REJECTED = "REJECTED"


class PromotionAuthorityBasis(str, Enum):
    """Bases de autoridade admissíveis para promoção ao Core ou Derived."""
    USER_EXPLICIT = "USER_EXPLICIT"
    VALID_USER_DERIVATION = "VALID_USER_DERIVATION"
    EXTERNAL_EVIDENCE = "EXTERNAL_EVIDENCE"
    HUMAN_DECISION = "HUMAN_DECISION"
    MODEL_HYPOTHESIS = "MODEL_HYPOTHESIS"  # Inadmissível isoladamente para promoção ao CORE


class ProposalRecord(BaseModel):
    """
    Registro canônico de uma proposta / mecanismo no pipeline com proveniência e estado ontológico estáveis.
    """
    proposal: str
    ontology_state: OntologyState = OntologyState.CANDIDATE
    source_stage: str = ""
    promotion_reason: str = ""
    promotion_basis: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
    rejection_reason: str = ""
    evidence_or_decision_basis: str = ""


class CriticalIssue(BaseModel):
    issue: str
    why_it_matters: str
    severity: str = "MEDIUM"  # HIGH | MEDIUM | LOW
    affected_part: str = ""
    origin: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS


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
    logical_alias: str = ""
    prompt_id: str = ""
    prompt_version: str = ""
    attempt: int = 1
    success: bool
    retry_count: int = 0
    delta_summary: str = ""


class SimpleIdeaState(BaseModel):
    schema_version: str = "0.3.0"
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

    # Exploração
    alternatives: List[AlternativeMechanism] = Field(default_factory=list)

    # Síntese e Revisão com Linhagem Estável
    core_mechanism: str = ""
    core_mechanism_justification: str = ""
    core_mechanism_basis: PromotionAuthorityBasis = PromotionAuthorityBasis.MODEL_HYPOTHESIS
    core_mechanism_hash: str = ""  # Hash referencial do core aceito
    proposal_records: List[ProposalRecord] = Field(default_factory=list)
    accepted_changes: List[str] = Field(default_factory=list)
    candidate_extensions: List[str] = Field(default_factory=list)
    rejected_changes: List[RejectedProposal] = Field(default_factory=list)
    remaining_uncertainties: List[str] = Field(default_factory=list)
    known_risks: List[str] = Field(default_factory=list)
    recommended_next_step: str = ""

    # Realidade Pós-Síntese (Testa estritamente o CORE sintetizado)
    tested_core_mechanism: str = ""
    tested_core_hash: str = ""
    reality_dependencies: List[str] = Field(default_factory=list)  # Apenas dependências do CORE aceito
    claims_needing_evidence: List[str] = Field(default_factory=list)
    candidate_tests: List[str] = Field(default_factory=list)  # Apenas testes do CORE aceito
    exploratory_candidate_tests: List[str] = Field(default_factory=list)  # Testes de extensões candidatas / rejeitadas

    # Governança do Loop
    reconstruction_count: int = 0
    max_reconstructions: int = 1
    essence_drift_detected: bool = False
    speculative_accretion_detected: bool = False
    ontology_contradiction_detected: bool = False
    human_intervention: bool = False
    stage_history: List[StageHistoryEntry] = Field(default_factory=list)

    def record_stage_execution(
        self,
        stage_id: str,
        stage_version: str,
        provider: str,
        model: str,
        success: bool,
        logical_alias: str = "",
        prompt_id: str = "",
        prompt_version: str = "",
        attempt: int = 1,
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
                logical_alias=logical_alias,
                prompt_id=prompt_id,
                prompt_version=prompt_version,
                attempt=attempt,
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
        if self.core_mechanism_justification:
            md.append(f"- **Justificativa de Promoção ao Core:** {self.core_mechanism_justification} (Base: `{self.core_mechanism_basis.value}`)\n\n")

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

        if self.candidate_extensions:
            md.append("## 6. Possibilidades Candidatas (Não Incorporadas ao Core)\n")
            for idx, cand in enumerate(self.candidate_extensions, 1):
                md.append(f"{idx}. *[CANDIDATE]* {cand}")
            md.append("\n")

        if self.rejected_changes:
            md.append("## 7. Propostas Rejeitadas (com Justificativa)\n")
            for rej in self.rejected_changes:
                md.append(f"- **Rejeitado:** {rej.proposal} (Origem: {rej.source_stage})")
                md.append(f"  *Motivo:* {rej.reason_rejected}")
            md.append("\n")

        if self.reality_dependencies or self.candidate_tests:
            md.append(f"## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: {self.tested_core_mechanism or self.core_mechanism})\n")
            if self.reality_dependencies:
                md.append("**Dependências Externas do Core:**")
                for dep in self.reality_dependencies:
                    md.append(f"- {dep}")
            if self.candidate_tests:
                md.append("\n**Testes Discriminativos do Core:**")
                for tst in self.candidate_tests:
                    md.append(f"- [ ] {tst}")
            md.append("\n")

        if self.exploratory_candidate_tests:
            md.append("## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)\n")
            for tst in self.exploratory_candidate_tests:
                md.append(f"- [ ] *[EXPLORATÓRIO]* {tst}")
            md.append("\n")

        md.append("## 10. Próximo Passo Recomendado\n")
        md.append(f"{self.recommended_next_step or 'Definir próximo experimento com usuários.'}\n")

        return "\n".join(md)
