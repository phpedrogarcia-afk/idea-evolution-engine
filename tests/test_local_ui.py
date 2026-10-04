from __future__ import annotations

import json
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterator
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from src.idea_evolution.artifacts.evolution_artifact import EvolutionArtifact
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.service.contracts import (
    EvolutionRequest,
    EvolutionResponse,
    ServiceFailureType,
    TreatmentMode,
)
from src.idea_evolution.service.evolution_service import IdeaEvolutionService
from src.idea_evolution.ui.server import (
    MAX_REQUEST_BODY_BYTES,
    create_local_ui_server,
    evolution_response_to_ui_data,
)
from src.idea_evolution.cli.main import parse_args


@contextmanager
def running_server(service_factory: Callable[[], Any]) -> Iterator[tuple[str, Any]]:
    server = create_local_ui_server(service_factory=service_factory, port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}", server
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def request_http(
    url: str,
    method: str = "GET",
    payload: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[int, bytes, Any]:
    request = Request(url, data=payload, headers=headers or {}, method=method)
    try:
        with urlopen(request, timeout=5) as response:
            return response.status, response.read(), response.headers
    except HTTPError as response:
        return response.code, response.read(), response.headers


def json_post(url: str, data: bytes, extra_headers: dict[str, str] | None = None):
    headers = {"Content-Type": "application/json"}
    if extra_headers:
        headers.update(extra_headers)
    return request_http(url, method="POST", payload=data, headers=headers)


def completed_artifact(idea: str = "Uma ideia original") -> EvolutionArtifact:
    return EvolutionArtifact(
        artifact_id="ART-UI-TEST",
        run_id="RUN-UI-TEST",
        treatment_mode=TreatmentMode.LEAN_L1,
        terminal_status="COMPLETED_DIRECT_ONE_PASS",
        original_idea=idea,
        human_intent="A intenção interpretada",
        refined_idea="Uma proposta atual",
        what_changed=["Uma mudança observável"],
        assumptions=["Uma premissa não verificada"],
        uncertainties=["Uma incerteza em aberto"],
        recommended_next_action="Testar a proposta com alguém que a usaria.",
    )


class ResponseService:
    def __init__(self, response: EvolutionResponse, gate: threading.Event | None = None, entered: threading.Event | None = None):
        self.response = response
        self.calls: list[EvolutionRequest] = []
        self.gate = gate
        self.entered = entered

    def evolve(self, request: EvolutionRequest) -> EvolutionResponse:
        self.calls.append(request)
        if self.entered:
            self.entered.set()
        if self.gate:
            self.gate.wait(timeout=5)
        return self.response


def test_get_home_and_health_are_local_and_do_not_create_provider_calls(tmp_path: Path):
    runner = FakeModelRunner()
    service = IdeaEvolutionService(runner=runner, runs_dir=tmp_path / "runs")

    with running_server(lambda: service) as (base_url, _server):
        status, html, headers = request_http(f"{base_url}/")
        health_status, health_body, _ = request_http(f"{base_url}/api/health")

    assert status == 200
    page = html.decode("utf-8")
    assert "O que vamos criar?" in page
    assert "Dependendo da configuração atual" in page
    assert "name=\"idea\"" in page
    assert "Access-Control-Allow-Origin" not in headers
    assert health_status == 200
    assert json.loads(health_body) == {"status": "ok"}
    assert runner.call_counts == {}


def test_post_runs_the_existing_service_and_maps_real_artifact_fields(tmp_path: Path):
    runner = FakeModelRunner()
    service = IdeaEvolutionService(runner=runner, runs_dir=tmp_path / "runs")
    idea = "Criar uma ferramenta para organizar ideias ainda vagas."

    with running_server(lambda: service) as (base_url, _server):
        status, body, headers = json_post(
            f"{base_url}/api/evolve",
            json.dumps({"idea": idea}, ensure_ascii=False).encode("utf-8"),
            {"Origin": base_url},
        )

    payload = json.loads(body)
    assert status == 200
    assert payload["success"] is True
    assert payload["artifact"]["original_idea"] == idea
    assert payload["artifact"]["refined_idea"]
    assert "human_intent" in payload["artifact"]
    assert "intent_provenance" in payload["artifact"]
    assert payload["artifact"]["original_idea_authority"] == "USER_EXPLICIT"
    assert payload["artifact"]["recommended_next_action_basis"]
    assert "Access-Control-Allow-Origin" not in headers
    assert runner.call_counts


def test_blank_idea_is_rejected_by_the_existing_service_without_model_calls(tmp_path: Path):
    runner = FakeModelRunner()
    service = IdeaEvolutionService(runner=runner, runs_dir=tmp_path / "runs")
    factory_calls = []

    with running_server(lambda: (factory_calls.append("called") or service)) as (base_url, _server):
        status, body, _ = json_post(f"{base_url}/api/evolve", b'{"idea":"  "}')

    payload = json.loads(body)
    assert status == 400
    assert payload["failure_type"] == ServiceFailureType.INVALID_INPUT.value
    assert runner.call_counts == {}
    assert factory_calls == []


def test_malformed_json_is_rejected_without_calling_service():
    calls = []

    with running_server(lambda: calls.append("factory")) as (base_url, _server):
        status, body, _ = json_post(f"{base_url}/api/evolve", b'{"idea":')

    assert status == 400
    assert json.loads(body)["failure_type"] == "INVALID_JSON"
    assert calls == []


def test_oversized_body_is_rejected_before_service_factory():
    calls = []
    too_large = json.dumps({"idea": "a" * MAX_REQUEST_BODY_BYTES}).encode("utf-8")

    with running_server(lambda: calls.append("factory")) as (base_url, _server):
        status, body, _ = json_post(f"{base_url}/api/evolve", too_large)

    assert status == 413
    assert json.loads(body)["failure_type"] == "REQUEST_TOO_LARGE"
    assert calls == []


def test_mapping_preserves_epistemic_labels_without_mutating_artifact():
    artifact = completed_artifact()
    before = artifact.model_dump(mode="json")
    response = EvolutionResponse(
        success=True,
        run_id=artifact.run_id,
        treatment_used=TreatmentMode.LEAN_L1,
        raw_idea=artifact.original_idea,
        terminal_status=artifact.terminal_status,
        artifact=artifact,
    )

    payload = evolution_response_to_ui_data(response)

    assert artifact.model_dump(mode="json") == before
    assert payload["artifact"]["intent_provenance"] == "MODEL_HYPOTHESIS"
    assert payload["artifact"]["assumptions_authority"] == "MODEL_HYPOTHESIS"
    expected_keys = {
        "schema_version", "original_idea", "original_idea_authority", "human_intent", "intent_provenance",
        "refined_idea", "refined_idea_authority", "what_changed", "critique",
        "assumptions", "assumptions_authority", "uncertainties", "intent_ledger",
        "useful_insights", "open_decisions", "coverage_status", "coverage_issues",
        "candidate_possibilities",
        "recommended_next_action", "recommended_next_action_basis",
        "recommended_next_action_status", "recommended_next_action_support_ref",
        "recommended_next_action_target_uncertainty", "human_decision_required",
        "human_decision_description",
    }
    assert set(payload["artifact"]) == expected_keys
    assert not {"quality_score", "maturity_percentage", "evidence_count", "risk_count", "dominant_question"} & set(payload["artifact"])


def test_human_decision_required_is_a_result_state_not_an_http_failure():
    artifact = EvolutionArtifact(
        artifact_id="ART-DECISION",
        run_id="RUN-DECISION",
        treatment_mode=TreatmentMode.LEAN_L1,
        terminal_status="HUMAN_DECISION_REQUIRED",
        original_idea="Escolher como dividir uma decisão de valor.",
        human_intent="Resolver uma escolha normativa.",
        refined_idea="Uma proposta que aguarda uma escolha humana.",
        human_decision_required=True,
        human_decision_description="Definir qual valor deve prevalecer.",
    )
    response = EvolutionResponse(
        success=True,
        run_id=artifact.run_id,
        treatment_used=TreatmentMode.LEAN_L1,
        raw_idea=artifact.original_idea,
        terminal_status="HUMAN_DECISION_REQUIRED",
        human_decision_requested=True,
        artifact=artifact,
    )
    service = ResponseService(response)

    with running_server(lambda: service) as (base_url, _server):
        status, body, _ = json_post(
            f"{base_url}/api/evolve",
            json.dumps({"idea": "Escolher como dividir uma decisão de valor."}, ensure_ascii=False).encode("utf-8"),
        )

    payload = json.loads(body)
    assert status == 200
    assert payload["success"] is True
    assert payload["artifact"]["human_decision_required"] is True
    assert payload["artifact"]["human_decision_description"] == "Definir qual valor deve prevalecer."


def test_typed_provider_failure_is_returned_without_stack_trace():
    response = EvolutionResponse(
        success=False,
        run_id="RUN-FAIL",
        treatment_used=TreatmentMode.LEAN_L1,
        raw_idea="Ideia válida para o teste",
        terminal_status="PROVIDER_UNAVAILABLE",
        failure_type=ServiceFailureType.PROVIDER_UNAVAILABLE,
        error_message="Provedor indisponível no momento.",
    )
    service = ResponseService(response)

    with running_server(lambda: service) as (base_url, _server):
        status, body, _ = json_post(
            f"{base_url}/api/evolve",
            json.dumps({"idea": "Ideia válida para o teste"}, ensure_ascii=False).encode("utf-8"),
        )

    payload = json.loads(body)
    assert status == 503
    assert payload["failure_type"] == ServiceFailureType.PROVIDER_UNAVAILABLE.value
    assert payload["error_message"] == "Provedor indisponível no momento."
    assert "Traceback" not in body.decode("utf-8")


def test_provider_configuration_failure_is_typed_and_does_not_expose_exception_text():
    def unavailable_provider():
        raise RuntimeError("API_KEY_ABSENT")

    with running_server(unavailable_provider) as (base_url, _server):
        status, body, _ = json_post(
            f"{base_url}/api/evolve", b'{"idea":"Valid idea for setup"}'
        )

    payload = json.loads(body)
    assert status == 503
    assert payload["failure_type"] == ServiceFailureType.PROVIDER_AUTH_FAILURE.value
    assert "API_KEY_ABSENT" not in payload["error_message"]
    assert "Traceback" not in body.decode("utf-8")


def test_unexpected_service_exception_is_not_misclassified_as_provider_failure():
    class BrokenService:
        def evolve(self, _request):
            raise RuntimeError("unexpected internal exception")

    with running_server(lambda: BrokenService()) as (base_url, _server):
        status, body, _ = json_post(
            f"{base_url}/api/evolve", b'{"idea":"Idea for internal error"}'
        )

    payload = json.loads(body)
    assert status == 500
    assert payload["failure_type"] == ServiceFailureType.INTERNAL_APPLICATION_FAILURE.value
    assert "unexpected internal exception" not in payload["error_message"]


def test_foreign_origin_is_rejected_before_service_factory():
    calls = []

    with running_server(lambda: calls.append("factory")) as (base_url, _server):
        status, body, _ = json_post(
            f"{base_url}/api/evolve",
            json.dumps({"idea": "Ideia válida"}, ensure_ascii=False).encode("utf-8"),
            {"Origin": "https://evil.example"},
        )

    assert status == 403
    assert json.loads(body)["failure_type"] == "LOCAL_REQUEST_REQUIRED"
    assert calls == []


def test_foreign_host_is_rejected():
    with running_server(lambda: None) as (base_url, _server):
        status, body, _ = request_http(f"{base_url}/api/health", headers={"Host": "evil.example"})

    assert status == 403
    assert json.loads(body)["failure_type"] == "LOCAL_REQUEST_REQUIRED"


def test_json_payload_round_trips_untrusted_text_and_frontend_uses_text_content(tmp_path: Path):
    runner = FakeModelRunner()
    service = IdeaEvolutionService(runner=runner, runs_dir=tmp_path / "runs")
    idea = '<script>alert("x")</script> — árvore & café'

    with running_server(lambda: service) as (base_url, _server):
        status, body, headers = json_post(
            f"{base_url}/api/evolve", json.dumps({"idea": idea}, ensure_ascii=False).encode("utf-8")
        )

    payload = json.loads(body.decode("utf-8"))
    app_js = Path(__file__).parents[1] / "src" / "idea_evolution" / "ui" / "static" / "app.js"
    script = app_js.read_text(encoding="utf-8")
    assert status == 200
    assert headers.get_content_type() == "application/json"
    assert payload["artifact"]["original_idea"] == idea
    assert "textContent" in script
    assert ".innerHTML" not in script


def test_duplicate_concurrent_submission_fails_closed():
    entered = threading.Event()
    release = threading.Event()
    response = EvolutionResponse(
        success=True,
        run_id="RUN-CONCURRENT",
        treatment_used=TreatmentMode.LEAN_L1,
        raw_idea="Ideia concorrente",
        terminal_status="COMPLETED_DIRECT_ONE_PASS",
        artifact=completed_artifact("Ideia concorrente"),
    )
    service = ResponseService(response, gate=release, entered=entered)
    first_result: list[tuple[int, bytes, Any]] = []

    with running_server(lambda: service) as (base_url, _server):
        first = threading.Thread(
            target=lambda: first_result.append(
                json_post(f"{base_url}/api/evolve", b'{"idea":"Ideia concorrente"}')
            ),
            daemon=True,
        )
        first.start()
        assert entered.wait(timeout=3)
        second_status, second_body, _ = json_post(
            f"{base_url}/api/evolve", b'{"idea":"Outra ideia"}'
        )
        release.set()
        first.join(timeout=5)

    assert second_status == 409
    assert json.loads(second_body)["failure_type"] == "REQUEST_ALREADY_RUNNING"
    assert len(service.calls) == 1
    assert first_result and first_result[0][0] == 200


def test_cli_ui_command_has_fixed_default_port_and_rejects_invalid_ports():
    args = parse_args(["ui"])
    assert args.command == "ui"
    assert args.port == 8765
    assert parse_args(["ui", "--port", "8766"]).port == 8766
    with pytest.raises(SystemExit):
        parse_args(["ui", "--port", "0"])


def test_server_refuses_non_loopback_bind_address():
    with pytest.raises(ValueError, match="127.0.0.1"):
        create_local_ui_server(lambda: None, port=8765, host="0.0.0.0")


def test_ui_does_not_expose_a_generic_file_route():
    with running_server(lambda: None) as (base_url, _server):
        status, body, _ = request_http(f"{base_url}/../../pyproject.toml")

    assert status == 404
    assert json.loads(body)["failure_type"] == "NOT_FOUND"
