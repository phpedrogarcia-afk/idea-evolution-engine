"""Servidor HTTP local e adaptador fino para o serviço de evolução existente."""

from __future__ import annotations

import json
import logging
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.resources import files
from typing import Callable, Any
from urllib.parse import urlsplit
from uuid import uuid4

from src.idea_evolution.artifacts.evolution_artifact import EvolutionArtifact
from src.idea_evolution.config.cost_policy import sanitize_secret_text
from src.idea_evolution.service.contracts import (
    EvolutionRequest,
    EvolutionResponse,
    ServiceFailureType,
    TreatmentMode,
)
from src.idea_evolution.service.evolution_service import IdeaEvolutionService


LOGGER = logging.getLogger(__name__)
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
MAX_REQUEST_BODY_BYTES = 64 * 1024

_STATIC_ASSETS = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/styles.css": ("styles.css", "text/css; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
    "/flask.svg": ("flask.svg", "image/svg+xml; charset=utf-8"),
}


def _enum_value(value: Any) -> Any:
    return value.value if hasattr(value, "value") else value


def _critique_data(item: Any) -> dict[str, Any]:
    return {
        "vulnerability": item.vulnerability,
        "severity": item.severity,
        "why_it_matters": item.why_it_matters,
        "affected_aspect": item.affected_aspect,
        "authority_basis": _enum_value(item.authority_basis),
        "gate_eligible": item.gate_eligible,
    }


def _possibility_data(item: Any) -> dict[str, Any]:
    return {
        "mechanism": item.mechanism,
        "authority_basis": _enum_value(item.authority_basis),
        "ontology_state": _enum_value(item.ontology_state),
        "justification": item.justification,
        "tradeoffs": list(item.tradeoffs),
        "path_id": item.path_id,
        "intent_ids": list(item.intent_ids),
    }


def _intent_ledger_data(item: Any) -> dict[str, Any]:
    return {
        "intent_id": item.intent_id,
        "source_quote": item.source_quote,
        "interpretation": item.interpretation,
        "importance": _enum_value(item.importance),
        "origin_type": _enum_value(item.origin_type),
        "treatment_in_current_form": item.treatment_in_current_form,
        "status": _enum_value(item.status),
    }


def _useful_insight_data(item: Any) -> dict[str, Any]:
    return {
        "insight_id": item.insight_id,
        "description": item.description,
        "related_intent_ids": list(item.related_intent_ids),
        "authority_basis": _enum_value(item.authority_basis),
    }


def _open_decision_data(item: Any) -> dict[str, Any]:
    return {
        "decision_id": item.decision_id,
        "question": item.question,
        "related_intent_ids": list(item.related_intent_ids),
    }


def _coverage_issue_data(item: Any) -> dict[str, Any]:
    return {
        "issue_type": _enum_value(item.issue_type),
        "description": item.description,
        "intent_id": item.intent_id,
        "path_id": item.path_id,
    }


def evolution_response_to_ui_data(response: EvolutionResponse) -> dict[str, Any]:
    """Projeta somente campos presentes no contrato real, sem alterar o artefato."""
    failure_type = _enum_value(response.failure_type) if response.failure_type else None
    result: dict[str, Any] = {
        "success": response.success,
        "terminal_status": response.terminal_status,
        "failure_type": failure_type,
    }
    if response.error_message:
        result["error_message"] = sanitize_secret_text(response.error_message)

    artifact: EvolutionArtifact | None = response.artifact
    if artifact is None:
        return result

    result["artifact"] = {
        "schema_version": artifact.schema_version,
        "original_idea": artifact.original_idea,
        "original_idea_authority": _enum_value(artifact.original_idea_authority),
        "human_intent": artifact.human_intent,
        "intent_provenance": _enum_value(artifact.intent_provenance),
        "refined_idea": artifact.refined_idea,
        "refined_idea_authority": _enum_value(artifact.refined_idea_authority),
        "what_changed": list(artifact.what_changed),
        "critique": [_critique_data(item) for item in artifact.critique],
        "assumptions": list(artifact.assumptions),
        "assumptions_authority": _enum_value(artifact.assumptions_authority),
        "uncertainties": list(artifact.uncertainties),
        "intent_ledger": [_intent_ledger_data(item) for item in artifact.intent_ledger],
        "useful_insights": [_useful_insight_data(item) for item in artifact.useful_insights],
        "open_decisions": [_open_decision_data(item) for item in artifact.open_decisions],
        "coverage_status": _enum_value(artifact.coverage_status),
        "coverage_issues": [_coverage_issue_data(item) for item in artifact.coverage_issues],
        "candidate_possibilities": [
            _possibility_data(item) for item in artifact.candidate_possibilities
        ],
        "recommended_next_action": artifact.recommended_next_action,
        "recommended_next_action_basis": _enum_value(artifact.recommended_next_action_basis),
        "recommended_next_action_status": artifact.recommended_next_action_status,
        "recommended_next_action_support_ref": artifact.recommended_next_action_support_ref,
        "recommended_next_action_target_uncertainty": artifact.recommended_next_action_target_uncertainty,
        "human_decision_required": bool(
            response.human_decision_requested
            or artifact.human_decision_required
            or response.terminal_status == "HUMAN_DECISION_REQUIRED"
        ),
        "human_decision_description": artifact.human_decision_description,
    }
    return result


