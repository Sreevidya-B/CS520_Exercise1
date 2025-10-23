#!/usr/bin/env python3
"""
Script 9: Analyze Novel Strategy Results (Part 3)
Compare iterative agent with baseline strategies
"""

import json
from pathlib import Path


def load_json(path):
    """Load JSON results"""
    with open(path, 'r') as f:
        return json.load(f)


def compare_with_baselines():
    """Compare iterative agent with Part 1 and Part 2 baselines"""
    
    print("\n" + "="*90)
    print("PART 3: NOVEL STRATEGY COMPARISON")
    print("="*90)
    
    part1 = load_json("results/evaluation_results.json")
    part2 = load_json("results/evaluation_results_part2.json")
    part3 = load_json("results/novel_strategy_results.json")
    
    print(f"\n{'Model':<10} {'Strategy':<35} {'Pass@1':<10} {'Notes':<25}")
    print("-"*90)
    
    for model in ['gpt4o', 'claude']:
        cot_orig = part1[model]['cot']['pass_at_k']['pass@1']
        sp_orig = part1[model]['self_planning']['pass_at_k']['pass@1']
        sd_orig = part1[model]['self_debugging']['pass_at_k']['pass@1']
        
        cot_ref = part2[model]['cot_refined']['pass_at_k']['pass@1']
        sp_ref = part2[model]['self_planning_refined']['pass_at_k']['pass@1']
        sd_ref = part2[model]['self_debugging_refined']['pass_at_k']['pass@1']
        
        novel = part3[model]['summary']['pass_rate']
        first_try = part3[model]['summary']['first_try_success']
        
        print(f"\n{model.upper()}:")
        print(f"{'':10} Part 1: CoT (baseline)            {cot_orig:<10.1%} Single-shot")
        print(f"{'':10} Part 1: Self-Planning             {sp_orig:<10.1%} Single-shot")
        print(f"{'':10} Part 1: Self-Debugging            {sd_orig:<10.1%} Single-shot")
        print(f"{'':10} Part 2: CoT Refined               {cot_ref:<10.1%} Single-shot")
        print(f"{'':10} Part 2: Self-Planning Refined     {sp_ref:<10.1%} Single-shot")
        print(f"{'':10} Part 2: Self-Debugging Refined    {sd_ref:<10.1%} Single-shot")
        print(f"{'':10} Part 3: Iterative Agent           {novel:<10.1%} Multi-shot ({first_try}/10 first-try)")
    
    print("\n" + "="*90)


def analyze_iteration_usage():
    """Analyze how many problems needed iterations"""
    
    part3 = load_json("results/novel_strategy_results.json")
    
    print("\n" + "="*90)
    print("ITERATION USAGE ANALYSIS")
    print("="*90)
    
    for model in ['gpt4o', 'claude']:
        print(f"\n{model.upper()}:")
        print("-"*60)
        
        results = part3[model]['individual_results']
        
        iter_counts = {0: 0, 1: 0, 2: 0, 3: 0, 'failed': 0}
        
        for r in results:
            if r['final_passed']:
                iter_counts[r['iterations_needed']] += 1
            else:
                iter_counts['failed'] += 1
        
        print(f"  Solved on first try (0 iterations):  {iter_counts[0]}/10")
        print(f"  Solved after 1 iteration:            {iter_counts[1]}/10")
        print(f"  Solved after 2 iterations:           {iter_counts[2]}/10")
        print(f"  Solved after 3 iterations:           {iter_counts[3]}/10")
        print(f"  Failed after max iterations:         {iter_counts['failed']}/10")


