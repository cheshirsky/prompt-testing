"""LLM prompt execution utility."""

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def run_prompt(prompt_name: str, context: dict) -> str:
    """Execute a prompt template with given context.
    
    Args:
        prompt_name: Name of prompt file in prompts/ directory
        context: Dict with:
            - task: Content of task.md (required)
            - design: Content of solution-design.md (required)
    
    Returns:
        LLM response content
    
    Raises:
        ValueError: If required context fields are missing
    """
    client = OpenAI()
    
    prompt_template = (PROMPTS_DIR / prompt_name).read_text()
    
    # Validate required inputs
    if not context.get('task'):
        raise ValueError("Missing required 'task' (task.md content)")
    
    if not context.get('design'):
        raise ValueError("Missing required 'design' (solution-design.md content)")
    
    # Build user message matching prompt's expected input format
    user_content_parts = []
    
    # @task.md - Required
    user_content_parts.append(f"@task.md:\n{context['task']}")
    
    # @solution-design.md - Required
    user_content_parts.append(f"@solution-design.md:\n{context['design']}")
    
    # @file.spec.ts - Optional (for TDD workflow: pass generated tests to code-gen)
    if context.get('spec'):
        user_content_parts.append(f"@file.spec.ts:\n{context['spec']}")
    
    user_content = "\n\n".join(user_content_parts)
    
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        messages=[
            {"role": "system", "content": prompt_template},
            {"role": "user", "content": user_content}
        ]
    )
    
    return response.choices[0].message.content

