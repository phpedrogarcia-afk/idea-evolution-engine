"""
src/idea_evolution/domain/evidence_boundary.py
Contratos e implementações da Fronteira da Realidade (Reality Boundary) (FioED-02).
Formaliza:
1. Capability Boundary (Modelos não criam EvidenceArtifacts observados soberanos).
2. Provenance Boundary (A classe do artefato decorre do canal de aquisição, não do texto gerado).
3. Transition Boundary (Evidência externa admitida não concede promoção unilateral ao modelo).
4. EvidencePassport, TestabilityBinding pré-declarado, estado WAITING_FOR_REALITY e EvidenceAdmissionGate.
"""

from __future__ import annotations
import hashlib
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class RealityInterface(str, Enum):
    """Interfaces legítimas da Realidade adequadas por classe de claim."""
    HUMAN_SOURCE = "HUMAN_SOURCE"
    HUMAN_OBSERVATION = "HUMAN_OBSERVATION"
    RUNTIME_OBSERVATION = "RUNTIME_OBSERVATION"
    PRIMARY_EXTERNAL_SOURCE = "PRIMARY_EXTERNAL_SOURCE"
    EXPERIMENT = "EXPERIMENT"
    SENSOR = "SENSOR"
    LOG = "LOG"
    DETERMINISTIC_PROOF = "DETERMINISTIC_PROOF"
    SIMULATION_ONLY = "SIMULATION_ONLY"
    NO_EXTERNAL_INTERFACE_REQUIRED = "NO_EXTERNAL_INTERFACE_REQUIRED"
    UNKNOWN = "UNKNOWN"


class EvidenceClass(str, Enum):
    """Taxonomia de classes de evidência relativas à claim."""
    MODEL_DERIVED = "MODEL_DERIVED"
    SYNTHETIC_SCENARIO = "SYNTHETIC_SCENARIO"
    SIMULATION = "SIMULATION"
    DETERMINISTIC_RUNTIME_OBSERVATION = "DETERMINISTIC_RUNTIME_OBSERVATION"
    PRIMARY_EXTERNAL_SOURCE = "PRIMARY_EXTERNAL_SOURCE"
    HUMAN_OBSERVATION = "HUMAN_OBSERVATION"
    INDEPENDENT_REPLICATION = "INDEPENDENT_REPLICATION"


class IndependenceClass(str, Enum):
    """Grau de independência do gerador da hipótese."""
    INTERNAL_GENERATIVE = "INTERNAL_GENERATIVE"                    # Gerado pelo mesmo modelo ou modelo similar
    INDEPENDENT_EXTERNAL_SOURCE = "INDEPENDENT_EXTERNAL_SOURCE"    # Fonte externa não gerada pelo sistema
    INDEPENDENT_HUMAN_SUBJECT = "INDEPENDENT_HUMAN_SUBJECT"        # Observação humana real fora do sistema
    DETERMINISTIC_SYSTEM_EXECUTION = "DETERMINISTIC_SYSTEM_EXECUTION" # Execução determinística de código/teste


class ArtifactAcquisitionChannel(str, Enum):
    """Canal físico/lógico pelo qual o artefato ingressou no runtime."""
    MODEL_GENERATION_CHANNEL = "MODEL_GENERATION_CHANNEL"          # Saída direta de LLM/gerador
    DETERMINISTIC_RUNNER_CHANNEL = "DETERMINISTIC_RUNNER_CHANNEL"  # Saída do test runner/processo local
    EXTERNAL_INGESTION_CHANNEL = "EXTERNAL_INGESTION_CHANNEL"      # Ingestão de API/dataset externo
    HUMAN_INTERVENTION_CHANNEL = "HUMAN_INTERVENTION_CHANNEL"      # Entrada direta do operador humano


class ArtifactNature(str, Enum):
    """Natureza epistêmica do artefato."""
    SYNTHETIC = "SYNTHETIC"  # Gerado, simulado ou imaginado
    OBSERVED = "OBSERVED"    # Capturado factual do mundo/runtime


class EvidencePassport(BaseModel):
    """
    Passaporte de Proveniência Epistêmica atribuído exclusivamente pelo runtime/canal de aquisição.
    O PAYLOAD PODE AFIRMAR QUALQUER COISA; O PASSAPORTE DETERMINA O CANAL DE ORIGEM.
    """
    passport_id: str
    acquisition_channel: ArtifactAcquisitionChannel
    collector_identity: str
    binding_id: str
    experiment_id: str
    request_id: str
    captured_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    raw_artifact_hash: str
    nature: ArtifactNature = ArtifactNature.SYNTHETIC
    evidence_class: EvidenceClass = EvidenceClass.MODEL_DERIVED
    independence_class: IndependenceClass = IndependenceClass.INTERNAL_GENERATIVE
    scope: str = "LOCAL"
    freshness_timestamp: Optional[str] = None


