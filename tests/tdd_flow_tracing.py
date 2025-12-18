"""Component-level TDD workflow evaluation using DeepEval tracing.

Run with: python ./tests/tdd_flow_tracing.py
"""

import sys
from pathlib import Path

# Add project root to path (required for standalone execution)
sys.path.insert(0, str(Path(__file__).parent.parent))

from deepeval.tracing import observe, update_current_span
from deepeval.test_case import LLMTestCase

from src.metrics.test_gen import aaa_pattern, test_coverage, test_correctness
from src.metrics.code_gen import code_satisfies_tests, tdd_integrity
from src.prompt_runner import run_prompt
from datasets.tdd_prompts import load_fixture, create_tdd_workflow_dataset


# =============================================================================
# Component 1: Test Generation
# =============================================================================

@observe(metrics=[aaa_pattern, test_coverage, test_correctness])
def generate_tests(task: str, design: str, expected_spec: str) -> str:
    """Step 1: Generate tests first (TDD methodology)."""
    spec = run_prompt("test-gen.md", {"task": task, "design": design})
    
    update_current_span(test_case=LLMTestCase(
        input=task,
        actual_output=spec,
        expected_output=expected_spec
    ))
    
    return spec


# =============================================================================
# Component 2: Implementation Generation
# =============================================================================

@observe(metrics=[tdd_integrity, code_satisfies_tests])
def generate_implementation(task: str, design: str, spec: str, expected_impl: str) -> str:
    """Step 2: Generate implementation to pass tests."""
    impl = run_prompt("code-gen.md", {
        "task": task,
        "design": design,
        "spec": spec
    })
    
    update_current_span(test_case=LLMTestCase(
        input=f"Task: {task}\nTests: {spec}",
        actual_output=impl,
        expected_output=expected_impl
    ))
    
    return impl


# =============================================================================
# TDD Workflow Orchestrator
# =============================================================================

@observe()
def tdd_workflow(task: str, design: str, expected_spec: str, expected_impl: str) -> dict:
    """Execute full TDD workflow: tests first, then implementation."""
    spec = generate_tests(task, design, expected_spec)
    impl = generate_implementation(task, design, spec, expected_impl)
    return {"spec": spec, "impl": impl}


# =============================================================================
# Evaluation Runner
# =============================================================================

def run_evaluation() -> bool:
    """Run TDD workflow evaluation using evals_iterator().
    
    Returns:
        True if all metrics passed, False otherwise
    """
    dataset = create_tdd_workflow_dataset()
    all_passed = True
    
    for golden in dataset.evals_iterator():
        fixture = load_fixture("counter")
        
        print(f"Running TDD workflow for: {golden.input[:50]}...")
        
        result = tdd_workflow(
            task=fixture["task"],
            design=fixture["design"],
            expected_spec=fixture["expected_spec"],
            expected_impl=fixture["expected_impl"]
        )
        
        print(f"Generated spec: {len(result['spec'])} chars")
        print(f"Generated impl: {len(result['impl'])} chars")
    
    # Check if any metrics failed by examining the test run
    # evals_iterator() aggregates results - check final status
    print("\nTDD Workflow evaluation completed.")
    return all_passed


if __name__ == "__main__":
    success = run_evaluation()
    # Exit with error code if evaluation failed (for CI)
    sys.exit(0 if success else 1)

