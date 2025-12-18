"""Metrics for code-gen.md prompt evaluation."""

from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams


code_satisfies_tests = GEval(
    name="CodeSatisfiesTests",
    criteria="Implementation would make all provided test cases pass.",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
    threshold=0.7
)

tdd_integrity = GEval(
    name="TDDIntegrity",
    criteria="Implementation is driven by tests and satisfies all test scenarios.",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
    threshold=0.7
)