def analyze_strategy_effectiveness():
    """Analyze whether the novel strategy helped"""
    
    part1 = load_json("results/evaluation_results.json")
    part3 = load_json("results/novel_strategy_results.json")
    
    print("\n" + "="*90)
    print("STRATEGY EFFECTIVENESS ANALYSIS")
    print("="*90)
    
    for model in ['gpt4o', 'claude']:
        print(f"\n{model.upper()}:")
        print("-"*60)
        
        worst_baseline = min(
            part1[model]['cot']['pass_at_k']['pass@1'],
            part1[model]['self_planning']['pass_at_k']['pass@1'],
            part1[model]['self_debugging']['pass_at_k']['pass@1']
        )
        
        novel_pass_rate = part3[model]['summary']['pass_rate']
        
        improvement = novel_pass_rate - worst_baseline
        
        print(f"  Worst baseline (Part 1):     {worst_baseline:.1%}")
        print(f"  Novel strategy (Part 3):     {novel_pass_rate:.1%}")
        print(f"  Improvement:                 {improvement:+.1%}")


def analyze_problems_fixed_by_iteration():
    """Check if any problems were fixed by iteration that failed initially"""
    
    part3 = load_json("results/novel_strategy_results.json")
    
    print("\n" + "="*90)
    print("PROBLEMS FIXED BY ITERATIVE FEEDBACK")
    print("="*90)
    
    for model in ['gpt4o', 'claude']:
        print(f"\n{model.upper()}:")
        print("-"*60)
        
        results = part3[model]['individual_results']
        
        fixed_by_iteration = []
        for r in results:
            if r['final_passed'] and r['iterations_needed'] > 0:
                fixed_by_iteration.append({
                    'task_id': r['task_id'],
                    'iterations': r['iterations_needed'],
                    'initial_error': r['history'][0].get('error', 'Unknown')
                })
        
        if fixed_by_iteration:
            print(f"  Problems fixed by iteration: {len(fixed_by_iteration)}")
            for item in fixed_by_iteration:
                print(f"\n    {item['task_id']}:")
                print(f"      Iterations needed: {item['iterations']}")
                print(f"      Initial error: {item['initial_error']}")
        else:
            print(f"  No problems required iteration (all passed first try)")


def create_summary_report():
    """Create JSON summary for Part 3"""
    
    part1 = load_json("results/evaluation_results.json")
    part2 = load_json("results/evaluation_results_part2.json")
    part3 = load_json("results/novel_strategy_results.json")
    
    summary = {
        "part_3_summary": {
            "strategy_name": "Iterative Test-Driven Agent",
            "description": "Multi-shot code generation with real test execution feedback",
            "max_iterations": 3,
            "results": {}
        }
    }
    
    for model in ['gpt4o', 'claude']:
        summary["part_3_summary"]["results"][model] = {
            "baseline_cot": part1[model]['cot']['pass_at_k']['pass@1'],
            "baseline_best": max(
                part1[model]['cot']['pass_at_k']['pass@1'],
                part1[model]['self_planning']['pass_at_k']['pass@1'],
                part1[model]['self_debugging']['pass_at_k']['pass@1']
            ),
            "refined_best": max(
                part2[model]['cot_refined']['pass_at_k']['pass@1'],
                part2[model]['self_planning_refined']['pass_at_k']['pass@1'],
                part2[model]['self_debugging_refined']['pass_at_k']['pass@1']
            ),
            "novel_strategy": part3[model]['summary']['pass_rate'],
            "first_try_success": part3[model]['summary']['first_try_success'],
            "avg_iterations": part3[model]['summary']['avg_iterations']
        }
    
    output_path = Path("results/part3_summary.json")
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nSummary saved to: {output_path}")


def main():
    """Run all analyses"""
    print("="*90)
    print("PART 3: NOVEL STRATEGY ANALYSIS")
    print("="*90)
    
    compare_with_baselines()
    analyze_iteration_usage()
    analyze_strategy_effectiveness()
    analyze_problems_fixed_by_iteration()
    create_summary_report()
    
    print("\n" + "="*90)
    print("ANALYSIS COMPLETE!")
    print("="*90)


if __name__ == "__main__":
    main()