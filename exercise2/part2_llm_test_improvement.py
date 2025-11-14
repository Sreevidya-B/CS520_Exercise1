#!/usr/bin/env python3
"""
Exercise 2 - Part 2: LLM-Assisted Test Generation & Coverage Improvement

Iteratively generates and improves test cases using LLMs to increase code coverage.
Follows convergence criteria: Coverage(i) - Coverage(i-2) <= 3% for 3 consecutive iterations.

For selected problems from Part 1:
- Generates targeted test improvement prompts
- Runs coverage analysis after each iteration
- Accumulates tests (never removes previous tests)
- Tracks convergence and deduplication
- Saves all prompts, tests and coverage data
"""

import json
import subprocess
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import os
import shutil

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import openai
except ImportError:
    openai = None


class TestImprovementAgent:
    """
    Manages iterative test improvement for a single problem using LLM-generated tests.
    
    Attributes:
        CONVERGENCE_THRESHOLD: Maximum allowed improvement (3%)
        CONVERGENCE_WINDOW: Number of iterations to check (3)
        MAX_ITERATIONS: Maximum number of improvement iterations (10)
    """
    
    CONVERGENCE_THRESHOLD = 3.0
    CONVERGENCE_WINDOW = 3
    MAX_ITERATIONS = 10
    
    def __init__(self, problem_num: str, model: str, strategy: str):
        """
        Initialize test improvement agent for a specific problem.
        
        Args:
            problem_num: Problem number (e.g., "2", "16")
            model: Model used in Exercise 1 (e.g., "gpt4o", "claude")
            strategy: Strategy used in Exercise 1 (e.g., "cot", "self_planning")
        """
        self.problem_num = problem_num
        self.model = model
        self.strategy = strategy
        
        script_dir = Path(__file__).parent.resolve()
        workspace_root = script_dir.parent
        
        self.solutions_base = workspace_root / 'generated_code'
        self.data_dir = workspace_root / 'data'
        self.part2_dir = script_dir / 'results' / 'part2_improved_tests'
        self.part2_dir.mkdir(parents=True, exist_ok=True)
        
        self.baseline_tests_dir = script_dir / 'tests' / 'original'
        self.improved_tests_dir = self.part2_dir / 'improved_tests' / f"problem_{problem_num}"
        self.improved_tests_dir.mkdir(parents=True, exist_ok=True)
        
        self.iteration_history = []
        self.prompts_used = []
        self.generated_tests = []
        
        self.problem_data = self._load_problem_data()
        self.solution_code = self._load_solution_code()
        
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        openai_key = os.getenv('OPENAI_API_KEY')
        
        if anthropic and anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
        else:
            self.anthropic_client = None
            
        if openai and openai_key:
            openai.api_key = openai_key
        else:
            if openai:
                openai.api_key = None
    
    def _load_problem_data(self) -> Dict:
        """Load problem specification from selected_problems.jsonl."""
        with open(self.data_dir / 'selected_problems.jsonl', 'r') as f:
            for line in f:
                problem = json.loads(line)
                if problem['task_id'].endswith(f"/{self.problem_num}"):
                    return problem
        raise ValueError(f"Problem {self.problem_num} not found in selected_problems.jsonl")
    
    def _load_solution_code(self) -> str:
        """Load the solution code that will be tested."""
        solution_path = (self.solutions_base / self.model / self.strategy / 
                        f"HumanEval_{self.problem_num}_0.py")
        
        if not solution_path.exists():
            raise FileNotFoundError(f"Solution not found: {solution_path}")
        
        with open(solution_path, 'r') as f:
            return f.read()
    
    def run_baseline_coverage(self) -> Dict:
        """
        Run baseline coverage analysis using original HumanEval tests.
        
        Returns:
            Dictionary containing coverage metrics
        """
        baseline_test = self.baseline_tests_dir / f"test_humaneval_{self.problem_num}.py"
        coverage_data = self._run_coverage_analysis(baseline_test, iteration=0)
        
        self.iteration_history.append({
            'iteration': 0,
            'description': 'Baseline (HumanEval tests only)',
            'line_coverage': coverage_data['line_coverage'],
            'branch_coverage': coverage_data['branch_coverage'],
            'tests_passed': coverage_data['tests_passed'],
            'tests_failed': coverage_data['tests_failed'],
            'num_tests': coverage_data['tests_passed'] + coverage_data['tests_failed'],
            'new_tests_added': 0,
            'prompt': None
        })
        
        return coverage_data
    
    def _run_coverage_analysis(self, test_file: Path, iteration: int) -> Dict:
        """
        Execute pytest with coverage analysis.
        
        Args:
            test_file: Path to test file to run
            iteration: Current iteration number
            
        Returns:
            Dictionary with coverage metrics and test results
        """
        solution_dir = self.solutions_base / self.model / self.strategy
        solution_file = solution_dir / f"HumanEval_{self.problem_num}_0.py"
        
        json_output = self.part2_dir / f"coverage_iter{iteration}_problem{self.problem_num}_{self.model}_{self.strategy}.json"
        
        cmd = [
            sys.executable, '-m', 'pytest',
            str(test_file),
            f'--model={self.model}',
            f'--strategy={self.strategy}',
            f'--cov={solution_dir}',
            '--cov-branch',
            '--cov-report=term-missing',
            f'--cov-report=json:{json_output}',
            '--tb=short',
            '-v',
            '--disable-warnings'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        passed = 0
        failed = 0
        
        match = re.search(r'(\d+)\s+passed', result.stdout)
        if match:
            passed = int(match.group(1))
        
        match = re.search(r'(\d+)\s+failed', result.stdout)
        if match:
            failed = int(match.group(1))
        
        if not json_output.exists():
            error_msg = f"Coverage JSON not generated at: {json_output}\n"
            error_msg += f"Return code: {result.returncode}\n"
            error_msg += f"STDOUT:\n{result.stdout}\n"
            error_msg += f"STDERR:\n{result.stderr}"
            raise RuntimeError(error_msg)
        
        with open(json_output, 'r') as f:
            coverage_data = json.load(f)
        
        all_files = list(coverage_data.get('files', {}).keys())
        
        file_coverage = None
        target_filename = f"HumanEval_{self.problem_num}_0.py"
        
        for file_path, file_data in coverage_data.get('files', {}).items():
            if target_filename in file_path or file_path.endswith(target_filename):
                summary = file_data.get('summary', {})
                file_coverage = {
                    'line_coverage': round(summary.get('percent_covered', 0), 2),
                    'branch_coverage': round(
                        (summary.get('covered_branches', 0) / summary.get('num_branches', 1) * 100) 
                        if summary.get('num_branches', 0) > 0 else 0, 
                        2
                    ),
                    'lines_covered': summary.get('covered_lines', 0),
                    'lines_total': summary.get('num_statements', 0),
                    'branches_covered': summary.get('covered_branches', 0),
                    'branches_total': summary.get('num_branches', 0),
                }
                break
        
        if file_coverage is None:
            error_msg = f"Could not extract coverage for {target_filename}\n"
            error_msg += f"Available files in coverage data:\n"
            for fp in all_files:
                error_msg += f"  - {fp}\n"
            error_msg += f"\nSolution file location: {solution_file}\n"
            error_msg += f"Solution file exists: {solution_file.exists()}\n"
            raise RuntimeError(error_msg)
        
        file_coverage.update({
            'tests_passed': passed,
            'tests_failed': failed
        })
        
        return file_coverage
    
    def generate_improvement_prompt(self, iteration: int, prev_coverage: Dict) -> str:
        """
        Generate LLM prompt for test improvement based on current coverage.
        
        Args:
            iteration: Current iteration number
            prev_coverage: Coverage data from previous iteration
            
        Returns:
            Prompt string for LLM
        """
        function_name = self.problem_data['entry_point']
        problem_statement = self.problem_data['prompt']
        branch_cov = prev_coverage['branch_coverage']
        line_cov = prev_coverage['line_coverage']
        
        if iteration == 1:
            prompt = f"""You are an expert software testing engineer. Generate comprehensive pytest unit tests to improve code coverage.

Problem Statement:
{problem_statement}

Function to Test:
```python
{self.solution_code}
```

Current Coverage:
- Branch Coverage: {branch_cov:.1f}%
- Line Coverage: {line_cov:.1f}%

Task:
Generate a comprehensive pytest test suite that increases branch coverage. Focus on:

1. Edge Cases: Empty inputs, None values, boundary conditions
2. Error Paths: Invalid inputs that should raise exceptions
3. Branch Coverage: Test all conditional paths (if/else branches)
4. Data Variations: Different data types, sizes, and patterns

Output Format:
Provide ONLY valid Python pytest code with no markdown formatting or explanations.
Include:
- Necessary imports (pytest, etc.)
- Multiple test functions with descriptive names
- Use pytest.raises() for exception testing
- Comments explaining what each test validates

Generate at least 8-12 distinct test cases covering different scenarios."""

        else:
            uncovered_branches = prev_coverage['branches_total'] - prev_coverage['branches_covered']
            
            prompt = f"""You are an expert software testing engineer performing iterative test improvement.

Problem Statement:
{problem_statement}

Function to Test:
```python
{self.solution_code}
```

Current Coverage (Iteration {iteration-1}):
- Branch Coverage: {branch_cov:.1f}% ({prev_coverage['branches_covered']}/{prev_coverage['branches_total']} branches)
- Line Coverage: {line_cov:.1f}%
- Uncovered: {uncovered_branches} branches remaining

Previous Tests Generated:
{len(self.generated_tests)} test sets already exist

Task:
Generate ADDITIONAL pytest tests to cover the remaining {uncovered_branches} untested branches.

Focus Areas:
"""
            
            if branch_cov < 30:
                prompt += "- Target basic conditional branches\n- Test simple if/else paths\n"
            elif branch_cov < 70:
                prompt += "- Target error handling paths\n- Test exception scenarios with pytest.raises()\n"
            else:
                prompt += "- Target edge cases and corner scenarios\n- Test rare branch combinations\n"
            
            prompt += """
Output Format:
Provide ONLY valid Python pytest code with no markdown or explanations.
Generate 3-5 NEW test functions different from existing tests.
Use descriptive function names like test_{function_name}_<scenario>."""
        
        return prompt
    
    def call_llm_for_tests(self, prompt: str, llm_choice: str = 'claude') -> str:
        """
        Call LLM API to generate test code.
        
        Args:
            prompt: Prompt to send to LLM
            llm_choice: Which LLM to use ('claude' or 'gpt4o')
            
        Returns:
            Generated test code as string
        """
        if llm_choice == 'claude':
            if not self.anthropic_client:
                raise RuntimeError(
                    "Anthropic client not initialized. "
                    "Please set ANTHROPIC_API_KEY environment variable or create .env file with:\n"
                    "ANTHROPIC_API_KEY=your_key_here"
                )
            
            response = self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        
        elif llm_choice == 'gpt4o':
            if not openai or not openai.api_key:
                raise RuntimeError(
                    "OpenAI not initialized. "
                    "Please set OPENAI_API_KEY environment variable or create .env file with:\n"
                    "OPENAI_API_KEY=your_key_here"
                )
            
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            return response['choices'][0]['message']['content']
        
        else:
            raise ValueError(f"Unknown LLM: {llm_choice}")
    
    def extract_test_code(self, llm_response: str) -> str:
        """
        Extract Python code from LLM response, removing markdown formatting.
        
        Args:
            llm_response: Raw response from LLM
            
        Returns:
            Cleaned Python code
        """
        pattern1 = r'```python\n(.*?)\n```'
        match = re.search(pattern1, llm_response, re.DOTALL)
        if match:
            code = match.group(1)
        else:
            pattern2 = r'```\n(.*?)\n```'
            match = re.search(pattern2, llm_response, re.DOTALL)
            if match:
                code = match.group(1)
            else:
                code = llm_response.strip()
        
        code = self._fix_test_signatures(code)
        return code
    
    def _fix_test_signatures(self, test_code: str) -> str:
        """
        Fix test functions to use solution_function fixture properly.
        
        Args:
            test_code: Raw test code from LLM
            
        Returns:
            Fixed test code with proper fixture usage
        """
        function_name = self.problem_data['entry_point']
        lines = test_code.split('\n')
        fixed_lines = []
        
        for line in lines:
            if line.strip().startswith('def test_') and '(solution_function)' not in line:
                if '():' in line:
                    line = line.replace('():', '(solution_function):')
                elif '(' in line and ')' not in line:
                    line = line.replace('(', '(solution_function, ')
            
            if function_name in line and 'def ' not in line and 'import' not in line:
                line = re.sub(rf'\b{function_name}\s*\(', 'solution_function(', line)
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def deduplicate_tests(self, new_tests: str) -> Tuple[str, int, int]:
        """
        Remove duplicate test functions from new tests.
        
        Args:
            new_tests: New test code to deduplicate
            
        Returns:
            Tuple of (deduplicated_code, num_new_tests, num_duplicates)
        """
        new_test_names = set(re.findall(r'def (test_\w+)\(', new_tests))
        
        existing_test_names = set()
        for test_code in self.generated_tests:
            existing_test_names.update(re.findall(r'def (test_\w+)\(', test_code))
        
        duplicates = new_test_names & existing_test_names
        
        if not duplicates:
            return new_tests, len(new_test_names), 0
        
        lines = new_tests.split('\n')
        deduplicated_lines = []
        skip_until_next_def = False
        
        for line in lines:
            match = re.match(r'def (test_\w+)\(', line)
            if match:
                func_name = match.group(1)
                if func_name in duplicates:
                    skip_until_next_def = True
                    continue
                else:
                    skip_until_next_def = False
            
            if not skip_until_next_def:
                deduplicated_lines.append(line)
        
        deduplicated_code = '\n'.join(deduplicated_lines)
        
        return deduplicated_code, len(new_test_names) - len(duplicates), len(duplicates)
    
    def run_improvement_iteration(self, iteration: int, llm_choice: str = 'claude') -> Optional[Dict]:
        """
        Run one iteration of test improvement.
        
        Args:
            iteration: Current iteration number
            llm_choice: Which LLM to use
            
        Returns:
            Coverage data dictionary or None if no new tests
        """
        prev_coverage = self.iteration_history[-1]
        
        prompt = self.generate_improvement_prompt(iteration, prev_coverage)
        self.prompts_used.append({
            'iteration': iteration,
            'prompt': prompt,
            'timestamp': datetime.now().isoformat()
        })
        
        llm_response = self.call_llm_for_tests(prompt, llm_choice)
        test_code = self.extract_test_code(llm_response)
        deduplicated_code, num_new, num_dupes = self.deduplicate_tests(test_code)
        
        if num_new == 0:
            return None
        
        self.generated_tests.append(deduplicated_code)
        combined_test_file = self._create_combined_test_file(iteration)
        coverage_data = self._run_coverage_analysis(combined_test_file, iteration)
        
        branch_improvement = coverage_data['branch_coverage'] - prev_coverage['branch_coverage']
        line_improvement = coverage_data['line_coverage'] - prev_coverage['line_coverage']
        
        self.iteration_history.append({
            'iteration': iteration,
            'description': f'LLM-generated tests (iteration {iteration})',
            'line_coverage': coverage_data['line_coverage'],
            'branch_coverage': coverage_data['branch_coverage'],
            'lines_covered': coverage_data['lines_covered'],
            'lines_total': coverage_data['lines_total'],
            'branches_covered': coverage_data['branches_covered'],
            'branches_total': coverage_data['branches_total'],
            'tests_passed': coverage_data['tests_passed'],
            'tests_failed': coverage_data['tests_failed'],
            'num_tests': coverage_data['tests_passed'] + coverage_data['tests_failed'],
            'new_tests_added': num_new,
            'duplicates_removed': num_dupes,
            'branch_improvement': round(branch_improvement, 2),
            'line_improvement': round(line_improvement, 2),
            'prompt': prompt,
            'llm_response': llm_response
        })
        
        return coverage_data
    
    def _create_combined_test_file(self, iteration: int) -> Path:
        """
        Create test file combining baseline tests with all accumulated LLM tests.
        
        Args:
            iteration: Current iteration number
            
        Returns:
            Path to combined test file
        """
        conftest_src = self.baseline_tests_dir / 'conftest.py'
        conftest_dst = self.improved_tests_dir / 'conftest.py'
        
        if conftest_src.exists() and not conftest_dst.exists():
            shutil.copy(conftest_src, conftest_dst)
        
        combined_file = self.improved_tests_dir / f"test_humaneval_{self.problem_num}_iter{iteration}.py"
        
        baseline_test = self.baseline_tests_dir / f"test_humaneval_{self.problem_num}.py"
        with open(baseline_test, 'r') as f:
            baseline_content = f.read()
        
        combined_content = baseline_content + "\n\n# LLM-Generated Tests (Accumulated)\n\n"
        
        for i, test_code in enumerate(self.generated_tests, 1):
            combined_content += f"\n# --- Iteration {i} Tests ---\n\n"
            combined_content += test_code + "\n"
        
        with open(combined_file, 'w', encoding='utf-8') as f:
            f.write(combined_content)
        
        return combined_file
    
    def check_convergence(self) -> bool:
        """
        Check if coverage has converged per assignment criteria.
        Convergence: Coverage(i) - Coverage(i-2) <= 3% for 3 consecutive iterations
        
        Returns:
            True if converged, False otherwise
        """
        if len(self.iteration_history) < self.CONVERGENCE_WINDOW + 1:
            return False
        
        recent = self.iteration_history[-self.CONVERGENCE_WINDOW:]
        
        for i in range(len(recent) - 2):
            improvement = recent[i+2]['branch_coverage'] - recent[i]['branch_coverage']
            if improvement > self.CONVERGENCE_THRESHOLD:
                return False
        
        return True
    
    def run_full_improvement(self, llm_choice: str = 'claude') -> Dict:
        """
        Run complete test improvement process until convergence or 100% coverage.
        
        Args:
            llm_choice: Which LLM to use for test generation
            
        Returns:
            Final report dictionary
        """
        self.run_baseline_coverage()
        
        if self.iteration_history[0]['branch_coverage'] >= 100:
            return self._generate_report()
        
        for iteration in range(1, self.MAX_ITERATIONS + 1):
            coverage = self.run_improvement_iteration(iteration, llm_choice)
            
            if coverage is None:
                break
            
            if coverage['branch_coverage'] >= 100:
                break
            
            if self.check_convergence():
                break
        
        return self._generate_report()
    
    def _generate_report(self) -> Dict:
        """
        Generate final report with all iterations.
        
        Returns:
            Complete report dictionary
        """
        report = {
            'problem_num': self.problem_num,
            'model': self.model,
            'strategy': self.strategy,
            'baseline_coverage': {
                'line': self.iteration_history[0]['line_coverage'],
                'branch': self.iteration_history[0]['branch_coverage']
            },
            'final_coverage': {
                'line': self.iteration_history[-1]['line_coverage'],
                'branch': self.iteration_history[-1]['branch_coverage']
            },
            'total_iterations': len(self.iteration_history) - 1,
            'total_improvement': {
                'line': round(self.iteration_history[-1]['line_coverage'] - 
                            self.iteration_history[0]['line_coverage'], 2),
                'branch': round(self.iteration_history[-1]['branch_coverage'] - 
                              self.iteration_history[0]['branch_coverage'], 2)
            },
            'converged': self.check_convergence(),
            'iterations': self.iteration_history,
            'prompts_used': self.prompts_used
        }
        
        report_file = self.part2_dir / f"report_problem{self.problem_num}_{self.model}_{self.strategy}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        return report


def main():
    """Main entry point for Part 2 test improvement."""
    
    print("Starting Part 2: LLM-Assisted Test Generation")
    print("=" * 60)
    
    script_dir = Path(__file__).parent.resolve()
    selection_file = script_dir / 'results' / 'part1_coverage' / 'selected_for_parts_2_3.json'
    
    if not selection_file.exists():
        raise FileNotFoundError(
            f"Part 1 selection file not found: {selection_file}. "
            f"Run part1_baseline_coverage.py first."
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
        
        agent = TestImprovementAgent(
            problem_num=problem_num,
            model=model,
            strategy=strategy
        )
        
        print(f"  Running iterative improvement...")
        report = agent.run_full_improvement(llm_choice='claude')
        all_reports.append(report)
        
        print(f"Completed: {report['total_iterations']} iterations")
        print(f"Baseline: {report['baseline_coverage']['branch']:.1f}%")
        print(f"Final: {report['final_coverage']['branch']:.1f}%")
        print(f"Total Improvement: {report['total_improvement']['branch']:.1f}%")
    
    print("\n" + "=" * 60)
    print("\nGenerating summary...")
    summary_file = script_dir / 'results' / 'part2_improved_tests' / 'part2_summary.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'problems_improved': len(selected_problems),
                'avg_baseline_branch_coverage': sum(r['baseline_coverage']['branch'] 
                                                   for r in all_reports) / len(all_reports),
                'avg_final_branch_coverage': sum(r['final_coverage']['branch'] 
                                                for r in all_reports) / len(all_reports),
                'avg_improvement': sum(r['total_improvement']['branch'] 
                                     for r in all_reports) / len(all_reports),
                'total_iterations': sum(r['total_iterations'] for r in all_reports)
            },
            'detailed_reports': all_reports
        }, f, indent=2)

    print(f"Summary saved to: {summary_file}")

if __name__ == "__main__":
    main()