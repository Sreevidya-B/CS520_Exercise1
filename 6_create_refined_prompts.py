#!/usr/bin/env python3
"""
Script 6: Create Refined Prompts Based on Failure Analysis
Generates improved prompts specifically targeting identified failure modes
"""

import json
from pathlib import Path

# Refined prompt templates targeting specific failure modes
REFINED_STRATEGIES = {
    "cot_refined": {
        "name": "Chain-of-Thought (Refined)",
        "description": "Fixes: Import issues, ensures complete code",
        "changes_made": [
            "Added 'CRITICAL REQUIREMENTS' section at top",
            "Added explicit import instruction",
            "Added 'Provide ONLY executable Python code' requirement",
            "Added 'Include ALL helper functions' instruction",
            "Simplified thinking steps to prevent over-explanation"
        ],
        "template": """Let's solve this step by step.

CRITICAL REQUIREMENTS:
1. Always include necessary imports at the top (e.g., from typing import List, Tuple, Dict, Optional)
2. Provide ONLY executable Python code
3. Include ALL helper functions mentioned in the problem
4. Match the exact function signatures from the prompt

Think through:
- What imports do I need? (List them explicitly)
- What helper functions are provided? (Include them all)
- What is the main algorithm?
- What are the edge cases?

Now provide your complete solution starting with imports:

{problem_prompt}"""
    },
    
    "self_planning_refined": {
        "name": "Self-Planning (Refined)",
        "description": "Adds explicit import and completeness checklist",
        "changes_made": [
            "Added 'MANDATORY CHECKLIST' as first step",
            "Made imports the #1 item in checklist",
            "Added explicit 'All helper functions included' check",
            "Added function signature verification step",
            "Added 'Now implement starting with imports' instruction"
        ],
        "template": """Before implementing, let's create a detailed plan:

Problem: {problem_prompt}

MANDATORY CHECKLIST:
Step 1: Identify required imports (typing, math, etc.)
Step 2: List all helper functions that must be included
Step 3: Choose data structures
Step 4: Design algorithm
Step 5: Identify edge cases

Detailed Plan:
1. IMPORTS NEEDED:
   - List all typing imports required (e.g., from typing import List, Tuple)
   - List any other modules needed

2. HELPER FUNCTIONS:
   - What helper functions are provided in the problem?
   - Include them ALL in the solution

3. ALGORITHM:
   - Step-by-step algorithm for the main function

4. EDGE CASES:
   - What edge cases need handling?

Now implement your plan. Start with imports, then all helper functions, then the main function:"""
    },
    
    "self_debugging_refined": {
        "name": "Self-Debugging (Refined)",
        "description": "Explicit completeness check, code-only output",
        "changes_made": [
            "Added 'COMPLETENESS CHECKLIST' before debugging",
            "Explicitly listed 'Missing imports' as first common error",
            "Added 'Missing helper functions' as second common error",
            "Added 'Provide ONLY the final code' to prevent verbose output",
            "Changed from 'debug/fix' mindset to 'implement completely' mindset"
        ],
        "template": """{problem_prompt}

COMPLETENESS CHECKLIST - Verify before submission:
1. All necessary imports included (from typing import ...)
2. All helper functions from problem included
3. Function signatures exactly match the prompt
4. No explanatory text outside code blocks
5. Common errors checked:
   - Missing imports
   - Missing helper functions
   - Incorrect function name
   - Off-by-one errors
   - Empty input handling

Now provide ONLY the final, complete Python code starting with imports:"""
    }
}

def load_selected_problems(input_path="data/selected_problems.jsonl"):
    """Load the selected problems"""
    problems = []
    with open(input_path, 'r') as f:
        for line in f:
            problems.append(json.loads(line))
    return problems

def generate_refined_prompts(problems):
    """Generate refined prompts for each problem and strategy"""
    strategies = ["cot_refined", "self_planning_refined", "self_debugging_refined"]
    
    all_prompts = {}
    
    for strategy in strategies:
        strategy_prompts = {}
        template = REFINED_STRATEGIES[strategy]["template"]
        
        for problem in problems:
            task_id = problem['task_id']
            problem_prompt = problem['prompt']
            
            # Generate refined prompt
            full_prompt = template.format(problem_prompt=problem_prompt)
            
            strategy_prompts[task_id] = {
                "prompt": full_prompt,
                "entry_point": problem['entry_point'],
                "test": problem['test']
            }
        
        all_prompts[strategy] = strategy_prompts
    
    return all_prompts

def save_refined_prompts(all_prompts, output_dir="prompts"):
    """Save refined prompts to files"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    for strategy, prompts in all_prompts.items():
        # prompts/{strategy}_prompts.json
        output_path = Path(output_dir) / f"{strategy}_prompts.json"
        with open(output_path, 'w') as f:
            json.dump(prompts, f, indent=2)

def save_prompt_templates_for_report():
    
    output_dir = Path("results/part2_data")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # results/part2_data/refined_cot_template.txt
    with open(output_dir / "refined_cot_template.txt", 'w') as f:
        f.write("REFINED CoT PROMPT TEMPLATE\n")
        f.write("="*80 + "\n\n")
        f.write(f"Description: {REFINED_STRATEGIES['cot_refined']['description']}\n\n")
        f.write("Changes Made:\n")
        for i, change in enumerate(REFINED_STRATEGIES['cot_refined']['changes_made'], 1):
            f.write(f"  {i}. {change}\n")
        f.write("\n" + "="*80 + "\n")
        f.write("TEMPLATE:\n")
        f.write("="*80 + "\n\n")
        f.write(REFINED_STRATEGIES['cot_refined']['template'])
    
    # results/part2_data/refined_self_planning_template.txt
    with open(output_dir / "refined_self_planning_template.txt", 'w') as f:
        f.write("REFINED SELF-PLANNING PROMPT TEMPLATE\n")
        f.write("="*80 + "\n\n")
        f.write(f"Description: {REFINED_STRATEGIES['self_planning_refined']['description']}\n\n")
        f.write("Changes Made:\n")
        for i, change in enumerate(REFINED_STRATEGIES['self_planning_refined']['changes_made'], 1):
            f.write(f"  {i}. {change}\n")
        f.write("\n" + "="*80 + "\n")
        f.write("TEMPLATE:\n")
        f.write("="*80 + "\n\n")
        f.write(REFINED_STRATEGIES['self_planning_refined']['template'])
    
    # results/part2_data/refined_self_debugging_template.txt
    with open(output_dir / "refined_self_debugging_template.txt", 'w') as f:
        f.write("REFINED SELF-DEBUGGING PROMPT TEMPLATE\n")
        f.write("="*80 + "\n\n")
        f.write(f"Description: {REFINED_STRATEGIES['self_debugging_refined']['description']}\n\n")
        f.write("Changes Made:\n")
        for i, change in enumerate(REFINED_STRATEGIES['self_debugging_refined']['changes_made'], 1):
            f.write(f"  {i}. {change}\n")
        f.write("\n" + "="*80 + "\n")
        f.write("TEMPLATE:\n")
        f.write("="*80 + "\n\n")
        f.write(REFINED_STRATEGIES['self_debugging_refined']['template'])

def main():
    print("Loading problems...")
    problems = load_selected_problems()
    
    print("Generating refined prompts...")
    all_prompts = generate_refined_prompts(problems)
    
    print("Saving refined prompts...")
    save_refined_prompts(all_prompts)
    
    print("Saving templates...")
    save_prompt_templates_for_report()
    
    print("\nRefined prompts created successfully!")

if __name__ == "__main__":
    main()