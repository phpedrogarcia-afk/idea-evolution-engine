"""
src/idea_evolution/domain/grounding.py
Mecanismo determinístico de validação de proveniência de autoridade (Authority Proof & Grounding Validator).
Impede autoridade inventada por modelos (Authority Spoofing) e protege a intenção humana.
"""

from __future__ import annotations
import re
import unicodedata
from typing import Tuple, List, Optional
from pydantic import BaseModel, Field
from src.idea_evolution.domain.state import PromotionAuthorityBasis


def _normalize_text(text: str) -> str:
    """Normaliza texto removendo acentos, pontuação e espaços extras para matching estrutural robusto."""
    if not text:
        return ""
    # Remove acentuação
    nfkd = unicodedata.normalize("NFKD", text)
    no_acc = "".join([c for c in nfkd if not unicodedata.combining(c)])
    # Lowercase e substitui pontuação por espaço
    clean = re.sub(r"[^\w\s]", " ", no_acc.lower())
    return " ".join(clean.split())


def _extract_significant_tokens(text: str) -> List[str]:
    """Extrai tokens significativos (comprimento >= 3, ignorando stopwords comuns)."""
    norm = _normalize_text(text)
    stopwords = {
        "para", "com", "por", "sem", "uma", "um", "dos", "das", "que", "de", "da", "do",
        "mais", "pessoas", "ajuda", "transformar", "claros", "claro", "ideia", "ideias", "projeto", "projetos",
        "the", "and", "for", "with", "that", "this", "from", "app", "aplicativo"
    }
    tokens = [t for t in norm.split() if len(t) >= 3 and t not in stopwords]
    return tokens


class GroundingRecord(BaseModel):
    """Registro determinístico de prova de ancoragem de uma proposição."""
    proposition: str
    claimed_basis: PromotionAuthorityBasis
    is_valid: bool
    grounding_source: str = ""
    evidence_or_span: str = ""
    failure_reason: str = ""


