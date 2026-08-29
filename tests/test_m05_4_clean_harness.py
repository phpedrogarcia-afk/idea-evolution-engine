"""
tests/test_m05_4_clean_harness.py
Offline verification of clean M05.4 execution harness with self-enforcing freeze gate,
crash-safe execution journal, and blind review renderer.

Verifies:
  CASE 1: Dirty worktree blocks execution before any model call.
  CASE 2: Critical file hash mismatch blocks execution.
  CASE 3: Manifest wrong provider blocks execution.
  CASE 4: Manifest wrong model blocks execution.
  CASE 5: Manifest duplicate cell blocks execution.
  CASE 6: Attempt already started blocks execution (single-use namespace).
  CASE 7: Valid matching frozen state executes 24 cells successfully with complete journal.
  CASE 8: Lean first-pass failure produces explicit cell failure without crash.
  CASE 9: Unexpected infrastructure exception records CELL_EXCEPTION and stops run.
  Negative control: Corrupted blind reveal path does NOT stop execution (blind isolation).
  Renderer isolation: Separate renderer creates packet with zero model execution and zero leaks.
  Immutability invariant: Historical experiment, Attempt-001, and Attempt-002 are never mutated.
"""

import os
import sys
import json
import shutil
import tempfile
from pathlib import Path
from unittest import TestCase, mock

from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.providers.base import ModelRunner, ModelResponse
from tools.experiments.execute_m05_4_frozen import (
    run_clean_harness,
    validate_frozen_execution_state,
    validate_frozen_manifest_cells,
    validate_attempt_single_use,
    calculate_sha256_file,
    EXECUTION_PLANE_HAS_NO_BLIND_KNOWLEDGE,
)
from tools.experiments.render_m05_4_blind_review import (
    render_blind_packet,
    BLIND_RENDERING_PLANE_HAS_NO_MODEL_EXECUTION,
)


class NullFirstPassModelRunner(ModelRunner):
    """Model runner that returns parsed=None on generate calls."""
    def __init__(self, provider: str = "groq", default_model: str = "openai/gpt-oss-120b"):
        self.provider = provider
        self.default_model = default_model
        self.call_count = 0

    def generate(self, prompt_text: str, output_schema, stage_name: str, model_name=None, max_repairs=1) -> ModelResponse:
        self.call_count += 1
        return ModelResponse(
            parsed=None,
            raw_text="{\"invalid\": \"json\"}",
            provider=self.provider,
            model=self.default_model,
            error="SCHEMA_VALIDATION_FAILED: simulated failure",
        )


class ExplodingModelRunner(ModelRunner):
    """Model runner that raises an unexpected exception after N calls."""
    def __init__(self, explode_at_call: int = 1, provider: str = "groq", default_model: str = "openai/gpt-oss-120b"):
        self.provider = provider
        self.default_model = default_model
        self.explode_at_call = explode_at_call
        self.call_count = 0

    def generate(self, prompt_text: str, output_schema, stage_name: str, model_name=None, max_repairs=1) -> ModelResponse:
        self.call_count += 1
        if self.call_count >= self.explode_at_call:
            raise ConnectionResetError("Simulated infrastructure connection reset")
        return ModelResponse(
            parsed=None,
            raw_text="ok",
            provider=self.provider,
            model=self.default_model,
        )


