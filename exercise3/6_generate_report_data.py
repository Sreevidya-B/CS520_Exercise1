"""
Exercise 3 - Step 6: Generate Report Data
Compiles all data for the final report.
"""

import json
from pathlib import Path


def compile_part1_data():
    """Compile Part 1 specification accuracy data."""
    script_dir = Path(__file__).parent
    eval_path = script_dir / "specifications" / "evaluation_results.json"
    
    if not eval_path.exists():
        raise FileNotFoundError(f"Run 3_evaluate_specifications.py first: {eval_path}")
    
    with open(eval_path, 'r', encoding='utf-8') as f:
        eval_data = json.load(f)
    
    part1_data = {
        'accuracy_summary': {},
        'incorrect_specs': []
    }
    
    for key, data in eval_data.items():
        part1_data['accuracy_summary'][key] = {
            'problem': data['problem_num'],
            'model': data['model'],
            'total': data['accuracy']['total'],
            'correct': data['accuracy']['correct'],
            'incorrect': data['accuracy']['incorrect'],
            'accuracy_rate': data['accuracy']['accuracy_rate']
        }
        
        for eval_result in data['evaluations']:
            if not eval_result['is_correct']:
                part1_data['incorrect_specs'].append({
                    'problem': data['problem_num'],
                    'model': data['model'],
                    'spec_number': eval_result['spec_number'],
                    'original': eval_result['original_assertion'],
                    'issues': eval_result['issues'],
                    'corrected': eval_result['corrected_assertion'],
                    'explanation': eval_result['explanation']
                })
    
    return part1_data


def compile_part2_data():
    """Compile Part 2 coverage comparison data."""
    script_dir = Path(__file__).parent
    coverage_path = script_dir / "coverage_comparison.json"
    
    if not coverage_path.exists():
        raise FileNotFoundError(f"Run 5_run_coverage_analysis.py first: {coverage_path}")
    
    with open(coverage_path, 'r', encoding='utf-8') as f:
        coverage_data = json.load(f)
    
    part2_data = {'coverage_comparisons': []}
    
    for key, data in coverage_data.items():
        comp = data['comparison']
        part2_data['coverage_comparisons'].append({
            'problem': comp['problem_num'],
            'model': comp['model'],
            'baseline_stmt': comp['baseline_stmt_cov'],
            'improved_stmt': comp['improved_stmt_cov'],
            'stmt_change': comp['stmt_change'],
            'baseline_branch': comp['baseline_branch_cov'],
            'improved_branch': comp['improved_branch_cov'],
            'branch_change': comp['branch_change']
        })
    
    return part2_data


def generate_markdown_report():
    """Generate report template with data tables."""
    part1 = compile_part1_data()
    part2 = compile_part2_data()
    
    md_lines = [
        "# Exercise 3: Specification-Guided Test Improvement",
        "",
        "---",
        "",
        "## Part 1: Generate, Evaluate and Refine Specifications - Specification Accuracy",
        "",
        "### Summary",
        "",
        "| Problem | Model  | Correct | Total | Accuracy |",
        "|---------|--------|---------|-------|----------|"
    ]
    
    for key, acc in sorted(part1['accuracy_summary'].items()):
        md_lines.append(
            f"|    {acc['problem']:2}   | {acc['model']:6} |    {acc['correct']}    |   {acc['total']}   |   {acc['accuracy_rate']:.1f}%  |"
        )
    
    total_correct = sum(acc['correct'] for acc in part1['accuracy_summary'].values())
    total_specs = sum(acc['total'] for acc in part1['accuracy_summary'].values())
    overall_accuracy = (total_correct / total_specs * 100) if total_specs > 0 else 0
    
    md_lines.extend([
        f"| **Overall** |        | ** {total_correct:2} ** | **{total_specs:2}** | ** {overall_accuracy:5.1f}%** |",
        "",
        "---",
        "",
        "## Part 2: Use Specifications to Guide Test Improvement - Coverage Comparison",
        "",
        "### Statement and Branch Coverage",
        "",
        "| Problem | Model | Baseline Stmt | Improved Stmt | Change | Baseline Branch | Improved Branch | Change  |",
        "|---------|-------|---------------|---------------|--------|-----------------|-----------------|---------|"
    ])
    
    for comp in sorted(part2['coverage_comparisons'], key=lambda x: (x['problem'], x['model'])):
        stmt_change_str = f"{comp['stmt_change']:+.2f}%"
        branch_change_str = f"{comp['branch_change']:+.2f}%"
        
        md_lines.append(
            f"|   {comp['problem']:2}    |  {comp['model']:6} |       {comp['baseline_stmt']:5.2f}% |       {comp['improved_stmt']:5.2f}% | {stmt_change_str:>6} |          {comp['baseline_branch']:5.2f}% |          {comp['improved_branch']:5.2f}% | {branch_change_str:>7} |"
        )
    
    script_dir = Path(__file__).parent
    output_path = script_dir / "REPORT_TEMPLATE.md"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))


if __name__ == "__main__":
    generate_markdown_report()