"""
Exercise 3 - Step 2: Generate Specification Prompts
Creates prompts for LLMs to generate formal specifications.
"""

import json
from pathlib import Path


def create_specification_prompt(problem_info, model):
    """Create prompt for generating formal specifications"""
    
    func_name = problem_info['function_name']
    signature = problem_info['signature']
    description = problem_info['description']
    
    prompt = f"""Problem description: {description}

Method signature: {signature}

Please write formal specifications as Python assertions that describe the correct behavior of this method.

Let 'res' denote the expected return value of {func_name}().

CRITICAL REQUIREMENTS:
- Do NOT call {func_name}() in your assertions (no self-reference)
- Do NOT use methods with side effects such as:
  - print, read, write, input operations
  - random number generation (random.random(), random.choice(), etc.)
  - timing functions (time.time(), datetime.now(), etc.)
  - data structure mutations (list.append(), dict.update(), set.add(), etc.)
- Express the relationship between inputs and 'res' using pure arithmetic, string operations, and boolean logic only

Generate approximately 5 formal specifications as Python assert statements.

Example format:
```python
# Specification 1: [Brief description of property]
assert [condition about inputs and res]

# Specification 2: [Brief description of property]
assert [condition about inputs and res]
```
"""
    
    return prompt


def generate_all_prompts():
    """Generate specification prompts for all problem×model combinations"""
    
    problem_file = Path(__file__).parent / 'problem_descriptions.json'
    if not problem_file.exists():
        raise FileNotFoundError("Run 1_extract_problem_info.py first")
    
    with open(problem_file, 'r') as f:
        problem_info = json.load(f)
    
    prompts_dir = Path(__file__).parent / 'prompts'
    prompts_dir.mkdir(exist_ok=True)
    
    models = ['gpt4o', 'claude']
    
    for problem_num, info in problem_info.items():
        for model in models:
            prompt = create_specification_prompt(info, model)
            
            filename = f"spec_generation_problem{problem_num}_{model}.txt"
            filepath = prompts_dir / filename
            
            with open(filepath, 'w') as f:
                f.write(prompt)


if __name__ == "__main__":
    generate_all_prompts()