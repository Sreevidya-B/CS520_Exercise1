#!/usr/bin/env python3
"""
Script 8: Test-Driven Agent with Feedback Loop (Part 3 Innovation)
Implements iterative code generation with real test feedback
"""

import json
import sys
from pathlib import Path
from openai import OpenAI
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
claude_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def generate_initial_code(model, problem_prompt):
    """Generate initial code attempt"""
    
    system_prompt = """You are an expert Python programmer. Generate clean, correct code.
    
CRITICAL: Provide ONLY the Python code in your response. 
- Include all necessary imports at the top
- Include all helper functions
- No markdown formatting
- No explanations
- Just pure executable Python code"""

    user_prompt = f"""Solve this programming problem:

{problem_prompt}

Remember: Only output executable Python code, nothing else."""

    if model == "gpt4o":
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0,
            max_tokens=2048
        )
        return response.choices[0].message.content
    
    else:  # claude
        response = claude_client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=2048,
            temperature=0.0,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return response.content[0].text


def debug_with_feedback(model, original_prompt, previous_code, error_message, iteration):
    """Generate improved code based on test failure feedback"""
    
    system_prompt = """You are an expert Python debugger. You will receive:
1. The original problem
2. Your previous code attempt  
3. The exact error message from running tests

Analyze the error, identify the bug, and provide corrected code.

CRITICAL: Provide ONLY the corrected Python code.
- Include all necessary imports
- Include all helper functions
- No markdown formatting
- No explanations or apologies
- Just the complete, corrected Python code"""

    user_prompt = f"""ORIGINAL PROBLEM:
{original_prompt}

YOUR PREVIOUS CODE (Iteration {iteration}):
```python
{previous_code}
```

TEST ERROR:
{error_message}

Analyze this error and provide the complete corrected code. Output only Python code."""

    if model == "gpt4o":
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0,
            max_tokens=2048
        )
        return response.choices[0].message.content
    
    else:  # claude
        response = claude_client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=2048,
            temperature=0.0,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return response.content[0].text


def extract_python_code(text):
    """Extract Python code from potential markdown formatting"""
    if "```python" in text:
        start = text.find("```python") + 9
        end = text.find("```", start)
        if end != -1:
            return text[start:end].strip()
    elif "```" in text:
        start = text.find("```") + 3
        end = text.find("```", start)
        if end != -1:
            code = text[start:end].strip()
            if code.startswith("python\n"):
                code = code[7:]
            return code
    return text.strip()


def execute_code_with_tests(code, test_code, entry_point):
    """Execute code with test cases and return results"""
    try:
        namespace = {}
        exec(code, namespace)
        
        if entry_point not in namespace:
            return False, f"Function '{entry_point}' not found in generated code"
        
        exec(test_code, namespace)
        return True, None
        
    except AssertionError as e:
        return False, f"Test assertion failed: {str(e)}"
    except Exception as e:
        return False, f"{type(e).__name__}: {str(e)}"


def iterative_agent_solve(model, problem, max_iterations=3):
    """
    Solve problem using iterative feedback loop
    
    Returns: dict with iteration history and final result
    """
    task_id = problem['task_id']
    problem_prompt = problem['prompt']
    entry_point = problem['entry_point']
    test_code = problem['test']
    
    history = []
    
    # Iteration 0: Initial attempt
    print(f"  Iteration 0: Generating initial code...")
    code = generate_initial_code(model, problem_prompt)
    code = extract_python_code(code)
    
    passed, error = execute_code_with_tests(code, test_code, entry_point)
    
    history.append({
        'iteration': 0,
        'code': code,
        'passed': passed,
        'error': error
    })
    
    if passed:
        print(f"Passed on first attempt!")
        return {
            'task_id': task_id,
            'iterations_needed': 0,
            'final_passed': True,
            'history': history
        }
    
    print(f"Failed: {error}")
    
    # Iterations 1 to max_iterations: Debug based on feedback
    for i in range(1, max_iterations + 1):
        print(f"Iteration {i}: Debugging with feedback...")

        code = debug_with_feedback(
            model, 
            problem_prompt, 
            history[-1]['code'], 
            history[-1]['error'],
            i
        )
        code = extract_python_code(code)
        
        passed, error = execute_code_with_tests(code, test_code, entry_point)
        
        history.append({
            'iteration': i,
            'code': code,
            'passed': passed,
            'error': error
        })
        
        if passed:
            print(f"Passed after {i} iteration(s)!")
            return {
                'task_id': task_id,
                'iterations_needed': i,
                'final_passed': True,
                'history': history
            }
        
        print(f"Still failing: {error}")

    print(f"Failed after {max_iterations} iterations")
    return {
        'task_id': task_id,
        'iterations_needed': max_iterations,
        'final_passed': False,
        'history': history
    }


def load_problems(path="data/selected_problems.jsonl"):
    """Load problems"""
    problems = []
    with open(path, 'r') as f:
        for line in f:
            problems.append(json.loads(line))
    return problems


def run_iterative_agent_experiment(models=None, max_iterations=3):
    """Run the full iterative agent experiment"""
    
    if models is None:
        models = ['gpt4o', 'claude']
    
    problems = load_problems()
    
    results = {}
    
    for model in models:
        print(f"\n{'='*70}")
        print(f"RUNNING ITERATIVE AGENT: {model.upper()}")
        print(f"{'='*70}\n")
        
        model_results = []
        
        for problem in problems:
            task_id = problem['task_id']
            print(f"\n{task_id}:")
            
            result = iterative_agent_solve(model, problem, max_iterations)
            model_results.append(result)
        
        # Calculate statistics
        total = len(model_results)
        passed = sum(1 for r in model_results if r['final_passed'])
        first_try = sum(1 for r in model_results if r['final_passed'] and r['iterations_needed'] == 0)
        
        results[model] = {
            'individual_results': model_results,
            'summary': {
                'total_problems': total,
                'passed': passed,
                'failed': total - passed,
                'pass_rate': passed / total,
                'first_try_success': first_try,
                'avg_iterations': sum(r['iterations_needed'] for r in model_results if r['final_passed']) / max(passed, 1)
            }
        }
        
        print(f"\n{'-'*70}")
        print(f"Summary for {model.upper()}:")
        print(f"  Total: {total}")
        print(f"  Passed: {passed} ({passed/total:.1%})")
        print(f"  First-try success: {first_try}")
        print(f"  Avg iterations (for solved): {results[model]['summary']['avg_iterations']:.2f}")
        print(f"{'-'*70}")
    
    # Save results
    output_path = Path("results/novel_strategy_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"Results saved to: {output_path}")
    print(f"{'='*70}")
    
    return results


def main():
    """Main function"""
    max_iterations = 3 
    
    print("="*70)
    print("PART 3: Novel Strategy: ITERATIVE TEST-DRIVEN AGENT")
    print("="*70)
    print(f"Max iterations per problem: {max_iterations}")
    print("="*70)
    
    run_iterative_agent_experiment(max_iterations=max_iterations)


if __name__ == "__main__":
    main()