def _response_status(response: EvolutionResponse) -> int:
    if response.success and response.artifact is not None:
        return 200
    if response.failure_type == ServiceFailureType.INVALID_INPUT:
        return 400
    if response.failure_type in {
        ServiceFailureType.PROVIDER_AUTH_FAILURE,
        ServiceFailureType.PROVIDER_RATE_LIMIT,
        ServiceFailureType.PROVIDER_SERVER_FAILURE,
        ServiceFailureType.PROVIDER_UNAVAILABLE,
        ServiceFailureType.COST_POLICY_BLOCKED,
    }:
        return 503
    if response.failure_type == ServiceFailureType.STRUCTURED_OUTPUT_FAILURE:
        return 502
    if response.success:
        return 500
    return 500


class _LocalThreadingHTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(
        self,
        address: tuple[str, int],
        handler: type[BaseHTTPRequestHandler],
        service_factory: Callable[[], IdeaEvolutionService],
    ) -> None:
        self.service_factory = service_factory
        self.evolution_lock = threading.Lock()
        super().__init__(address, handler)


class _UIRequestHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "FioIdeiasLocalUI"
    sys_version = ""

    @property
    def ui_server(self) -> _LocalThreadingHTTPServer:
        return self.server  # type: ignore[return-value]

    def _host_matches(self) -> bool:
        host_header = self.headers.get("Host", "")
        try:
            host = urlsplit(f"//{host_header}")
            host_name = (host.hostname or "").lower()
            host_port = host.port
            if host_port is None and self.server.server_port == 80:
                host_port = 80
        except ValueError:
            return False
        return (
            host_name == DEFAULT_HOST
            and host_port == self.server.server_port
            and not host.username
            and not host.password
            and not host.path
            and not host.query
            and not host.fragment
        )

    def _origin_matches(self) -> bool:
        origin_header = self.headers.get("Origin")
        if origin_header is None:
            return True
        try:
            origin = urlsplit(origin_header)
            origin_name = (origin.hostname or "").lower()
            origin_port = origin.port
            if origin_port is None and origin.scheme == "http":
                origin_port = 80
        except ValueError:
            return False
        return (
            origin.scheme == "http"
            and origin_name == DEFAULT_HOST
            and origin_port == self.server.server_port
            and not origin.username
            and not origin.password
            and not origin.path
            and not origin.query
            and not origin.fragment
        )

    def _send_bytes(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        if self.close_connection:
            self.send_header("Connection", "close")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "img-src 'self' data:; connect-src 'self'; object-src 'none'; "
            "base-uri 'none'; form-action 'self'; frame-ancestors 'none'",
        )
        self.end_headers()
        if body and self.command != "HEAD":
            self.wfile.write(body)

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self._send_bytes(status, body, "application/json; charset=utf-8")

    def _send_error(self, status: int, message: str, code: str) -> None:
        self.close_connection = True
        self._send_json(status, {"success": False, "failure_type": code, "error_message": message})

    def _reject_non_local(self) -> bool:
        if not self._host_matches() or not self._origin_matches():
            self._send_error(403, "A interface aceita apenas solicitações locais.", "LOCAL_REQUEST_REQUIRED")
            return True
        return False

    def do_GET(self) -> None:
        if self._reject_non_local():
            return
        path = urlsplit(self.path).path
        if path == "/api/health":
            self._send_json(200, {"status": "ok"})
            return
        asset = _STATIC_ASSETS.get(path)
        if asset is None:
            self._send_error(404, "Rota não encontrada.", "NOT_FOUND")
            return
        name, content_type = asset
        body = files("src.idea_evolution.ui").joinpath("static", name).read_bytes()
        self._send_bytes(200, body, content_type)

    def do_POST(self) -> None:
        if self._reject_non_local():
            return
        if urlsplit(self.path).path != "/api/evolve":
            self._send_error(404, "Rota não encontrada.", "NOT_FOUND")
            return
        if self.headers.get("Transfer-Encoding"):
            self._send_error(400, "Envie o conteúdo com Content-Length.", "INVALID_REQUEST")
            return
        if self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower() != "application/json":
            self._send_error(415, "O conteúdo deve ser enviado como JSON.", "UNSUPPORTED_MEDIA_TYPE")
            return
        try:
            content_length = int(self.headers.get("Content-Length", ""))
        except ValueError:
            self._send_error(411, "Informe o tamanho do conteúdo enviado.", "LENGTH_REQUIRED")
            return
        if content_length < 0:
            self._send_error(400, "Tamanho do conteúdo inválido.", "INVALID_REQUEST")
            return
        if content_length > MAX_REQUEST_BODY_BYTES:
            self._send_error(413, "A ideia excede o limite de envio desta interface.", "REQUEST_TOO_LARGE")
            return

        raw_body = self.rfile.read(content_length)
        if len(raw_body) != content_length:
            self._send_error(400, "O conteúdo enviado está incompleto.", "INVALID_REQUEST")
            return
        try:
            decoded = raw_body.decode("utf-8", errors="strict")

            def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
                value: dict[str, Any] = {}
                for key, item in pairs:
                    if key in value:
                        raise ValueError("chave JSON duplicada")
                    value[key] = item
                return value

            payload = json.loads(
                decoded,
                object_pairs_hook=reject_duplicate_keys,
                parse_constant=lambda _value: (_ for _ in ()).throw(ValueError("constante JSON inválida")),
            )
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            self._send_error(400, "O conteúdo deve ser um JSON válido.", "INVALID_JSON")
            return
        if not isinstance(payload, dict) or set(payload) != {"idea"}:
            self._send_error(400, "Envie somente o campo idea como texto.", "INVALID_REQUEST")
            return
        idea = payload.get("idea")
        if not isinstance(idea, str):
            self._send_error(400, "O campo idea deve ser um texto.", "INVALID_INPUT")
            return

        request = EvolutionRequest(
            raw_idea=idea,
            treatment_mode=TreatmentMode.LEAN_L1,
            run_id=f"RUN-UI-{uuid4().hex}",
        )
        validation_error = request.validate_input()
        if validation_error:
            invalid_response = EvolutionResponse(
                success=False,
                run_id=request.run_id or "RUN-UI-INVALID",
                treatment_used=TreatmentMode.LEAN_L1,
                raw_idea=request.raw_idea,
                terminal_status="INVALID_INPUT",
                failure_type=ServiceFailureType.INVALID_INPUT,
                error_message=validation_error,
            )
            self._send_json(400, evolution_response_to_ui_data(invalid_response))
            return
        if not self.ui_server.evolution_lock.acquire(blocking=False):
            self._send_error(409, "Já existe uma evolução em andamento nesta interface.", "REQUEST_ALREADY_RUNNING")
            return

        try:
            try:
                service = self.ui_server.service_factory()
            except Exception as exc:
                # Não registrar texto da ideia, credenciais ou mensagem bruta da exceção.
                LOGGER.error("UI service initialization failed (%s)", type(exc).__name__)
                error_text = str(exc)
                if any(marker in error_text.lower() for marker in ("unsupported_provider", "cost_policy")):
                    failure = ServiceFailureType.COST_POLICY_BLOCKED
                else:
                    failure = IdeaEvolutionService._classify_error(
                        error_text, default=ServiceFailureType.PROVIDER_UNAVAILABLE
                    )
                self._send_error(
                    503,
                    "Não foi possível iniciar o provedor configurado. Verifique a configuração local.",
                    failure.value,
                )
                return

            try:
                response = service.evolve(request)
            except Exception as exc:
                LOGGER.error("UI evolution failed (%s)", type(exc).__name__)
                self._send_error(
                    500,
                    "Ocorreu um erro interno inesperado. Nenhuma resposta utilizável foi retornada.",
                    ServiceFailureType.INTERNAL_APPLICATION_FAILURE.value,
                )
                return

            payload_out = evolution_response_to_ui_data(response)
            status = _response_status(response)
            if response.success and response.artifact is None:
                payload_out = {
                    "success": False,
                    "terminal_status": "ARTIFACT_MISSING",
                    "failure_type": ServiceFailureType.INTERNAL_APPLICATION_FAILURE.value,
                    "error_message": "A execução terminou sem retornar uma proposta utilizável.",
                }
                status = 500
            self._send_json(status, payload_out)
        finally:
            self.ui_server.evolution_lock.release()

    def do_HEAD(self) -> None:
        if self._reject_non_local():
            return
        if urlsplit(self.path).path in _STATIC_ASSETS:
            asset = _STATIC_ASSETS[urlsplit(self.path).path]
            body = files("src.idea_evolution.ui").joinpath("static", asset[0]).read_bytes()
            self._send_bytes(200, body, asset[1])
            return
        self._send_error(404, "Rota não encontrada.", "NOT_FOUND")

    def do_OPTIONS(self) -> None:
        if self._reject_non_local():
            return
        self.send_response(405)
        self.send_header("Allow", "GET, HEAD, POST")
        self.send_header("Content-Length", "0")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def do_PUT(self) -> None:
        self._send_error(405, "Método não permitido.", "METHOD_NOT_ALLOWED")

    def do_PATCH(self) -> None:
        self._send_error(405, "Método não permitido.", "METHOD_NOT_ALLOWED")

    def do_DELETE(self) -> None:
        self._send_error(405, "Método não permitido.", "METHOD_NOT_ALLOWED")


def create_local_ui_server(
    service_factory: Callable[[], IdeaEvolutionService],
    port: int = DEFAULT_PORT,
    host: str = DEFAULT_HOST,
) -> ThreadingHTTPServer:
    """Cria servidor estritamente preso a IPv4 loopback; `port=0` serve para testes."""
    if host != DEFAULT_HOST:
        raise ValueError("A interface local só pode escutar em 127.0.0.1.")
    if not 0 <= port <= 65535:
        raise ValueError("Porta inválida.")
    return _LocalThreadingHTTPServer((DEFAULT_HOST, port), _UIRequestHandler, service_factory)
