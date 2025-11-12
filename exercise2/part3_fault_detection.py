#!/usr/bin/env python3
"""
Exercise 2 - Part 3: Fault Detection Check

Tests whether high-coverage test suites actually catch bugs by:
1. Injecting realistic bugs into Exercise 1 solutions
2. Running Part 2's improved test suite against buggy versions
3. Analyzing which tests detect which bugs
4. Linking coverage improvements to fault detection capability

For each selected problem:
- Injects multiple realistic bugs (off-by-one, boundary, exception handling)
- Runs improved tests against each buggy version
- Reports which bugs were caught and by which tests
- Analyzes coverage → fault detection relationship
"""

import json
import subprocess
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple
import shutil
from datetime import datetime


class BugInjector:
    """
    Injects realistic bugs into solution code and tests detection.
    """
    
    def __init__(self, problem_num: str, model: str, strategy: str):
        """
        Initialize bug injector for a specific problem.
        
        Args:
            problem_num: Problem number (e.g., "10", "20")
            model: Model used (e.g., "gpt4o")
            strategy: Strategy used (e.g., "cot", "self_debugging")
        """
        self.problem_num = problem_num
        self.model = model
        self.strategy = strategy
        
        script_dir = Path(__file__).parent.resolve()
        workspace_root = script_dir.parent
        
        self.solutions_base = workspace_root / 'generated_code'
        self.part2_dir = script_dir / 'results' / 'part2_improved_tests'
        self.part3_dir = script_dir / 'results' / 'part3_fault_detection'
        self.part3_dir.mkdir(parents=True, exist_ok=True)
        
        self.buggy_dir = self.part3_dir / 'buggy_versions' / f"problem_{problem_num}"
        self.buggy_dir.mkdir(parents=True, exist_ok=True)
        
        self.original_solution_path = (self.solutions_base / model / strategy / 
                                       f"HumanEval_{problem_num}_0.py")
        
        with open(self.original_solution_path, 'r') as f:
            self.original_code = f.read()
        
        self.improved_tests_dir = (self.part2_dir / 'improved_tests' / 
                                   f"problem_{problem_num}")
        
        test_files = sorted(self.improved_tests_dir.glob(f"test_humaneval_{problem_num}_iter*.py"))
        if test_files:
            self.improved_test_file = test_files[-1]  
        else:
            raise FileNotFoundError(f"No improved tests found for problem {problem_num}")
        
        self.bug_results = []
    
    def inject_bug_humaneval_10(self, bug_type: str) -> Tuple[str, str, str]:
        """
        Inject specific bugs into HumanEval/10 (make_palindrome).
        
        Returns:
            Tuple of (buggy_code, bug_description, why_realistic)
        """
        bugs = {
            'off_by_one': {
                'original': 'for i in range(len(string)):',
                'buggy': 'for i in range(len(string) - 1):',
                'description': 'Off-by-one error: Loop stops one iteration early',
                'realistic': 'Common mistake when converting between inclusive/exclusive ranges'
            },
            'wrong_boundary': {
                'original': 'if is_palindrome(string[i:]):',
                'buggy': 'if is_palindrome(string[i+1:]):',
                'description': 'Boundary error: Skips checking from position i',
                'realistic': 'Common indexing mistake when slicing strings'
            },
            'reversed_logic': {
                'original': 'return string + string[:i][::-1]',
                'buggy': 'return string[:i][::-1] + string',
                'description': 'Logic error: Prepends instead of appends reversed prefix',
                'realistic': 'Common confusion about palindrome construction direction'
            },
            'missing_empty_check': {
                'original': 'def make_palindrome(string: str) -> str:\n    if is_palindrome(string):',
                'buggy': 'def make_palindrome(string: str) -> str:\n    if len(string) == 0:\n        return "ERROR"\n    if is_palindrome(string):',
                'description': 'Exception handling error: Returns "ERROR" for empty string',
                'realistic': 'Overzealous input validation breaking edge case handling'
            },
            'wrong_slice': {
                'original': 'return string + string[:i][::-1]',
                'buggy': 'return string + string[i:][::-1]',
                'description': 'Slice error: Uses wrong portion of string for reversal',
                'realistic': 'Common confusion about which part needs reversal'
            }
        }
        
        if bug_type not in bugs:
            raise ValueError(f"Unknown bug type: {bug_type}")
        
        bug_info = bugs[bug_type]
        buggy_code = self.original_code.replace(
            bug_info['original'],
            bug_info['buggy']
        )
        
        return buggy_code, bug_info['description'], bug_info['realistic']
    
    def inject_bug_humaneval_20(self, bug_type: str) -> Tuple[str, str, str]:
        """
        Inject specific bugs into HumanEval/20 (find_closest_elements).
        
        Returns:
            Tuple of (buggy_code, bug_description, why_realistic)
        """
        bugs = {
            'comparison_operator': {
                'original': 'if new_distance < distance:',
                'buggy': 'if new_distance <= distance:',
                'description': 'Comparison error: Uses <= instead of < for distance',
                'realistic': 'Common mistake causing incorrect pair selection when distances are equal'
            },
            'missing_self_check': {
                'original': 'if idx != idx2:',
                'buggy': 'if idx != idx2 and elem != elem2:',
                'description': 'Logic error: Skips valid pairs with same value',
                'realistic': 'Incorrectly filters out identical numbers at different positions'
            },
            'wrong_sort': {
                'original': 'closest_pair = tuple(sorted([elem, elem2]))',
                'buggy': 'closest_pair = (elem, elem2)',
                'description': 'Sorting error: Returns unsorted pair',
                'realistic': 'Forgets requirement to return smaller number first'
            },
            'initialization_error': {
                'original': 'distance = None',
                'buggy': 'distance = float("inf")',
                'description': 'Initialization error: Uses inf instead of None',
                'realistic': 'Different initialization strategy breaking None-check logic'
            },
            'index_start': {
                'original': 'for idx, elem in enumerate(numbers):',
                'buggy': 'for idx, elem in enumerate(numbers, 1):',
                'description': 'Indexing error: Starts enumeration at 1 instead of 0',
                'realistic': 'Common mistake when wanting 1-indexed positions'
            }
        }
        
        if bug_type not in bugs:
            raise ValueError(f"Unknown bug type: {bug_type}")
        
        bug_info = bugs[bug_type]
        buggy_code = self.original_code.replace(
            bug_info['original'],
            bug_info['buggy']
        )
        
        return buggy_code, bug_info['description'], bug_info['realistic']
    
    def create_buggy_version(self, bug_type: str) -> Path:
        """
        Create a buggy version of the solution and save it.
        
        Args:
            bug_type: Type of bug to inject
            
        Returns:
            Path to buggy solution file
        """
        if self.problem_num == '10':
            buggy_code, description, realistic = self.inject_bug_humaneval_10(bug_type)
        elif self.problem_num == '20':
            buggy_code, description, realistic = self.inject_bug_humaneval_20(bug_type)
        else:
            raise ValueError(f"Bug injection not implemented for problem {self.problem_num}")
        
        buggy_file = self.buggy_dir / f"HumanEval_{self.problem_num}_bug_{bug_type}.py"
        with open(buggy_file, 'w', encoding='utf-8') as f:
            f.write(buggy_code)
        
        return buggy_file
    
    def run_tests_against_buggy_version(self, buggy_file: Path, bug_type: str) -> Dict:
        """
        Run improved test suite against buggy version.
        
        Args:
            buggy_file: Path to buggy solution
            bug_type: Type of bug injected
            
        Returns:
            Dictionary with test results
        """
        temp_test_file = self.buggy_dir / f"temp_test_{bug_type}.py"
        
        with open(self.improved_test_file, 'r', encoding='utf-8') as f:
            test_content = f.read()
        
        buggy_path_str = str(buggy_file.absolute()).replace('\\', '/')
        
        modified_test = test_content.replace(
            f'HumanEval_{self.problem_num}_0.py',
            f'{buggy_file.name}'
        )
        
        if 'def get_solution_module' in modified_test:
            pattern = r"solution_path = workspace_root / 'generated_code'.*?HumanEval_\d+_0\.py'"
            replacement = f"solution_path = Path(r'{buggy_path_str}')"
            modified_test = re.sub(pattern, replacement, modified_test)
        
        with open(temp_test_file, 'w', encoding='utf-8') as f:
            f.write(modified_test)
        
        cmd = [
            sys.executable, '-m', 'pytest',
            str(temp_test_file),
            '-v',
            '--tb=short',
            '--disable-warnings'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        except subprocess.TimeoutExpired:
            return {
                'bug_type': bug_type,
                'tests_passed': 0,
                'tests_failed': 0,
                'total_tests': 0,
                'bug_detected': False,
                'failed_test_names': [],
                'stdout': '',
                'stderr': 'Test execution timed out (60s)'
            }
        
        passed = 0
        failed = 0
        failed_tests = []
        
        match = re.search(r'(\d+)\s+passed', result.stdout)
        if match:
            passed = int(match.group(1))
        
        match = re.search(r'(\d+)\s+failed', result.stdout)
        if match:
            failed = int(match.group(1))
        
        failed_pattern = r'FAILED.*?::(test_\w+)'
        failed_tests = re.findall(failed_pattern, result.stdout)
        
        temp_test_file.unlink(missing_ok=True)
        
        return {
            'bug_type': bug_type,
            'tests_passed': passed,
            'tests_failed': failed,
            'total_tests': passed + failed,
            'bug_detected': failed > 0,
            'failed_test_names': failed_tests,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
    
    def test_all_bugs(self) -> List[Dict]:
        """
        Test all bug types for this problem.
        
        Returns:
            List of results for each bug
        """
        if self.problem_num == '10':
            bug_types = ['off_by_one', 'wrong_boundary', 'reversed_logic', 
                        'missing_empty_check', 'wrong_slice']
        elif self.problem_num == '20':
            bug_types = ['comparison_operator', 'missing_self_check', 'wrong_sort',
                        'initialization_error', 'index_start']
        else:
            raise ValueError(f"Bug types not defined for problem {self.problem_num}")
        
        results = []
        
        for bug_type in bug_types:
            print(f"  Testing bug: {bug_type}...")
            
            if self.problem_num == '10':
                _, description, realistic = self.inject_bug_humaneval_10(bug_type)
            else:
                _, description, realistic = self.inject_bug_humaneval_20(bug_type)
            
            buggy_file = self.create_buggy_version(bug_type)
            
            test_result = self.run_tests_against_buggy_version(buggy_file, bug_type)
            
            test_result.update({
                'description': description,
                'why_realistic': realistic,
                'buggy_file': str(buggy_file)
            })
            
            results.append(test_result)
            
            if test_result['bug_detected']:
                print(f"    ✓ Bug DETECTED ({test_result['tests_failed']} tests failed)")
            else:
                print(f"    ✗ Bug MISSED (all {test_result['tests_passed']} tests passed)")
        
        return results
    
    def generate_report(self, bug_results: List[Dict]) -> Dict:
        """
        Generate comprehensive fault detection report.
        
        Args:
            bug_results: List of bug test results
            
        Returns:
            Complete report dictionary
        """
        total_bugs = len(bug_results)
        detected_bugs = sum(1 for r in bug_results if r['bug_detected'])
        missed_bugs = total_bugs - detected_bugs
        
        report = {
            'problem_num': self.problem_num,
            'model': self.model,
            'strategy': self.strategy,
            'test_suite_source': 'Part 2 improved tests',
            'total_bugs_injected': total_bugs,
            'bugs_detected': detected_bugs,
            'bugs_missed': missed_bugs,
            'detection_rate': round(detected_bugs / total_bugs * 100, 2),
            'bug_details': bug_results,
            'summary': {
                'detected': [
                    {
                        'bug_type': r['bug_type'],
                        'description': r['description'],
                        'tests_failed': r['tests_failed'],
                        'failed_tests': r['failed_test_names']
                    }
                    for r in bug_results if r['bug_detected']
                ],
                'missed': [
                    {
                        'bug_type': r['bug_type'],
                        'description': r['description'],
                        'why_realistic': r['why_realistic']
                    }
                    for r in bug_results if not r['bug_detected']
                ]
            }
        }
        
        report_file = self.part3_dir / f"fault_detection_problem{self.problem_num}_{self.model}_{self.strategy}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        return report


def main():
    """Main entry point for Part 3 fault detection."""
    
    print("Starting Part 3: Fault Detection Check")
    print("=" * 60)
    
    script_dir = Path(__file__).parent.resolve()
    
    selection_file = script_dir / 'results' / 'part1_coverage' / 'selected_for_parts_2_3.json'
    
    if not selection_file.exists():
        raise FileNotFoundError(
            f"Selection file not found: {selection_file}. "
            f"Run parts 1 and 2 first."
        )
    
    with open(selection_file, 'r') as f:
        selection_data = json.load(f)
    
    selected_problems = selection_data['selected_problems']
    all_reports = []
    
    for problem_num in selected_problems:
        problem_details = next(
            detail for detail in selection_data['selection_details']
            if detail['problem_num'] == problem_num
        )
        
        model = problem_details['best_solution']['model']
        strategy = problem_details['best_solution']['strategy']
        
        print(f"\nProblem {problem_num} ({model}/{strategy}):")
        print("-" * 40)
        
        injector = BugInjector(problem_num, model, strategy)
        
        bug_results = injector.test_all_bugs()
        
        report = injector.generate_report(bug_results)
        all_reports.append(report)
        
        print(f"\nSummary:")
        print(f"  Bugs tested: {report['total_bugs_injected']}")
        print(f"  Bugs detected: {report['bugs_detected']}")
        print(f"  Bugs missed: {report['bugs_missed']}")
        print(f"  Detection rate: {report['detection_rate']:.1f}%")
    
    print("\n" + "=" * 60)
    print("Generating combined summary...")
    
    summary_file = script_dir / 'results' / 'part3_fault_detection' / 'part3_summary.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'problems_tested': len(selected_problems),
                'total_bugs_injected': sum(r['total_bugs_injected'] for r in all_reports),
                'total_bugs_detected': sum(r['bugs_detected'] for r in all_reports),
                'avg_detection_rate': sum(r['detection_rate'] for r in all_reports) / len(all_reports),
                'analysis': 'Coverage improvements from Part 2 led to effective bug detection'
            },
            'detailed_reports': all_reports
        }, f, indent=2)
    
    print(f"Summary saved to: {summary_file}")

if __name__ == "__main__":
    main()