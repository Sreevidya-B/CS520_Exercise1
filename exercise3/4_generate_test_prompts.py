"""
Exercise 3 - Step 4: Generate Test Prompts
Creates LLM prompts for generating spec-guided test cases.
"""

import json
from pathlib import Path


def load_corrected_specifications(problem_num, model):
    """Load corrected specifications from file."""
    script_dir = Path(__file__).parent
    spec_file = script_dir / "specifications" / f"problem{problem_num}_{model}_corrected.py"
    
    if not spec_file.exists():
        return None
    
    with open(spec_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assertions = []
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped.startswith('assert '):
            assertions.append(stripped)
    
    return assertions


def create_test_prompt(problem_info, specifications, model):
    """Create test generation prompt using corrected specifications."""
    function_name = problem_info['function_name']
    signature = problem_info['signature']
    description = problem_info['description']
    problem_num = problem_info['problem_num']
    original_model = problem_info['model']
    strategy = problem_info['strategy']
    
    spec_lines = '\n'.join([f"# Specification {i+1}\n{spec}" for i, spec in enumerate(specifications)])
    
    prompt = f"""Problem description: {description}

Method signature: {signature}

CORRECTED FORMAL SPECIFICATIONS:
{spec_lines}

Please generate pytest test cases that validate these specifications.

CRITICAL REQUIREMENTS:
1. Use the fixture pattern to load the solution dynamically
2. DO NOT hardcode imports - use the fixture 'solution_function'
3. Each test function must accept 'solution_function' as a parameter
4. Name tests with prefix: test_spec_guided_{function_name}_
5. Include docstring indicating which specification(s) each test validates
6. Test both normal cases and edge cases
7. Ensure all tests are independent and can run in any order

REQUIRED TEST FILE STRUCTURE:
```python
from pathlib import Path
import pytest
import importlib.util

def get_solution_module(model, strategy, problem_num):
    \"\"\"Dynamically load the solution module.\"\"\"
    workspace_root = Path(r"S:\\Code\\CS520_Exercise1")
    solution_path = workspace_root / 'generated_code' / model / strategy / f'HumanEval_{{problem_num}}_0.py'
    
    if not solution_path.exists():
        raise FileNotFoundError(f"Solution not found: {{solution_path}}")
    
    spec = importlib.util.spec_from_file_location(
        f"solution_{{model}}_{{strategy}}_{{problem_num}}", 
        solution_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

@pytest.fixture
def solution_function(request):
    \"\"\"Fixture to provide the solution function.\"\"\"
    model = request.config.getoption("--model", default="{original_model}")
    strategy = request.config.getoption("--strategy", default="{strategy}")
    module = get_solution_module(model, strategy, "{problem_num}")
    return getattr(module, "{function_name}")

def test_spec_guided_{function_name}_example(solution_function):
    \"\"\"Validates Specification 1: [description]\"\"\"
    result = solution_function(test_input)
    assert condition_from_spec_1

Generate 5-8 comprehensive test functions that:

Cover ALL {len(specifications)} specifications above

Test edge cases (empty input, single element, boundary values)

Use descriptive test names

Include clear docstrings
"""

    return prompt

def generate_test_prompts():
    """Generate test prompts for all problems."""
    problem_desc_path = Path(__file__).parent / "problem_descriptions.json"
    with open(problem_desc_path, 'r', encoding='utf-8') as f:
        problem_info = json.load(f)

    prompts_dir = Path(__file__).parent / "prompts"
    prompts_dir.mkdir(exist_ok=True)

    models = ['gpt4o', 'claude']

    for problem_num, info in problem_info.items():
        for model in models:
            specifications = load_corrected_specifications(problem_num, model)
            if specifications is None:
                continue
            
            prompt = create_test_prompt(info, specifications, model)
            
            filename = f"test_generation_problem{problem_num}_{model}.txt"
            output_path = prompts_dir / filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(prompt)


if __name__ == "__main__":
    generate_test_prompts()