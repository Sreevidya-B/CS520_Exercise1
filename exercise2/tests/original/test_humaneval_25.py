"""
Test suite for HumanEval/25 - factorize
"""
import pytest
from pathlib import Path

def get_solution_module(model, strategy, problem_num):
    workspace_root = Path(r"S:\Code\CS520_Exercise1")
    solution_path = workspace_root / 'generated_code' / model / strategy / f'HumanEval_{problem_num}_0.py'
    
    if not solution_path.exists():
        raise FileNotFoundError(f"Solution not found: {solution_path}")
    
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        f"solution_{model}_{strategy}_{problem_num}", 
        solution_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module



METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate(2) == [2]
    assert candidate(4) == [2, 2]
    assert candidate(8) == [2, 2, 2]
    assert candidate(3 * 19) == [3, 19]
    assert candidate(3 * 19 * 3 * 19) == [3, 3, 19, 19]
    assert candidate(3 * 19 * 3 * 19 * 3 * 19) == [3, 3, 3, 19, 19, 19]
    assert candidate(3 * 19 * 19 * 19) == [3, 19, 19, 19]
    assert candidate(3 * 2 * 3) == [2, 3, 3]


@pytest.fixture
def solution_function(request):
    model = request.config.getoption("--model", default="gpt4o")
    strategy = request.config.getoption("--strategy", default="cot")
    module = get_solution_module(model, strategy, "25")
    return getattr(module, "factorize")

def test_factorize_humaneval(solution_function):
    check(solution_function)
