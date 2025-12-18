"""Evaluation datasets for TDD prompt testing."""

from pathlib import Path
from deepeval.dataset import EvaluationDataset, Golden


FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def load_fixture(name: str) -> dict:
    """Load a fixture by name.
    
    Args:
        name: Name of the fixture directory under fixtures/
    
    Returns:
        Dict containing task, design, expected_spec, and expected_impl
    """
    base = FIXTURES_DIR / name
    return {
        "task": (base / "task.md").read_text(),
        "design": (base / "solution-design.md").read_text(),
        "expected_spec": (base / "expected" / f"{name}.spec.ts").read_text(),
        "expected_impl": (base / "expected" / f"{name}.ts").read_text(),
    }


def create_test_gen_dataset() -> EvaluationDataset:
    """Dataset for evaluating test-gen.md prompt.
    
    Returns:
        EvaluationDataset with goldens for test generation evaluation
    """
    fixture = load_fixture("counter")
    
    return EvaluationDataset(goldens=[
        Golden(
            input=fixture["task"],
            expected_output=fixture["expected_spec"],
            additional_metadata={"design": fixture["design"]}
        )
    ])


def create_code_gen_dataset() -> EvaluationDataset:
    """Dataset for evaluating code-gen.md prompt.
    
    Returns:
        EvaluationDataset with goldens for code generation evaluation
    """
    fixture = load_fixture("counter")
    
    return EvaluationDataset(goldens=[
        Golden(
            input=fixture["task"],
            expected_output=fixture["expected_impl"],
            additional_metadata={
                "design": fixture["design"],
                "spec": fixture["expected_spec"]
            }
        )
    ])


def create_tdd_workflow_dataset() -> EvaluationDataset:
    """Dataset for evaluating full TDD workflow.
    
    Returns:
        EvaluationDataset with goldens for TDD workflow evaluation
    """
    fixture = load_fixture("counter")
    
    return EvaluationDataset(goldens=[
        Golden(
            input=fixture["task"],
            expected_output=fixture["expected_impl"],
            additional_metadata={
                "design": fixture["design"],
                "expected_spec": fixture["expected_spec"]
            }
        )
    ])

