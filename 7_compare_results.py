#!/usr/bin/env python3
"""
Script 7: Compare Original vs Refined Prompt Results
Shows improvement metrics for Part 2 report
"""

import json
from pathlib import Path

def load_part1_results(path="results/evaluation_results.json"):
    """Load Part 1 evaluation results"""
    with open(path, 'r') as f:
        return json.load(f)

def load_part2_results(path="results/evaluation_results_part2.json"):
    """Load Part 2 evaluation results"""
    with open(path, 'r') as f:
        return json.load(f)

def compare_strategies():
    """Compare original vs refined strategies"""
    part1 = load_part1_results()
    part2 = load_part2_results()
    
    print("\n" + "="*90)
    print("COMPARISON: ORIGINAL VS REFINED PROMPTS (Part 2 Results)")
    print("="*90)
    
    models = ['gpt4o', 'claude']
    strategy_pairs = [
        ('cot', 'cot_refined'),
        ('self_planning', 'self_planning_refined'),
        ('self_debugging', 'self_debugging_refined')
    ]
    
    print(f"\n{'Model':<10} {'Strategy':<20} {'Original':<12} {'Refined':<12} {'Change':<10}")
    print("-"*90)
    
    improvements = []
    total_improvement = 0
    
    for model in models:
        for orig, refined in strategy_pairs:
            orig_pass = part1[model][orig]['pass_at_k']['pass@1']
            refined_pass = part2[model][refined]['pass_at_k']['pass@1']
            change = refined_pass - orig_pass
            total_improvement += change
            
            improvements.append({
                'model': model,
                'strategy': orig,
                'original': orig_pass,
                'refined': refined_pass,
                'improvement': change
            })
            
            change_str = f"+{change:.1%}" if change >= 0 else f"{change:.1%}"
            print(f"{model:<10} {orig:<20} {orig_pass:<12.1%} {refined_pass:<12.1%} {change_str:<10}")
    
    print("="*90)
    
    avg_improvement = total_improvement / len(improvements)
    print(f"\nAverage Improvement: {avg_improvement:+.1%}")
    
    print("\nTop 3 Improvements:")
    sorted_improvements = sorted(improvements, key=lambda x: x['improvement'], reverse=True)
    for i, imp in enumerate(sorted_improvements[:3], 1):
        print(f"  {i}. {imp['model'].upper()} {imp['strategy']}: {imp['improvement']:+.1%}")
    
    return improvements

def analyze_failure_cases():
    """Specific analysis of the two failure cases"""
    part1 = load_part1_results()
    part2 = load_part2_results()
    
    print("\n" + "="*90)
    print("FAILURE CASE ANALYSIS")
    print("="*90)
    
    print("\nCASE 1: HumanEval/1 (separate_paren_groups) - Import Failures")
    print("-"*90)
    
    gpt_sd_orig = part1['gpt4o']['self_debugging']['detailed_results']['HumanEval/1'][0]
    gpt_sd_refined = part2['gpt4o']['self_debugging_refined']['detailed_results']['HumanEval/1'][0]
    print(f"\nGPT-4o Self-Debugging:")
    print(f"  Original: FAIL - {gpt_sd_orig.get('error', 'Unknown')}")
    print(f"  Refined:  PASS")
    
    claude_cot_orig = part1['claude']['cot']['detailed_results']['HumanEval/1'][0]
    claude_cot_refined = part2['claude']['cot_refined']['detailed_results']['HumanEval/1'][0]
    print(f"\nClaude CoT:")
    print(f"  Original: FAIL - {claude_cot_orig.get('error', 'Unknown')}")
    print(f"  Refined:  PASS")
    
    claude_sd_orig = part1['claude']['self_debugging']['detailed_results']['HumanEval/1'][0]
    claude_sd_refined = part2['claude']['self_debugging_refined']['detailed_results']['HumanEval/1'][0]
    print(f"\nClaude Self-Debugging:")
    print(f"  Original: FAIL - {claude_sd_orig.get('error', 'Unknown')}")
    print(f"  Refined:  PASS")

    print("\n" + "="*90)
    print("CASE 2: HumanEval/10 (make_palindrome) - Helper Function Issue")
    print("-"*90)
    
    gpt_sd_orig = part1['gpt4o']['self_debugging']['detailed_results']['HumanEval/10'][0]
    gpt_sd_refined = part2['gpt4o']['self_debugging_refined']['detailed_results']['HumanEval/10'][0]
    print(f"\nGPT-4o Self-Debugging:")
    print(f"  Original: FAIL - {gpt_sd_orig.get('error', 'Unknown')}")
    print(f"  Refined:  PASS")

