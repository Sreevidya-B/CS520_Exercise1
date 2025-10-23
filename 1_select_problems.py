#!/usr/bin/env python3
"""
Script 1: Select 10 HumanEval Problems
This script loads HumanEval and selects a diverse set of problems for experimentation.
"""

import json
import gzip
from pathlib import Path

def load_humaneval(data_path="human-eval/data/HumanEval.jsonl.gz"):
    """Load all HumanEval problems"""
    problems = []
    with gzip.open(data_path, 'rt') as f:
        for line in f:
            problems.append(json.loads(line))
    return problems

def select_problems(problems, indices=None):
    """
    Select specific problems by index or use default selection
    
    Default selection provides a mix of difficulty levels:
    - Easy: 0, 1, 2 (simple list/string operations)
    - Medium: 10, 16, 20, 25 (requires some logic)
    - Hard: 50, 75, 100 (complex algorithms)
    """
    if indices is None:
        # Default: Mix of easy, medium, hard
        indices = [0, 1, 2, 10, 16, 20, 25, 50, 75, 100]
    
    selected = [problems[i] for i in indices]
    return selected, indices

def save_selected_problems(problems, output_path="data/selected_problems.jsonl"):
    """Save selected problems to file"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        for problem in problems:
            f.write(json.dumps(problem) + '\n')
    
    print(f"Saved {len(problems)} problems to {output_path}")

def print_problem_summary(problems):
    """Print a summary of selected problems"""
    print("\n" + "="*70)
    print("SELECTED PROBLEMS SUMMARY")
    print("="*70)
    
    for i, problem in enumerate(problems, 1):
        task_id = problem['task_id']
        # Extract function name and first line of docstring
        prompt_lines = problem['prompt'].strip().split('\n')
        func_line = [l for l in prompt_lines if 'def ' in l][0]
        
        print(f"\n{i}. {task_id}")
        print(f"   Function: {func_line.strip()}")
        
        # Try to get first line of docstring
        try:
            docstring_start = problem['prompt'].index('"""') + 3
            docstring_end = problem['prompt'].index('"""', docstring_start)
            docstring = problem['prompt'][docstring_start:docstring_end].strip()
            first_line = docstring.split('\n')[0][:80]
            print(f"   Description: {first_line}...")
        except:
            print(f"   Description: [See prompt for details]")
    
    print("\n" + "="*70)

def main():
    print("Loading HumanEval dataset...")
    problems = load_humaneval()
    print(f"Loaded {len(problems)} total problems")
    
    # Select 10 problems
    print("\nSelecting 10 problems (mix of difficulty)...")
    selected, indices = select_problems(problems)
    
    # Print summary
    print_problem_summary(selected)
    
    # Save to file
    save_selected_problems(selected)
    
    # Also save just the indices for reference
    with open("data/selected_indices.json", 'w') as f:
        json.dump({"indices": indices, "count": len(indices)}, f, indent=2)
    
    print(f"\nSetup complete! Selected problems saved to data/")
    print(f"- Problems: data/selected_problems.jsonl")
    print(f"- Indices: data/selected_indices.json")
    
    return selected

if __name__ == "__main__":
    main()