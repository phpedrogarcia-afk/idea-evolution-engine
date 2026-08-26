"""
src/idea_evolution/stages/contracts.py
Contratos tipados Pydantic para os outputs estruturados de cada estágio do pipeline com proveniência de promoção e integridade ontológica.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class UnderstandOutput(BaseModel):
    interpreted_problem: str
    human_intent: str
    proposed_mechanism: str = ""
    explicit_mechanism: str = ""
    inferred_candidates: List[str] = Field(default_factory=list)
    actors_or_users: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    ambiguities: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    structured_idea: str


class IssueDetail(BaseModel):
    issue: str
    why_it_matters: str
    severity: str = "MEDIUM"
    affected_part: str = ""


class AttackOutput(BaseModel):
    critical_issues: List[IssueDetail] = Field(default_factory=list)
    fragile_assumptions: List[str] = Field(default_factory=list)
    contradictions: List[str] = Field(default_factory=list)
    failure_modes: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    overclaims: List[str] = Field(default_factory=list)


class CritiqueOutput(BaseModel):
    critical_issues: List[IssueDetail] = Field(default_factory=list)
    fragile_assumptions: List[str] = Field(default_factory=list)
    contradictions: List[str] = Field(default_factory=list)
    failure_modes: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)


class RevisionOutput(BaseModel):
    revised_idea: str
    changes_applied: List[str] = Field(default_factory=list)
    issues_addressed: List[str] = Field(default_factory=list)
    intent_preserved: bool = True
    justification: str = ""


class AlternativeItem(BaseModel):
    mechanism: str
    addresses_issues: List[str] = Field(default_factory=list)
    preserves_intent: bool = True
    tradeoffs: List[str] = Field(default_factory=list)
    novelty_or_difference: str = ""


class AlternativesOutput(BaseModel):
    alternatives: List[AlternativeItem] = Field(default_factory=list)


class RealityCheckOutput(BaseModel):
    feasibility_notes: List[str] = Field(default_factory=list)
    reality_dependencies: List[str] = Field(default_factory=list)
    claims_needing_evidence: List[str] = Field(default_factory=list)
    potential_blockers: List[str] = Field(default_factory=list)
    candidate_tests: List[str] = Field(default_factory=list)
    exploratory_candidate_tests: List[str] = Field(default_factory=list)


class RejectedItem(BaseModel):
    proposal: str
    reason_rejected: str
    source_stage: str = ""


class AcceptedChangeItem(BaseModel):
    proposal: str
    promotion_reason: str
    source_stage: str = "ALTERNATIVES"
    evidence_or_decision_basis: str = ""


class SynthesizeOutput(BaseModel):
    refined_idea: str
    core_mechanism: str = ""
    core_mechanism_justification: str = ""
    accepted_changes: List[AcceptedChangeItem] = Field(default_factory=list)
    candidate_possibilities: List[str] = Field(default_factory=list)
    rejected_changes: List[RejectedItem] = Field(default_factory=list)
    remaining_uncertainties: List[str] = Field(default_factory=list)
    known_risks: List[str] = Field(default_factory=list)
    recommended_next_step: str = ""


class FinalReviewOutput(BaseModel):
    material_issues_remaining: List[str] = Field(default_factory=list)
    essence_drift_detected: bool = False
    speculative_accretion_detected: bool = False
    ontology_contradiction_detected: bool = False
    drift_explanation: str = ""
    unresolved_critical_issue: bool = False
    recommendation: str = "REFINED_IDEA_READY"  # REFINED_IDEA_READY | RECONSTRUCT
    review_summary: str = ""


class BaselineRefineOutput(BaseModel):
    summary: str
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    refined_version: str
    next_steps: List[str] = Field(default_factory=list)
