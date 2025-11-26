"""
Exercise 3 - Step 5: Run Coverage Analysis
Runs pytest with coverage for baseline and spec-guided tests.
"""

import json
import subprocess
import sys
from pathlib import Path


def run_baseline_coverage(problem_num, model, strategy):
    """Run coverage for baseline Exercise 2 tests."""
    script_dir = Path(__file__).parent
    workspace_root = script_dir.parent
    
    test_file = workspace_root / "exercise2" / "tests" / "original" / f"test_humaneval_{problem_num}.py"
    generated_code_dir = workspace_root / "generated_code"
    
    if not test_file.exists():
        return None
    
    coverage_dir = script_dir / "coverage_reports" / f"baseline_problem{problem_num}"
    coverage_dir.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        sys.executable, "-m", "pytest",
        str(test_file),
        f"--model={model}",
        f"--strategy={strategy}",
        f"--cov={generated_code_dir}",
        "--cov-branch",
        f"--cov-report=html:{coverage_dir / 'html'}",
        f"--cov-report=json:{coverage_dir / 'coverage.json'}",
        "-v"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=workspace_root)
        
        coverage_json = coverage_dir / "coverage.json"
        if not coverage_json.exists():
            return None
        
        with open(coverage_json, 'r') as f:
            coverage_data = json.load(f)
        
        target_file = f"HumanEval_{problem_num}_0.py"
        
        for file_path, file_data in coverage_data.get('files', {}).items():
            if target_file in file_path:
                summary = file_data.get('summary', {})
                return {
                    'stmt_coverage': round(summary.get('percent_covered', 0), 2),
                    'branch_coverage': round(
                        (summary.get('covered_branches', 0) / summary.get('num_branches', 1) * 100)
                        if summary.get('num_branches', 0) > 0 else 0,
                        2
                    ),
                    'num_statements': summary.get('num_statements', 0),
                    'covered_statements': summary.get('covered_lines', 0),
                    'num_branches': summary.get('num_branches', 0),
                    'covered_branches': summary.get('covered_branches', 0),
                    'html_report': str(coverage_dir / 'html' / 'index.html')
                }
        
        return None
        
    except (subprocess.TimeoutExpired, Exception):
        return None
    except Exception:
        return None


def run_improved_coverage(problem_num, test_model, strategy):
    """Run coverage for baseline + spec-guided tests."""
    script_dir = Path(__file__).parent
    workspace_root = script_dir.parent
    
    baseline_test = workspace_root / "exercise2" / "tests" / "original" / f"test_humaneval_{problem_num}.py"
    spec_test = script_dir / "tests" / f"test_spec_guided_problem{problem_num}_{test_model}.py"
    generated_code_dir = workspace_root / "generated_code"
    
    if not baseline_test.exists() or not spec_test.exists():
        return None
    
    coverage_dir = script_dir / "coverage_reports" / f"improved_problem{problem_num}_{test_model}"
    coverage_dir.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        sys.executable, "-m", "pytest",
        str(baseline_test),
        str(spec_test),
        f"--model={test_model}",
        f"--strategy={strategy}",
        f"--cov={generated_code_dir}",
        "--cov-branch",
        f"--cov-report=html:{coverage_dir / 'html'}",
        f"--cov-report=json:{coverage_dir / 'coverage.json'}",
        "-v"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=workspace_root)
        
        coverage_json = coverage_dir / "coverage.json"
        if not coverage_json.exists():
            return None
        
        with open(coverage_json, 'r') as f:
            coverage_data = json.load(f)
        
        target_file = f"HumanEval_{problem_num}_0.py"
        
        for file_path, file_data in coverage_data.get('files', {}).items():
            if target_file in file_path:
                summary = file_data.get('summary', {})
                return {
                    'stmt_coverage': round(summary.get('percent_covered', 0), 2),
                    'branch_coverage': round(
                        (summary.get('covered_branches', 0) / summary.get('num_branches', 1) * 100)
                        if summary.get('num_branches', 0) > 0 else 0,
                        2
                    ),
                    'num_statements': summary.get('num_statements', 0),
                    'covered_statements': summary.get('covered_lines', 0),
                    'num_branches': summary.get('num_branches', 0),
                    'covered_branches': summary.get('covered_branches', 0),
                    'html_report': str(coverage_dir / 'html' / 'index.html')
                }
        
        return None
        
    except (subprocess.TimeoutExpired, Exception):
        return None
    except Exception:
        return None


def compare_coverage(baseline, improved, problem_num, model):
    """Compare baseline and improved coverage."""
    if not baseline or not improved:
        return None
    
    return {
        'problem_num': problem_num,
        'model': model,
        'baseline_stmt_cov': baseline['stmt_coverage'],
        'improved_stmt_cov': improved['stmt_coverage'],
        'stmt_change': round(improved['stmt_coverage'] - baseline['stmt_coverage'], 2),
        'baseline_branch_cov': baseline['branch_coverage'],
        'improved_branch_cov': improved['branch_coverage'],
        'branch_change': round(improved['branch_coverage'] - baseline['branch_coverage'], 2),
        'baseline_report': baseline['html_report'],
        'improved_report': improved['html_report']
    }


def run_all_coverage_analysis():
    """Main function to run coverage analysis."""
    script_dir = Path(__file__).parent
    problem_desc_path = script_dir / "problem_descriptions.json"
    
    if not problem_desc_path.exists():
        raise FileNotFoundError(f"Run 1_extract_problem_info.py first: {problem_desc_path}")
    
    with open(problem_desc_path, 'r', encoding='utf-8') as f:
        problem_info = json.load(f)
    
    all_results = {}
    
    for problem_num, info in problem_info.items():
        for test_model in ['gpt4o', 'claude']:
            key = f"problem{problem_num}_{test_model}"
            
            baseline = run_baseline_coverage(problem_num, info['model'], info['strategy'])
            improved = run_improved_coverage(problem_num, test_model, info['strategy'])
            comparison = compare_coverage(baseline, improved, problem_num, test_model)
            
            if comparison:
                all_results[key] = {
                    'baseline': baseline,
                    'improved': improved,
                    'comparison': comparison
                }
    
    output_path = script_dir / "coverage_comparison.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2)


if __name__ == "__main__":
    run_all_coverage_analysis()
