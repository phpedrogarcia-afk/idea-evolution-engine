"""
src/idea_evolution/rendering/human_result.py
Renderizador determinístico de resultados humanos para EvolutionArtifact (M06 P6).

Transcreve o artefato canônico de evolução de ideias em Markdown limpo, estruturado
e inteligível para o usuário final, sem inferência adicional, sem chamadas de modelo,
sem jargões de laboratório e com estrita preservação das garantias ontológicas e epistêmicas.
"""

from __future__ import annotations

import re
from typing import Optional, List, Dict, Any

from src.idea_evolution.artifacts.evolution_artifact import (
    EvolutionArtifact,
    CritiqueItem,
    CandidatePossibility,
)
from src.idea_evolution.domain.state import PromotionAuthorityBasis
from src.idea_evolution.config.cost_policy import sanitize_secret_text


class HumanResultRenderer:
    """
    Renderizador determinístico e passivo para apresentação ao usuário final.
    
    Invariantes Operacionais:
    1. RENDERER_MODEL_CALLS = 0 (apenas formatação determinística).
    2. Sem reescrita semântica ou invenção de conteúdo ausente.
    3. Ideia original e proposta de refinamento visíveis e comparáveis.
    4. Distinção inegociável entre intenção declarada vs intenção inferida.
    5. Premissas, incertezas e candidatos mantêm status explícito.
    6. HUMAN_DECISION_REQUIRED apresentado como estado de domínio legítimo (não erro).
    7. Zero termos experimentais (Condição A/B/C, M05, RPL, etc.).
    8. Zero vazamento de segredos, tokens brutos ou enums ontológicos internos.
    """

    @classmethod
    def render(cls, artifact: EvolutionArtifact) -> str:
        """
        Converte deterministicamente um EvolutionArtifact em apresentação Markdown limpa.
        Falha de forma fechada (fail-closed) se o artefato for inválido ou ausente.
        """
        if artifact is None or not isinstance(artifact, EvolutionArtifact):
            raise ValueError("HumanResultRenderer: Artefato inválido ou ausente. Falha fechada.")

        if not artifact.original_idea or not artifact.original_idea.strip():
            raise ValueError("HumanResultRenderer: original_idea vazia ou ausente no artefato.")

        sections: List[str] = []

        # ---------------------------------------------------------------------------
        # Cabeçalho do Produto
        # ---------------------------------------------------------------------------
        sections.append("# FIOIDEIAS V1 — Maturação de Ideia\n")

        # ---------------------------------------------------------------------------
        # 1. Ideia Original (Preservação Fiel e Completa)
        # ---------------------------------------------------------------------------
        sections.append("## Ideia Original:\n")
        original_clean = artifact.original_idea.strip()
        quoted_original = "\n".join(f"> {line}" for line in original_clean.splitlines())
        sections.append(f"{quoted_original}\n")

        # ---------------------------------------------------------------------------
        # 2. Ideia Refinada (Proposta pelo Sistema)
        # ---------------------------------------------------------------------------
        sections.append("## Ideia Refinada (Proposta pelo Sistema)\n")
        refined_clean = artifact.refined_idea.strip() if artifact.refined_idea else "Em desenvolvimento."
        sections.append(f"{refined_clean}\n")
        sections.append(f"- **Mecanismo Proposto:** {refined_clean}\n")

        if artifact.what_changed:
            sections.append("### Mudanças Principais:\n")
            for change in artifact.what_changed:
                clean_chg = change.strip()
                if clean_chg:
                    sections.append(f"- {clean_chg}")
            sections.append("")

        # ---------------------------------------------------------------------------
        # 3. Intenção Identificada / Preservada
        # ---------------------------------------------------------------------------
        if artifact.human_intent and artifact.human_intent.strip():
            sections.append("## Intenção Identificada\n")
            if artifact.intent_provenance == PromotionAuthorityBasis.USER_EXPLICIT:
                intent_label = "Intenção declarada por você"
            else:
                intent_label = "Leitura da intenção (identificada a partir da ideia)"
            sections.append(f"- **{intent_label}:** {artifact.human_intent.strip()}\n")

        # ---------------------------------------------------------------------------
        # 4. Pontos de Atenção e Críticas
        # ---------------------------------------------------------------------------
        if artifact.critique:
            critique_lines = ["## Pontos de Atenção e Críticas\n"]
            sev_labels = {
                "HIGH": "Severidade Alta",
                "MEDIUM": "Severidade Média",
                "LOW": "Severidade Baixa",
            }
            for crit in artifact.critique:
                sev = sev_labels.get(crit.severity.upper(), crit.severity)
                critique_lines.append(f"- **[{sev}]** {crit.vulnerability.strip()}")
                if crit.why_it_matters and crit.why_it_matters.strip():
                    critique_lines.append(f"  - *Impacto:* {crit.why_it_matters.strip()}")
                if crit.affected_aspect and crit.affected_aspect.strip():
                    critique_lines.append(f"  - *Aspecto Afetado:* {crit.affected_aspect.strip()}")
            critique_lines.append("")
            sections.append("\n".join(critique_lines))

        # ---------------------------------------------------------------------------
        # 5. Premissas (Explicitadas como suposições não verificadas)
        # ---------------------------------------------------------------------------
        if artifact.assumptions:
            asm_lines = [
                "## Premissas\n",
                "As seguintes premissas foram assumidas pelo sistema e requerem validação empírica:\n",
            ]
            for asm in artifact.assumptions:
                clean_asm = asm.strip()
                if clean_asm:
                    asm_lines.append(f"- {clean_asm}")
            asm_lines.append("")
            sections.append("\n".join(asm_lines))

        # ---------------------------------------------------------------------------
        # 6. Incertezas Mapeadas (Visíveis e não mascaradas)
        # ---------------------------------------------------------------------------
        if artifact.uncertainties:
            unc_lines = ["## Incertezas Mapeadas\n"]
            for unc in artifact.uncertainties:
                clean_unc = unc.strip()
                if clean_unc:
                    unc_lines.append(f"- {clean_unc}")
            unc_lines.append("")
            sections.append("\n".join(unc_lines))

        # ---------------------------------------------------------------------------
        # 7. Possibilidades e Alternativas (Propostas não-autoritativas)
        # ---------------------------------------------------------------------------
        if artifact.candidate_possibilities:
            cand_lines = [
                "## Possibilidades e Alternativas\n",
                "Alternativas e extensões exploratórias geradas pelo sistema (não incorporadas ao núcleo):\n",
            ]
            for cand in artifact.candidate_possibilities:
                cand_lines.append(f"- **{cand.mechanism.strip()}**")
                if cand.justification and cand.justification.strip():
                    cand_lines.append(f"  - *Justificativa:* {cand.justification.strip()}")
                if cand.tradeoffs:
                    cand_lines.append(f"  - *Compensações (Trade-offs):* {', '.join(cand.tradeoffs)}")
            cand_lines.append("")
            sections.append("\n".join(cand_lines))

        # ---------------------------------------------------------------------------
        # 8. Decisão Humana Necessária (Bifurcação Normativa Válida)
        # ---------------------------------------------------------------------------
        if artifact.human_decision_required or artifact.terminal_status == "HUMAN_DECISION_REQUIRED":
            decision_lines = [
                "## Decisão Humana Necessária (BIFURCAÇÃO NORMATIVA DETECTADA)\n",
                "Esta ideia exige uma decisão humana soberana para prosseguir.",
            ]
            if artifact.human_decision_description and artifact.human_decision_description.strip():
                decision_lines.append(f"- **Ponto de Escolha:** {artifact.human_decision_description.strip()}")
            decision_lines.append("")
            sections.append("\n".join(decision_lines))

        # ---------------------------------------------------------------------------
        # 9. Próximo Passo Recomendado
        # ---------------------------------------------------------------------------
        if artifact.recommended_next_action and artifact.recommended_next_action.strip():
            sections.append("## Próximo Passo Recomendado\n")
            sections.append(f"{artifact.recommended_next_action.strip()}\n")

        # Montagem do texto final
        raw_output = "\n".join(sections).strip() + "\n"

        # ---------------------------------------------------------------------------
        # Sanitização Rigorosa de Segredos e Termos Internos de Laboratório
        # ---------------------------------------------------------------------------
        sanitized_output = sanitize_secret_text(raw_output)

        return sanitized_output


def render_human_result(artifact: EvolutionArtifact) -> str:
    """Função utilitária funcional para conveniência de importação."""
    return HumanResultRenderer.render(artifact)
