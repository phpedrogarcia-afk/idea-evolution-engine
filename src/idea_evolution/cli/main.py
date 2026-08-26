"""
src/idea_evolution/cli/main.py
Interface de Linha de Comando (CLI) para o Idea Evolution Engine MVP.
Comandos:
  iee evolve --idea "..." [--topology standard | critique_revision] [--model-config path/to/config.yaml] [--dry-run]
  iee compare --fixture-file path/to/fixture.json
  iee inspect-run RUN-YYYYMMDD-NNN
  iee providers doctor
  iee routes show [--model-config path/to/config.yaml] [--topology standard | critique_revision]
"""

import sys
import os
import argparse
from pathlib import Path
import json

from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.orchestration.baseline import BaselineRunner
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.providers.native import NativeModelRunner, check_providers_health
from src.idea_evolution.config.routing import ModelRoutingConfig
from src.idea_evolution.providers.router import RunnerRouter
from src.idea_evolution.domain.state import RunStatus

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
RUNS_DIR = REPO_ROOT / "runs"


def parse_args():
    parser = argparse.ArgumentParser(
        prog="iee",
        description="Idea Evolution Engine — CLI do Simple Loop MVP & Multi-Model Routing",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # EVOLVE
    evolve_p = subparsers.add_parser("evolve", help="Maturar uma ideia crua através do Simple Loop")
    evolve_p.add_argument("--idea", "-i", type=str, help="Texto da ideia crua")
    evolve_p.add_argument("--idea-file", "-f", type=Path, help="Arquivo contendo o texto da ideia")
    evolve_p.add_argument(
        "--topology",
        "-t",
        choices=["standard", "critique_revision"],
        default="standard",
        help="Topologia do loop (standard = Condição B, critique_revision = Condição C)",
    )
    evolve_p.add_argument(
        "--provider",
        "-p",
        choices=["fake", "groq", "openai", "gemini", "anthropic"],
        default="fake",
        help="Provedor padrão (usado se não houver --model-config)",
    )
    evolve_p.add_argument("--model", "-m", type=str, default=None, help="Nome do modelo padrão")
    evolve_p.add_argument("--model-config", "-c", type=Path, default=None, help="Caminho para arquivo YAML/JSON de configuração de rotas multi-modelo")
    evolve_p.add_argument("--dry-run", action="store_true", help="Valida rotas e monta plano de execução sem chamar nenhum modelo")

    # COMPARE
    comp_p = subparsers.add_parser("compare", help="Executar comparação experimental (A vs B vs C) sobre uma fixture")
    comp_p.add_argument("--fixture-file", "-f", type=Path, required=True, help="Caminho para o JSON da fixture")

    # INSPECT-RUN
    insp_p = subparsers.add_parser("inspect-run", help="Inspecionar detalhes de uma execução passada")
    insp_p.add_argument("run_id", type=str, help="ID da execução (ex: RUN-20260826-001)")

    # PROVIDERS
    prov_p = subparsers.add_parser("providers", help="Gerenciamento e diagnóstico de provedores de IA")
    prov_sub = prov_p.add_subparsers(dest="prov_command", required=True)
    prov_sub.add_parser("doctor", help="Verifica adaptadores instalados e presença de credenciais sem expor valores")

    # ROUTES
    routes_p = subparsers.add_parser("routes", help="Inspeção de rotas de modelos por estágio")
    routes_sub = routes_p.add_subparsers(dest="routes_command", required=True)
    show_p = routes_sub.add_parser("show", help="Exibe o mapeamento de estágios para provedores/modelos")
    show_p.add_argument("--model-config", "-c", type=Path, default=None, help="Arquivo de configuração de rotas")
    show_p.add_argument("--topology", "-t", choices=["standard", "critique_revision"], default="standard")

    return parser.parse_args()


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    args = parse_args()

    if args.command == "evolve":
        idea_text = args.idea
        if args.idea_file:
            if not args.idea_file.exists():
                print(f"[ERRO] Arquivo de ideia não encontrado: {args.idea_file}")
                sys.exit(1)
            idea_text = args.idea_file.read_text(encoding="utf-8")

        if not idea_text and not args.dry_run:
            print("[ERRO] É necessário fornecer a ideia via --idea ou --idea-file.")
            sys.exit(1)

        top_map = {
            "standard": "STANDARD_6_STAGE",
            "critique_revision": "ITERATIVE_CRITIQUE_REVISION",
        }
        topology = top_map[args.topology]

        # Carregar ou montar configuração de roteamento
        if args.model_config:
            if not args.model_config.exists():
                print(f"[ERRO] Arquivo de configuração não encontrado: {args.model_config}")
                sys.exit(1)
            config = ModelRoutingConfig.from_file(args.model_config)
        else:
            config = ModelRoutingConfig.default_single_model(provider=args.provider, model=args.model or "default-model")

        router = RunnerRouter(config=config)

        # DRY RUN
        if args.dry_run:
            print("=" * 65)
            print("       IDEA EVOLUTION ENGINE — DRY RUN / PLAN DE EXECUÇÃO")
            print("=" * 65)
            print(f"  Topologia:            {topology}")
            print(f"  Routing Config Hash:  {config.compute_hash()[:16]}...")
            print(f"  Schema Version:       {config.schema_version}")
            print("-" * 65)
            print("  MAPEAMENTO DE ESTÁGIOS:")
            temp_runner = SimpleLoopRunner(router=router, topology=topology)
            for stg in temp_runner.get_required_stages():
                alias, m_def = config.resolve_stage(stg)
                print(f"    - {stg:<22} -> [{alias:<12}] {m_def.provider}/{m_def.model}")
            print("-" * 65)
            print("[OK] PLAN VALID: Zero chamadas de modelo realizadas no dry-run.")
            print("=" * 65)
            sys.exit(0)

        # EXECUÇÃO DO LOOP
        loop_runner = SimpleLoopRunner(router=router, topology=topology)

        print("=" * 65)
        print("          IDEA EVOLUTION ENGINE — SIMPLE LOOP RUNNER")
        print("=" * 65)
        print(f"  Ideia:     {idea_text[:60]}...")
        print(f"  Topologia: {topology}")
        print(f"  Config:    {args.model_config.name if args.model_config else 'default_single_model'}")
        print(f"  Hash:      {config.compute_hash()[:16]}...")
        print("-" * 65)
        print("Executando estágios dirigidos...")

        state = loop_runner.run(idea_text)

        print("-" * 65)
        print(f"Status Final: {state.status.value}")
        print(f"Run ID:       {state.run_id}")
        print(f"Artefatos salvos em: runs/{state.run_id}/")
        print("=" * 65)
        print("\n" + state.to_human_markdown())
        sys.exit(0 if state.status in [RunStatus.REFINED_IDEA_READY, RunStatus.REFINEMENT_INCOMPLETE] else 1)

    elif args.command == "compare":
        if not args.fixture_file.exists():
            print(f"[ERRO] Arquivo de fixture não encontrado: {args.fixture_file}")
            sys.exit(1)

        fixture_data = json.loads(args.fixture_file.read_text(encoding="utf-8"))
        idea_text = fixture_data.get("idea_text") or fixture_data.get("original_idea")

        print(f"Executando comparação experimental sobre fixture: {fixture_data.get('name')}")
        runner = FakeModelRunner()

        # Condição A: Baseline
        b_runner = BaselineRunner(runner)
        res_a = b_runner.run(idea_text)

        # Condição B: Standard Simple Loop
        loop_b = SimpleLoopRunner(runner=runner, topology="STANDARD_6_STAGE")
        res_b = loop_b.run(idea_text)

        # Condição C: Iterative Critique-Revision
        loop_c = SimpleLoopRunner(runner=runner, topology="ITERATIVE_CRITIQUE_REVISION")
        res_c = loop_c.run(idea_text)

        print("\n[OK] Comparação concluída.")
        print(f"  - Baseline A: {res_a['run_id']}")
        print(f"  - Condition B (Standard): {res_b.run_id}")
        print(f"  - Condition C (Critique-Revision): {res_c.run_id}")

    elif args.command == "inspect-run":
        run_path = RUNS_DIR / args.run_id
        if not run_path.exists():
            print(f"[ERRO] Run ID '{args.run_id}' não encontrado em runs/")
            sys.exit(1)

        final_md = run_path / "final.md"
        trace_json = run_path / "trace.json"

        if final_md.exists():
            print(final_md.read_text(encoding="utf-8"))
        if trace_json.exists():
            trace = json.loads(trace_json.read_text(encoding="utf-8"))
            print("\n--- Telemetria do Run ---")
            print(f"Duração Total: {trace.get('total_duration_seconds', 0):.2f}s")
            print(f"Estágios Executados: {trace.get('total_stages_executed', 0)}")

    elif args.command == "providers" and args.prov_command == "doctor":
        health = check_providers_health()
        print("=" * 80)
        print("          IDEA EVOLUTION ENGINE — PROVIDERS DOCTOR & CATALOG HEALTH")
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
        print("NOTAS DE GOVERNANÇA E PRIVACIDADE:")
        for pid, info in health.items():
            if info["privacy_class"] == "PROVIDER_MAY_USE_FOR_PRODUCT_IMPROVEMENT":
                print(f"  * [{info['name']}]: Termos do Free Tier permitem uso de dados pelo provedor para melhoria de produto.")
            if info["catalog_status"] == "SHUT_DOWN":
                print(f"  * [ALERTA - {info['name']}]: O modelo '{info['default_model']}' está encerrado! Recomendado: '{info['replacement']}'.")
            if not info["free_eligible"]:
                print(f"  * [{info['name']}]: Provedor classificado como {info['cost_class']}. Bloqueado sob política padrão FREE_ONLY.")
        print("-" * 80)
        print("Nenhum valor secreto é exibido ou gravado. Zero chamadas de inferência realizadas.")
        print("=" * 80)

    elif args.command == "routes" and args.routes_command == "show":
        if args.model_config:
            config = ModelRoutingConfig.from_file(args.model_config)
        else:
            config = ModelRoutingConfig.default_single_model()

        top_map = {
            "standard": "STANDARD_6_STAGE",
            "critique_revision": "ITERATIVE_CRITIQUE_REVISION",
        }
        topology = top_map[args.topology]
        runner = SimpleLoopRunner(config=config, topology=topology)

        print("=" * 65)
        print("          IDEA EVOLUTION ENGINE — ROUTES INSPECTOR")
        print("=" * 65)
        print(f"  Topologia:            {topology}")
        print(f"  Routing Config Hash:  {config.compute_hash()[:16]}...")
        print("-" * 65)
        for stg in runner.get_required_stages():
            alias, m_def = config.resolve_stage(stg)
            print(f"  {stg:<22} -> [{alias:<12}] {m_def.provider}/{m_def.model}")
        print("=" * 65)


if __name__ == "__main__":
    main()
