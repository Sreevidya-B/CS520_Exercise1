"""
Exercise 3 - Step 1: Extract Problem Information
Extracts problems 10 and 20 from Exercise 2 selection.
"""

import json
from pathlib import Path


def load_selected_problems():
    """Load the 2 problems selected in Exercise 2"""
    selection_file = Path(__file__).parent.parent / 'exercise2' / 'results' / 'part1_coverage' / 'selected_for_parts_2_3.json'
    
    if not selection_file.exists():
        raise FileNotFoundError(f"Run Exercise 2 Part 1 first: {selection_file}")
    
    with open(selection_file, 'r') as f:
        return json.load(f)


def load_humaneval_problems():
    """Load HumanEval dataset"""
    data_file = Path(__file__).parent.parent / 'data' / 'selected_problems.jsonl'
    
    problems = {}
    with open(data_file, 'r') as f:
        for line in f:
            problem = json.loads(line)
            problem_num = problem['task_id'].split('/')[-1]
            problems[problem_num] = problem
    
    return problems


def extract_signature_and_description(problem_data):
    """Extract signature and description from HumanEval problem"""
    prompt = problem_data['prompt']
    entry_point = problem_data['entry_point']
    
    lines = prompt.split('\n')
    
    # Find the main function definition
    signature = None
    func_start_idx = None
    
    for i, line in enumerate(lines):
        if f'def {entry_point}' in line:
            func_start_idx = i
            sig_lines = [line.strip()]
            j = i + 1
            while j < len(lines) and ':' not in ''.join(sig_lines):
                if lines[j].strip():
                    sig_lines.append(lines[j].strip())
                j += 1
            signature = ' '.join(sig_lines).rstrip(':').strip()
            break
    
    # Extract description from the docstring that follows the function definition
    description_lines = []
    in_docstring = False
    found_docstring = False
    
    # Start from the function definition line
    if func_start_idx is not None:
        for i in range(func_start_idx, len(lines)):
            line = lines[i]
            
            if '"""' in line:
                if not in_docstring:
                    # Opening docstring
                    in_docstring = True
                    found_docstring = True
                    
                    # Check for single-line docstring
                    parts = line.split('"""')
                    if len(parts) >= 3:  # """text"""
                        text = parts[1].strip()
                        if text and not text.startswith('>>>'):
                            description_lines.append(text)
                        break
                    elif len(parts) >= 2:  # """text (continues)
                        text = parts[1].strip()
                        if text and not text.startswith('>>>'):
                            description_lines.append(text)
                else:
                    # Closing docstring
                    text = line.split('"""')[0].strip()
                    if text and not text.startswith('>>>') and not text.startswith('('):
                        description_lines.append(text)
                    break
                continue
            
            if in_docstring:
                stripped = line.strip()
                # Stop at examples or skip example lines
                if stripped.startswith('>>>'):
                    break
                # Skip lines that look like example output (start with parenthesis or numbers)
                if stripped and not stripped.startswith('...') and not stripped.startswith('(') and not stripped[0].isdigit():
                    description_lines.append(stripped)
    
    description = ' '.join(description_lines).strip()
    
    # Clean up common artifacts
    description = description.replace('  ', ' ')
    
    return signature, description


def extract_problem_info():
    """Extract structured information for Exercise 3"""
    selection = load_selected_problems()
    humaneval_problems = load_humaneval_problems()
    
    problem_info = {}
    
    for detail in selection['selection_details']:
        problem_num = detail['problem_num']
        problem_data = humaneval_problems[problem_num]
        
        signature, description = extract_signature_and_description(problem_data)
        
        problem_info[problem_num] = {
            'problem_id': problem_data['task_id'],
            'problem_num': problem_num,
            'function_name': problem_data['entry_point'],
            'signature': signature,
            'description': description,
            'model': detail['best_solution']['model'],
            'strategy': detail['best_solution']['strategy']
        }
    
    output_file = Path(__file__).parent / 'problem_descriptions.json'
    with open(output_file, 'w') as f:
        json.dump(problem_info, f, indent=2)
    
    return problem_info


if __name__ == "__main__":
    extract_problem_info()