#!/usr/bin/env python3
"""
Script 4: Evaluate Generated Code
This script tests generated code against HumanEval test cases and calculates pass@k metrics.
"""

import json
import sys
import traceback
from pathlib import Path
from collections import defaultdict

def load_problems(path="data/selected_problems.jsonl"):
    """Load problems from JSONL file"""
    problems = []
    with open(path, 'r') as f:
        for line in f:
            problems.append(json.loads(line))
    return problems

def execute_code_with_tests(code, test_code, entry_point):
    """
    Execute generated code with test cases
    
    Returns:
        (passed: bool, error: str or None)
    """
    try:
        # Create namespace and execute generated code
        namespace = {}
        exec(code, namespace)
        
        # Check if entry point function exists
        if entry_point not in namespace:
            return False, f"Function '{entry_point}' not found in generated code"
        
        # Execute test code in same namespace
        exec(test_code, namespace)
        
        # If we get here, all tests passed
        return True, None
        
    except AssertionError as e:
        return False, f"Test assertion failed: {str(e)}"
    except Exception as e:
        return False, f"{type(e).__name__}: {str(e)}"

def evaluate_model_strategy(model, strategy, problems, k=1):
    """
    Evaluate all k solutions for each problem using a specific model and strategy
    
    Returns:
        Dictionary with evaluation results
    """
    code_dir = Path(f"generated_code/{model}/{strategy}")
    
    if not code_dir.exists():
        print(f"Warning: Directory {code_dir} does not exist")
        return None
    
    results_by_problem = defaultdict(list)
    
    for problem in problems:
        task_id = problem['task_id']
        entry_point = problem['entry_point']
        test_code = problem['test']
        
        file_name = task_id.replace('/', '_')
        
        print(f"\n{task_id}:")
        
        # Evaluate all k solutions for this problem
        for i in range(k):
            code_file = code_dir / f"{file_name}_{i}.py"
            
            if not code_file.exists():
                print(f"  Solution {i}: (file not found)")
                results_by_problem[task_id].append({
                    'passed': False,
                    'error': 'Generated code file not found'
                })
                continue
            
            with open(code_file, 'r') as f:
                code = f.read()
            
            print(f"  Testing {task_id} ({code_file.name})...", end=" ")
            passed, error = execute_code_with_tests(code, test_code, entry_point)
            
            if passed:
                print("Passed")
            else:
                print(f"Failed ({error})")

            results_by_problem[task_id].append({
                'passed': passed,
                'error': error
            })
    
    # Calculate metrics
    total_problems = len(problems)
    problems_with_at_least_one_pass = sum(
        1 for results in results_by_problem.values() 
        if any(r['passed'] for r in results)
    )
    
    # Calculate pass@k
    if k == 1:
        pass_at_k = problems_with_at_least_one_pass / total_problems
    else:
        pass_at_k_sum = 0
        for results in results_by_problem.values():
            n = len(results)
            c = sum(1 for r in results if r['passed'])
            if c > 0:
                prob_all_wrong = 1.0
                for i in range(min(k, n)):
                    prob_all_wrong *= (n - c - i) / (n - i)
                pass_at_k_sum += (1 - prob_all_wrong)
        pass_at_k = pass_at_k_sum / total_problems
    
    passed_problems = [
        task_id for task_id, results in results_by_problem.items()
        if any(r['passed'] for r in results)
    ]
    
    failed_problems = [
        task_id for task_id, results in results_by_problem.items()
        if not any(r['passed'] for r in results)
    ]
    
    return {
        'model': model,
        'strategy': strategy,
        'total_problems': total_problems,
        'k': k,
        'problems_solved': problems_with_at_least_one_pass,
        'problems_failed': len(failed_problems),
        'pass_at_k': {
            f'pass@{k}': pass_at_k
        },
        'passed_problems': passed_problems,
        'failed_problems': failed_problems,
        'detailed_results': dict(results_by_problem)
    }

def evaluate_all(models=None, strategies=None, k=1, problems_path="data/selected_problems.jsonl"):
    """
    Evaluate all combinations of models and strategies with k solutions per problem.
    """
    if models is None:
        models = ['gpt4o', 'claude']
    if strategies is None:
        # strategies = ['cot', 'self_planning', 'self_debugging'] # uncomment this line to run for part-1 only
        strategies = [
            'cot', 'self_planning', 'self_debugging',
            'cot_refined', 'self_planning_refined', 'self_debugging_refined'
        ] # uncomment this line to run for part-2 only
    
    print("\n" + "="*70)
    print(f"EVALUATING ALL CONFIGURATIONS (k={k})")
    print("="*70)
    
    problems = load_problems(problems_path)
    print(f"Loaded {len(problems)} problems\n")
    
    all_results = {}
    
    for model in models:
        all_results[model] = {}
        for strategy in strategies:
            print("\n" + "="*70)
            print(f"Evaluating: {model.upper()} - {strategy.upper()} (k={k})")
            print("="*70)
            
            results = evaluate_model_strategy(model, strategy, problems, k=k)
            
            if results:
                all_results[model][strategy] = results
                
                print("\n" + "="*70)
                print(f"Results for {model.upper()} - {strategy.upper()}:")
                print("="*70)
                print(f"Total problems: {results['total_problems']}")
                print(f"Problems solved (≥1 correct): {results['problems_solved']}")
                print(f"Problems failed (all wrong): {results['problems_failed']}")
                print(f"pass@{k}: {results['pass_at_k'][f'pass@{k}']:.2%}")
                print("="*70)
    
    # Save results
    # output_path = Path("results/evaluation_results.json") # uncomment this line to run for part-1 only
    output_path = Path("results/evaluation_results_part2.json") # uncomment this line to run for part-2 only
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print("\n" + "="*70)
    print(f"Evaluation complete! Results saved to {output_path}")
    print("="*70)
    
    # Print summary table
    print("\n" + "="*70)
    print(f"SUMMARY TABLE (k={k})")
    print("="*70)
    print(f"{'Model':<12} {'Strategy':<22} {'pass@'+str(k):<10} {'Solved':<10}")
    print("-"*70)
    
    for model in models:
        for strategy in strategies:
            if strategy in all_results[model]:
                results = all_results[model][strategy]
                pass_rate = results['pass_at_k'][f'pass@{k}']
                solved = f"{results['problems_solved']}/{results['total_problems']}"
                print(f"{model:<12} {strategy:<22} {pass_rate:<10.1%} {solved:<10}")
    
    print("="*70)
    
    return all_results

def main():
    import sys
    
    # Default k=1 for pass@1 evaluation
    k = 1
    
    # Allow k override from command line
    if len(sys.argv) > 1 and sys.argv[1].startswith('k='):
        k = int(sys.argv[1].split('=')[1])
        print(f"Using k={k} (overridden from command line)")
    
    evaluate_all(k=k)
    
    print("\n" + "="*70)
    print("EVALUATION COMPLETE!")
    print("="*70)
    # print("Results saved to: results/evaluation_results.json") # uncomment this line to run for part-1 only
    print("Results saved to: results/evaluation_results_part2.json") # uncomment this line to run for part-2 only
    print("="*70)

if __name__ == "__main__":
    main()