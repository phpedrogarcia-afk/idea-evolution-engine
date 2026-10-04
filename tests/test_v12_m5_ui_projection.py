from __future__ import annotations

import argparse
from pathlib import Path

import pytest

from src.idea_evolution.artifacts.evolution_artifact import (
    CandidatePossibility,
    CoverageIssue,
    CoverageIssueType,
    CoverageStatus,
    EvolutionArtifact,
    IntentImportance,
    IntentLedgerItem,
    IntentOriginType,
    IntentTreatmentStatus,
    OpenDecision,
    TreatmentMode,
    UsefulInsight,
)
from src.idea_evolution.service.contracts import EvolutionRequest, EvolutionResponse
from src.idea_evolution.ui.server import create_local_ui_server, evolution_response_to_ui_data


M5_UI_FIXTURE_NAMES = (
    "fiobase_rich",
    "narrow_csv_json",
    "empty_insights",
    "multiple_paths",
    "open_decisions",
    "coverage_no_blocking_gap",
    "coverage_unresolved",
    "human_decision_required",
    "schema_1_0_legacy",
    "malicious_text",
)


def _fiobase_artifact() -> EvolutionArtifact:
    idea = (
        "Quero criar uma base reutilizável para começar projetos com contexto "
        "e aprendizados anteriores."
    )
    uncertainties = [
        "Qual parte do contexto realmente ajuda no primeiro passo?",
        "Como manter os aprendizados revisáveis ao longo do tempo?",
    ]
    ledger = [
        IntentLedgerItem(
            intent_id="I-CORE",
            source_quote="base reutilizável",
            interpretation="Começar novos projetos com uma estrutura que possa ser reaproveitada.",
            importance=IntentImportance.CORE_INTENT,
            origin_type=IntentOriginType.USER_EXPLICIT,
            treatment_in_current_form="A proposta mantém uma base de partida reutilizável.",
            status=IntentTreatmentStatus.PRESERVED,
        ),
        IntentLedgerItem(
            intent_id="I-LEARNINGS",
            source_quote="aprendizados anteriores",
            interpretation="Reaproveitar aprendizados sem retirar do usuário a revisão do contexto.",
            importance=IntentImportance.MATERIAL_SUBINTENT,
            origin_type=IntentOriginType.USER_EXPLICIT,
            treatment_in_current_form="A proposta deixa a seleção dos aprendizados para revisão.",
            status=IntentTreatmentStatus.DEFERRED,
        ),
    ]
    return EvolutionArtifact(
        artifact_id="ART-M5-FIOBASE",
        run_id="RUN-M5-FIOBASE",
        treatment_mode=TreatmentMode.LEAN_L1,
        terminal_status="COMPLETED_DIRECT_ONE_PASS",
        original_idea=idea,
        human_intent="Preparar melhor o início de novos projetos usando experiências anteriores.",
        refined_idea=(
            "Uma base reutilizável reúne orientações e aprendizados anteriores e os apresenta "
            "como propostas revisáveis antes de aplicá-los a um novo projeto."
        ),
        what_changed=["A ideia agora separa a base reutilizável da escolha sobre o que aplicar."],
        critique=[],
        assumptions=["Os aprendizados anteriores podem ser descritos de forma útil."],
        uncertainties=uncertainties,
        intent_ledger=ledger,
        useful_insights=[
            UsefulInsight(
                insight_id="U-CONTEXT",
                description="Reunir aprendizados sem considerar o contexto pode levar a recomendações inadequadas.",
                related_intent_ids=["I-LEARNINGS"],
            )
        ],
        open_decisions=[
            OpenDecision(
                decision_id="D-LEARNINGS",
                question="Quais aprendizados devem ser sugeridos no início de cada projeto?",
                related_intent_ids=["I-LEARNINGS"],
            )
        ],
        coverage_status=CoverageStatus.NO_BLOCKING_GAP_DETECTED,
        candidate_possibilities=[
            CandidatePossibility(
                path_id="PATH-SKILL",
                mechanism="Uma skill local invocada no início do projeto prepara uma orientação contextual.",
                justification="Pode reunir regras e aprendizados em um ponto reutilizável.",
                tradeoffs=["Exige manutenção das lições.", "O conteúdo permanece revisável pelo usuário."],
                intent_ids=["I-CORE", "I-LEARNINGS"],
            ),
            CandidatePossibility(
                path_id="PATH-SCAFFOLD",
                mechanism="Um scaffold inicial organiza arquivos e orientações a partir de um perfil escolhido.",
                justification="Torna a preparação concreta antes do trabalho específico.",
                tradeoffs=["Pode impor estrutura cedo demais."],
                intent_ids=["I-CORE"],
            ),
        ],
        recommended_next_action=(
            "Experimentar a base em um projeto pequeno e observar quais orientações foram úteis."
        ),
        recommended_next_action_target_uncertainty=uncertainties[0],
    )