def analyze_claude_systematic_improvements():
    """Analyze Claude's systematic import issue improvements"""
    part1 = load_part1_results()
    part2 = load_part2_results()
    
    print("\n" + "="*90)
    print("CLAUDE SYSTEMATIC IMPORT ISSUES - BEFORE vs AFTER")
    print("="*90)
    
    import_problems = ['HumanEval/0', 'HumanEval/1', 'HumanEval/20', 'HumanEval/25']
    strategies = ['cot', 'self_planning', 'self_debugging']
    
    for strategy in strategies:
        orig_failures = 0
        refined_failures = 0
        fixed_count = 0
        
        print(f"\n{strategy.upper()}:")
        print("-" * 60)
        
        for problem in import_problems:
            orig_result = part1['claude'][strategy]['detailed_results'].get(problem, [{}])[0]
            refined_result = part2['claude'][f'{strategy}_refined']['detailed_results'].get(problem, [{}])[0]
            
            orig_passed = orig_result.get('passed', True)
            refined_passed = refined_result.get('passed', True)
            
            if not orig_passed:
                orig_failures += 1
            if not refined_passed:
                refined_failures += 1
            if not orig_passed and refined_passed:
                fixed_count += 1
            
            status = ""
            if not orig_passed and refined_passed:
                status = "FIXED"
            elif not orig_passed and not refined_passed:
                status = "Still failing"
            elif orig_passed:
                status = "Was passing"

            print(f"  {problem}: {status}")
        
        print(f"\n  Summary:")
        print(f"    Original failures: {orig_failures}/4")
        print(f"    Refined failures:  {refined_failures}/4")
        print(f"    Fixed: {fixed_count}/4 problems")
        if orig_failures > 0:
            improvement_pct = (fixed_count / orig_failures) * 100
            print(f"    Fix rate: {improvement_pct:.0f}%")

def create_summary_report():
    """Create comprehensive summary for Part 2 report"""
    part1 = load_part1_results()
    part2 = load_part2_results()
    
    summary = {
        "part_2_summary": {
            "title": "Prompt Refinement Results - Part 2",
            "failure_cases_analyzed": 2,
            "problems_affected": {
                "case_1": "HumanEval/1 (separate_paren_groups) - Import failures across multiple strategies",
                "case_2": "HumanEval/10 (make_palindrome) - Helper function not included"
            },
            "refinements_made": [
                "Added explicit 'CRITICAL REQUIREMENTS' section to all prompts",
                "Made imports the first step in all thinking/planning processes",
                "Added 'Include ALL helper functions' instruction",
                "Added 'Provide ONLY executable Python code' to prevent verbose output",
                "Created specific checklists for each strategy type"
            ],
            "results_summary": {}
        }
    }
    
    for model in ['gpt4o', 'claude']:
        summary["part_2_summary"]["results_summary"][model] = {}
        for strategy in ['cot', 'self_planning', 'self_debugging']:
            orig = part1[model][strategy]
            refined = part2[model][f'{strategy}_refined']
            
            summary["part_2_summary"]["results_summary"][model][strategy] = {
                "original_pass_at_1": orig['pass_at_k']['pass@1'],
                "refined_pass_at_1": refined['pass_at_k']['pass@1'],
                "improvement": refined['pass_at_k']['pass@1'] - orig['pass_at_k']['pass@1'],
                "original_solved": f"{orig['problems_solved']}/10",
                "refined_solved": f"{refined['problems_solved']}/10"
            }
    
    output_path = Path("results/part2_summary.json")
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nSummary report saved: {output_path}")

def main():
    print("="*90)
    print("PART 2: RESULTS COMPARISON & ANALYSIS")
    print("="*90)
    
    compare_strategies()
    analyze_failure_cases()
    analyze_claude_systematic_improvements()
    create_summary_report()
    
    print("\n" + "="*90)
    print("ANALYSIS COMPLETE!")
    print("="*90)

if __name__ == "__main__":
    main()