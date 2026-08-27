"""
src/idea_evolution/domain/idea_ecology.py
Contratos e estruturas do Modelo de Ecologia de Ideias (FioED-02).
Formaliza: Fertile Unknowns (U_f), Gap Unknowns (U_g), Zona de Incubação Protegida (Z_p),
Kernel de Identidade (K), PressureReadiness estruturado (sem score escalar),
os 4 Verbos Operacionais (SEE, KEEP, PRESS, COMMIT) e Questões Discriminativas (Q*).
"""

from __future__ import annotations
import hashlib
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from src.idea_evolution.domain.state import OntologyState, PromotionAuthorityBasis


class UnknownKind(str, Enum):
    """
    Classificação ontológica de incertezas no FioED.
    U_f != Falha ou ignorância; é potencial fértil a ser preservado.
    """
    FERTILE_UNKNOWN = "FERTILE_UNKNOWN"  # U_f: Potencial fértil sem pergunta ou interface de teste imediata
    GAP_UNKNOWN = "GAP_UNKNOWN"          # U_g: Incerteza formulada com caminho legítimo de discriminação


class UnknownRecord(BaseModel):
    """Registro tipado de incerteza dentro da ecologia da ideia."""
    unknown_id: str
    kind: UnknownKind = UnknownKind.FERTILE_UNKNOWN
    description: str
    source_refs: List[str] = Field(default_factory=list)
    protected_in_zone: bool = True
    can_generate_questions: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class KernelStatus(str, Enum):
    """Status de autoridade do Kernel de Identidade de uma ideia."""
    MODEL_INFERRED_KERNEL = "MODEL_INFERRED_KERNEL"      # Proposta pelo modelo (não é soberana)
    SOURCE_DERIVED_KERNEL = "SOURCE_DERIVED_KERNEL"      # Mapeada diretamente do texto da fonte
    HUMAN_CONFIRMED_KERNEL = "HUMAN_CONFIRMED_KERNEL"    # Confirmada formalmente por autoridade humana
    CONTESTED_KERNEL = "CONTESTED_KERNEL"                # Em tensão ou contestação
    UNKNOWN_KERNEL = "UNKNOWN_KERNEL"


class IdentityKernel(BaseModel):
    """
    Kernel de Identidade K(h): O que precisa desaparecer antes que deixe de ser a mesma ideia?
    Um modelo pode inferir um candidato, mas NÃO pode autoestabelecer confirmação humana.
    """
    kernel_id: str
    core_elements: List[str] = Field(default_factory=list)
    status: KernelStatus = KernelStatus.MODEL_INFERRED_KERNEL
    source_refs: List[str] = Field(default_factory=list)
    is_human_confirmed: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class EcologicalVerb(str, Enum):
    """Os 4 Verbos Operacionais Fundamentais na Ecologia do FioED."""
    SEE = "SEE"        # Observar sem obrigação de alterar ou julgar
    KEEP = "KEEP"      # Preservar em incubação sem implicar promoção ou valor objetivo
    PRESS = "PRESS"    # Aplicar pressão local e delimitada sobre uma hipótese/U_g
    COMMIT = "COMMIT"  # Alocar autoridade/recursos ou adotar decisão definitiva


class PressureReadinessDimension(BaseModel):
    """
    Vetor multidimensional de prontidão para pressão.
    NÃO É UM SCORE ESCALAR. Não possui pesos arbitrários.
    """
    identity_relation_clear: bool = False   # Se a falha do mecanismo não ameaça o Kernel
    question_well_formed: bool = False      # Se a incerteza possui pergunta clara
    observable_contrast_defined: bool = False # Se existem contrastes observáveis
    evidence_path_feasible: bool = False    # Se há rota legítima para realidade
    state_discrimination_ready: bool = False # Se observações distintas geram ações distintas
    decision_relevance_present: bool = False # Se responder altera uma decisão humana/técnica
    scope_strictly_contained: bool = False  # Se o raio de impacto do teste é local
    human_override_blocking: bool = False   # Se o humano impôs HumanIncubationOverride


