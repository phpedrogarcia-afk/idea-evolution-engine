"""
src/idea_evolution/cli/main.py
Interface de Linha de Comando (CLI) para FioIdeias V1 — Ponto de Entrada Estável (P5).

Roteia exclusivamente através da camada de serviço IdeaEvolutionService com
o tratamento Lean L1 como padrão canônico de produto, sob política estrita
de custo de bolso zero (OUT_OF_POCKET_COST = ZERO) e proveniência ontológica.
"""

from __future__ import annotations

import sys
import os
import argparse
from pathlib import Path
import json
from typing import Optional, List, Dict, Any

from src.idea_evolution.service.contracts import (
    EvolutionRequest,
    EvolutionResponse,
    TreatmentMode,
    ServiceFailureType,
)
from src.idea_evolution.service.evolution_service import IdeaEvolutionService
from src.idea_evolution.rendering.human_result import HumanResultRenderer
from src.idea_evolution.config.cost_policy import (
    ProviderConfig,
    CostEligibility,
    ZeroCostGuard,
    sanitize_secret_text,
)
from src.idea_evolution.config.catalog import ModelCatalog
from src.idea_evolution.providers.base import ModelRunner
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.providers.native import NativeModelRunner, check_providers_health
from src.idea_evolution.orchestration.baseline import BaselineRunner
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.config.routing import ModelRoutingConfig

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
RUNS_DIR = REPO_ROOT / "runs"


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Configura o analisador de argumentos da CLI do FioIdeias V1."""
    parser = argparse.ArgumentParser(
        prog="iee",
        description="Idea Evolution Engine — FioIdeias V1",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ---------------------------------------------------------------------------
    # COMANDO CANÔNICO DE PRODUTO: evolve
    # ---------------------------------------------------------------------------
    evolve_p = subparsers.add_parser(
        "evolve",
        help="Maturar e refinar uma ideia crua preservando intenção humana, incertezas e proveniência",
        description="Maturar e refinar uma ideia crua através do FioIdeias V1 (caminho padrão Lean L1)."
    )
    evolve_p.add_argument(
        "raw_idea",
        nargs="?",
        default=None,
        help="Texto da ideia crua a ser maturada (argumento posicional direto)",
    )
    evolve_p.add_argument(
        "--idea",
        "-i",
        type=str,
        default=None,
        help="Texto da ideia crua (alternativa ao argumento posicional)",
    )
    evolve_p.add_argument(
        "--idea-file",
        "-f",
        type=Path,
        default=None,
        help="Arquivo contendo o texto da ideia crua",
    )
    evolve_p.add_argument(
        "--fast",
        action="store_true",
        help="Executa refinamento rápido de passada única (Fast Fallback)",
    )
    evolve_p.add_argument(
        "--json",
        action="store_true",
        help="Exibe a saída exclusivamente em JSON serializado do EvolutionArtifact",
    )
    evolve_p.add_argument(
        "--provider",
        "-p",
        type=str,
        default=None,
        help="Provedor de inferência (padrão: cerebras)",
    )
    evolve_p.add_argument(
        "--model",
        "-m",
        type=str,
        default=None,
        help="Identificador do modelo a ser utilizado",
    )
    evolve_p.add_argument(
        "--runs-dir",
        type=Path,
        default=None,
        help="Diretório customizado para armazenamento de rastros de execução",
    )
    evolve_p.add_argument(
        "--dry-run",
        action="store_true",
        help="Valida rotas e configuração de custo sem realizar chamadas de modelo",
    )
    evolve_p.add_argument(
        "--debug",
        action="store_true",
        help="Exibe detalhes técnicos operacionais para diagnóstico",
    )

    # ---------------------------------------------------------------------------
    # COMANDOS DE SUPORTE E DIAGNÓSTICO
    # ---------------------------------------------------------------------------
    # COMPARE (Pesquisa / Benchmarking controlado)
    comp_p = subparsers.add_parser("compare", help="Executar comparação experimental sobre uma fixture")
    comp_p.add_argument("--fixture-file", "-f", type=Path, required=True, help="Caminho para o JSON da fixture")

    # INSPECT-RUN
    insp_p = subparsers.add_parser("inspect-run", help="Inspecionar detalhes de uma execução passada")
    insp_p.add_argument("run_id", type=str, help="ID da execução (ex: RUN-20260904-001)")

    # PROVIDERS
    prov_p = subparsers.add_parser("providers", help="Gerenciamento e diagnóstico de provedores de IA")
    prov_sub = prov_p.add_subparsers(dest="prov_command", required=True)
    prov_sub.add_parser("doctor", help="Verifica adaptadores instalados e presença de credenciais sem expor valores")

    # ROUTES
    routes_p = subparsers.add_parser("routes", help="Inspeção de rotas de modelos por estágio")
    routes_sub = routes_p.add_subparsers(dest="routes_command", required=True)
    show_p = routes_sub.add_parser("show", help="Exibe o mapeamento de estágios para provedores/modelos")
    show_p.add_argument("--model-config", "-c", type=Path, default=None, help="Arquivo de configuração de rotas")

    return parser.parse_args(argv)


def resolve_runner(
    provider: Optional[str] = None,
    model: Optional[str] = None,
) -> ModelRunner:
    """Resolve o executor ModelRunner apropriado sob a política de custo zero."""
    prov = (provider or os.environ.get("IEE_PROVIDER", "cerebras")).lower().strip()

    if prov.startswith("fake"):
        return FakeModelRunner(provider=prov, default_model=model or "fake-model-v1")
    elif prov == "cerebras":
        from src.idea_evolution.providers.cerebras import CerebrasRunner
        return CerebrasRunner(model_name=model or "openai/gpt-oss-120b")
    else:
        return NativeModelRunner(provider=prov, default_model=model or "default-model")


def run_evolve(args: argparse.Namespace, runner: Optional[ModelRunner] = None) -> int:
    """Executa o comando evolve através da camada de serviço IdeaEvolutionService."""
    # 1. Resolução do texto da ideia
    idea_text = args.raw_idea or args.idea
    if args.idea_file:
        if not args.idea_file.exists():
            print(f"[ERRO OPERACIONAL] INVALID_INPUT: Arquivo de ideia não encontrado: {args.idea_file}", file=sys.stderr)
            return 1
        try:
            idea_text = args.idea_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[ERRO OPERACIONAL] INVALID_INPUT: Falha ao ler arquivo: {sanitize_secret_text(str(e))}", file=sys.stderr)
            return 1

    # Validação preliminar de entrada
    if not idea_text or not idea_text.strip() or len(idea_text.strip()) < 3:
        err_msg = "A ideia fornecida está vazia ou é excessivamente curta (mínimo 3 caracteres)."
        if getattr(args, "json", False):
            print(json.dumps({
                "success": False,
                "failure_type": ServiceFailureType.INVALID_INPUT.value,
                "error_message": err_msg,
            }, indent=2, ensure_ascii=False))
        else:
            print(f"[ERRO OPERACIONAL] INVALID_INPUT: {err_msg}", file=sys.stderr)
        return 1

    # 2. Resolução do executor de modelo
    if runner is None:
        try:
            runner = resolve_runner(args.provider, args.model)
        except Exception as e:
            sanitized_err = sanitize_secret_text(str(e))
            fail_type = (
                ServiceFailureType.COST_POLICY_BLOCKED.value
                if ("UNSUPPORTED_PROVIDER" in sanitized_err or "COST_POLICY" in sanitized_err)
                else ServiceFailureType.PROVIDER_FAILURE.value
            )
            if getattr(args, "json", False):
                print(json.dumps({
                    "success": False,
                    "failure_type": fail_type,
                    "error_message": sanitized_err,
                }, indent=2, ensure_ascii=False))
            else:
                print(f"[ERRO OPERACIONAL] {fail_type}: {sanitized_err}", file=sys.stderr)
            return 1

    # 3. Dry-Run / Plano de Execução (se solicitado)
    if getattr(args, "dry_run", False):
        p_config = ProviderConfig.infer_from_runner(runner, model_name=args.model)
        is_valid, reason = ZeroCostGuard.validate_provider_config(p_config)
        if not is_valid:
            print(f"[ERRO DE POLÍTICA] COST_POLICY_BLOCKED: {reason}", file=sys.stderr)
            return 1

        treatment_name = "FAST_FALLBACK (Passada Única)" if getattr(args, "fast", False) else "LEAN_L1 (Padrão V1)"
        print("=" * 65)
        print("       FIOIDEIAS V1 — PLANO DE EXECUÇÃO / DRY RUN")
        print("=" * 65)
        print(f"  Tratamento:           {treatment_name}")
        print(f"  Provedor:             {p_config.provider}")
        print(f"  Modelo de Transporte: {p_config.transport_model}")
        print(f"  Modelo Científico:    {p_config.scientific_model}")
        print(f"  Custo Elegível:       {p_config.cost_eligibility.value}")
        print(f"  Guarda de Custo Zero: APROVADA")
        print("-" * 65)
        print("[OK] PLANO VÁLIDO: Zero chamadas reais de modelo realizadas.")
        print("=" * 65)
        return 0

    # 4. Determinação do tratamento (Lean L1 padrão incondicional; --fast apenas se explicitado)
    treatment = TreatmentMode.FAST_FALLBACK if getattr(args, "fast", False) else TreatmentMode.LEAN_L1

    # 5. Delegação estrita ao IdeaEvolutionService
    runs_dir = args.runs_dir or RUNS_DIR
    service = IdeaEvolutionService(
        runner=runner,
        default_treatment=treatment,
        runs_dir=runs_dir,
    )

    req = EvolutionRequest(
        raw_idea=idea_text,
        treatment_mode=treatment,
        model_name=args.model,
    )

    response: EvolutionResponse = service.evolve(req)

    # 6. Emissão de Resultados (JSON ou Texto)
    if getattr(args, "json", False):
        if response.artifact is not None:
            print(response.artifact.model_dump_json(indent=2))
        else:
            err_payload = {
                "success": response.success,
                "run_id": response.run_id,
                "terminal_status": response.terminal_status,
                "failure_type": response.failure_type.value if response.failure_type else None,
                "error_message": sanitize_secret_text(response.error_message or ""),
            }
            print(json.dumps(err_payload, indent=2, ensure_ascii=False))
        return 0 if response.success else 1

    # Modo texto limpo (sem poluição laboratorial)
    if not response.success:
        fail_code = response.failure_type.value if response.failure_type else "OPERATIONAL_FAILURE"
        sanitized_err = sanitize_secret_text(response.error_message or "Falha durante o processo de maturação.")
        print(f"[ERRO OPERACIONAL] {fail_code}: {sanitized_err}", file=sys.stderr)
        return 1

    # 7. Renderização humana canônica de produto via HumanResultRenderer (M06 P6)
    if response.artifact is None:
        print("[ERRO OPERACIONAL] ARTIFACT_MISSING: Nenhum artefato produzido pela evolução.", file=sys.stderr)
        return 1

    # Persistência do artefato canônico para inspeção e auditoria sem chamadas adicionais de modelo
    if response.run_id and runs_dir:
        run_folder = Path(runs_dir) / response.run_id
        if run_folder.exists():
            try:
                (run_folder / "evolution_artifact.json").write_text(
                    response.artifact.model_dump_json(indent=2), encoding="utf-8"
                )
            except Exception:
                pass

    rendered_text = HumanResultRenderer.render(response.artifact)
    print(rendered_text)
    return 0


def run_compare(args: argparse.Namespace) -> int:
    """Executa comparação experimental sobre uma fixture."""
    if not args.fixture_file.exists():
        print(f"[ERRO] Arquivo de fixture não encontrado: {args.fixture_file}", file=sys.stderr)
        return 1

    fixture_data = json.loads(args.fixture_file.read_text(encoding="utf-8"))
    idea_text = fixture_data.get("idea_text") or fixture_data.get("original_idea")

    print(f"Executando comparação experimental sobre fixture: {fixture_data.get('name')}")
    runner = FakeModelRunner()

    b_runner = BaselineRunner(runner)
    res_a = b_runner.run(idea_text)

    loop_b = SimpleLoopRunner(runner=runner, topology="STANDARD_6_STAGE")
    res_b = loop_b.run(idea_text)

    loop_c = SimpleLoopRunner(runner=runner, topology="ITERATIVE_CRITIQUE_REVISION")
    res_c = loop_c.run(idea_text)

    print("\n[OK] Comparação concluída.")
    print(f"  - Baseline A: {res_a['run_id']}")
    print(f"  - Condition B (Standard): {res_b.run_id}")
    print(f"  - Condition C (Critique-Revision): {res_c.run_id}")
    return 0


def run_inspect(args: argparse.Namespace) -> int:
    """Inspeciona detalhes de uma execução passada."""
    run_path = RUNS_DIR / args.run_id
    if not run_path.exists():
        print(f"[ERRO] Run ID '{args.run_id}' não encontrado em runs/", file=sys.stderr)
        return 1

    art_json = run_path / "evolution_artifact.json"
    if art_json.exists():
        print(art_json.read_text(encoding="utf-8"))
        return 0

    final_md = run_path / "final.md"
    if final_md.exists():
        print(final_md.read_text(encoding="utf-8"))
        return 0

    trace_json = run_path / "trace.json"
    if trace_json.exists():
        trace = json.loads(trace_json.read_text(encoding="utf-8"))
        print("\n--- Telemetria do Run ---")
        print(f"Duração Total: {trace.get('total_duration_seconds', 0):.2f}s")
        print(f"Estágios Executados: {trace.get('total_stages_executed', 0)}")
        return 0

    print(f"[ERRO] Nenhum artefato encontrado em runs/{args.run_id}/", file=sys.stderr)
    return 1


def run_providers_doctor(args: argparse.Namespace) -> int:
    """Diagnóstico e conformidade de provedores sob política de custo zero."""
    health = check_providers_health()
    print("=" * 80)
    print("          FIOIDEIAS V1 — DIAGNÓSTICO DE PROVEDORES & GOVERNANÇA")
    print("=" * 80)
    print(f"{'PROVEDOR':<16} {'ADAPTADOR':<12} {'MODELO PADRÃO':<24} {'STATUS':<10} {'COST CLASS':<14} {'FREE_ONLY':<10}")
    print("-" * 80)
    for pid, info in health.items():
        adapt_str = "[OK] Sim" if info["adapter_available"] else "[--] Nao"
        status_str = info["catalog_status"]
        cost_str = info["cost_class"]
        free_str = "[OK] Sim" if info["free_eligible"] else "[X] Nao"
        print(f"{info['name']:<16} {adapt_str:<12} {info['default_model']:<24} {status_str:<10} {cost_str:<14} {free_str:<10}")

    print("-" * 80)
    print("Nenhum segredo ou credencial é exibido. Zero chamadas de inferência realizadas.")
    print("=" * 80)
    return 0


def run_routes_show(args: argparse.Namespace) -> int:
    """Inspeção de rotas de modelos por estágio."""
    if args.model_config:
        config = ModelRoutingConfig.from_file(args.model_config)
    else:
        config = ModelRoutingConfig.default_single_model()

    print("=" * 65)
    print("          FIOIDEIAS V1 — INSPEÇÃO DE ROTAS")
    print("=" * 65)
    print(f"  Routing Config Hash:  {config.compute_hash()[:16]}...")
    print("-" * 65)
    for stg, m_def in config.stage_assignments.items():
        print(f"  {stg:<22} -> {m_def.provider}/{m_def.model}")
    print("=" * 65)
    return 0


def main(argv: Optional[List[str]] = None, runner: Optional[ModelRunner] = None) -> int:
    """Ponto de entrada estável e canônico do CLI iee."""
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    args = parse_args(argv)

    if args.command == "evolve":
        return run_evolve(args, runner=runner)
    elif args.command == "compare":
        return run_compare(args)
    elif args.command == "inspect-run":
        return run_inspect(args)
    elif args.command == "providers" and getattr(args, "prov_command", None) == "doctor":
        return run_providers_doctor(args)
    elif args.command == "routes" and getattr(args, "routes_command", None) == "show":
        return run_routes_show(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