class TestM054CleanHarness(TestCase):
    """Test suite for clean execution harness, self-enforcing freeze gate, journal, and renderer."""

    def setUp(self):
        self.repo_root = Path(__file__).resolve().parent.parent
        self.hist_raw_path = self.repo_root / "experiments" / "EXP-M05.4-PROSPECTIVE" / "raw"
        self.hist_before = {str(f): f.read_bytes() for f in self.hist_raw_path.rglob("*") if f.is_file()}

        self.att1_dir = self.repo_root / "experiments" / "EXP-M05.4-PROSPECTIVE-RERUN-20260829" / "attempt-001-invalid"
        self.att1_before = {str(f): f.read_bytes() for f in self.att1_dir.rglob("*") if f.is_file()}

        self.att2_dir = self.repo_root / "experiments" / "EXP-M05.4-PROSPECTIVE-RERUN-20260829" / "REAL-EXECUTION-ATTEMPT-002"
        self.att2_before = {str(f): f.read_bytes() for f in self.att2_dir.rglob("*") if f.is_file()}

    def tearDown(self):
        # Invariant: historical experiment was never mutated
        hist_after = {str(f): f.read_bytes() for f in self.hist_raw_path.rglob("*") if f.is_file()}
        self.assertEqual(self.hist_before, hist_after, "Historical experiment was mutated during test!")

        # Invariant: Attempt-001 was never mutated
        att1_after = {str(f): f.read_bytes() for f in self.att1_dir.rglob("*") if f.is_file()}
        self.assertEqual(self.att1_before, att1_after, "Attempt-001 was mutated during test!")

        # Invariant: Attempt-002 was never mutated
        att2_after = {str(f): f.read_bytes() for f in self.att2_dir.rglob("*") if f.is_file()}
        self.assertEqual(self.att2_before, att2_after, "Attempt-002 was mutated during test!")

    def _setup_test_universe(self, temp_path: Path) -> Path:
        """Sets up a complete isolated test universe matching frozen state."""
        exp_dir = temp_path / "experiments" / "EXP-M05.4-PROSPECTIVE-RERUN-20260829"
        exp_dir.mkdir(parents=True)

        real_exp_dir = self.repo_root / "experiments" / "EXP-M05.4-PROSPECTIVE-RERUN-20260829"
        real_holdout_dir = self.repo_root / "experiments" / "EXP-M05.4-PROSPECTIVE"
        (temp_path / "experiments" / "EXP-M05.4-PROSPECTIVE").mkdir(parents=True, exist_ok=True)

        for fname in ["HOLDOUT-IDEAS.json", "EVALUATION-RUBRIC.md", "ANALYSIS-PLAN.md", "PREREGISTRATION.md"]:
            shutil.copy2(real_holdout_dir / fname, temp_path / "experiments" / "EXP-M05.4-PROSPECTIVE" / fname)

        for fname in [
            "RERUN-PROTOCOL-AMENDMENT-001.md",
            "PRE-EXECUTION-BLINDING-CORRECTION-001.md",
            "PRE-EXECUTION-BLINDING-CORRECTION-002.md",
            "RERUN-EXECUTION-MANIFEST.json",
            "RERUN-RETRY-SEMANTICS-FROZEN.md",
            "BLIND-REVEAL.sha256",
        ]:
            shutil.copy2(real_exp_dir / fname, exp_dir / fname)

        # Copy code files
        (temp_path / "tools" / "experiments").mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.repo_root / "tools" / "experiments" / "execute_m05_4_frozen.py", temp_path / "tools" / "experiments" / "execute_m05_4_frozen.py")
        shutil.copy2(self.repo_root / "tools" / "experiments" / "render_m05_4_blind_review.py", temp_path / "tools" / "experiments" / "render_m05_4_blind_review.py")

        (temp_path / "src" / "idea_evolution").mkdir(parents=True, exist_ok=True)
        for sub in ["experiments", "orchestration", "config", "providers", "domain", "tracing", "stages"]:
            src_sub = self.repo_root / "src" / "idea_evolution" / sub
            if src_sub.is_dir():
                shutil.copytree(src_sub, temp_path / "src" / "idea_evolution" / sub)

        # Create freeze manifest in test universe matching these files
        from tools.experiments.execute_m05_4_frozen import calculate_sha256_file
        file_keys = {
            "execute_m05_4_frozen.py": temp_path / "tools" / "experiments" / "execute_m05_4_frozen.py",
            "render_m05_4_blind_review.py": temp_path / "tools" / "experiments" / "render_m05_4_blind_review.py",
            "m05_4_runner.py": temp_path / "src" / "idea_evolution" / "experiments" / "m05_4_runner.py",
            "baseline.py": temp_path / "src" / "idea_evolution" / "orchestration" / "baseline.py",
            "simple_loop.py": temp_path / "src" / "idea_evolution" / "orchestration" / "simple_loop.py",
            "lean_loop.py": temp_path / "src" / "idea_evolution" / "orchestration" / "lean_loop.py",
            "early_epistemic_gate.py": temp_path / "src" / "idea_evolution" / "domain" / "early_epistemic_gate.py",
            "routing.py": temp_path / "src" / "idea_evolution" / "config" / "routing.py",
            "catalog.py": temp_path / "src" / "idea_evolution" / "config" / "catalog.py",
            "native.py": temp_path / "src" / "idea_evolution" / "providers" / "native.py",
            "router.py": temp_path / "src" / "idea_evolution" / "providers" / "router.py",
            "blind_renderer.py": temp_path / "src" / "idea_evolution" / "experiments" / "blind_renderer.py",
            "HOLDOUT-IDEAS.json": temp_path / "experiments" / "EXP-M05.4-PROSPECTIVE" / "HOLDOUT-IDEAS.json",
            "EVALUATION-RUBRIC.md": temp_path / "experiments" / "EXP-M05.4-PROSPECTIVE" / "EVALUATION-RUBRIC.md",
            "ANALYSIS-PLAN.md": temp_path / "experiments" / "EXP-M05.4-PROSPECTIVE" / "ANALYSIS-PLAN.md",
            "PREREGISTRATION.md": temp_path / "experiments" / "EXP-M05.4-PROSPECTIVE" / "PREREGISTRATION.md",
            "RERUN-PROTOCOL-AMENDMENT-001.md": exp_dir / "RERUN-PROTOCOL-AMENDMENT-001.md",
            "PRE-EXECUTION-BLINDING-CORRECTION-001.md": exp_dir / "PRE-EXECUTION-BLINDING-CORRECTION-001.md",
            "PRE-EXECUTION-BLINDING-CORRECTION-002.md": exp_dir / "PRE-EXECUTION-BLINDING-CORRECTION-002.md",
            "RERUN-EXECUTION-MANIFEST.json": exp_dir / "RERUN-EXECUTION-MANIFEST.json",
            "RERUN-RETRY-SEMANTICS-FROZEN.md": exp_dir / "RERUN-RETRY-SEMANTICS-FROZEN.md",
            "BLIND-REVEAL.sha256": exp_dir / "BLIND-REVEAL.sha256",
        }
        hashes = {k: calculate_sha256_file(v) for k, v in file_keys.items()}
        freeze_data = {
            "experiment_id": "EXP-M05.4-PROSPECTIVE-RERUN-20260829",
            "execution_critical_hashes": hashes,
        }
        (exp_dir / "RERUN-FREEZE-MANIFEST.json").write_text(json.dumps(freeze_data, indent=2))

        return exp_dir

    def test_case_1_dirty_worktree_blocked(self):
        """CASE 1: Dirty worktree blocks execution before any provider call."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            exp_dir = self._setup_test_universe(temp_path)
            fake_runner = FakeModelRunner(provider="groq", default_model="openai/gpt-oss-120b")

            with mock.patch("tools.experiments.execute_m05_4_frozen.check_git_worktree_clean", return_value=False):
                with self.assertRaises(RuntimeError) as ctx:
                    run_clean_harness(
                        runner=fake_runner,
                        repo_root=temp_path,
                        exp_dir=exp_dir,
                        attempt_id="attempt-003-test",
                        skip_git_check=False,
                        verbose=False,
                    )
                self.assertIn("DIRTY_WORKTREE_EXECUTION_FORBIDDEN", str(ctx.exception))
                self.assertEqual(sum(fake_runner.call_counts.values()), 0, "Fake provider calls must be 0")

    def test_case_2_hash_mismatch_blocked(self):
        """CASE 2: Critical file hash mismatch blocks execution before any call."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            exp_dir = self._setup_test_universe(temp_path)
            fake_runner = FakeModelRunner(provider="groq", default_model="openai/gpt-oss-120b")

            # Mutate one critical file
            holdout_file = temp_path / "experiments" / "EXP-M05.4-PROSPECTIVE" / "HOLDOUT-IDEAS.json"
            holdout_file.write_text('{"mutated": true}')

            with self.assertRaises(RuntimeError) as ctx:
                run_clean_harness(
                    runner=fake_runner,
                    repo_root=temp_path,
                    exp_dir=exp_dir,
                    attempt_id="attempt-003-test",
                    skip_git_check=True,
                    verbose=False,
                )
            self.assertIn("FROZEN_STATE_MUTATION", str(ctx.exception))
            self.assertEqual(sum(fake_runner.call_counts.values()), 0, "Fake provider calls must be 0")

    def test_case_3_wrong_provider_cell_blocked(self):
        """CASE 3: Manifest cell with wrong provider is blocked before execution."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            exp_dir = self._setup_test_universe(temp_path)
            fake_runner = FakeModelRunner(provider="groq", default_model="openai/gpt-oss-120b")

            manifest_file = exp_dir / "RERUN-EXECUTION-MANIFEST.json"
            man_data = json.loads(manifest_file.read_text())
            man_data["cells"][0]["provider"] = "openai"
            manifest_file.write_text(json.dumps(man_data))

            freeze_file = exp_dir / "RERUN-FREEZE-MANIFEST.json"
            freeze_data = json.loads(freeze_file.read_text())
            freeze_data["execution_critical_hashes"]["RERUN-EXECUTION-MANIFEST.json"] = calculate_sha256_file(manifest_file)
            freeze_file.write_text(json.dumps(freeze_data))

            with self.assertRaises(RuntimeError) as ctx:
                run_clean_harness(
                    runner=fake_runner,
                    repo_root=temp_path,
                    exp_dir=exp_dir,
                    attempt_id="attempt-003-test",
                    skip_git_check=True,
                    verbose=False,
                )
            self.assertIn("FROZEN_PROVIDER_VIOLATION", str(ctx.exception))
            self.assertEqual(sum(fake_runner.call_counts.values()), 0, "Fake provider calls must be 0")

    def test_case_4_wrong_model_cell_blocked(self):
        """CASE 4: Manifest cell with wrong model is blocked before execution."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            exp_dir = self._setup_test_universe(temp_path)
            fake_runner = FakeModelRunner(provider="groq", default_model="openai/gpt-oss-120b")

            manifest_file = exp_dir / "RERUN-EXECUTION-MANIFEST.json"
            man_data = json.loads(manifest_file.read_text())
            man_data["cells"][0]["model"] = "gpt-4o"
            manifest_file.write_text(json.dumps(man_data))

            freeze_file = exp_dir / "RERUN-FREEZE-MANIFEST.json"
            freeze_data = json.loads(freeze_file.read_text())
            freeze_data["execution_critical_hashes"]["RERUN-EXECUTION-MANIFEST.json"] = calculate_sha256_file(manifest_file)
            freeze_file.write_text(json.dumps(freeze_data))

            with self.assertRaises(RuntimeError) as ctx:
                run_clean_harness(
                    runner=fake_runner,
                    repo_root=temp_path,
                    exp_dir=exp_dir,
                    attempt_id="attempt-003-test",
                    skip_git_check=True,
                    verbose=False,
                )
            self.assertIn("FROZEN_MODEL_VIOLATION", str(ctx.exception))
            self.assertEqual(sum(fake_runner.call_counts.values()), 0, "Fake provider calls must be 0")

    def test_case_5_duplicate_cell_blocked(self):
        """CASE 5: Duplicate cell in manifest is blocked before execution."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            exp_dir = self._setup_test_universe(temp_path)
            fake_runner = FakeModelRunner(provider="groq", default_model="openai/gpt-oss-120b")

            manifest_file = exp_dir / "RERUN-EXECUTION-MANIFEST.json"
            man_data = json.loads(manifest_file.read_text())
            man_data["cells"][1]["cell_id"] = man_data["cells"][0]["cell_id"]
            manifest_file.write_text(json.dumps(man_data))

            freeze_file = exp_dir / "RERUN-FREEZE-MANIFEST.json"
            freeze_data = json.loads(freeze_file.read_text())
            freeze_data["execution_critical_hashes"]["RERUN-EXECUTION-MANIFEST.json"] = calculate_sha256_file(manifest_file)
            freeze_file.write_text(json.dumps(freeze_data))

            with self.assertRaises(RuntimeError) as ctx:
                run_clean_harness(
                    runner=fake_runner,
                    repo_root=temp_path,
                    exp_dir=exp_dir,
                    attempt_id="attempt-003-test",
                    skip_git_check=True,
                    verbose=False,
                )
            self.assertIn("FROZEN_CELL_DUPLICATE", str(ctx.exception))
            self.assertEqual(sum(fake_runner.call_counts.values()), 0, "Fake provider calls must be 0")

    def test_case_6_attempt_already_started_blocked(self):
        """CASE 6: Attempt directory already containing evidence is blocked from overwrite."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            exp_dir = self._setup_test_universe(temp_path)
            fake_runner = FakeModelRunner(provider="groq", default_model="openai/gpt-oss-120b")

            attempt_dir = exp_dir / "REAL-EXECUTION-ATTEMPT-003"
            attempt_dir.mkdir(parents=True)
            (attempt_dir / "REAL-EXECUTION-START-RECEIPT.json").write_text('{"existing": true}')

            with self.assertRaises(RuntimeError) as ctx:
                run_clean_harness(
                    runner=fake_runner,
                    repo_root=temp_path,
                    exp_dir=exp_dir,
                    attempt_id="REAL-EXECUTION-ATTEMPT-003",
                    skip_git_check=True,
                    allow_overwrite=False,
                    verbose=False,
                )
            self.assertIn("ATTEMPT_ALREADY_STARTED", str(ctx.exception))
            self.assertEqual(sum(fake_runner.call_counts.values()), 0, "Fake provider calls must be 0")

    def test_case_7_valid_frozen_execution_with_journal(self):
        """CASE 7: Valid matching frozen state executes 24 cells and writes complete journal."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            exp_dir = self._setup_test_universe(temp_path)
            fake_runner = FakeModelRunner(provider="groq", default_model="openai/gpt-oss-120b")

            result = run_clean_harness(
                runner=fake_runner,
                repo_root=temp_path,
                exp_dir=exp_dir,
                attempt_id="REAL-EXECUTION-ATTEMPT-003-VALID",
                skip_git_check=True,
                verbose=False,
            )

            self.assertEqual(result["cells_attempted"], 24)
            self.assertEqual(result["cells_success"], 24)
            self.assertEqual(result["cells_failed"], 0)

            attempt_dir = exp_dir / "REAL-EXECUTION-ATTEMPT-003-VALID"
            receipt = json.loads((attempt_dir / "REAL-EXECUTION-START-RECEIPT.json").read_text())
            self.assertEqual(receipt["frozen_state_validation"], "PASS")

            # Check journal records: 24 STARTED and 24 COMPLETED
            journal_file = attempt_dir / "REAL-EXECUTION-JOURNAL.jsonl"
            self.assertTrue(journal_file.exists())
            lines = [json.loads(line) for line in journal_file.read_text(encoding="utf-8").strip().split("\n")]
            started = [l for l in lines if l["event"] == "CELL_STARTED"]
            completed = [l for l in lines if l["event"] == "CELL_COMPLETED"]
            exceptions = [l for l in lines if l["event"] == "CELL_EXCEPTION"]

            self.assertEqual(len(started), 24)
            self.assertEqual(len(completed), 24)
            self.assertEqual(len(exceptions), 0)

    def test_case_8_lean_null_first_pass_in_clean_harness(self):
        """CASE 8: Lean first pass generation failure produces explicit FAILED cell without Python crash."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            exp_dir = self._setup_test_universe(temp_path)
            null_runner = NullFirstPassModelRunner(provider="groq", default_model="openai/gpt-oss-120b")

            result = run_clean_harness(
                runner=null_runner,
                repo_root=temp_path,
                exp_dir=exp_dir,
                attempt_id="REAL-EXECUTION-ATTEMPT-003-NULL-TEST",
                skip_git_check=True,
                verbose=False,
            )

            self.assertEqual(result["cells_attempted"], 24)
            self.assertEqual(result["cells_failed"], 24)  # All cells fail fail-closed
            self.assertEqual(result["cells_success"], 0)

            # Check Condition C output explicitly has FIRST_PASS_FAILED terminal status
            attempt_dir = exp_dir / "REAL-EXECUTION-ATTEMPT-003-NULL-TEST"
            cond_c_raw = json.loads((attempt_dir / "raw" / "IDEA-01_condition_c.json").read_text(encoding="utf-8"))
            self.assertEqual(cond_c_raw["status"], "FAILED")
            self.assertEqual(cond_c_raw["terminal_status"], "FIRST_PASS_FAILED")

    def test_case_9_unexpected_exception_stops_run_and_journals(self):
        """CASE 9: Unexpected infrastructure exception records CELL_EXCEPTION and stops remaining cells."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            exp_dir = self._setup_test_universe(temp_path)
            exploding_runner = ExplodingModelRunner(explode_at_call=2, provider="groq", default_model="openai/gpt-oss-120b")

            attempt_id = "REAL-EXECUTION-ATTEMPT-003-EXPLODE"
            with self.assertRaises(ConnectionResetError):
                run_clean_harness(
                    runner=exploding_runner,
                    repo_root=temp_path,
                    exp_dir=exp_dir,
                    attempt_id=attempt_id,
                    skip_git_check=True,
                    verbose=False,
                )

            attempt_dir = exp_dir / attempt_id
            journal_file = attempt_dir / "REAL-EXECUTION-JOURNAL.jsonl"
            self.assertTrue(journal_file.exists())
            lines = [json.loads(line) for line in journal_file.read_text(encoding="utf-8").strip().split("\n")]

            exceptions = [l for l in lines if l["event"] == "CELL_EXCEPTION"]
            self.assertEqual(len(exceptions), 1)
            self.assertEqual(exceptions[0]["exception_class"], "ConnectionResetError")

            # Partial manifest was written
            partial_manifest = attempt_dir / "PARTIAL-EXECUTION-MANIFEST.json"
            self.assertTrue(partial_manifest.exists())
            pdata = json.loads(partial_manifest.read_text(encoding="utf-8"))
            self.assertEqual(pdata["status"], "INTERRUPTED")

    def test_execution_blind_isolation_negative_control(self):
        """Negative control: prove execution succeeds when reveal path is blocked/broken."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            exp_dir = self._setup_test_universe(temp_path)
            fake_runner = FakeModelRunner(provider="groq", default_model="openai/gpt-oss-120b")

            (exp_dir / "BLIND-REVEAL.json").write_text("CORRUPTED_SECRET_SHOULD_NEVER_BE_READ")

            result = run_clean_harness(
                runner=fake_runner,
                repo_root=temp_path,
                exp_dir=exp_dir,
                attempt_id="attempt-003-isolation-test",
                skip_git_check=True,
                verbose=False,
            )
            self.assertEqual(result["cells_attempted"], 24)

    def test_blind_renderer_provider_isolation(self):
        """Test that separate blind renderer creates packet with zero model execution and zero leaks."""
        self.assertTrue(BLIND_RENDERING_PLANE_HAS_NO_MODEL_EXECUTION, "Renderer must declare no model execution")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            attempt_dir = temp_path / "attempt-003-test"
            raw_dir = attempt_dir / "raw"
            raw_dir.mkdir(parents=True)

            real_holdout = self.repo_root / "experiments" / "EXP-M05.4-PROSPECTIVE" / "HOLDOUT-IDEAS.json"
            holdout_ideas = json.loads(real_holdout.read_text())

            mappings = {}
            for item in holdout_ideas:
                idea_id = item["idea_id"]
                mappings[idea_id] = {
                    "RESULT_1": "CONDITION_C",
                    "RESULT_2": "CONDITION_A",
                    "RESULT_3": "CONDITION_B",
                }
                for cond in ["condition_a", "condition_b", "condition_c"]:
                    raw_file = raw_dir / f"{idea_id}_{cond}.json"
                    raw_file.write_text(json.dumps({
                        "rendered_semantic_text": f"### Output for {idea_id} {cond}\nRefined content here.",
                        "model_calls": 1,
                        "status": "SUCCESS"
                    }))

            reveal_file = temp_path / "BLIND-REVEAL-TEST.json"
            reveal_file.write_text(json.dumps({
                "experiment_id": "EXP-M05.4-PROSPECTIVE-RERUN-20260829",
                "mappings": mappings
            }))

            render_res = render_blind_packet(
                attempt_dir=attempt_dir,
                reveal_file=reveal_file,
                holdout_file=real_holdout,
                verbose=False
            )

            self.assertTrue(render_res["leak_audit_pass"], f"Leaks found: {render_res['leaks']}")
            self.assertEqual(render_res["leak_count"], 0)
            self.assertTrue(Path(render_res["packet_path"]).exists())


if __name__ == "__main__":
    import unittest
    unittest.main()