class PressureReadiness(BaseModel):
    """Avaliação estruturada de prontidão para pressão localizada."""
    target_hypothesis_ref: str
    dimensions: PressureReadinessDimension
    is_ready_for_pressure: bool = False
    blocking_reasons: List[str] = Field(default_factory=list)

    @classmethod
    def evaluate(cls, target_ref: str, dims: PressureReadinessDimension) -> PressureReadiness:
        reasons = []
        if dims.human_override_blocking:
            reasons.append("HumanIncubationOverride ativo: Humano determinou manter em incubação.")
        if not dims.identity_relation_clear:
            reasons.append("Relação com o Kernel de Identidade não está clara; risco de colapso do Kernel.")
        if not dims.question_well_formed:
            reasons.append("A incerteza ainda é um Fertile Unknown (U_f) sem pergunta bem formulada.")
        if not dims.observable_contrast_defined:
            reasons.append("Faltam contrastes observáveis para discriminar os estados.")
        if not dims.state_discrimination_ready:
            reasons.append("Falta discriminação de estado: diferentes respostas levariam à mesma ação.")
        if not dims.scope_strictly_contained:
            reasons.append("Escopo não está contido; pressão pode causar efeitos colaterais descontrolados.")

        ready = (len(reasons) == 0 and dims.decision_relevance_present and dims.evidence_path_feasible)
        if not ready and not reasons:
            reasons.append("Relevância decisória ou viabilidade de rota de evidência ausente.")

        return cls(
            target_hypothesis_ref=target_ref,
            dimensions=dims,
            is_ready_for_pressure=ready,
            blocking_reasons=reasons,
        )


class QuestionKind(str, Enum):
    """Evolução tipada de perguntas na ecologia."""
    EMERGENT_QUESTION = "EMERGENT_QUESTION"        # Pergunta conceitual significativa em U_f
    QUESTION_CANDIDATE = "QUESTION_CANDIDATE"      # Pergunta candidata a teste
    DISCRIMINATING_QUESTION = "DISCRIMINATING_QUESTION" # Q*: Pergunta com discriminação de estado comprovada


class DiscriminatingQuestion(BaseModel):
    """
    Questão Discriminativa Q*:
    Q* = Pergunta + Contraste Observável + Rota de Evidência + Discriminação de Estado + Escopo Local.
    NÃO é mera retórica ou string em prosa.
    """
    question_id: str
    question_text: str
    kind: QuestionKind = QuestionKind.EMERGENT_QUESTION
    target_unknown_ref: Optional[str] = None
    target_hypothesis_ref: Optional[str] = None
    protected_kernel_refs: List[str] = Field(default_factory=list)
    observable_contrast: str = ""
    possible_outcomes: List[str] = Field(default_factory=list)
    required_evidence_class: str = "DETERMINISTIC_RUNTIME_OBSERVATION"
    decision_consequence: str = ""
    pressure_scope: str = "LOCAL"
    has_state_discrimination: bool = False
    status: str = "PROPOSED"

    def validate_state_discrimination(self, outcome_action_map: Dict[str, str]) -> bool:
        """
        Condição necessária de discriminação de estado:
        Pelo menos dois desfechos legítimos devem resultar em transições de estado materialmente distintas.
        """
        if len(self.possible_outcomes) < 2:
            self.has_state_discrimination = False
            return False
        
        distinct_actions = set(outcome_action_map.get(out, "") for out in self.possible_outcomes if out in outcome_action_map)
        self.has_state_discrimination = (len(distinct_actions) >= 2)
        if self.has_state_discrimination and self.is_fully_formed_qstar():
            self.kind = QuestionKind.DISCRIMINATING_QUESTION
        return self.has_state_discrimination

    def is_fully_formed_qstar(self) -> bool:
        """
        Q* Canônico = Question + ObservableContrast + EvidencePath + StateDiscrimination + LocalScope.
        A discriminação de estado é necessária, mas não suficiente sozinha.
        """
        return bool(
            self.question_text
            and self.observable_contrast
            and self.required_evidence_class
            and self.pressure_scope.upper() == "LOCAL"
            and self.has_state_discrimination
        )



class HumanIncubationOverride(BaseModel):
    """
    Preservação Soberana Humana:
    O humano pode declarar KEEP_IN_INCUBATION para proteger uma ideia de pressão prematura,
    mesmo que o sistema detecte que uma parte seja tecnicamente testável.
    """
    override_id: str
    target_idea_or_aspect: str
    human_rationale: str
    preserve_in_incubation: bool = True
    active: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
