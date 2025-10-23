#!/usr/bin/env python3
"""
Script 2: Generate Prompts for Different Strategies
This creates prompt templates for Chain-of-Thought (CoT), Self-Planning and Self-Debugging prompting strategies.
"""

import json
from pathlib import Path

# Prompt templates for each strategy
STRATEGIES = {
    "cot": {
        "name": "Chain-of-Thought (CoT)",
        "template": """Let's solve this step by step.

First, think through the problem:
1. What is the problem asking for?
2. What approach should we use?
3. What are the edge cases?

Then provide your solution:

{problem_prompt}"""
    },
    
    "self_planning": {
        "name": "Self-Planning",
        "template": """Before implementing, let's create a plan:

Problem: {problem_prompt}

Plan:
- What data structures will you use?
- What is your algorithm?
- What edge cases need handling?

Now implement your plan:"""
    },
    
    "self_debugging": {
        "name": "Self-Debugging",
        "template": """{problem_prompt}

After writing your solution:
1. Identify potential bugs or edge cases
2. Explain how your code handles them
3. Provide the corrected implementation"""
    }
}

def load_selected_problems(input_path="data/selected_problems.jsonl"):
    """Load the selected problems"""
    problems = []
    with open(input_path, 'r') as f:
        for line in f:
            problems.append(json.loads(line))
    return problems

def generate_prompts(problems, strategies=None):
    """
    Generate prompts for each problem and strategy
    
    Returns: dict with structure:
    {
        "cot": {
            "HumanEval/0": "prompt text...",
            "HumanEval/1": "prompt text...",
            ...
        },
        "self_planning": {...},
        ...
    }
    """
    if strategies is None:
        strategies = ["cot", "self_planning", "self_debugging"]
    
    all_prompts = {}
    
    for strategy in strategies:
        if strategy not in STRATEGIES:
            print(f"Warning: Unknown strategy '{strategy}', skipping")
            continue
        
        strategy_prompts = {}
        template = STRATEGIES[strategy]["template"]
        
        for problem in problems:
            task_id = problem['task_id']
            problem_prompt = problem['prompt']
            
            # Generate prompt by filling in template
            full_prompt = template.format(problem_prompt=problem_prompt)
            
            strategy_prompts[task_id] = {
                "prompt": full_prompt,
                "entry_point": problem['entry_point'],
                "test": problem['test']
            }
        
        all_prompts[strategy] = strategy_prompts
        print(f"Generated {len(strategy_prompts)} prompts for {STRATEGIES[strategy]['name']}")
    
    return all_prompts

def save_prompts(all_prompts, output_dir="prompts"):
    """Save prompts to separate JSON files for each strategy"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    for strategy, prompts in all_prompts.items():
        output_path = Path(output_dir) / f"{strategy}_prompts.json"
        with open(output_path, 'w') as f:
            json.dump(prompts, f, indent=2)
        print(f"   Saved to: {output_path}")

def main():
    print("Loading selected problems...")
    problems = load_selected_problems()
    print(f"Loaded {len(problems)} problems")
    
    print("\nGenerating prompts for each strategy...")
    all_prompts = generate_prompts(problems, strategies=["cot", "self_planning", "self_debugging"])
    
    print("\nSaving prompts to files...")
    save_prompts(all_prompts)
    
    print("\nPrompt generation complete!")
    print(f"Prompts saved to prompts/ directory")
        
    return all_prompts

if __name__ == "__main__":
    main()