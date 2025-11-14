#!/usr/bin/env python3
"""
Exercise 2 - Part 1: Baseline Coverage Analysis

Analyzes code coverage for Exercise 1 solutions using pytest-cov.
Tests only baseline strategies (cot, self_planning, self_debugging).

Outputs:
- coverage_table.csv: Summary table with line/branch coverage
- detailed_results.json: Full coverage data for all solutions
- coverage_summary.json: Aggregate statistics
- selected_for_parts_2_3.json: 2 problems selected for Parts 2-3

Selection Metric: |test% - branch%| × test% (largest gaps)
"""

import json
import subprocess
import sys
import csv
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re

class CoverageAnalyzer:
    
    MODELS = ['gpt4o', 'claude']
    STRATEGIES = ['cot', 'self_planning', 'self_debugging']
    MIN_TEST_PASS_THRESHOLD = 80
    
    def __init__(self):
        self.results = []
        
        script_dir = Path(__file__).parent.resolve()
        workspace_root = script_dir.parent
        
        self.solutions_base = workspace_root / 'generated_code'
        self.data_dir = workspace_root / 'data'
        self.tests_dir = script_dir / 'tests' / 'original'
        self.exercise2_dir = script_dir / 'results' / 'part1_coverage'
        
        self.coverage_reports_dir = self.exercise2_dir / 'coverage_reports'
        self.html_reports_dir = self.exercise2_dir / 'htmlcov'
        
        self.exercise2_dir.mkdir(parents=True, exist_ok=True)
        self.coverage_reports_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.solutions_base.exists():
            raise FileNotFoundError(f"Solutions not found: {self.solutions_base}")
        if not (self.data_dir / 'selected_problems.jsonl').exists():
            raise FileNotFoundError(f"Problems file not found: {self.data_dir / 'selected_problems.jsonl'}")
    
    def setup_test_suites(self):
        """Create pytest test suites from HumanEval tests"""
        self.tests_dir.mkdir(parents=True, exist_ok=True)
        
        problems = []
        with open(self.data_dir / 'selected_problems.jsonl', 'r') as f:
            for line in f:
                problems.append(json.loads(line))
        
        for problem in problems:
            self._create_test_suite(problem)
        
        self._create_conftest()
    
    def _create_test_suite(self, problem: Dict):
        """Create pytest test file with HumanEval tests"""
        task_id = problem['task_id']
        problem_num = task_id.split('/')[-1]
        entry_point = problem['entry_point']
        test_code_raw = problem['test']
        
        test_file = self.tests_dir / f"test_humaneval_{problem_num}.py"
        workspace_root_abs = str(Path(__file__).parent.parent.absolute())
        
        test_code = f'''"""
Test suite for {task_id} - {entry_point}
"""
import pytest
from pathlib import Path

def get_solution_module(model, strategy, problem_num):
    workspace_root = Path(r"{workspace_root_abs}")
    solution_path = workspace_root / 'generated_code' / model / strategy / f'HumanEval_{{problem_num}}_0.py'
    
    if not solution_path.exists():
        raise FileNotFoundError(f"Solution not found: {{solution_path}}")
    
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        f"solution_{{model}}_{{strategy}}_{{problem_num}}", 
        solution_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

{test_code_raw}

@pytest.fixture
def solution_function(request):
    model = request.config.getoption("--model", default="gpt4o")
    strategy = request.config.getoption("--strategy", default="cot")
    module = get_solution_module(model, strategy, "{problem_num}")
    return getattr(module, "{entry_point}")

def test_{entry_point}_humaneval(solution_function):
    check(solution_function)
'''
        
        with open(test_file, 'w') as f:
            f.write(test_code)
    
    def _create_conftest(self):
        """Create pytest configuration"""
        conftest_path = self.tests_dir / 'conftest.py'
        
        conftest_code = '''"""Pytest configuration"""
import pytest

def pytest_addoption(parser):
    parser.addoption("--model", action="store", default="gpt4o",
                     help="Model to test (gpt4o/claude)")
    parser.addoption("--strategy", action="store", default="cot",
                     help="Strategy to test")

@pytest.fixture
def model(request):
    return request.config.getoption("--model")

@pytest.fixture
def strategy(request):
    return request.config.getoption("--strategy")
'''
        
        with open(conftest_path, 'w') as f:
            f.write(conftest_code)
    
    def run_coverage_for_solution(self, problem_num: str, model: str, 
                               strategy: str) -> Optional[Dict]:
        """Run coverage analysis for a specific solution"""
        
        solution_file = self.solutions_base / model / strategy / f"HumanEval_{problem_num}_0.py"
        
        if not solution_file.exists():
            return None
        
        test_file = self.tests_dir / f"test_humaneval_{problem_num}.py"
        if not test_file.exists():
            return None
        
        json_output = self.coverage_reports_dir / f"coverage_{problem_num}_{model}_{strategy}.json"
        xml_output = self.coverage_reports_dir / f"coverage_{problem_num}_{model}_{strategy}.xml"
        
        html_output = self.exercise2_dir / "htmlcov" / model / strategy / problem_num
        html_output.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            sys.executable, '-m', 'pytest',
            str(test_file),
            f'--model={model}',
            f'--strategy={strategy}',
            f'--cov={self.solutions_base / model / strategy}',
            '--cov-branch',
            '--cov-report=term-missing',
            f'--cov-report=json:{json_output}',
            f'--cov-report=xml:{xml_output}',
            f'--cov-report=html:{html_output}',
            '--tb=short',
            '-v',
            '--disable-warnings'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        except subprocess.TimeoutExpired:
            return None
        except (OSError, ValueError):
            return None
        
        tests_passed, tests_failed = self._count_tests(result.stdout)
        total_tests = tests_passed + tests_failed
        
        if total_tests == 0:
            return None
        
        test_pass_percent = (tests_passed / total_tests * 100)

        if not json_output.exists():
            return None
        
        try:
            with open(json_output, 'r') as f:
                coverage_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
        
        file_coverage = self._extract_file_coverage(coverage_data, solution_file)
        
        if file_coverage is None:
            return None
        
        return {
            'problem_num': problem_num,
            'model': model,
            'strategy': strategy,
            'tests_passed': tests_passed,
            'tests_failed': tests_failed,
            'test_pass_percent': round(test_pass_percent, 2),
            'line_coverage': file_coverage['line_percent'],
            'branch_coverage': file_coverage['branch_percent'],
            'lines_covered': file_coverage['lines_covered'],
            'lines_total': file_coverage['lines_total'],
            'branches_covered': file_coverage['branches_covered'],
            'branches_total': file_coverage['branches_total'],
            'interpretation': self._interpret_coverage(
                problem_num,
                file_coverage['line_percent'],
                file_coverage['branch_percent'],
                file_coverage['branches_total'],
                tests_passed > 0
            ),
            'json_report': str(json_output),
            'xml_report': str(xml_output),
            'html_report': str(html_output / 'index.html')
        }
    
    def _count_tests(self, stdout: str) -> Tuple[int, int]:
        """Count test results with validation"""
        passed = 0
        failed = 0
        
        match = re.search(r'(\d+)\s+passed.*?(\d+)\s+failed', stdout, re.DOTALL)
        if match:
            passed = int(match.group(1))
            failed = int(match.group(2))
        else:
            match = re.search(r'(\d+)\s+passed', stdout)
            if match:
                passed = int(match.group(1))
            
            match = re.search(r'(\d+)\s+failed', stdout)
            if match:
                failed = int(match.group(1))
        
        if passed == 0 and failed == 0:
            if 'PASSED' in stdout:
                passed = 1
            elif 'FAILED' in stdout:
                failed = 1
        
        return passed, failed
    
    def _extract_file_coverage(self, coverage_data: Dict, code_file: Path) -> Optional[Dict]:
        """Extract coverage data with validation"""
        
        for file_path, file_data in coverage_data.get('files', {}).items():
            if str(code_file.name) in file_path or str(code_file) in file_path:
                summary = file_data.get('summary', {})
                
                required_fields = ['num_statements', 'covered_lines']
                if not all(field in summary for field in required_fields):
                    return None
                
                num_branches = summary.get('num_branches', 0)
                covered_branches = summary.get('covered_branches', 0)
                branch_percent = round(
                    (covered_branches / num_branches * 100) if num_branches > 0 else 0, 
                    2
                )
                
                if not (0 <= summary.get('percent_covered', -1) <= 100):
                    return None
                
                if num_branches > 0 and not (0 <= branch_percent <= 100):
                    return None
                
                return {
                    'line_percent': round(summary.get('percent_covered', 0), 2),
                    'branch_percent': branch_percent,
                    'lines_covered': summary.get('covered_lines', 0),
                    'lines_total': summary.get('num_statements', 0),
                    'branches_covered': covered_branches,
                    'branches_total': num_branches
                }
        
        totals = coverage_data.get('totals', {})
        if not totals:
            return None
        
        num_branches = totals.get('num_branches', 0)
        covered_branches = totals.get('covered_branches', 0)
        
        return {
            'line_percent': round(totals.get('percent_covered', 0), 2),
            'branch_percent': round(
                (covered_branches / num_branches * 100) if num_branches > 0 else 0, 
                2
            ),
            'lines_covered': totals.get('covered_lines', 0),
            'lines_total': totals.get('num_statements', 0),
            'branches_covered': covered_branches,
            'branches_total': num_branches
        }
    
    def _interpret_coverage(self, problem_num: str, line_percent: float, 
                           branch_percent: float, total_branches: int,
                           tests_passed: bool) -> str:
        """Context-specific one-line interpretation"""
        if not tests_passed:
            return "Tests failed - solution has runtime errors"
        
        if total_branches == 0:
            return f"No branches - linear code with {line_percent:.0f}% line coverage"
        
        if branch_percent == 0:
            return "Zero branch coverage - no conditional paths tested"
        elif branch_percent < 40:
            untested = total_branches - int(total_branches * branch_percent/100)
            return f"Low branch coverage ({branch_percent:.0f}%) - {untested} of {total_branches} branches untested"
        elif branch_percent < 70:
            return f"Moderate coverage ({branch_percent:.0f}%) - some edge cases likely missed"
        elif branch_percent < 90:
            return f"Good coverage ({branch_percent:.0f}%) - most paths tested"
        elif branch_percent < 100:
            untested = total_branches - int(total_branches * branch_percent/100)
            return f"High coverage ({branch_percent:.0f}%) - {untested} untested branches remaining"
        else:
            return f"Complete coverage (100%) - all {total_branches} branches tested"
    
    def analyze_all_solutions(self):
        """Test all solutions from Exercise 1 - Baseline (Part 1 strategies)"""
        
        problem_nums = []
        with open(self.data_dir / 'selected_problems.jsonl', 'r') as f:
            for line in f:
                problem = json.loads(line)
                problem_nums.append(problem['task_id'].split('/')[-1])
        
        for problem_num in problem_nums:
            for model in self.MODELS:
                for strategy in self.STRATEGIES:
                    result = self.run_coverage_for_solution(problem_num, model, strategy)
                    if result:
                        self.results.append(result)
    
    def generate_table(self):
        """Generate coverage table with summary statistics"""
        
        if not self.results:
            return
        
        csv_file = self.exercise2_dir / 'coverage_table.csv'
        with open(csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'Problem', 'Model', 'Strategy',
                'Tests Passed', 'Tests Failed', 'Test Pass %',
                'Line Coverage %', 'Lines (Covered/Total)',
                'Branch Coverage %', 'Branches (Covered/Total)',
                'Interpretation'
            ])
            writer.writeheader()
            
            for r in sorted(self.results, key=lambda x: (x['problem_num'], x['model'], x['strategy'])):
                writer.writerow({
                    'Problem': f"HumanEval/{r['problem_num']}",
                    'Model': r['model'],
                    'Strategy': r['strategy'],
                    'Tests Passed': r['tests_passed'],
                    'Tests Failed': r['tests_failed'],
                    'Test Pass %': r['test_pass_percent'],
                    'Line Coverage %': r['line_coverage'],
                    'Lines (Covered/Total)': f"{r['lines_covered']}/{r['lines_total']}",
                    'Branch Coverage %': r['branch_coverage'],
                    'Branches (Covered/Total)': f"{r['branches_covered']}/{r['branches_total']}",
                    'Interpretation': r['interpretation']
                })
        
        detailed_file = self.exercise2_dir / 'detailed_results.json'
        with open(detailed_file, 'w') as f:
            json.dump({'results': self.results}, f, indent=2)
        
        summary = {
            'total_solutions_tested': len(self.results),
            'avg_test_pass_percent': round(
                sum(r['test_pass_percent'] for r in self.results) / len(self.results), 2
            ),
            'avg_line_coverage': round(
                sum(r['line_coverage'] for r in self.results) / len(self.results), 2
            ),
            'avg_branch_coverage': round(
                sum(r['branch_coverage'] for r in self.results) / len(self.results), 2
            ),
            'min_branch_coverage': min(r['branch_coverage'] for r in self.results),
            'max_branch_coverage': max(r['branch_coverage'] for r in self.results),
            'solutions_with_full_pass': sum(1 for r in self.results if r['test_pass_percent'] == 100),
            'solutions_with_high_branch': sum(1 for r in self.results if r['branch_coverage'] >= 80)
        }
        
        summary_file = self.exercise2_dir / 'coverage_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
    
    def select_problems_for_parts_2_3(self) -> List[str]:
        """
        Select 2 problems with largest coverage gaps and room for improvement.
        
        Selection criteria:
        1. Test pass % >= 80% (reliable baseline)
        2. Branch coverage > 0% AND < 100% (branches exist to improve)
        3. Largest gap metric: |test% - branch%| × test%
        """
        
        problem_gaps = {}
        
        for r in self.results:
            problem_num = r['problem_num']
            
            # Filter: High test pass rate AND has branches to improve
            if (r['test_pass_percent'] >= self.MIN_TEST_PASS_THRESHOLD and 
                r['branch_coverage'] > 0 and  # Must have branches
                r['branch_coverage'] < 100):   # Must have room for improvement
                
                gap = abs(r['test_pass_percent'] - r['branch_coverage'])
                gap_metric = gap * (r['test_pass_percent'] / 100)
                
                if problem_num not in problem_gaps:
                    problem_gaps[problem_num] = []
                
                problem_gaps[problem_num].append({
                    'model': r['model'],
                    'strategy': r['strategy'],
                    'gap_metric': gap_metric,
                    'test_pass': r['test_pass_percent'],
                    'branch_cov': r['branch_coverage'],
                    'branches_total': r['branches_total'],
                    'branches_uncovered': r['branches_total'] - r['branches_covered']
                })
        
        # Check if we have any valid problems
        if not problem_gaps:
            print("\nWARNING: No problems found with branches to improve!")
            print("Criteria: test_pass >= 80%, 0% < branch_coverage < 100%")
            print("\nFalling back to all problems with branches (even if already 100%)")
            
            # Fallback: Include problems with branches, even at 100%
            for r in self.results:
                problem_num = r['problem_num']
                if r['test_pass_percent'] >= self.MIN_TEST_PASS_THRESHOLD and r['branch_coverage'] > 0:
                    gap = abs(r['test_pass_percent'] - r['branch_coverage'])
                    gap_metric = gap * (r['test_pass_percent'] / 100)
                    
                    if problem_num not in problem_gaps:
                        problem_gaps[problem_num] = []
                    
                    problem_gaps[problem_num].append({
                        'model': r['model'],
                        'strategy': r['strategy'],
                        'gap_metric': gap_metric,
                        'test_pass': r['test_pass_percent'],
                        'branch_cov': r['branch_coverage'],
                        'branches_total': r['branches_total'],
                        'branches_uncovered': r['branches_total'] - r['branches_covered']
                    })
        
        # Select best solution per problem (highest gap)
        problem_max_gaps = {}
        for problem, solutions in problem_gaps.items():
            max_solution = max(solutions, key=lambda x: x['gap_metric'])
            problem_max_gaps[problem] = {
                'max_gap_metric': max_solution['gap_metric'],
                'best_solution': max_solution,
                'all_solutions': solutions
            }
        
        # Sort by gap metric (descending)
        sorted_problems = sorted(
            problem_max_gaps.items(),
            key=lambda x: x[1]['max_gap_metric'],
            reverse=True
        )
        
        # Select top 2
        selected = [sorted_problems[i][0] for i in range(min(2, len(sorted_problems)))]
        
        # Enhanced selection data with reasoning
        selection_data = {
            'selection_method': {
                'formula': '|test% - branch%| × test%',
                'approach': 'Select 2 problems with largest coverage gaps',
                'filter': 'test_pass >= 80% AND 0% < branch_coverage < 100%',
                'rationale': 'Problems must have existing branches with room for improvement'
            },
            'selected_problems': selected,
            'selection_details': [
                {
                    'problem_num': prob,
                    'gap_metric': round(problem_max_gaps[prob]['max_gap_metric'], 2),
                    'best_solution': problem_max_gaps[prob]['best_solution'],
                    'improvement_potential': f"{problem_max_gaps[prob]['best_solution']['branches_uncovered']} uncovered branches",
                    'all_candidate_solutions': len(problem_max_gaps[prob]['all_solutions'])
                }
                for prob in selected
            ],
            'all_candidates_ranked': [
                {
                    'problem_num': prob,
                    'gap_metric': round(data['max_gap_metric'], 2),
                    'test_pass': data['best_solution']['test_pass'],
                    'branch_cov': data['best_solution']['branch_cov'],
                    'model': data['best_solution']['model'],
                    'strategy': data['best_solution']['strategy']
                }
                for prob, data in sorted_problems[:5]  # Top 5 for reference
            ]
        }
        
        selection_file = self.exercise2_dir / 'selected_for_parts_2_3.json'
        with open(selection_file, 'w') as f:
            json.dump(selection_data, f, indent=2)
        
        # Print selection summary
        print("\n" + "="*60)
        print("PROBLEM SELECTION FOR PARTS 2-3")
        print("="*60)
        for detail in selection_data['selection_details']:
            sol = detail['best_solution']
            print(f"\nProblem {detail['problem_num']}:")
            print(f"  Model/Strategy: {sol['model']}/{sol['strategy']}")
            print(f"  Test Pass: {sol['test_pass']:.1f}%")
            print(f"  Branch Coverage: {sol['branch_cov']:.1f}%")
            print(f"  Gap Metric: {detail['gap_metric']:.2f}")
            print(f"  Improvement Potential: {detail['improvement_potential']}")
        print("="*60)
        
        return selected