class TestabilityBinding(BaseModel):
    """
    Contrato de Ligação de Testabilidade (TestabilityBinding):
    Pré-declara formalmente as transições de estado para cada desfecho ANTES da observação.
    IMUTÁVEL APÓS A EMISSÃO DO REQUEST OU ANEXAÇÃO DE EVIDÊNCIA.
    """
    binding_id: str
    question_id: str
    target_claim: str
    target_hypothesis_ref: str
    observable_variable: str
    predeclared_transitions: Dict[str, str] = Field(default_factory=dict)
    required_evidence_class: EvidenceClass
    required_reality_interface: RealityInterface
    required_independence: IndependenceClass
    scope: str = "LOCAL"
    protected_kernel_refs: List[str] = Field(default_factory=list)
    version: int = 1
    is_frozen: bool = False
    attached_evidence_id: Optional[str] = None

    def freeze_for_experiment(self, experiment_id: str) -> None:
        """Congela o binding para impedir edições 'post-hoc' (pintar o alvo após a flecha)."""
        self.is_frozen = True

    def amend_before_request(self, new_predeclarations: Dict[str, str], reason: str) -> TestabilityBinding:
        """Permite emenda apenas antes do congelamento/requisição."""
        if self.is_frozen or self.attached_evidence_id is not None:
            raise ValueError("CANNOT_AMEND_FROZEN_BINDING: Não é permitido reescrever regras após observação.")
        return TestabilityBinding(
            binding_id=f"{self.binding_id}_v{self.version + 1}",
            question_id=self.question_id,
            target_claim=self.target_claim,
            target_hypothesis_ref=self.target_hypothesis_ref,
            observable_variable=self.observable_variable,
            predeclared_transitions=new_predeclarations,
            required_evidence_class=self.required_evidence_class,
            required_reality_interface=self.required_reality_interface,
            required_independence=self.required_independence,
            scope=self.scope,
            protected_kernel_refs=self.protected_kernel_refs,
            version=self.version + 1,
            is_frozen=False,
        )


class EvidenceRequestStatus(str, Enum):
    REQUEST_ISSUED = "REQUEST_ISSUED"
    WAITING_FOR_REALITY = "WAITING_FOR_REALITY"  # Hard state: O ramo aguarda observação real sem inventar o chão
    EVIDENCE_RECEIVED = "EVIDENCE_RECEIVED"
    CANCELLED = "CANCELLED"


class EvidenceRequest(BaseModel):
    """Requisição formal de evidência dirigida a uma interface da realidade."""
    request_id: str
    binding_id: str
    question_id: str
    required_interface: RealityInterface
    required_evidence_class: EvidenceClass
    target_claim: str
    status: EvidenceRequestStatus = EvidenceRequestStatus.WAITING_FOR_REALITY
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class EvidenceAdmissionOutcome(str, Enum):
    ADMITTED = "ADMITTED"
    REJECTED_BINDING_MISMATCH = "REJECTED_BINDING_MISMATCH"
    REJECTED_WRONG_EVIDENCE_CLASS = "REJECTED_WRONG_EVIDENCE_CLASS"
    REJECTED_PROVENANCE_INVALID = "REJECTED_PROVENANCE_INVALID"
    REJECTED_SYNTHETIC_NOT_ADMISSIBLE = "REJECTED_SYNTHETIC_NOT_ADMISSIBLE"
    REJECTED_REPLAY_DETECTED = "REJECTED_REPLAY_DETECTED"
    INCONCLUSIVE = "INCONCLUSIVE"


