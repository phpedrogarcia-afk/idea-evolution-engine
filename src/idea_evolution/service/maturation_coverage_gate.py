"""Deterministic M3 checks for explicit maturation coverage in M1 artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.idea_evolution.artifacts.evolution_artifact import (
    CoverageIssue,
    CoverageIssueType,
    CoverageStatus,
    EvolutionArtifact,
    IntentImportance,
    IntentTreatmentStatus,
    SCHEMA_VERSION_1_1,
)


@dataclass(frozen=True)
class MaturationCoverageEvaluation:
    """Result of structural checks; a clean result is not semantic proof."""

    status: CoverageStatus
    issues: tuple[CoverageIssue, ...]


class MaturationCoverageGate:
    """Collect only demonstrable structural coverage defects from a typed artifact."""

    @classmethod
    def evaluate(cls, artifact: EvolutionArtifact) -> MaturationCoverageEvaluation:
        if artifact.schema_version != SCHEMA_VERSION_1_1:
            raise ValueError("MaturationCoverageGate evaluates only newly produced schema 1.1 artifacts.")
        if artifact.coverage_status != CoverageStatus.NOT_EVALUATED or artifact.coverage_issues:
            raise ValueError("MaturationCoverageGate requires a fresh NOT_EVALUATED artifact.")

        issues: list[CoverageIssue] = []
        seen: set[tuple[CoverageIssueType, Optional[str], Optional[str]]] = set()
        intent_ids = {item.intent_id for item in artifact.intent_ledger}

        def add_issue(
            issue_type: CoverageIssueType,
            description: str,
            *,
            intent_id: Optional[str] = None,
            path_id: Optional[str] = None,
        ) -> None:
            # One issue of a given type per structured subject is enough for M4;
            # the key also collapses the core-intent check with the ledger check.
            key = (issue_type, intent_id, path_id)
            if key in seen:
                return
            seen.add(key)
            issues.append(CoverageIssue(
                issue_type=issue_type,
                description=description,
                intent_id=intent_id,
                path_id=path_id,
            ))

        def untreated_issue_type(importance: IntentImportance) -> CoverageIssueType:
            if importance == IntentImportance.EXPLICIT_CONSTRAINT:
                return CoverageIssueType.EXPLICIT_CONSTRAINT_UNTREATED
            return CoverageIssueType.MATERIAL_INTENT_UNTREATED

        # Ledger values and their enumerated status are typed upstream. Here we
        # check the coverage-bearing fields without interpreting their prose.
        for item in artifact.intent_ledger:
            issue_type = untreated_issue_type(item.importance)
            if not item.interpretation.strip():
                add_issue(
                    issue_type,
                    f"Intent {item.intent_id} has no non-empty structured interpretation.",
                    intent_id=item.intent_id,
                )
            if not item.treatment_in_current_form.strip():
                add_issue(
                    issue_type,
                    f"Intent {item.intent_id} has no explicit treatment in current_form.",
                    intent_id=item.intent_id,
                )

            if item.status == IntentTreatmentStatus.CONFLICT_FOUND:
                add_issue(
                    CoverageIssueType.CONFLICT_FOUND,
                    f"Intent {item.intent_id} is explicitly marked CONFLICT_FOUND.",
                    intent_id=item.intent_id,
                )
            elif item.status in (
                IntentTreatmentStatus.PROVISIONALLY_MODIFIED,
                IntentTreatmentStatus.DEFERRED,
            ):
                exposed = any(
                    decision.question.strip() and item.intent_id in decision.related_intent_ids
                    for decision in artifact.open_decisions
                )
                if not exposed:
                    exposure_issue = (
                        CoverageIssueType.PROVISIONAL_MODIFICATION_NOT_EXPOSED
                        if item.status == IntentTreatmentStatus.PROVISIONALLY_MODIFIED
                        else CoverageIssueType.DEFERRED_ITEM_NOT_EXPOSED
                    )
                    add_issue(
                        exposure_issue,
                        f"Intent {item.intent_id} has no non-empty open_decision linked by intent ID.",
                        intent_id=item.intent_id,
                    )

        # Candidate paths count only through explicit, valid intent references.
        for path in artifact.candidate_possibilities:
            refs = path.intent_ids
            invalid = sorted(set(refs) - intent_ids)
            duplicate_refs = len(refs) != len(set(refs))
            if not refs or invalid or duplicate_refs:
                detail = "has no intent references" if not refs else "has invalid or duplicate intent references"
                add_issue(
                    CoverageIssueType.INTENT_REFERENCE_INVALID,
                    f"Candidate path {path.path_id or '[without path_id]'} {detail}.",
                    path_id=path.path_id,
                )
            if not path.mechanism.strip():
                add_issue(
                    CoverageIssueType.STRUCTURAL_COVERAGE_FAILURE,
                    f"Candidate path {path.path_id or '[without path_id]'} has an empty mechanism.",
                    path_id=path.path_id,
                )

        core_items = [item for item in artifact.intent_ledger if item.importance == IntentImportance.CORE_INTENT]
        if not core_items:
            add_issue(
                CoverageIssueType.STRUCTURAL_COVERAGE_FAILURE,
                "The structured intent ledger contains no CORE_INTENT.",
            )
        else:
            for item in core_items:
                addressed_by_path = any(
                    item.intent_id in path.intent_ids and path.mechanism.strip()
                    for path in artifact.candidate_possibilities
                )
                addressed_in_current_form = bool(
                    artifact.refined_idea.strip() and item.treatment_in_current_form.strip()
                )
                if not addressed_by_path and not addressed_in_current_form:
                    add_issue(
                        CoverageIssueType.MATERIAL_INTENT_UNTREATED,
                        f"CORE_INTENT {item.intent_id} has no structured path or current_form treatment.",
                        intent_id=item.intent_id,
                    )

        if not artifact.refined_idea.strip():
            add_issue(
                CoverageIssueType.CURRENT_FORM_REFERENCE_GAP,
                "The current form is empty.",
            )

        target = artifact.recommended_next_action_target_uncertainty
        if target is not None and (not target.strip() or target not in artifact.uncertainties):
            add_issue(
                CoverageIssueType.STRUCTURAL_COVERAGE_FAILURE,
                "The next action references a missing or empty uncertainty target.",
            )

        status = CoverageStatus.REPAIR_REQUIRED if issues else CoverageStatus.NO_BLOCKING_GAP_DETECTED
        return MaturationCoverageEvaluation(status=status, issues=tuple(issues))

    @classmethod
    def apply(cls, artifact: EvolutionArtifact) -> EvolutionArtifact:
        """Return a newly validated artifact; never mutate the mapper's input."""
        result = cls.evaluate(artifact)
        payload = artifact.model_dump(mode="python")
        payload["coverage_status"] = result.status
        payload["coverage_issues"] = list(result.issues)
        return EvolutionArtifact.model_validate(payload)
