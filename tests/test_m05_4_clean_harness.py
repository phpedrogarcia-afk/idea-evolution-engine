"""
tests/test_m05_4_clean_harness.py
Offline verification of clean M05.4 execution harness and blind review renderer.

Verifies:
  1. 24-cell manifest execution with FakeModelRunner in temp namespace.
  2. Fail-closed status logic and proper telemetry classification.
  3. Strict blind isolation in execution plane (negative control).
  4. Provider isolation and metadata leak prevention in blind rendering plane.
  5. Zero mutation of historical experiment evidence.
"""

import os
import sys
import json
import shutil
import tempfile
from pathlib import Path
from unittest import TestCase, mock

from src.idea_evolution.providers.fake import FakeModelRunner
from tools.experiments.execute_m05_4_frozen import (
    run_clean_harness,
    validate_provider_guards,
    EXECUTION_PLANE_HAS_NO_BLIND_KNOWLEDGE,
)
from tools.experiments.render_m05_4_blind_review import (
    render_blind_packet,
    BLIND_RENDERING_PLANE_HAS_NO_MODEL_EXECUTION,
)


class TestM054CleanHarness(TestCase):
    """Test suite for clean execution harness and separate renderer."""

    def setUp(self):
        self.repo_root = Path(__file__).resolve().parent.parent
        self.hist_raw_path = self.repo_root / "experiments" / "EXP-M05.4-PROSPECTIVE" / "raw"
        self.hist_before = {str(f): f.read_bytes() for f in self.hist_raw_path.rglob("*") if f.is_file()}

    def tearDown(self):
        # Verify historical experiment was never mutated
        hist_after = {str(f): f.read_bytes() for f in self.hist_raw_path.rglob("*") if f.is_file()}
        self.assertEqual(self.hist_before, hist_after, "Historical experiment was mutated during test!")

    def test_clean_harness_offline_24_cells(self):
        """Execute 24 cells via manifest using FakeModelRunner in temp directory."""
        self.assertTrue(EXECUTION_PLANE_HAS_NO_BLIND_KNOWLEDGE, "Execution plane must declare blind isolation")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            exp_dir = temp_path / "experiments" / "EXP-M05.4-PROSPECTIVE-RERUN-20260829"
            exp_dir.mkdir(parents=True)

            # Copy holdout and manifest
            real_holdout = self.repo_root / "experiments" / "EXP-M05.4-PROSPECTIVE" / "HOLDOUT-IDEAS.json"
            real_manifest = self.repo_root / "experiments" / "EXP-M05.4-PROSPECTIVE-RERUN-20260829" / "RERUN-EXECUTION-MANIFEST.json"
            shutil.copy2(real_holdout, exp_dir / "HOLDOUT-IDEAS.json")
            shutil.copy2(real_manifest, exp_dir / "RERUN-EXECUTION-MANIFEST.json")

            fake_runner = FakeModelRunner(provider="groq", default_model="openai/gpt-oss-120b")

            result = run_clean_harness(
                runner=fake_runner,
                exp_dir=exp_dir,
                attempt_id="attempt-002-test",
                holdout_file=exp_dir / "HOLDOUT-IDEAS.json",
                manifest_file=exp_dir / "RERUN-EXECUTION-MANIFEST.json",
                verbose=False,
            )

            self.assertEqual(result["cells_attempted"], 24)
            self.assertEqual(result["cells_success"], 24)
            self.assertEqual(result["cells_failed"], 0)
            self.assertEqual(result["calls_by_condition"]["CONDITION_A"], 8)
            self.assertGreaterEqual(result["calls_by_condition"]["CONDITION_B"], 48)  # 8 ideas x 6 stages
            self.assertLessEqual(result["calls_by_condition"]["CONDITION_C"], 16)     # <= 2 per idea

            # Check attempt-002 directory artifacts
            attempt_dir = exp_dir / "attempt-002-test"
            self.assertTrue((attempt_dir / "REAL-EXECUTION-START-RECEIPT.json").exists())
            self.assertTrue((attempt_dir / "REAL-EXECUTION-MANIFEST.json").exists())
            self.assertTrue((attempt_dir / "REAL-EXECUTION-EVIDENCE-MANIFEST.json").exists())
            self.assertTrue((attempt_dir / "REAL-EXECUTION-SUMMARY.md").exists())

            # Check telemetry contract
            real_man = json.loads((attempt_dir / "REAL-EXECUTION-MANIFEST.json").read_text())
            self.assertEqual(real_man["transport_retries"], "UNKNOWN_NOT_INSTRUMENTED")
            self.assertEqual(real_man["structured_output_repairs"], "UNKNOWN_NOT_INSTRUMENTED")

            # Check raw files exist
            raw_dir = attempt_dir / "raw"
            self.assertEqual(len(list(raw_dir.glob("*.json"))), 24)

    def test_execution_blind_isolation_negative_control(self):
        """Negative control: prove execution succeeds when reveal path is blocked/broken."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            exp_dir = temp_path / "experiments" / "EXP-M05.4-PROSPECTIVE-RERUN-20260829"
            exp_dir.mkdir(parents=True)

            real_holdout = self.repo_root / "experiments" / "EXP-M05.4-PROSPECTIVE" / "HOLDOUT-IDEAS.json"
            real_manifest = self.repo_root / "experiments" / "EXP-M05.4-PROSPECTIVE-RERUN-20260829" / "RERUN-EXECUTION-MANIFEST.json"
            shutil.copy2(real_holdout, exp_dir / "HOLDOUT-IDEAS.json")
            shutil.copy2(real_manifest, exp_dir / "RERUN-EXECUTION-MANIFEST.json")

            # Intentionally create an invalid reveal file that would crash if read
            fake_reveal_path = exp_dir / "BLIND-REVEAL.json"
            fake_reveal_path.write_text("INVALID_JSON_CORRUPTED_SECRET_SHOULD_NEVER_BE_READ")

            fake_runner = FakeModelRunner(provider="groq", default_model="openai/gpt-oss-120b")

            # Must succeed cleanly because execution plane never reads reveal
            result = run_clean_harness(
                runner=fake_runner,
                exp_dir=exp_dir,
                attempt_id="attempt-002-isolation-test",
                holdout_file=exp_dir / "HOLDOUT-IDEAS.json",
                manifest_file=exp_dir / "RERUN-EXECUTION-MANIFEST.json",
                verbose=False,
            )
            self.assertEqual(result["cells_attempted"], 24)

    def test_blind_renderer_provider_isolation(self):
        """Test that separate blind renderer creates packet with zero model execution and zero leaks."""
        self.assertTrue(BLIND_RENDERING_PLANE_HAS_NO_MODEL_EXECUTION, "Renderer must declare no model execution")

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            attempt_dir = temp_path / "attempt-002-test"
            raw_dir = attempt_dir / "raw"
            raw_dir.mkdir(parents=True)

            # Create synthetic raw outputs for 8 ideas
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
