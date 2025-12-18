"""E2E evaluation of test-gen.md prompt.

Run with: deepeval test run ./tests/test_ut_gen.py
"""

from deepeval import assert_test
from deepeval.test_case import LLMTestCase

from src.metrics.test_gen import aaa_pattern, test_coverage, test_correctness
from src.prompt_runner import run_prompt
from datasets.tdd_prompts import create_test_gen_dataset


def test_ut_generation():
    """Evaluate test-gen.md prompt against metrics."""
    dataset = create_test_gen_dataset()
    
    for golden in dataset.goldens:
        task = golden.input
        design = golden.additional_metadata.get("design", "")
        
        print(f"Executing prompt for: {task[:50]}...")
        
        actual_output = run_prompt("test-gen.md", {
            "task": task,
            "design": design
        })
        
        full_input = f"{task}\n\n{design}" if design else task
        
        test_case = LLMTestCase(
            input=full_input,
            actual_output=actual_output,
            expected_output=golden.expected_output
        )
        
        assert_test(test_case, [aaa_pattern, test_coverage, test_correctness])
