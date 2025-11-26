"""
Exercise 3 - Step 3: Evaluate Specifications
Interactive evaluation of LLM-generated specifications.
"""

import json
from pathlib import Path


def load_raw_specifications(problem_num, model):
    """Load raw LLM-generated specifications from file"""
    spec_file = Path(__file__).parent / "specifications" / f"problem{problem_num}_{model}_raw.py"
    
    if not spec_file.exists():
        return None
    
    with open(spec_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assertions = []
    for line in content.split('\n'):
        stripped = line.strip()
        if stripped.startswith('assert '):
            assertions.append(stripped)
    
    return assertions


def evaluate_specification_interactive(spec_num, assertion, problem_num, model):
    """Present specification to user for evaluation"""
    
    print(f"\n{'-' * 60}")
    print(f"Specification #{spec_num}")
    print(f"{'-' * 60}")
    print(assertion)
    print(f"{'-' * 60}")
    
    while True:
        response = input("Correct? (y/n): ").strip().lower()
        if response in ['y', 'n']:
            break
    
    is_correct = (response == 'y')
    
    evaluation = {
        'spec_number': spec_num,
        'problem_num': problem_num,
        'model': model,
        'original_assertion': assertion,
        'is_correct': is_correct,
        'issues': [],
        'corrected_assertion': assertion if is_correct else '',
        'explanation': ''
    }
    
    if not is_correct:
        issues = []
        while True:
            issue = input("Issue (empty to finish): ").strip()
            if not issue:
                break
            issues.append(issue)
        evaluation['issues'] = issues
        
        corrected = input("Corrected assertion: ").strip()
        evaluation['corrected_assertion'] = corrected
        
        explanation = input("Explanation: ").strip()
        evaluation['explanation'] = explanation
    
    return evaluation


def calculate_accuracy(evaluations):
    """Calculate accuracy rate"""
    total = len(evaluations)
    correct = sum(1 for e in evaluations if e['is_correct'])
    accuracy = (correct / total * 100) if total > 0 else 0
    
    return {
        'total': total,
        'correct': correct,
        'incorrect': total - correct,
        'accuracy_rate': accuracy
    }


def save_evaluation_results(all_evaluations, output_file):
    """Save evaluation results to JSON"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_evaluations, f, indent=2, ensure_ascii=False)


def generate_corrected_spec_file(evaluations, problem_num, model):
    """Generate file with only correct assertions"""
    output_path = Path(__file__).parent / "specifications" / f"problem{problem_num}_{model}_corrected.py"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Corrected specifications for Problem {problem_num} ({model})\n\n")
        
        for eval_result in evaluations:
            if eval_result['is_correct']:
                f.write(f"{eval_result['original_assertion']}\n")
            else:
                if eval_result['corrected_assertion']:
                    f.write(f"{eval_result['corrected_assertion']}\n")


def evaluate_all_specifications():
    """Main evaluation function"""
    
    spec_dir = Path(__file__).parent / "specifications"
    if not spec_dir.exists():
        raise FileNotFoundError("Create specifications/ directory first")
    
    problems = ['10', '20']
    models = ['gpt4o', 'claude']
    
    all_evaluations = {}
    accuracy_summary = {}
    
    for problem_num in problems:
        for model in models:
            key = f"problem{problem_num}_{model}"
            
            print(f"\n{'='*60}")
            print(f"Problem {problem_num} - {model.upper()}")
            print(f"{'='*60}")
            
            assertions = load_raw_specifications(problem_num, model)
            if assertions is None:
                continue
            
            evaluations = []
            for i, assertion in enumerate(assertions, 1):
                eval_result = evaluate_specification_interactive(i, assertion, problem_num, model)
                evaluations.append(eval_result)
            
            accuracy = calculate_accuracy(evaluations)
            accuracy_summary[key] = accuracy
            
            print(f"\nAccuracy: {accuracy['correct']}/{accuracy['total']} ({accuracy['accuracy_rate']:.1f}%)")
            
            all_evaluations[key] = {
                'problem_num': problem_num,
                'model': model,
                'evaluations': evaluations,
                'accuracy': accuracy
            }
            
            generate_corrected_spec_file(evaluations, problem_num, model)
    
    output_path = Path(__file__).parent / "specifications" / "evaluation_results.json"
    save_evaluation_results(all_evaluations, output_path)
    
    print(f"\n{'='*60}")
    print("OVERALL SUMMARY")
    print(f"{'='*60}")
    for key, acc in accuracy_summary.items():
        print(f"{key}: {acc['correct']}/{acc['total']} ({acc['accuracy_rate']:.1f}%)")


if __name__ == "__main__":
    evaluate_all_specifications()