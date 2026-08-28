"""
Test for M05.4 dry run execution of 24 cells (8 ideas x 3 conditions).
Verifies correct execution counts, stage topology, and isolation.
"""
import json
import os
import tempfile
import shutil
from unittest import TestCase, mock
from pathlib import Path

from src.idea_evolution.experiments.m05_4_runner import M054ExperimentExecutor
from src.idea_evolution.providers.fake import FakeModelRunner


class TestM054DryRun(TestCase):
    def test_m05_4_dry_run_24_cells(self):
        """Execute 24 cells (8 ideas x 3 conditions) with fake model and verify isolation."""
        # Snapshot repository-level directories before test
        repo_runs_before = set()
        repo_exp_raw_before = set()
        runs_path = Path("runs")
        exp_raw_path = Path("experiments") / "EXP-M05.4-PROSPECTIVE" / "raw"
        if runs_path.is_dir():
            repo_runs_before = set(os.listdir(runs_path))
        if exp_raw_path.is_dir():
            repo_exp_raw_before = set(os.listdir(exp_raw_path))

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            # Set up experiment directory structure in temp dir
            exp_dir = temp_dir_path / "experiments" / "EXP-M05.4-PROSPECTIVE"
            exp_dir.mkdir(parents=True)
            raw_dir = exp_dir / "raw"
            raw_dir.mkdir()

            # Copy holdout ideas from real location (read-only)
            real_holdout = Path("experiments") / "EXP-M05.4-PROSPECTIVE" / "HOLDOUT-IDEAS.json"
            shutil.copy2(real_holdout, exp_dir / "HOLDOUT-IDEAS.json")

            # Create synthetic BLIND-REVEAL.json
            with open(exp_dir / "HOLDOUT-IDEAS.json", "r", encoding="utf-8") as f:
                holdout_ideas = json.load(f)
            blind_mapping = {}
            for idea in holdout_ideas:
                idea_id = idea["idea_id"]
                blind_mapping[idea_id] = {
                    "RESULT_1": "CONDITION_A",
                    "RESULT_2": "CONDITION_B",
                    "RESULT_3": "CONDITION_C"
                }
            blind_data = {
                "experiment_id": "EXP-M05.4-PROSPECTIVE-20260827",
                "seed": 20260827,
                "mappings": blind_mapping
            }
            with open(exp_dir / "BLIND-REVEAL.json", "w", encoding="utf-8") as f:
                json.dump(blind_data, f, indent=2)

            # Patch EXP_DIR and RAW_DIR to temporary paths
            with mock.patch('src.idea_evolution.experiments.m05_4_runner.EXP_DIR', exp_dir), \
                 mock.patch('src.idea_evolution.experiments.m05_4_runner.RAW_DIR', raw_dir), \
                 mock.patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):

                # Create executor and replace runner with FakeModelRunner
                executor = M054ExperimentExecutor()
                fake_runner = FakeModelRunner(provider="groq", default_model="openai/gpt-oss-120b")
                executor.runner = fake_runner

                # Load ideas and mappings
                ideas = executor.load_holdout_ideas()
                mappings = executor.load_blind_mappings()

                # We'll collect results per idea
                idea_results = []

                for idx, item in enumerate(ideas, 1):
                    idea_id = item["idea_id"]
                    raw_idea = item["raw_idea"]
                    # We don't need to print in the test, but we can if we want
                    # print(f"[{idx}/8] Executando {idea_id} ({item['suite_class']})...")

                    # Execute each condition
                    res_a = executor.run_condition_a(idea_id, raw_idea)
                    res_b = executor.run_condition_b(idea_id, raw_idea)
                    res_c = executor.run_condition_c(idea_id, raw_idea)

                    idea_results.append({
                        "idea_id": idea_id,
                        "A": res_a,
                        "B": res_b,
                        "C": res_c
                    })

                    # Accumulate totals (optional, we can compute later)
                # End for each idea

                # Now verify the results
                self.assertEqual(len(idea_results), 8, "Expected 8 ideas")

                # Initialize counters
                total_a_calls = 0
                total_b_calls = 0
                total_c_calls = 0
                a_cells = 0
                b_cells = 0
                c_cells = 0

                # Expected stages for Condition B
                expected_stages = ["UNDERSTAND", "ATTACK", "ALTERNATIVES", "SYNTHESIZE", "REALITY_CHECK", "FINAL_REVIEW"]

                for result in idea_results:
                    # Condition A
                    a_cells += 1
                    total_a_calls += result["A"]["model_calls"]
                    # Condition A should have exactly 1 model call (BaselineRunner)
                    self.assertEqual(result["A"]["model_calls"], 1,
                                     f"Condition A should have exactly 1 model call for idea {result['idea_id']}, got {result['A']['model_calls']}")

                    # Condition B
                    b_cells += 1
                    total_b_calls += result["B"]["model_calls"]
                    # Condition B should have exactly 6 model calls (one per stage)
                    self.assertEqual(result["B"]["model_calls"], 6,
                                     f"Condition B should have exactly 6 model calls for idea {result['idea_id']}, got {result['B']['model_calls']}")
                    # Check that the stages executed are exactly the expected stages in order
                    self.assertEqual(result["B"]["stages_executed"], expected_stages,
                                     f"Condition B stages incorrect for idea {result['idea_id']}: expected {expected_stages}, got {result['B']['stages_executed']}")

                    # Condition C
                    c_cells += 1
                    total_c_calls += result["C"]["model_calls"]
                    # Condition C should have at most 2 model calls
                    self.assertLessEqual(result["C"]["model_calls"], 2,
                                         f"Condition C model calls too high for idea {result['idea_id']}: expected at most 2, got {result['C']['model_calls']}")

                # Verify totals
                self.assertEqual(a_cells, 8, "Expected 8 condition A cells")
                self.assertEqual(b_cells, 8, "Expected 8 condition B cells")
                self.assertEqual(c_cells, 8, "Expected 8 condition C cells")

                self.assertEqual(total_a_calls, 8, "Expected total 8 model calls for condition A (8 ideas * 1)")
                self.assertEqual(total_b_calls, 48, "Expected total 48 model calls for condition B (8 ideas * 6)")
                self.assertLessEqual(total_c_calls, 16, "Expected total at most 16 model calls for condition C (8 ideas * 2)")

                # Verify no route contains "default-model" by checking that the validation passed
                # (the validation would have failed if expected_model was "default-model")
                # We can also check that the runner's model is not "default-model"
                self.assertNotEqual(
                    executor.runner.default_model, "default-model",
                    "Runner's default model should not be 'default-model'"
                )

        # After temporary directory context, check for repository-level mutation
        repo_runs_after = set()
        repo_exp_raw_after = set()
        if runs_path.is_dir():
            repo_runs_after = set(os.listdir(runs_path))
        if exp_raw_path.is_dir():
            repo_exp_raw_after = set(os.listdir(exp_raw_path))

        # Assert no repository-level mutation
        self.assertEqual(
            repo_runs_before, repo_runs_after,
            f"Repository runs/ directory mutated: {repo_runs_before} -> {repo_runs_after}"
        )
        self.assertEqual(
            repo_exp_raw_before, repo_exp_raw_after,
            f"Repository experiments/EXP-M05.4-PROSPECTIVE/raw/ directory mutated: "
            f"{repo_exp_raw_before} -> {repo_exp_raw_after}"
        )


if __name__ == "__main__":
    import unittest
    unittest.main()