#!/usr/bin/env python3
"""
Script 5: Extract Failure Data for Part 2
Collects generated code, test cases and errors
"""

import json
from pathlib import Path

def load_evaluation_results(path="results/evaluation_results.json"):
    """Load evaluation results from Part 1"""
    with open(path, 'r') as f:
        return json.load(f)

def load_problem(task_id, problems_path="data/selected_problems.jsonl"):
    """Load a specific problem with its test cases"""
    with open(problems_path, 'r') as f:
        for line in f:
            problem = json.loads(line)
            if problem['task_id'] == task_id:
                return problem
    return None

def extract_failure_case_1_data():
    """
    Extract all data for Failure Case 1: HumanEval/1
    """
    problem = load_problem("HumanEval/1")
    eval_results = load_evaluation_results()
    
    # Get GPT-4o Self-Debugging data
    gpt_result = eval_results['gpt4o']['self_debugging']['detailed_results']['HumanEval/1'][0]
    gpt_code_path = Path("generated_code/gpt4o/self_debugging/HumanEval_1_0.py")
    gpt_code = ""
    if gpt_code_path.exists():
        with open(gpt_code_path, 'r') as f:
            gpt_code = f.read()
    
    # Get Claude CoT data
    claude_result = eval_results['claude']['cot']['detailed_results']['HumanEval/1'][0]
    claude_code_path = Path("generated_code/claude/cot/HumanEval_1_0.py")
    claude_code = ""
    if claude_code_path.exists():
        with open(claude_code_path, 'r') as f:
            claude_code = f.read()
    
    # Get Claude Self-Debugging data
    claude_sd_result = eval_results['claude']['self_debugging']['detailed_results']['HumanEval/1'][0]
    claude_sd_code_path = Path("generated_code/claude/self_debugging/HumanEval_1_0.py")
    claude_sd_code = ""
    if claude_sd_code_path.exists():
        with open(claude_sd_code_path, 'r') as f:
            claude_sd_code = f.read()
    
    # Get original prompts
    gpt_prompt = ""
    claude_prompt = ""
    
    gpt_prompt_path = Path("prompts/self_debugging_prompts.json")
    if gpt_prompt_path.exists():
        with open(gpt_prompt_path, 'r') as f:
            prompts = json.load(f)
            gpt_prompt = prompts["HumanEval/1"]["prompt"]
    
    claude_prompt_path = Path("prompts/cot_prompts.json")
    if claude_prompt_path.exists():
        with open(claude_prompt_path, 'r') as f:
            prompts = json.load(f)
            claude_prompt = prompts["HumanEval/1"]["prompt"]
    
    return {
        "problem_id": "HumanEval/1",
        "problem_name": "Separate Parentheses Groups",
        "problem_prompt": problem['prompt'],
        "test_cases": problem['test'],
        "entry_point": problem['entry_point'],
        "failures": {
            "gpt4o_self_debugging": {
                "passed": gpt_result['passed'],
                "error": gpt_result.get('error', 'N/A'),
                "generated_code": gpt_code,
                "original_prompt": gpt_prompt
            },
            "claude_cot": {
                "passed": claude_result['passed'],
                "error": claude_result.get('error', 'N/A'),
                "generated_code": claude_code,
                "original_prompt": claude_prompt
            },
            "claude_self_debugging": {
                "passed": claude_sd_result['passed'],
                "error": claude_sd_result.get('error', 'N/A'),
                "generated_code": claude_sd_code,
                "original_prompt": gpt_prompt
            }
        }
    }

