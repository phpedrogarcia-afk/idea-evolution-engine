"""One bounded, typed repair for deterministic M3 coverage gaps."""

from __future__ import annotations

import json
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from src.idea_evolution.artifacts.evolution_artifact import (
    CoverageIssue,
    CoverageIssueType,
    CoverageStatus,
    EvolutionArtifact,
    IntentTreatmentStatus,
    OpenDecision,
    SCHEMA_VERSION_1_1,
)


class _ClosedPatchModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class IntentTreatmentRepair(_ClosedPatchModel):
    intent_id: str = Field(min_length=1)
    treatment_in_current_form: Optional[str] = None
    status: Optional[IntentTreatmentStatus] = None

    @field_validator("intent_id")
    @classmethod
    def nonblank_intent_id(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("intent_id must not be blank")
        return value

    @field_validator("treatment_in_current_form")
    @classmethod
    def nonblank_treatment_when_supplied(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("treatment_in_current_form must not be blank")
        return value

    @model_validator(mode="after")
    def has_edit(self) -> IntentTreatmentRepair:
        if not ({"treatment_in_current_form", "status"} & self.model_fields_set):
            raise ValueError("intent repair must change a permitted field")
        return self


class CandidatePathRepair(_ClosedPatchModel):
    path_id: str = Field(min_length=1)
    intent_ids: Optional[list[str]] = None
    mechanism: Optional[str] = None

    @field_validator("path_id")
    @classmethod
    def nonblank_path_id(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("path_id must not be blank")
        return value

    @field_validator("mechanism")
    @classmethod
    def nonblank_mechanism_when_supplied(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("mechanism must not be blank")
        return value

    @field_validator("intent_ids")
    @classmethod
    def valid_intent_ids(cls, value: Optional[list[str]]) -> Optional[list[str]]:
        if value is None:
            return value
        if not value or any(not item.strip() for item in value):
            raise ValueError("intent_ids must contain nonblank identifiers")
        if len(value) != len(set(value)):
            raise ValueError("intent_ids must be unique")
        return value

    @model_validator(mode="after")
    def has_edit(self) -> CandidatePathRepair:
        if not ({"intent_ids", "mechanism"} & self.model_fields_set):
            raise ValueError("path repair must change a permitted field")
        return self


class OpenDecisionRepair(_ClosedPatchModel):
    related_intent_id: str = Field(min_length=1)
    question: str = Field(min_length=1)
    target_decision_id: Optional[str] = None

    @field_validator("related_intent_id", "question")
    @classmethod
    def nonblank_values(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("decision repair values must not be blank")
        return value

    @field_validator("target_decision_id")
    @classmethod
    def nonblank_target_when_supplied(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("target_decision_id must not be blank")
        return value


class MaturationRepairPatch(_ClosedPatchModel):
    """Only coverage-bearing fields are expressible; authority fields are absent."""

    intent_repairs: list[IntentTreatmentRepair] = Field(default_factory=list)
    path_repairs: list[CandidatePathRepair] = Field(default_factory=list)
    open_decision_repairs: list[OpenDecisionRepair] = Field(default_factory=list)
    refined_idea: Optional[str] = None
    # Omission means unchanged; explicit null removes an invalid optional link.
    recommended_next_action_target_uncertainty: Optional[str] = None

    @field_validator("refined_idea")
    @classmethod
    def nonblank_refined_idea_when_supplied(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("refined_idea must not be blank")
        return value

    @field_validator("recommended_next_action_target_uncertainty")
    @classmethod
    def nonblank_uncertainty_when_supplied(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("uncertainty target must be nonblank or null")
        return value

    @model_validator(mode="after")
    def has_operation(self) -> MaturationRepairPatch:
        if not (
            self.intent_repairs
            or self.path_repairs
            or self.open_decision_repairs
            or "refined_idea" in self.model_fields_set
            or "recommended_next_action_target_uncertainty" in self.model_fields_set
        ):
            raise ValueError("repair patch must contain at least one operation")
        if len({item.intent_id for item in self.intent_repairs}) != len(self.intent_repairs):
            raise ValueError("duplicate intent repair target")
        if len({item.path_id for item in self.path_repairs}) != len(self.path_repairs):
            raise ValueError("duplicate path repair target")
        decision_targets = [item.target_decision_id for item in self.open_decision_repairs if item.target_decision_id]
        if len(decision_targets) != len(set(decision_targets)):
            raise ValueError("duplicate open-decision repair target")
        return self


class RepairPatchRejected(ValueError):
    """A repair is rejected atomically; no partial candidate escapes."""


class MaturationFocusedRepair:
    """Build a minimal repair request and atomically apply its closed patch."""

    _INTENT_ISSUES = {
        CoverageIssueType.MATERIAL_INTENT_UNTREATED,
        CoverageIssueType.EXPLICIT_CONSTRAINT_UNTREATED,
        CoverageIssueType.CONFLICT_FOUND,
        CoverageIssueType.PROVISIONAL_MODIFICATION_NOT_EXPOSED,
        CoverageIssueType.DEFERRED_ITEM_NOT_EXPOSED,
    }

    @staticmethod
    def build_prompt(artifact: EvolutionArtifact, issues: list[CoverageIssue]) -> str:
        """Include only the frozen evidence and current structures needed for repair."""
        context = {
            "original_idea": artifact.original_idea,
            "human_intent": artifact.human_intent,
            "current_form": artifact.refined_idea,
            "intent_ledger": [item.model_dump(mode="json") for item in artifact.intent_ledger],
            "candidate_paths": [
                {
                    "path_id": item.path_id,
                    "mechanism": item.mechanism,
                    "intent_ids": item.intent_ids,
                    "authority_basis": item.authority_basis.value,
                }
                for item in artifact.candidate_possibilities
            ],
            "open_decisions": [item.model_dump(mode="json") for item in artifact.open_decisions],
            "uncertainties": artifact.uncertainties,
            "next_action_uncertainty_target": artifact.recommended_next_action_target_uncertainty,
            "coverage_issues": [item.model_dump(mode="json") for item in issues],
        }
        return (
            "Repare somente os defeitos estruturais de cobertura listados. "
            "Não reinicie a ideação, não reescreva a ideia do usuário e preserve todo material válido não implicado. "
            "Retorne apenas um MaturationRepairPatch válido, sem campos extras. Use os IDs estruturais exatos. "
            "Citações USER_EXPLICIT, identidade dos intents, proveniência, autoridade humana, identidade do run, "
            "histórico do provedor e hash científico são imutáveis e não podem ser editados. "
            "Mecanismos continuam MODEL_HYPOTHESIS; não invente evidência USER_EXPLICIT, autoridade humana ou precisão. "
            "Uma decisão aberta não é solicitação de decisão humana. Se houver conflito não resolvido, exponha-o; "
            "não o apague apenas para limpar o gate. Para decisão nova, omita target_decision_id; a aplicação gera ID.\n\n"
            "CONTEXTO ESTRUTURADO MÍNIMO:\n"
            + json.dumps(context, ensure_ascii=False, separators=(",", ":"))
        )

    @classmethod
    def apply_patch(
        cls,
        artifact: EvolutionArtifact,
        patch: MaturationRepairPatch,
        issues: list[CoverageIssue],
    ) -> EvolutionArtifact:
        """Build and validate a complete candidate, resetting only M3's evaluation fields."""
        if artifact.schema_version != SCHEMA_VERSION_1_1:
            raise RepairPatchRejected("only schema 1.1 artifacts are repairable")
        if not issues:
            raise RepairPatchRejected("a repair requires at least one blocking issue")

        payload = artifact.model_dump(mode="python")
        issue_types_by_intent: dict[str, set[CoverageIssueType]] = {}
        issue_types_by_path: dict[str, set[CoverageIssueType]] = {}
        for issue in issues:
            if issue.intent_id is not None:
                issue_types_by_intent.setdefault(issue.intent_id, set()).add(issue.issue_type)
            if issue.path_id is not None:
                issue_types_by_path.setdefault(issue.path_id, set()).add(issue.issue_type)

        intent_by_id = {item["intent_id"]: item for item in payload["intent_ledger"]}
        known_intents = set(intent_by_id)
        for operation in patch.intent_repairs:
            item = intent_by_id.get(operation.intent_id)
            if item is None:
                raise RepairPatchRejected(f"unknown intent target: {operation.intent_id}")
            issue_types = issue_types_by_intent.get(operation.intent_id, set())
            if not (issue_types & cls._INTENT_ISSUES):
                raise RepairPatchRejected(f"intent target is not linked to a blocking issue: {operation.intent_id}")

            if "treatment_in_current_form" in operation.model_fields_set:
                if not issue_types & {
                    CoverageIssueType.MATERIAL_INTENT_UNTREATED,
                    CoverageIssueType.EXPLICIT_CONSTRAINT_UNTREATED,
                    CoverageIssueType.CONFLICT_FOUND,
                }:
                    raise RepairPatchRejected("treatment edit is unrelated to the target issue")
                item["treatment_in_current_form"] = operation.treatment_in_current_form

            if "status" in operation.model_fields_set:
                old_status = IntentTreatmentStatus(item["status"])
                new_status = operation.status
                if new_status is None:
                    raise RepairPatchRejected("intent status cannot be null")
                if old_status == IntentTreatmentStatus.CONFLICT_FOUND:
                    if CoverageIssueType.CONFLICT_FOUND not in issue_types:
                        raise RepairPatchRejected("conflict status lacks its linked conflict issue")
                    if new_status == IntentTreatmentStatus.CONFLICT_FOUND:
                        raise RepairPatchRejected("a conflict status edit must actually resolve or defer the conflict")
                    if (
                        "treatment_in_current_form" not in operation.model_fields_set
                        or not operation.treatment_in_current_form
                        or not operation.treatment_in_current_form.strip()
                    ):
                        raise RepairPatchRejected("resolving a conflict requires explicit treatment")
                    if new_status in (
                        IntentTreatmentStatus.PROVISIONALLY_MODIFIED,
                        IntentTreatmentStatus.DEFERRED,
                    ) and not any(
                        decision.related_intent_id == operation.intent_id
                        for decision in patch.open_decision_repairs
                    ):
                        raise RepairPatchRejected("provisional/deferred conflict repair requires a linked open decision")
                elif old_status == IntentTreatmentStatus.DEFERRED:
                    if new_status != old_status and not (
                        bool(issue_types & {
                            CoverageIssueType.MATERIAL_INTENT_UNTREATED,
                            CoverageIssueType.EXPLICIT_CONSTRAINT_UNTREATED,
                        })
                        and
                        "treatment_in_current_form" in operation.model_fields_set
                        and operation.treatment_in_current_form
                        and new_status in (IntentTreatmentStatus.PRESERVED, IntentTreatmentStatus.EXPANDED)
                    ):
                        raise RepairPatchRejected("a deferred intent needs an explicit treatment before reclassification")
                elif old_status == IntentTreatmentStatus.PROVISIONALLY_MODIFIED and new_status != old_status:
                    raise RepairPatchRejected("a provisional modification cannot be silently reclassified")
                item["status"] = new_status

        paths = {item.get("path_id"): item for item in payload["candidate_possibilities"]}
        for operation in patch.path_repairs:
            item = paths.get(operation.path_id)
            if item is None:
                raise RepairPatchRejected(f"unknown candidate path target: {operation.path_id}")
            issue_types = issue_types_by_path.get(operation.path_id, set())
            if not issue_types & {
                CoverageIssueType.INTENT_REFERENCE_INVALID,
                CoverageIssueType.STRUCTURAL_COVERAGE_FAILURE,
            }:
                raise RepairPatchRejected(f"candidate path has no repairable linked issue: {operation.path_id}")
            if "intent_ids" in operation.model_fields_set:
                if CoverageIssueType.INTENT_REFERENCE_INVALID not in issue_types:
                    raise RepairPatchRejected("intent reference edit is unrelated to the path issue")
                if operation.intent_ids is None or not operation.intent_ids or not set(operation.intent_ids) <= known_intents:
                    raise RepairPatchRejected("candidate path references must be known and non-empty")
                item["intent_ids"] = operation.intent_ids
            if "mechanism" in operation.model_fields_set:
                if CoverageIssueType.STRUCTURAL_COVERAGE_FAILURE not in issue_types:
                    raise RepairPatchRejected("mechanism edit is unrelated to the path issue")
                if item["mechanism"].strip():
                    raise RepairPatchRejected("a valid existing path mechanism must be preserved")
                item["mechanism"] = operation.mechanism

        decisions = payload["open_decisions"]
        decisions_by_id = {item["decision_id"]: item for item in decisions}
        for operation in patch.open_decision_repairs:
            if operation.related_intent_id not in known_intents:
                raise RepairPatchRejected(f"unknown intent target for open decision: {operation.related_intent_id}")
            issue_types = issue_types_by_intent.get(operation.related_intent_id, set())
            transition_exposes_conflict = any(
                intent_repair.intent_id == operation.related_intent_id
                and intent_repair.status in (
                    IntentTreatmentStatus.PROVISIONALLY_MODIFIED,
                    IntentTreatmentStatus.DEFERRED,
                )
                and CoverageIssueType.CONFLICT_FOUND in issue_types
                for intent_repair in patch.intent_repairs
            )
            if not transition_exposes_conflict and not issue_types & {
                CoverageIssueType.PROVISIONAL_MODIFICATION_NOT_EXPOSED,
                CoverageIssueType.DEFERRED_ITEM_NOT_EXPOSED,
            }:
                raise RepairPatchRejected("open decision is unrelated to a provisional/deferred coverage issue")
            if operation.target_decision_id is None:
                index = 1
                while f"M4-DECISION-{index:03d}" in decisions_by_id:
                    index += 1
                decision_id = f"M4-DECISION-{index:03d}"
                decision = {
                    "decision_id": decision_id,
                    "question": operation.question,
                    "related_intent_ids": [operation.related_intent_id],
                }
                decisions.append(decision)
                decisions_by_id[decision_id] = decision
            else:
                decision = decisions_by_id.get(operation.target_decision_id)
                if decision is None:
                    raise RepairPatchRejected(f"unknown open-decision target: {operation.target_decision_id}")
                decision["question"] = operation.question
                if operation.related_intent_id not in decision["related_intent_ids"]:
                    decision["related_intent_ids"].append(operation.related_intent_id)

        if "refined_idea" in patch.model_fields_set:
            may_update_form = any(
                issue.issue_type == CoverageIssueType.CURRENT_FORM_REFERENCE_GAP
                for issue in issues
            ) or any(
                issue.issue_type in {
                    CoverageIssueType.MATERIAL_INTENT_UNTREATED,
                    CoverageIssueType.EXPLICIT_CONSTRAINT_UNTREATED,
                    CoverageIssueType.CONFLICT_FOUND,
                }
                for issue in issues
            )
            if not may_update_form or patch.refined_idea is None:
                raise RepairPatchRejected("current-form edit is absent or unrelated to a coverage issue")
            payload["refined_idea"] = patch.refined_idea

        if "recommended_next_action_target_uncertainty" in patch.model_fields_set:
            old_target = artifact.recommended_next_action_target_uncertainty
            if old_target is None or (old_target.strip() and old_target in artifact.uncertainties):
                raise RepairPatchRejected("next-action uncertainty target is not currently invalid")
            new_target = patch.recommended_next_action_target_uncertainty
            if new_target is not None and new_target not in artifact.uncertainties:
                raise RepairPatchRejected("next-action target must reference an existing uncertainty or be null")
            payload["recommended_next_action_target_uncertainty"] = new_target

        # The candidate is validated from the original in one construction. Old M3
        # findings are intentionally discarded only for this fresh deterministic pass.
        payload["coverage_status"] = CoverageStatus.NOT_EVALUATED
        payload["coverage_issues"] = []
        try:
            candidate = EvolutionArtifact.model_validate(payload)
        except Exception as exc:
            raise RepairPatchRejected(f"candidate validation failed: {type(exc).__name__}") from exc

        cls._assert_only_permitted_fields_changed(artifact, candidate, patch)
        return candidate

    @staticmethod
    def mark_unresolved(
        artifact: EvolutionArtifact,
        issues: list[CoverageIssue],
        logical_model_calls_used: int,
    ) -> EvolutionArtifact:
        payload = artifact.model_dump(mode="python")
        payload["coverage_status"] = CoverageStatus.UNRESOLVED
        payload["coverage_issues"] = issues
        payload["total_model_calls"] = logical_model_calls_used
        return EvolutionArtifact.model_validate(payload)

    @staticmethod
    def _assert_only_permitted_fields_changed(
        original: EvolutionArtifact,
        candidate: EvolutionArtifact,
        patch: MaturationRepairPatch,
    ) -> None:
        before = original.model_dump(mode="python")
        after = candidate.model_dump(mode="python")
        mutable_top_level = {
            "refined_idea",
            "intent_ledger",
            "candidate_possibilities",
            "open_decisions",
            "recommended_next_action_target_uncertainty",
            "coverage_status",
            "coverage_issues",
        }
        for key in before.keys() - mutable_top_level:
            if before[key] != after[key]:
                raise RepairPatchRejected(f"immutable artifact field changed: {key}")

        intent_mutable = {item.intent_id: item.model_fields_set for item in patch.intent_repairs}
        if len(before["intent_ledger"]) != len(after["intent_ledger"]):
            raise RepairPatchRejected("intent ledger identity/size changed")
        for old, new in zip(before["intent_ledger"], after["intent_ledger"]):
            if old["intent_id"] != new["intent_id"]:
                raise RepairPatchRejected("intent identity changed")
            allowed = intent_mutable.get(old["intent_id"], set())
            for key in old.keys() - allowed:
                if old[key] != new[key]:
                    raise RepairPatchRejected(f"immutable intent field changed: {key}")

        path_mutable = {item.path_id: item.model_fields_set for item in patch.path_repairs}
        if len(before["candidate_possibilities"]) != len(after["candidate_possibilities"]):
            raise RepairPatchRejected("candidate path collection changed")
        for old, new in zip(before["candidate_possibilities"], after["candidate_possibilities"]):
            if old["path_id"] != new["path_id"]:
                raise RepairPatchRejected("candidate path identity changed")
            allowed = path_mutable.get(old["path_id"], set())
            for key in old.keys() - allowed:
                if old[key] != new[key]:
                    raise RepairPatchRejected(f"immutable candidate path field changed: {key}")

        if len(after["open_decisions"]) < len(before["open_decisions"]):
            raise RepairPatchRejected("existing open decisions were removed")
        patched_targets = {
            item.target_decision_id
            for item in patch.open_decision_repairs
            if item.target_decision_id is not None
        }
        decisions_after = {item["decision_id"]: item for item in after["open_decisions"]}
        for old in before["open_decisions"]:
            updated = decisions_after.get(old["decision_id"])
            if updated is None:
                raise RepairPatchRejected("existing open decision identity changed")
            if old["decision_id"] not in patched_targets and old != updated:
                raise RepairPatchRejected("unrelated open decision changed")