def main():
    analyzer = CoverageAnalyzer()
    
    try:
        print("Setting up test suites...")
        analyzer.setup_test_suites()
        print(f"Created test files in: {analyzer.tests_dir}")
        
        print("\nRunning coverage analysis...")
        analyzer.analyze_all_solutions()
        
        print(f"\nCollected {len(analyzer.results)} results")
        
        if not analyzer.results:
            print("\nERROR: No coverage results collected!")
            print("\nDebugging information:")
            print(f"  Solutions directory: {analyzer.solutions_base}")
            print(f"  Tests directory: {analyzer.tests_dir}")
            print(f"  Data file: {analyzer.data_dir / 'selected_problems.jsonl'}")
            
            for model in analyzer.MODELS:
                for strategy in analyzer.STRATEGIES:
                    sol_dir = analyzer.solutions_base / model / strategy
                    if sol_dir.exists():
                        count = len(list(sol_dir.glob('*.py')))
                        print(f"  Found {count} solutions in: {model}/{strategy}")
            return
        
        print("Generating reports...")
        analyzer.generate_table()
        selected_problems = analyzer.select_problems_for_parts_2_3()
        
        print(f"\nAnalysis complete. Results: {analyzer.exercise2_dir}")
        print(f"Selected problems for Parts 2-3: {', '.join(selected_problems)}")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()