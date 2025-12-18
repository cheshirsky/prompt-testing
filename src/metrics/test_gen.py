"""Metrics for test-gen.md prompt evaluation."""

from deepeval.metrics import GEval, PromptAlignmentMetric
from deepeval.test_case import LLMTestCaseParams


aaa_pattern = PromptAlignmentMetric(
    prompt_instructions=[
        "Each test follows Arrange-Act-Assert pattern",
        "Each test has a single assertion"
    ],
    threshold=0.7
)

test_coverage = GEval(
    name="TestCoverage",
    criteria="Tests cover happy path, edge cases, and error scenarios.",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
    threshold=0.6
)

test_correctness = GEval(
    name="TestCorrectness",
    criteria="Generated tests match the expected test scenarios.",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
    threshold=0.6
)

