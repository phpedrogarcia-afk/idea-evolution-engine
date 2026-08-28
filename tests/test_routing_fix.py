"""
Test to verify that the routing fix for M05.4 Condition B works correctly.
This test mechanically establishes that Condition B's Simple Loop stages 
resolve the intended model through actual routing logic.
"""
import os
import tempfile
import shutil
from unittest import TestCase
from unittest.mock import Mock, patch
from pathlib import Path

from src.idea_evolution.experiments.m05_4_runner import M054ExperimentExecutor
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.config.routing import ModelRoutingConfig
from src.idea_evolution.providers.router import RunnerRouter
from src.idea_evolution.orchestration.simple_loop import SimpleLoopRunner


class TestConditionBRouting(TestCase):
    def test_condition_b_routes_all_stages_to_correct_model(self):
        """Test that Condition B routes all Simple Loop stages to the experiment's model."""
        # Arrange: Create a temporary directory for the experiment
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            # Set up the experiment directory structure
            exp_dir = temp_dir_path / "experiments" / "EXP-M05.4-PROSPECTIVE"
            exp_dir.mkdir(parents=True)
            raw_dir = exp_dir / "raw"
            raw_dir.mkdir()

            # Copy the necessary files from the real experiment directory to the temporary experiment directory
            real_exp_dir = Path("experiments") / "EXP-M05.4-PROSPECTIVE"
            for file_name in ["HOLDOUT-IDEAS.json", "BLIND-REVEAL.json", "M05.4-HUMAN-REVIEW-TEMPLATE.md"]:
                src_file = real_exp_dir / file_name
                dst_file = exp_dir / file_name
                shutil.copy2(src_file, dst_file)

            # Patch the EXP_DIR and RAW_DIR in the m05_4_runner module to point to our temporary directories
            with patch('src.idea_evolution.experiments.m05_4_runner.EXP_DIR', exp_dir), \
                     patch('src.idea_evolution.experiments.m05_4_runner.RAW_DIR', raw_dir):
                # Set environment variable for the executor (it expects GROQ_API_KEY)
                os.environ["GROQ_API_KEY"] = "fake-key"
                executor = M054ExperimentExecutor()
                # Now replace the runner with a fake one
                fake_runner = FakeModelRunner(provider="groq", default_model="openai/gpt-oss-120b")
                executor.runner = fake_runner

                # We'll capture the router that gets passed to SimpleLoopRunner
                original_simple_loop_runner = SimpleLoopRunner
                captured_router = None

                def mock_simple_loop_runner(*args, **kwargs):
                    nonlocal captured_router
                    # The SimpleLoopRunner constructor can take either (runner, ...) or (router, ...)
                    if 'router' in kwargs:
                        captured_router = kwargs['router']
                    elif len(args) > 0 and hasattr(args[0], 'config'):
                        # If the first argument is a router (which has a config attribute)
                        captured_router = args[0]
                    # Call the original constructor
                    return original_simple_loop_runner(*args, **kwargs)

                # Patch the SimpleLoopRunner in the module where it is used (m05_4_runner)
                import src.idea_evolution.experiments.m05_4_runner as m05_4_runner_module
                m05_4_runner_module.SimpleLoopRunner = mock_simple_loop_runner

                try:
                    # Act: Run condition B for a dummy idea
                    executor.run_condition_b("idea-01", "This is a test idea.")
                finally:
                    # Restore the original SimpleLoopRunner
                    m05_4_runner_module.SimpleLoopRunner = original_simple_loop_runner
                    # Clean up the environment variable
                    if "GROQ_API_KEY" in os.environ:
                        del os.environ["GROQ_API_KEY"]

                # Assert: Check that the captured router is configured correctly
                self.assertIsNotNone(captured_router, "SimpleLoopRunner was not instantiated (or router not captured)")
                # The router should have a config with one model named "default" that matches the fake_runner's model
                self.assertTrue(hasattr(captured_router, 'config'), "Router does not have a config attribute")
                config = captured_router.config
                self.assertIn("default", config.models, "Config does not have a 'default' model")
                model_def = config.models["default"]
                self.assertEqual(model_def.provider, fake_runner.provider, f"Expected provider {fake_runner.provider}, got {model_def.provider}")
                self.assertEqual(model_def.model, fake_runner.default_model, f"Expected model {fake_runner.default_model}, got {model_def.model}")
                
                # Also check that the router's custom_runners has the "default" key pointing to our fake_runner
                self.assertIn("default", captured_router.custom_runners, "Router's custom_runners does not have 'default' key")
                self.assertIs(captured_router.custom_runners["default"], fake_runner, "Router's custom_runners['default'] is not the fake_runner")
                
                # Now verify that the router actually resolves each stage to the correct model
                # Get the stages that Standard 6-stage topology requires
                expected_stages = ["UNDERSTAND", "ATTACK", "ALTERNATIVES", "SYNTHESIZE", "REALITY_CHECK", "FINAL_REVIEW"]
                
                # Create a mock catalog for validation (doesn't need to be real for this test)
                from src.idea_evolution.config.catalog import ModelCatalog
                catalog = ModelCatalog()
                
                for stage in expected_stages:
                    # This should not raise an exception
                    alias, resolved_model_def = captured_router.config.resolve_stage(stage, catalog=catalog)
                    self.assertEqual(alias, "default", f"Stage {stage} resolved to alias '{alias}', expected 'default'")
                    self.assertEqual(resolved_model_def.provider, fake_runner.provider, f"Stage {stage} provider mismatch")
                    self.assertEqual(resolved_model_def.model, fake_runner.default_model, f"Stage {stage} model mismatch: expected {fake_runner.default_model}, got {resolved_model_def.model}")
                
                # Additionally, prove that "default-model" cannot reach NativeModelRunner during M05.4 execution
                # by verifying that the router's config does not contain "default-model" as a model
                model_names = [m.model for m in config.models.values()]
                self.assertNotIn("default-model", model_names, "Router config should not contain 'default-model' as a model")
                
                # Also verify that the default_model_alias points to "default"
                self.assertEqual(config.default_model_alias, "default", f"Expected default_model_alias='default', got '{config.default_model_alias}'")