def _response(artifact: EvolutionArtifact) -> EvolutionResponse:
    return EvolutionResponse(
        success=True,
        run_id=artifact.run_id,
        treatment_used=artifact.treatment_mode,
        raw_idea=artifact.original_idea,
        terminal_status=artifact.terminal_status,
        human_decision_requested=artifact.human_decision_required,
        artifact=artifact,
    )


def build_m5_ui_fixture_bank() -> dict[str, EvolutionResponse]:
    rich = _fiobase_artifact()
    bank = {"fiobase_rich": _response(rich)}

    narrow = EvolutionArtifact(
        artifact_id="ART-M5-NARROW",
        run_id="RUN-M5-NARROW",
        treatment_mode=TreatmentMode.LEAN_L1,
        terminal_status="COMPLETED_DIRECT_ONE_PASS",
        original_idea="Converter um arquivo CSV para JSON preservando os cabeçalhos das colunas.",
        human_intent="Converter CSV em JSON preservando os cabeçalhos.",
        refined_idea="Um conversor lê os cabeçalhos do CSV e os mantém como chaves dos objetos JSON.",
        uncertainties=[],
        candidate_possibilities=[
            CandidatePossibility(
                path_id="PATH-CSV",
                mechanism="Ler a primeira linha como cabeçalhos e mapear cada linha aos pares cabeçalho/valor.",
                intent_ids=[],
            )
        ],
        recommended_next_action="Testar a conversão com um arquivo pequeno que contenha cabeçalhos repetidos.",
    )
    bank["narrow_csv_json"] = _response(narrow)

    empty_insights = rich.model_copy(update={"useful_insights": []})
    bank["empty_insights"] = _response(empty_insights)

    multiple_paths = rich.model_copy(update={
        "candidate_possibilities": [
            *rich.candidate_possibilities,
            CandidatePossibility(
                path_id="PATH-CHECKLIST",
                mechanism="Uma lista curta de verificação prepara cada novo projeto sem criar arquivos automaticamente.",
                justification="Mantém as orientações visíveis antes de qualquer alteração local.",
                tradeoffs=["Depende de revisão manual."],
                intent_ids=["I-CORE"],
            ),
        ]
    })
    bank["multiple_paths"] = _response(multiple_paths)

    open_decisions = rich.model_copy(update={
        "open_decisions": [
            *rich.open_decisions,
            OpenDecision(
                decision_id="D-REVIEW",
                question="Com que frequência as orientações devem ser revisadas?",
                related_intent_ids=["I-LEARNINGS"],
            ),
        ]
    })
    bank["open_decisions"] = _response(open_decisions)

    bank["coverage_no_blocking_gap"] = _response(rich)

    unresolved = rich.model_copy(update={
        "coverage_status": CoverageStatus.UNRESOLVED,
        "coverage_issues": [CoverageIssue(
            issue_type=CoverageIssueType.MATERIAL_INTENT_UNTREATED,
            description="CORE_INTENT I-CORE has no explicit treatment in current_form.",
            intent_id="I-CORE",
        )],
    })
    bank["coverage_unresolved"] = _response(unresolved)

    decision_required = rich.model_copy(update={
        "terminal_status": "HUMAN_DECISION_REQUIRED",
        "human_decision_required": True,
        "human_decision_description": "Definir quais aprendizados podem ser incluídos como contexto inicial.",
    })
    bank["human_decision_required"] = _response(decision_required)

    legacy_payload = rich.model_dump(mode="json")
    legacy_payload["schema_version"] = "1.0"
    for key in ("intent_ledger", "useful_insights", "open_decisions", "coverage_status", "coverage_issues"):
        legacy_payload.pop(key, None)
    for possibility in legacy_payload["candidate_possibilities"]:
        possibility.pop("path_id", None)
        possibility.pop("intent_ids", None)
    legacy = EvolutionArtifact.model_validate(legacy_payload)
    bank["schema_1_0_legacy"] = _response(legacy)

    malicious = rich.model_dump(mode="python")
    malicious["original_idea"] = (
        '<script>alert("idea")</script> & trecho literal; base reutilizável; aprendizados anteriores'
    )
    malicious["intent_ledger"][0]["source_quote"] = "<script>alert(\"idea\")</script>"
    malicious["human_intent"] = '<img src=x onerror="alert(1)">'
    malicious["useful_insights"][0]["description"] = '<svg onload="alert(2)">texto</svg>'
    malicious["candidate_possibilities"][0]["mechanism"] = "</article><script>alert(3)</script>"
    bank["malicious_text"] = _response(EvolutionArtifact.model_validate(malicious))

    assert set(bank) == set(M5_UI_FIXTURE_NAMES)
    return bank


