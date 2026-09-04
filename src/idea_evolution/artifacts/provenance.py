"""
src/idea_evolution/artifacts/provenance.py
Recibo de auditoria determinística de proveniência e ontologia do FioIdeias V1 (M06 P3).

Garante conformidade com o princípio fundamental:
USER_EXPLICIT != VALID_USER_DERIVATION != MODEL_CANDIDATE != UNKNOWN

Custo de execução = 0 chamadas de modelo.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from pydantic import BaseModel, Field
from src.idea_evolution.domain.state import PromotionAuthorityBasis, OntologyState

if TYPE_CHECKING:
    from src.idea_evolution.artifacts.evolution_artifact import EvolutionArtifact


class ProvenanceReceipt(BaseModel):
    """
    Recibo determinístico de completude e integridade da proveniência de um EvolutionArtifact.
    Classifica exclusivamente itens semânticos de produto (não metadados técnicos).
    """
    user_explicit_count: int = 0
    valid_derivation_count: int = 0
    model_candidate_count: int = 0
    unknown_count: int = 0
    rejected_count: int = 0
    deferred_count: int = 0
    unlabeled_semantic_item_count: int = 0
    audit_timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

    @property
    def total_audited_items(self) -> int:
        return (
            self.user_explicit_count
            + self.valid_derivation_count
            + self.model_candidate_count
            + self.unknown_count
            + self.rejected_count
            + self.deferred_count
            + self.unlabeled_semantic_item_count
        )

    @property
    def is_epistemically_safe(self) -> bool:
        """Seguro se não houver itens semânticos sem rótulo de autoridade."""
        return self.unlabeled_semantic_item_count == 0


def audit_artifact_provenance(artifact: EvolutionArtifact) -> ProvenanceReceipt:
    """
    Audita exaustivamente a proveniência dos itens semânticos de um EvolutionArtifact.
    Garante que nenhum item semântico do produto permaneça sem classe de autoridade.
    Custo de IA = 0 chamadas.
    """
    user_explicit = 0
    valid_derivation = 0
    model_candidate = 0
    unknown_count = 0
    rejected_count = 0
    deferred_count = 0
    unlabeled = 0

    # 1. Ideia Original do Usuário (Entrada Humana)
    orig_auth = getattr(artifact, "original_idea_authority", PromotionAuthorityBasis.USER_EXPLICIT)
    if orig_auth == PromotionAuthorityBasis.USER_EXPLICIT:
        user_explicit += 1
    elif orig_auth == PromotionAuthorityBasis.VALID_USER_DERIVATION:
        valid_derivation += 1
    elif orig_auth is None:
        unlabeled += 1
    else:
        unlabeled += 1

    # 2. Intenção Humana Interpretada
    if artifact.intent_provenance == PromotionAuthorityBasis.VALID_USER_DERIVATION:
        valid_derivation += 1
    elif artifact.intent_provenance == PromotionAuthorityBasis.USER_EXPLICIT:
        user_explicit += 1
    elif artifact.intent_provenance is None:
        unlabeled += 1
    else:
        unlabeled += 1

    # 3. Ideia Refinada Proposta pelo Sistema
    refined_auth = getattr(artifact, "refined_idea_authority", PromotionAuthorityBasis.MODEL_HYPOTHESIS)
    if refined_auth == PromotionAuthorityBasis.MODEL_HYPOTHESIS:
        model_candidate += 1
    elif refined_auth == PromotionAuthorityBasis.VALID_USER_DERIVATION:
        valid_derivation += 1
    elif refined_auth == PromotionAuthorityBasis.USER_EXPLICIT:
        user_explicit += 1
    elif refined_auth is None:
        unlabeled += 1
    else:
        unlabeled += 1

    # 4. Itens de Crítica e Vulnerabilidade
    for crit in artifact.critique:
        crit_auth = getattr(crit, "authority_basis", PromotionAuthorityBasis.MODEL_HYPOTHESIS)
        if crit_auth == PromotionAuthorityBasis.MODEL_HYPOTHESIS:
            model_candidate += 1
        elif crit_auth == PromotionAuthorityBasis.USER_EXPLICIT:
            user_explicit += 1
        elif crit_auth is None:
            unlabeled += 1
        else:
            model_candidate += 1

    # 5. Premissas Identificadas (Assumptions)
    assump_auth = getattr(artifact, "assumptions_authority", PromotionAuthorityBasis.MODEL_HYPOTHESIS)
    for _ in artifact.assumptions:
        if assump_auth == PromotionAuthorityBasis.MODEL_HYPOTHESIS:
            model_candidate += 1
        elif assump_auth == PromotionAuthorityBasis.USER_EXPLICIT:
            user_explicit += 1
        elif assump_auth is None:
            unlabeled += 1
        else:
            unlabeled += 1

    # 6. Incertezas / Lacunas Epistêmicas (Uncertainties / Unknowns)
    for _ in artifact.uncertainties:
        unknown_count += 1

    # 7. Possibilidades / Candidatos Propostos
    for cand in artifact.candidate_possibilities:
        cand_state = getattr(cand, "ontology_state", OntologyState.CANDIDATE)
        if cand_state == OntologyState.REJECTED:
            rejected_count += 1
        elif cand_state == OntologyState.DEFERRED:
            deferred_count += 1
        elif cand.authority_basis == PromotionAuthorityBasis.MODEL_HYPOTHESIS:
            model_candidate += 1
        elif cand.authority_basis == PromotionAuthorityBasis.VALID_USER_DERIVATION:
            valid_derivation += 1
        elif cand.authority_basis == PromotionAuthorityBasis.USER_EXPLICIT:
            user_explicit += 1
        elif cand.authority_basis is None:
            unlabeled += 1
        else:
            unlabeled += 1

    return ProvenanceReceipt(
        user_explicit_count=user_explicit,
        valid_derivation_count=valid_derivation,
        model_candidate_count=model_candidate,
        unknown_count=unknown_count,
        rejected_count=rejected_count,
        deferred_count=deferred_count,
        unlabeled_semantic_item_count=unlabeled,
    )
