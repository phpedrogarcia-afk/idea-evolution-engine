"""
src/idea_evolution/cli/main.py
Interface de Linha de Comando (CLI) para o Idea Evolution Engine MVP.
Comandos:
  iee evolve --idea "..." [--topology STANDARD | CRITIQUE_REVISION]
  iee compare --fixture-file path/to/fixture.json
  iee inspect-run RUN-YYYYMMDD-NNN
"""

import sys
import os
import argparse
from pathlib import Path
import json

from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner
from src.idea_evolution.orchestration.baseline import BaselineRunner
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.providers.native import NativeModelRunner
from src.idea_evolution.domain.state import RunStatus

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
RUNS_DIR = REPO_ROOT / "runs"


def parse_args():
    parser = argparse.ArgumentParser(
        prog="iee",
        description="Idea Evolution Engine — CLI do Simple Loop MVP",
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
        choices=["fake", "groq", "openai"],
        default="fake",
        help="Provedor de inferência (padrão: fake offline)",
    )
    evolve_p.add_argument("--model", "-m", type=str, default=None, help="Nome do modelo a ser usado")

    # COMPARE
    comp_p = subparsers.add_parser("compare", help="Executar comparação experimental (A vs B vs C) sobre uma fixture")
    comp_p.add_argument("--fixture-file", "-f", type=Path, required=True, help="Caminho para o JSON da fixture")

    # INSPECT-RUN
    insp_p = subparsers.add_parser("inspect-run", help="Inspecionar detalhes de uma execução passada")
    insp_p.add_argument("run_id", type=str, help="ID da execução (ex: RUN-20260826-001)")

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

        if not idea_text:
            print("[ERRO] É necessário fornecer a ideia via --idea ou --idea-file.")
            sys.exit(1)

        # Escolha do runner
        if args.provider == "fake":
            runner = FakeModelRunner()
        else:
            runner = NativeModelRunner(provider=args.provider, default_model=args.model)

        top_map = {
            "standard": "STANDARD_6_STAGE",
            "critique_revision": "ITERATIVE_CRITIQUE_REVISION",
        }
        loop_runner = SimpleLoopRunner(runner=runner, topology=top_map[args.topology])

        print("=" * 65)
        print("          IDEA EVOLUTION ENGINE — SIMPLE LOOP RUNNER")
        print("=" * 65)
        print(f"  Ideia:     {idea_text[:60]}...")
        print(f"  Topologia: {top_map[args.topology]}")
        print(f"  Provider:  {args.provider.upper()}")
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
        loop_b = SimpleLoopRunner(runner, topology="STANDARD_6_STAGE")
        res_b = loop_b.run(idea_text)

        # Condição C: Iterative Critique-Revision
        loop_c = SimpleLoopRunner(runner, topology="ITERATIVE_CRITIQUE_REVISION")
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


if __name__ == "__main__":
    main()
