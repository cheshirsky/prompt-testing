"""E2E evaluation of code-gen.md prompt.

Run with: deepeval test run ./tests/test_code_gen.py
"""

from deepeval import assert_test
from deepeval.test_case import LLMTestCase

from src.metrics.code_gen import code_satisfies_tests, tdd_integrity
from src.prompt_runner import run_prompt
from datasets.tdd_prompts import create_code_gen_dataset


def test_code_generation():
    """Evaluate code-gen.md prompt against metrics."""
    dataset = create_code_gen_dataset()
    
    for golden in dataset.goldens:
        task = golden.input
        design = golden.additional_metadata.get("design", "")
        spec = golden.additional_metadata.get("spec", "")
        
        print(f"Executing prompt for: {task[:50]}...")
        
        actual_output = run_prompt("code-gen.md", {
            "task": task,
            "design": design,
            "spec": spec
        })
        
        full_input = f"{task}\n\n{design}\n\n{spec}"
        
        test_case = LLMTestCase(
            input=full_input,
            actual_output=actual_output,
            expected_output=golden.expected_output
        )
        
        assert_test(test_case, [code_satisfies_tests, tdd_integrity])