@pytest.fixture(scope="module")
def m5_ui_fixture_bank() -> dict[str, EvolutionResponse]:
    return build_m5_ui_fixture_bank()


@pytest.mark.parametrize("case_name", M5_UI_FIXTURE_NAMES)
def test_m5_api_fixture_cases_are_typed_and_adapter_serializable(
    case_name: str,
    m5_ui_fixture_bank: dict[str, EvolutionResponse],
):
    response = m5_ui_fixture_bank[case_name]
    payload = evolution_response_to_ui_data(response)

    assert payload["success"] is True
    assert isinstance(payload["artifact"], dict)
    assert payload["artifact"]["original_idea"] == response.artifact.original_idea
    assert payload["artifact"]["refined_idea"] == response.artifact.refined_idea


def test_adapter_exposes_only_real_m5_fields_and_preserves_path_and_intent_links(m5_ui_fixture_bank):
    response = m5_ui_fixture_bank["fiobase_rich"]
    before = response.artifact.model_dump(mode="json")

    payload = evolution_response_to_ui_data(response)
    artifact = payload["artifact"]

    assert artifact["schema_version"] == "1.1"
    assert artifact["useful_insights"][0] == {
        "insight_id": "U-CONTEXT",
        "description": response.artifact.useful_insights[0].description,
        "related_intent_ids": ["I-LEARNINGS"],
        "authority_basis": "MODEL_HYPOTHESIS",
    }
    assert artifact["candidate_possibilities"][0]["path_id"] == "PATH-SKILL"
    assert artifact["candidate_possibilities"][0]["intent_ids"] == ["I-CORE", "I-LEARNINGS"]
    assert artifact["recommended_next_action_target_uncertainty"] == response.artifact.uncertainties[0]
    assert artifact["intent_ledger"][0]["source_quote"] == "base reutilizável"
    assert artifact["intent_ledger"][0]["origin_type"] == "USER_EXPLICIT"
    assert artifact["coverage_status"] == "NO_BLOCKING_GAP_DETECTED"
    assert response.artifact.model_dump(mode="json") == before
    assert not {"quality_score", "maturity_percentage", "evidence_count", "risk_count", "progress_percentage"} & set(artifact)


def test_empty_insights_and_single_path_remain_empty_or_single_without_fake_counts(m5_ui_fixture_bank):
    empty = evolution_response_to_ui_data(m5_ui_fixture_bank["empty_insights"])["artifact"]
    narrow = evolution_response_to_ui_data(m5_ui_fixture_bank["narrow_csv_json"])["artifact"]

    assert empty["useful_insights"] == []
    assert len(narrow["candidate_possibilities"]) == 1
    app_js = Path(__file__).parents[1] / "src" / "idea_evolution" / "ui" / "static" / "app.js"
    source = app_js.read_text(encoding="utf-8")
    assert "usable.length === 0" in source
    assert "maturity_percentage" not in source
    assert "progress_percentage" not in source