def extract_failure_case_2_data():
    """
    Extract all data for Failure Case 2: HumanEval/10
    """
    problem = load_problem("HumanEval/10")
    eval_results = load_evaluation_results()
    
    # Get GPT-4o Self-Debugging data (failed)
    gpt_sd_result = eval_results['gpt4o']['self_debugging']['detailed_results']['HumanEval/10'][0]
    gpt_sd_code_path = Path("generated_code/gpt4o/self_debugging/HumanEval_10_0.py")
    gpt_sd_code = ""
    if gpt_sd_code_path.exists():
        with open(gpt_sd_code_path, 'r') as f:
            gpt_sd_code = f.read()
    
    # Get GPT-4o CoT data (passed)
    gpt_cot_result = eval_results['gpt4o']['cot']['detailed_results']['HumanEval/10'][0]
    gpt_cot_code_path = Path("generated_code/gpt4o/cot/HumanEval_10_0.py")
    gpt_cot_code = ""
    if gpt_cot_code_path.exists():
        with open(gpt_cot_code_path, 'r') as f:
            gpt_cot_code = f.read()
    
    # Get Claude CoT data (passed)
    claude_result = eval_results['claude']['cot']['detailed_results']['HumanEval/10'][0]
    claude_code_path = Path("generated_code/claude/cot/HumanEval_10_0.py")
    claude_code = ""
    if claude_code_path.exists():
        with open(claude_code_path, 'r') as f:
            claude_code = f.read()
    
    # Get prompts
    gpt_sd_prompt = ""
    gpt_cot_prompt = ""
    
    sd_prompt_path = Path("prompts/self_debugging_prompts.json")
    if sd_prompt_path.exists():
        with open(sd_prompt_path, 'r') as f:
            prompts = json.load(f)
            gpt_sd_prompt = prompts["HumanEval/10"]["prompt"]
    
    cot_prompt_path = Path("prompts/cot_prompts.json")
    if cot_prompt_path.exists():
        with open(cot_prompt_path, 'r') as f:
            prompts = json.load(f)
            gpt_cot_prompt = prompts["HumanEval/10"]["prompt"]
    
    return {
        "problem_id": "HumanEval/10",
        "problem_name": "Make Palindrome",
        "problem_prompt": problem['prompt'],
        "test_cases": problem['test'],
        "entry_point": problem['entry_point'],
        "failure": {
            "gpt4o_self_debugging": {
                "passed": gpt_sd_result['passed'],
                "error": gpt_sd_result.get('error', 'N/A'),
                "generated_code": gpt_sd_code,
                "original_prompt": gpt_sd_prompt
            }
        },
        "successful_comparisons": {
            "gpt4o_cot": {
                "passed": gpt_cot_result['passed'],
                "generated_code": gpt_cot_code,
                "original_prompt": gpt_cot_prompt
            },
            "claude_cot": {
                "passed": claude_result['passed'],
                "generated_code": claude_code
            }
        }
    }

def main():
    """Extract all failure data and save to JSON"""
    
    print("Extracting Failure Case 1 data...")
    case1_data = extract_failure_case_1_data()
    
    print("Extracting Failure Case 2 data...")
    case2_data = extract_failure_case_2_data()
    
    output = {
        "part_2_failure_analysis": {
            "failure_case_1": case1_data,
            "failure_case_2": case2_data
        }
    }
    
    output_path = Path("results/part2_failure_data.json")
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nFailure data extracted and saved to: {output_path}")
    
    # Additionally, saving individual files for easier access
    
    data_dir = Path("results/part2_data")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Case 1 files
    # case1_problem.txt - Problem definition
    with open(data_dir / "case1_problem.txt", 'w') as f:
        f.write(case1_data['problem_prompt'])
    
    # case1_test_cases.txt - Test cases
    with open(data_dir / "case1_test_cases.txt", 'w') as f:
        f.write(case1_data['test_cases'])

    # case1_gpt4o_code.py - Failed GPT-4o code
    with open(data_dir / "case1_gpt4o_code.py", 'w') as f:
        f.write(case1_data['failures']['gpt4o_self_debugging']['generated_code'])
    
    # case1_gpt4o_prompt.txt - Original GPT-4o prompt
    with open(data_dir / "case1_gpt4o_prompt.txt", 'w') as f:
        f.write(case1_data['failures']['gpt4o_self_debugging']['original_prompt'])
    
    # case1_claude_code.py - Failed Claude code
    with open(data_dir / "case1_claude_code.py", 'w') as f:
        f.write(case1_data['failures']['claude_cot']['generated_code'])

    # case1_claude_prompt.txt - Original Claude prompt
    with open(data_dir / "case1_claude_prompt.txt", 'w') as f:
        f.write(case1_data['failures']['claude_cot']['original_prompt'])
    
    # Case 2 files
    # case2_problem.txt - Problem definition
    with open(data_dir / "case2_problem.txt", 'w') as f:
        f.write(case2_data['problem_prompt'])

    # case2_test_cases.txt - Test cases
    with open(data_dir / "case2_test_cases.txt", 'w') as f:
        f.write(case2_data['test_cases'])

    # case2_gpt4o_failed_code.py - Failed GPT-4o code
    with open(data_dir / "case2_gpt4o_failed_code.py", 'w') as f:
        f.write(case2_data['failure']['gpt4o_self_debugging']['generated_code'])

    # case2_gpt4o_success_code.py - Successful GPT-4o code for comparison
    with open(data_dir / "case2_gpt4o_success_code.py", 'w') as f:
        f.write(case2_data['successful_comparisons']['gpt4o_cot']['generated_code'])

    # case2_gpt4o_prompt.txt - Original GPT-4o prompt
    with open(data_dir / "case2_gpt4o_prompt.txt", 'w') as f:
        f.write(case2_data['failure']['gpt4o_self_debugging']['original_prompt'])

    # case2_claude_success_code.py - Successful Claude code for comparison
    with open(data_dir / "case2_claude_success_code.py", 'w') as f:
        f.write(case2_data['successful_comparisons']['claude_cot']['generated_code'])


if __name__ == "__main__":
    main()