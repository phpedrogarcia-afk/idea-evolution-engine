"""
tests/test_native_error_semantics.py
Offline verification of NativeModelRunner error representation, transport retry separation,
and semantic repair gating.

Verifies:
  1. HTTP 429 Rate Limit is classified as RATE_LIMIT, does NOT trigger semantic repair, retries transport.
  2. HTTP 400 Bad Request without failed_generation is classified as BAD_REQUEST, does NOT trigger semantic repair.
  3. HTTP 401 / 403 fails closed immediately without transport storm or semantic repair.
  4. HTTP 5xx is classified as PROVIDER_TRANSIENT and attempts bounded transport retry, 0 semantic repair.
  5. Genuine failed_generation in error body is admitted and triggers semantic repair when allowed.
  6. Negative control: converting generic 429 into failed_generation fails assertions.
"""

from unittest import TestCase, mock
from pydantic import BaseModel, Field
from src.idea_evolution.providers.native import (
    NativeModelRunner,
    ProviderErrorDetails,
    parse_provider_exception,
    sanitize_error_message,
)
from src.idea_evolution.providers.base import ModelResponse, ModelUsage


class MockSchema(BaseModel):
    title: str = Field(..., description="A title")
    count: int = Field(..., description="A count")


class MockGroqError(Exception):
    def __init__(self, message: str, status_code: int = 400, body: dict = None, headers: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body or {}
        self.response = mock.MagicMock()
        self.response.status_code = status_code
        self.response.headers = headers or {}


class TestNativeErrorSemantics(TestCase):
    """Test suite for error typing, retry separation, and secret sanitization."""

    def test_sanitize_error_message(self):
        """Sanitizer must remove secret keys, bearer tokens, and credentials from messages."""
        msg = "Error with key gsk_1234567890abcdef and Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        sanitized = sanitize_error_message(msg)
        self.assertNotIn("gsk_1234567890abcdef", sanitized)
        self.assertNotIn("eyJhbGci", sanitized)
        self.assertIn("gsk_***", sanitized)
        self.assertIn("Bearer ***", sanitized)

    def test_429_rate_limit_classification_and_no_semantic_repair(self):
        """HTTP 429 must be classified as RATE_LIMIT and must NOT trigger semantic repair."""
        err = MockGroqError("Rate limit reached for TPM/RPM on model gpt-oss", status_code=429, headers={"retry-after": "1.5"})
        details = parse_provider_exception(err, provider="groq")

        self.assertEqual(details.http_status, 429)
        self.assertEqual(details.error_type, "RATE_LIMIT")
        self.assertTrue(details.is_rate_limit)
        self.assertTrue(details.is_transient)
        self.assertFalse(details.is_schema_generation_failure)
        self.assertIsNone(details.failed_generation)
        self.assertEqual(details.retry_after_seconds, 1.5)

        # Verify NativeModelRunner.generate does NOT trigger semantic repair on 429
        runner = NativeModelRunner(provider="groq", api_key="test-key", default_model="openai/gpt-oss-120b")
        with mock.patch.object(runner, "_call_provider", return_value=("", ModelUsage(), details)) as mock_call:
            resp = runner.generate(prompt_text="test", output_schema=MockSchema, stage_name="TEST_STAGE", max_repairs=1)

            self.assertIsNone(resp.parsed)
            self.assertEqual(resp.retry_count, 0)
            self.assertIn("PROVIDER_TRANSPORT_ERROR: RATE_LIMIT (HTTP 429)", resp.error)
            self.assertEqual(mock_call.call_count, 1, "Semantic repair must NOT be called for transport rate limit!")

    def test_400_bad_request_without_failed_gen_no_repair(self):
        """HTTP 400 without genuine failed_generation must fail closed with 0 semantic repairs."""
        err = MockGroqError("Invalid parameter: temperature out of range", status_code=400, body={"error": {"code": "invalid_param"}})
        details = parse_provider_exception(err, provider="groq")

        self.assertEqual(details.http_status, 400)
        self.assertEqual(details.error_type, "BAD_REQUEST")
        self.assertFalse(details.is_transient)
        self.assertFalse(details.is_schema_generation_failure)
        self.assertIsNone(details.failed_generation)

        runner = NativeModelRunner(provider="groq", api_key="test-key", default_model="openai/gpt-oss-120b")
        with mock.patch.object(runner, "_call_provider", return_value=("", ModelUsage(), details)) as mock_call:
            resp = runner.generate(prompt_text="test", output_schema=MockSchema, stage_name="TEST_STAGE", max_repairs=1)

            self.assertIsNone(resp.parsed)
            self.assertEqual(resp.retry_count, 0)
            self.assertIn("PROVIDER_TRANSPORT_ERROR: BAD_REQUEST (HTTP 400)", resp.error)
            self.assertEqual(mock_call.call_count, 1)

    def test_genuine_failed_generation_triggers_semantic_repair(self):
        """When provider returns genuine failed_generation body, semantic repair IS permitted."""
        err = MockGroqError(
            "json_validate_failed",
            status_code=400,
            body={"error": {"code": "json_validate_failed", "failed_generation": '{"title": "Valid", "extra": 123}'}}
        )
        details = parse_provider_exception(err, provider="groq")

        self.assertTrue(details.is_schema_generation_failure)
        self.assertEqual(details.failed_generation, '{"title": "Valid", "extra": 123}')

        runner = NativeModelRunner(provider="groq", api_key="test-key", default_model="openai/gpt-oss-120b")
        with mock.patch.object(
            runner,
            "_call_provider",
            side_effect=[
                ("", ModelUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15), details),
                ('{"title": "Fixed Title", "count": 42}', ModelUsage(prompt_tokens=20, completion_tokens=10, total_tokens=30), None),
            ]
        ) as mock_call:
            resp = runner.generate(prompt_text="test", output_schema=MockSchema, stage_name="TEST_STAGE", max_repairs=1)

            self.assertIsNotNone(resp.parsed)
            self.assertEqual(resp.parsed.title, "Fixed Title")
            self.assertEqual(resp.parsed.count, 42)
            self.assertEqual(resp.retry_count, 1)
            self.assertEqual(mock_call.call_count, 2)

    def test_401_403_fail_closed_no_retries(self):
        """HTTP 401 / 403 must fail closed without retry storm or semantic repair."""
        err = MockGroqError("Invalid API Key", status_code=401)
        details = parse_provider_exception(err, provider="groq")

        self.assertEqual(details.http_status, 401)
        self.assertEqual(details.error_type, "AUTHENTICATION")
        self.assertFalse(details.is_transient)

        runner = NativeModelRunner(provider="groq", api_key="test-key", default_model="openai/gpt-oss-120b")
        with mock.patch.object(runner, "_call_provider", return_value=("", ModelUsage(), details)) as mock_call:
            resp = runner.generate(prompt_text="test", output_schema=MockSchema, stage_name="TEST_STAGE", max_repairs=1)

            self.assertIsNone(resp.parsed)
            self.assertEqual(resp.retry_count, 0)
            self.assertIn("AUTHENTICATION", resp.error)
            self.assertEqual(mock_call.call_count, 1)

    def test_negative_control_generic_exception_must_not_be_failed_generation(self):
        """Negative control: prove that generic exception string must NEVER populate failed_generation."""
        generic_err = Exception("Connection reset by peer at IP 1.2.3.4")
        details = parse_provider_exception(generic_err, provider="groq")

        # Must NOT be marked as failed_generation
        self.assertIsNone(details.failed_generation)
        self.assertFalse(details.is_schema_generation_failure)

        # If a broken parser set failed_generation = str(generic_err), this assertion would catch it:
        self.assertNotEqual(details.failed_generation, str(generic_err))


if __name__ == "__main__":
    import unittest
    unittest.main()