def test_open_decisions_are_not_human_decision_authority(m5_ui_fixture_bank):
    open_response = m5_ui_fixture_bank["open_decisions"]
    open_payload = evolution_response_to_ui_data(open_response)["artifact"]
    decision_payload = evolution_response_to_ui_data(m5_ui_fixture_bank["human_decision_required"])["artifact"]

    assert open_payload["open_decisions"]
    assert open_payload["human_decision_required"] is False
    assert decision_payload["human_decision_required"] is True
    assert decision_payload["human_decision_description"]


def test_coverage_statuses_keep_their_epistemic_meaning(m5_ui_fixture_bank):
    no_blocking = evolution_response_to_ui_data(m5_ui_fixture_bank["coverage_no_blocking_gap"])["artifact"]
    unresolved = evolution_response_to_ui_data(m5_ui_fixture_bank["coverage_unresolved"])["artifact"]
    app_js = Path(__file__).parents[1] / "src" / "idea_evolution" / "ui" / "static" / "app.js"
    source = app_js.read_text(encoding="utf-8")

    assert no_blocking["coverage_status"] == "NO_BLOCKING_GAP_DETECTED"
    assert no_blocking["coverage_issues"] == []
    assert unresolved["coverage_status"] == "UNRESOLVED"
    assert unresolved["coverage_issues"][0]["issue_type"] == "MATERIAL_INTENT_UNTREATED"
    assert "Checagem estrutural: nenhuma lacuna bloqueante detectada." in source
    assert "Há um ponto estrutural não resolvido nesta maturação." in source
    assert "✓ Validado" not in source
    assert "Cobertura completa" not in source


def test_schema_1_0_legacy_artifact_uses_defaults_without_claiming_a_coverage_run(m5_ui_fixture_bank):
    payload = evolution_response_to_ui_data(m5_ui_fixture_bank["schema_1_0_legacy"])["artifact"]

    assert payload["schema_version"] == "1.0"
    assert payload["useful_insights"] == []
    assert payload["open_decisions"] == []
    assert payload["intent_ledger"] == []
    assert payload["coverage_status"] == "NOT_EVALUATED"
    assert payload["coverage_issues"] == []
    assert all(path["path_id"] is None and path["intent_ids"] == [] for path in payload["candidate_possibilities"])


def test_malicious_text_round_trips_as_data_and_untrusted_renderer_stays_text(m5_ui_fixture_bank):
    payload = evolution_response_to_ui_data(m5_ui_fixture_bank["malicious_text"])
    app_js = Path(__file__).parents[1] / "src" / "idea_evolution" / "ui" / "static" / "app.js"
    source = app_js.read_text(encoding="utf-8")

    assert payload["artifact"]["original_idea"].startswith("<script>")
    assert payload["artifact"]["useful_insights"][0]["description"].startswith("<svg")
    assert payload["artifact"]["candidate_possibilities"][0]["mechanism"].startswith("</article>")
    assert "textContent" in source
    assert ".innerHTML" not in source


class _OfflineFixtureService:
    def __init__(self, fixture_bank: dict[str, EvolutionResponse]):
        self.fixture_bank = fixture_bank

    def evolve(self, request: EvolutionRequest) -> EvolutionResponse:
        prefix, separator, case_name = request.raw_idea.partition(":")
        if prefix != "M5_FIXTURE" or not separator or case_name not in self.fixture_bank:
            raise ValueError("Fixture visual inexistente.")
        return self.fixture_bank[case_name]


def _serve_visual_fixtures() -> None:
    parser = argparse.ArgumentParser(description="Servidor offline de fixtures visuais M5.")
    parser.add_argument("--serve-fixtures", action="store_true")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if not args.serve_fixtures:
        parser.error("Use --serve-fixtures para habilitar somente as respostas fictícias offline.")
    bank = build_m5_ui_fixture_bank()
    server = create_local_ui_server(
        service_factory=lambda: _OfflineFixtureService(bank),
        port=args.port,
        host="127.0.0.1",
    )
    print(f"M5 offline fixture UI at http://127.0.0.1:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    _serve_visual_fixtures()