class EvidenceAdmissionDecision(BaseModel):
    """Veredito determinístico do EvidenceAdmissionGate."""
    decision_id: str
    outcome: EvidenceAdmissionOutcome
    passport_ref: str
    binding_ref: str
    is_admitted: bool
    adjudicated_transition: Optional[str] = None
    reason: str
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class EvidenceAdmissionGate:
    """
    Portão Epistêmico Determinístico de Admissão de Evidência.
    Verifica se o EvidencePassport cumpre estritamente os requisitos do TestabilityBinding congelado.
    """

    @classmethod
    def evaluate(
        cls,
        binding: TestabilityBinding,
        passport: EvidencePassport,
        observed_outcome_value: str,
        seen_passports_pool: Optional[List[str]] = None,
    ) -> EvidenceAdmissionDecision:
        decision_id = f"ADM-{hashlib.sha256((binding.binding_id + passport.passport_id).encode()).hexdigest()[:8]}"

        # 1. Verificar correspondência de Binding
        if passport.binding_id != binding.binding_id:
            return EvidenceAdmissionDecision(
                decision_id=decision_id,
                outcome=EvidenceAdmissionOutcome.REJECTED_BINDING_MISMATCH,
                passport_ref=passport.passport_id,
                binding_ref=binding.binding_id,
                is_admitted=False,
                reason=f"Binding mismatch: passaporte emitido para {passport.binding_id}, mas apresentado para {binding.binding_id}.",
            )

        # 2. Verificar se o artefato é sintético quando observação empírica é exigida
        requires_external = binding.required_reality_interface not in (RealityInterface.SIMULATION_ONLY, RealityInterface.NO_EXTERNAL_INTERFACE_REQUIRED)
        if requires_external and passport.nature == ArtifactNature.SYNTHETIC:
            return EvidenceAdmissionDecision(
                decision_id=decision_id,
                outcome=EvidenceAdmissionOutcome.REJECTED_SYNTHETIC_NOT_ADMISSIBLE,
                passport_ref=passport.passport_id,
                binding_ref=binding.binding_id,
                is_admitted=False,
                reason="Evidência sintética (gerada por modelo) não pode fechar claims empíricas sobre a realidade.",
            )

        # 3. Verificar classe de evidência
        if passport.evidence_class != binding.required_evidence_class:
            return EvidenceAdmissionDecision(
                decision_id=decision_id,
                outcome=EvidenceAdmissionOutcome.REJECTED_WRONG_EVIDENCE_CLASS,
                passport_ref=passport.passport_id,
                binding_ref=binding.binding_id,
                is_admitted=False,
                reason=f"Classe de evidência incompatível: exigida {binding.required_evidence_class}, recebida {passport.evidence_class}.",
            )

        # 4. Detecção de Replay de Experimento Anterior
        if seen_passports_pool and passport.passport_id in seen_passports_pool:
            return EvidenceAdmissionDecision(
                decision_id=decision_id,
                outcome=EvidenceAdmissionOutcome.REJECTED_REPLAY_DETECTED,
                passport_ref=passport.passport_id,
                binding_ref=binding.binding_id,
                is_admitted=False,
                reason="Replay detectado: Este EvidencePassport já foi utilizado em um experimento prévio.",
            )

        # 5. Admissão e Resolução da Transição Pré-declarada
        transition = binding.predeclared_transitions.get(observed_outcome_value)
        if not transition or observed_outcome_value.upper() == "INCONCLUSIVE":
            return EvidenceAdmissionDecision(
                decision_id=decision_id,
                outcome=EvidenceAdmissionOutcome.INCONCLUSIVE,
                passport_ref=passport.passport_id,
                binding_ref=binding.binding_id,
                is_admitted=True,
                adjudicated_transition="PRESERVE_UNKNOWN",
                reason="Evidência admitida mas o desfecho é inconclusivo; preservando incerteza.",
            )

        return EvidenceAdmissionDecision(
            decision_id=decision_id,
            outcome=EvidenceAdmissionOutcome.ADMITTED,
            passport_ref=passport.passport_id,
            binding_ref=binding.binding_id,
            is_admitted=True,
            adjudicated_transition=transition,
            reason=f"Evidência admitida com sucesso. Transição pré-declarada aplicada: {transition}",
        )


class ObservedEvidenceFactory:
    """
    Fábrica determinística de runtime para emissão de ObservedArtifacts e EvidencePassports legítimos.
    Disponível apenas para canais de runtime (test runner, ingestão externa, intervenção humana).
    Modelos LLM NÃO têm permissão de invocar esta fábrica diretamente.
    """

    @classmethod
    def create_runtime_observation(
        cls,
        binding_id: str,
        experiment_id: str,
        request_id: str,
        raw_content: str,
        collector_id: str = "IEE_RUNTIME_RUNNER",
    ) -> EvidencePassport:
        content_hash = hashlib.sha256(raw_content.encode()).hexdigest()
        passport_id = f"PASS-RT-{content_hash[:8]}"
        return EvidencePassport(
            passport_id=passport_id,
            acquisition_channel=ArtifactAcquisitionChannel.DETERMINISTIC_RUNNER_CHANNEL,
            collector_identity=collector_id,
            binding_id=binding_id,
            experiment_id=experiment_id,
            request_id=request_id,
            raw_artifact_hash=content_hash,
            nature=ArtifactNature.OBSERVED,
            evidence_class=EvidenceClass.DETERMINISTIC_RUNTIME_OBSERVATION,
            independence_class=IndependenceClass.DETERMINISTIC_SYSTEM_EXECUTION,
        )

    @classmethod
    def create_human_observation(
        cls,
        binding_id: str,
        experiment_id: str,
        request_id: str,
        raw_feedback: str,
        human_id: str = "HUMAN_OPERATOR",
    ) -> EvidencePassport:
        content_hash = hashlib.sha256(raw_feedback.encode()).hexdigest()
        passport_id = f"PASS-HUMAN-{content_hash[:8]}"
        return EvidencePassport(
            passport_id=passport_id,
            acquisition_channel=ArtifactAcquisitionChannel.HUMAN_INTERVENTION_CHANNEL,
            collector_identity=human_id,
            binding_id=binding_id,
            experiment_id=experiment_id,
            request_id=request_id,
            raw_artifact_hash=content_hash,
            nature=ArtifactNature.OBSERVED,
            evidence_class=EvidenceClass.HUMAN_OBSERVATION,
            independence_class=IndependenceClass.INDEPENDENT_HUMAN_SUBJECT,
        )
