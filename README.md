# Prompt Testing

A simple DeepEval test setup illustrating how to evaluate a set of prompts (in this case, for TDD workflows).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env` with your OpenAI key:
```
OPENAI_API_KEY=sk-...
```

## Run Tests

**E2E evaluations** (individual prompt testing):
```bash
deepeval test run ./tests/
```

**Full TDD flow with tracing** (component-level evaluation):
```bash
python ./tests/tdd_flow_tracing.py
```

## Project Structure

```
prompts/          # Prompt templates
fixtures/         # Test fixtures (task.md, solution-design.md, expected outputs)
src/metrics/      # DeepEval metrics definitions
datasets/         # Dataset loader
tests/            # Eval examples
```

