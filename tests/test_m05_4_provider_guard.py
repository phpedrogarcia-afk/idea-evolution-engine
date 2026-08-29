"""
tests/test_m05_4_provider_guard.py

Regression test for M05.4 P1: provider-spec bypass.

Accepted finding (do not re-derive):
  Normal construction pins provider="groq", model="openai/gpt-oss-120b".
  If executor.runner is internally replaced/misconfigured with a wrong provider,
  Conditions A and C silently pass that wrong provider to the provider boundary.
  Condition B rejected the wrong provider pre-call only because of an unrelated
  model-name failure, not a deliberate provider guard.

This test proves the fix:
  _validate_model_routing() must detect a wrong runner provider BEFORE any
  FakeModelRunner.generate() is ever invoked.

Cases:
  CASE_A: wrong provider + correct model => rejected pre-execution
  CASE_B: wrong provider + wrong model   => rejected pre-execution
  CASE_C: correct provider + correct model (control) => passes validation

All invalid-provider cases must produce zero FakeModelRunner.generate calls.
The guard must use RuntimeError (not assert) so it survives python -O.
"""
import os
import tempfile
import shutil
from pathlib import Path
from unittest import TestCase, mock

from src.idea_evolution.experiments.m05_4_runner import M054ExperimentExecutor
from src.idea_evolution.providers.fake import FakeModelRunner


def _make_executor_with_runner(runner):
    """Build a patched M054ExperimentExecutor with the given runner injected."""
    with mock.patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
        executor = M054ExperimentExecutor()
    executor.runner = runner
    return executor


class TestM054ProviderGuard(TestCase):
    """Regression suite for P1: provider-spec bypass through misconfigured runner."""

    def test_wrong_provider_correct_model_rejected_before_execution(self):
        """CASE A: wrong provider + correct model must raise RuntimeError pre-execution."""
        fake = FakeModelRunner(provider="wrong-provider", default_model="openai/gpt-oss-120b")
        executor = _make_executor_with_runner(fake)

        with self.assertRaises(RuntimeError) as ctx:
            executor._validate_model_routing()

        error_msg = str(ctx.exception)
        self.assertIn("PROVIDER_SPEC_VIOLATION", error_msg)
        self.assertIn("wrong-provider", error_msg)

        total_calls = sum(fake.call_counts.values())
        self.assertEqual(total_calls, 0,
            f"CASE_A: FakeModelRunner.generate must not be called, got {total_calls}: {fake.call_counts}")

    def test_wrong_provider_wrong_model_rejected_before_execution(self):
        """CASE B: wrong provider + wrong model must raise RuntimeError pre-execution."""
        fake = FakeModelRunner(provider="bad-provider", default_model="some-other-model")
        executor = _make_executor_with_runner(fake)

        with self.assertRaises(RuntimeError) as ctx:
            executor._validate_model_routing()

        error_msg = str(ctx.exception)
        self.assertIn("PROVIDER_SPEC_VIOLATION", error_msg)
        self.assertIn("bad-provider", error_msg)

        total_calls = sum(fake.call_counts.values())
        self.assertEqual(total_calls, 0,
            f"CASE_B: FakeModelRunner.generate must not be called, got {total_calls}: {fake.call_counts}")

    def test_correct_provider_correct_model_passes_validation(self):
        """CASE C: correct frozen spec must pass _validate_model_routing without error."""
        fake = FakeModelRunner(provider="groq", default_model="openai/gpt-oss-120b")
        executor = _make_executor_with_runner(fake)

        try:
            executor._validate_model_routing()
        except RuntimeError as exc:
            self.fail(f"CASE_C: _validate_model_routing raised unexpectedly: {exc}")

        total_calls = sum(fake.call_counts.values())
        self.assertEqual(total_calls, 0,
            f"CASE_C: _validate_model_routing must not invoke generate(), got {total_calls}")

    def test_correct_provider_wrong_model_rejected(self):
        """GUARD 2: correct provider but wrong model must be rejected with MODEL_SPEC_VIOLATION."""
        fake = FakeModelRunner(provider="groq", default_model="gpt-4-wrong-model")
        executor = _make_executor_with_runner(fake)

        with self.assertRaises(RuntimeError) as ctx:
            executor._validate_model_routing()

        self.assertIn("MODEL_SPEC_VIOLATION", str(ctx.exception))
        total_calls = sum(fake.call_counts.values())
        self.assertEqual(total_calls, 0, f"GUARD2: zero generate() calls expected, got {total_calls}")

    def test_wrong_provider_execute_all_aborts_before_conditions(self):
        """Wrong provider must abort execute_all before run_condition_a/b/c are invoked."""
        fake = FakeModelRunner(provider="evil-provider", default_model="openai/gpt-oss-120b")
        executor = _make_executor_with_runner(fake)

        condition_calls = []

        def _track(name):
            def _inner(*args, **kwargs):
                condition_calls.append(name)
                return {}
            return _inner

        with mock.patch.object(executor, "run_condition_a", side_effect=_track("A")), \
             mock.patch.object(executor, "run_condition_b", side_effect=_track("B")), \
             mock.patch.object(executor, "run_condition_c", side_effect=_track("C")), \
             mock.patch.object(executor, "load_holdout_ideas", return_value=[]), \
             mock.patch.object(executor, "load_blind_mappings", return_value={}):

            with self.assertRaises(RuntimeError) as ctx:
                executor.execute_all()

        self.assertIn("PROVIDER_SPEC_VIOLATION", str(ctx.exception))
        self.assertEqual(condition_calls, [],
            f"No condition runner must be invoked, but got: {condition_calls}")
        total_calls = sum(fake.call_counts.values())
        self.assertEqual(total_calls, 0, "Zero FakeModelRunner.generate calls expected")


if __name__ == "__main__":
    import unittest
    unittest.main()