class AuthorityProofValidator:
    """
    Validador determinístico de autoridade de promoção.
    Garante que declarações de autoridade feitas por modelos (ex: USER_EXPLICIT)
    sejam estritamente comprovadas contra a entrada humana ou registros formais.
    """

    @classmethod
    def validate_user_explicit(cls, original_idea: str, proposition: str) -> Tuple[bool, str, str]:
        """
        Valida se a proposição possui fundamentação explícita na entrada humana original.
        Regra:
        1. Substring direta no texto normalizado; OU
        2. Cobertura significativa de tokens no input original.
        Inventar termos novos sem que nenhuma palavra exista no input humano é estritamente REJEITADO.
        """
        norm_orig = _normalize_text(original_idea)
        norm_prop = _normalize_text(proposition)

        if not norm_orig or not norm_prop:
            return False, "", "Entrada original ou proposição vazia."

        # 1. Substring span match direto
        if norm_prop in norm_orig:
            return True, norm_prop, "Substring direta exata encontrada no input humano original."

        # 2. Análise de tokens de novidade técnica
        prop_tokens = _extract_significant_tokens(proposition)
        orig_tokens = set(_extract_significant_tokens(original_idea))

        if not prop_tokens:
            return True, norm_orig, "Proposição geral sem novidade técnica específica."

        unsupported_tokens = [t for t in prop_tokens if t not in orig_tokens]

        # Se mais de 50% dos tokens da proposição ou tokens arquiteturais chave não estiverem no input humano
        if unsupported_tokens:
            unsupported_str = ", ".join(unsupported_tokens)
            return (
                False,
                "",
                f"SPOOFING_DETECTED: A proposição introduz conceitos não solicitados no input humano: [{unsupported_str}].",
            )

        return True, ", ".join(prop_tokens), "Todos os conceitos centrais foram expressos pelo usuário humano."

    @classmethod
    def validate_user_derivation(
        cls,
        original_idea: str,
        human_intent: str,
        proposition: str,
        derivation_proof: str,
    ) -> Tuple[bool, str, str]:
        """
        Valida se a proposição é uma dedução lógica estritamente necessária a partir das premissas humanas.
        Regra:
        Uma funcionalidade meramente 'elegante', 'útil' ou 'plausível' (ex: mind map, criptografia, IA)
        NÃO é uma derivação lógica válida da premissa genérica 'organizar ideias'.
        """
        if not derivation_proof or len(derivation_proof.strip()) < 10:
            return False, "", "Dedução sem justificativa lógica formal de necessidade estrita."

        norm_proof = _normalize_text(derivation_proof)
        # Se a prova apenas alega utilidade/conveniência sem demonstrar necessidade lógica
        if any(term in norm_proof for term in ["util", "melhor", "elegante", "moderno", "conveniente", "recomendado", "desejavel"]):
            if not any(term in norm_proof for term in ["necessario", "estrito", "entail", "deducao", "requisito", "impossivel"]):
                return (
                    False,
                    "",
                    "INVALID_DERIVATION: A justificação descreve conveniência/utilidade, mas não necessidade lógica estrita.",
                )

        return True, derivation_proof, "Derivação lógica válida fundamentada em premissas humanas."

    @classmethod
    def validate_external_evidence(cls, evidence_ref: str) -> Tuple[bool, str, str]:
        """
        Valida se a autoridade EXTERNAL_EVIDENCE referencia um artefato/ID de evidência real.
        Texto em prosa do modelo não constitui evidência externa.
        """
        if not evidence_ref or not evidence_ref.strip():
            return False, "", "Nenhuma referência a ID de evidência externa ou benchmark foi fornecida."

        norm_ref = evidence_ref.strip()
        # Exige formato estruturado de evidência (ex: EVI-xxx, EXP-xxx, BENCHMARK-xxx, URL, DOI, RUN-xxx)
        valid_patterns = [r"^EVI-", r"^EXP-", r"^BENCHMARK-", r"^RUN-", r"^DOI:", r"^HTTP[S]?://"]
        if not any(re.search(pat, norm_ref, re.IGNORECASE) for pat in valid_patterns):
            return (
                False,
                "",
                f"INVALID_EVIDENCE_REF: '{evidence_ref}' é texto descritivo e não um ID de evidência auditável (ex: EXP-xxx, EVI-xxx, DOI:xxx).",
            )

        return True, evidence_ref, "Referência formal a evidência externa verificada."

    @classmethod
    def validate_human_decision(cls, decision_ref: str, human_intervention_flag: bool) -> Tuple[bool, str, str]:
        """
        Valida se a autoridade HUMAN_DECISION decorre de uma intervenção humana real registrada no estado.
        O modelo de IA não tem permissão para fabricar uma decisão humana.
        """
        if not human_intervention_flag:
            return (
                False,
                "",
                "FABRICATED_HUMAN_DECISION: Nenhuma intervenção humana formal (human_intervention=True) foi registrada na execução.",
            )

        if not decision_ref or len(decision_ref.strip()) < 5:
            return False, "", "Referência à decisão humana ausente ou insuficiente."

        return True, decision_ref, "Decisão humana formal confirmada no registro de execução."

    @classmethod
    def audit_proposal_authority(
        cls,
        original_idea: str,
        human_intent: str,
        proposal: str,
        claimed_basis: PromotionAuthorityBasis,
        justification: str,
        evidence_or_decision_basis: str,
        human_intervention_flag: bool = False,
    ) -> GroundingRecord:
        """
        Audita determinísticamente a autoridade de uma proposição.
        Retorna o GroundingRecord com veredito final.
        """
        if claimed_basis == PromotionAuthorityBasis.USER_EXPLICIT:
            is_valid, span, reason = cls.validate_user_explicit(original_idea, proposal)
            return GroundingRecord(
                proposition=proposal,
                claimed_basis=claimed_basis,
                is_valid=is_valid,
                grounding_source="ORIGINAL_HUMAN_INPUT",
                evidence_or_span=span,
                failure_reason=reason if not is_valid else "",
            )

        elif claimed_basis == PromotionAuthorityBasis.VALID_USER_DERIVATION:
            is_valid, span, reason = cls.validate_user_derivation(original_idea, human_intent, proposal, justification)
            return GroundingRecord(
                proposition=proposal,
                claimed_basis=claimed_basis,
                is_valid=is_valid,
                grounding_source="HUMAN_INTENT_DERIVATION",
                evidence_or_span=span,
                failure_reason=reason if not is_valid else "",
            )

        elif claimed_basis == PromotionAuthorityBasis.EXTERNAL_EVIDENCE:
            is_valid, span, reason = cls.validate_external_evidence(evidence_or_decision_basis)
            return GroundingRecord(
                proposition=proposal,
                claimed_basis=claimed_basis,
                is_valid=is_valid,
                grounding_source="EXTERNAL_AUDITABLE_EVIDENCE",
                evidence_or_span=span,
                failure_reason=reason if not is_valid else "",
            )

        elif claimed_basis == PromotionAuthorityBasis.HUMAN_DECISION:
            is_valid, span, reason = cls.validate_human_decision(evidence_or_decision_basis, human_intervention_flag)
            return GroundingRecord(
                proposition=proposal,
                claimed_basis=claimed_basis,
                is_valid=is_valid,
                grounding_source="HUMAN_OPERATOR_DECISION",
                evidence_or_span=span,
                failure_reason=reason if not is_valid else "",
            )

        else:  # MODEL_HYPOTHESIS
            return GroundingRecord(
                proposition=proposal,
                claimed_basis=claimed_basis,
                is_valid=False,
                grounding_source="MODEL_SYNTHESIS",
                evidence_or_span="",
                failure_reason="MODEL_HYPOTHESIS is not an admissible authority basis for CORE promotion.",
            )
