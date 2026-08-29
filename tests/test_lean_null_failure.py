"""
tests/test_lean_null_failure.py
Regression tests for Lean Loop null-failure hardening (Attempt-002 failure mode).

Verifies:
  1. When runner returns parsed=None on First Pass:
     - No AttributeError is raised.
     - EarlyEpistemicGate is NOT called with None.
     - LeanLoopRunner returns explicit fail-closed LeanRunResult (terminal_status='FIRST_PASS_FAILED').
     - total_model_calls == 1.
  2. Positive control: valid first_pass generates normal Lean run without regression.
  3. Precondition guard: EarlyEpistemicGate.evaluate(..., first_pass=None) raises ValueError.
"""

from unittest import TestCase, mock
from src.idea_evolution.orchestration.lean_loop import LeanLoopRunner, LeanRunResult
from src.idea_evolution.domain.early_epistemic_gate import EarlyEpistemicGate, LeanFirstPassOutput
from src.idea_evolution.domain.epistemic_contracts import SourceAnchor
from src.idea_evolution.providers.fake import FakeModelRunner
from src.idea_evolution.providers.base import ModelRunner, ModelResponse


class NullFirstPassModelRunner(ModelRunner):
    """Model runner that returns parsed=None on all generate calls."""
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


class TestLeanNullFailureHardening(TestCase):
    """Test suite verifying null-safety and fail-closed behavior in LeanLoopRunner."""

    def test_null_first_pass_produces_typed_failure_without_crash(self):
        """When first pass generation fails (parsed=None), LeanLoopRunner must return FIRST_PASS_FAILED."""
        runner = NullFirstPassModelRunner()
        lean_runner = LeanLoopRunner(runner=runner, model_name="openai/gpt-oss-120b")

        with mock.patch.object(EarlyEpistemicGate, "evaluate", wraps=EarlyEpistemicGate.evaluate) as spy_gate:
            result: LeanRunResult = lean_runner.run(original_idea="Test idea that will fail parsing")

            # Must NOT crash with AttributeError
            self.assertIsInstance(result, LeanRunResult)
            self.assertEqual(result.terminal_status, "FIRST_PASS_FAILED")
            self.assertEqual(result.total_model_calls, 1)
            self.assertFalse(result.decision_progress_detected)
            self.assertIsNone(result.first_pass)
            self.assertIsNone(result.gate_result)

            # EarlyEpistemicGate must NOT have been called with None
            spy_gate.assert_not_called()

    def test_gate_precondition_guard_rejects_none(self):
        """EarlyEpistemicGate.evaluate must raise ValueError if first_pass is None."""
        anchor = SourceAnchor.create_human_input_anchor("Test idea")
        with self.assertRaises(ValueError) as ctx:
            EarlyEpistemicGate.evaluate(source_anchor=anchor, first_pass=None)  # type: ignore
        self.assertIn("first_pass cannot be None", str(ctx.exception))

    def test_positive_control_valid_first_pass(self):
        """Positive control: valid first pass continues to work normally."""
        runner = FakeModelRunner(provider="groq", default_model="openai/gpt-oss-120b")
        lean_runner = LeanLoopRunner(runner=runner, model_name="openai/gpt-oss-120b")

        result: LeanRunResult = lean_runner.run(original_idea="Test idea with valid fake runner")
        self.assertIsInstance(result, LeanRunResult)
        self.assertIn(result.terminal_status, ["COMPLETED_DIRECT_ONE_PASS", "COMPLETED", "HUMAN_DECISION_REQUIRED", "STOP_NO_USEFUL_WORK"])
        self.assertIsNotNone(result.first_pass)
        self.assertIsNotNone(result.gate_result)
        self.assertGreaterEqual(result.total_model_calls, 1)


if __name__ == "__main__":
    import unittest
    unittest.main()
