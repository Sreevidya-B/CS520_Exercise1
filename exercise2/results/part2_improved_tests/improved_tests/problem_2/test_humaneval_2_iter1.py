"""
Test suite for HumanEval/2 - truncate_number
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
    assert candidate(3.5) == 0.5
    assert abs(candidate(1.33) - 0.33) < 1e-6
    assert abs(candidate(123.456) - 0.456) < 1e-6


@pytest.fixture
def solution_function(request):
    model = request.config.getoption("--model", default="gpt4o")
    strategy = request.config.getoption("--strategy", default="cot")
    module = get_solution_module(model, strategy, "2")
    return getattr(module, "truncate_number")

def test_truncate_number_humaneval(solution_function):
    check(solution_function)


# LLM-Generated Tests (Accumulated)


# --- Iteration 1 Tests ---

import pytest
import math

def test_truncate_number_positive_float(solution_function):
    # Test basic positive float with decimal part
    assert solution_function(3.5) == 0.5
    assert solution_function(10.75) == 0.75
    assert solution_function(1.1) == 0.1

def test_truncate_number_whole_numbers(solution_function):
    # Test whole numbers (should return 0.0)
    assert solution_function(5.0) == 0.0
    assert solution_function(10.0) == 0.0
    assert solution_function(1.0) == 0.0

def test_truncate_number_small_positive(solution_function):
    # Test numbers between 0 and 1
    assert solution_function(0.5) == 0.5
    assert solution_function(0.99) == 0.99
    assert solution_function(0.01) == 0.01

def test_truncate_number_zero(solution_function):
    # Test zero input
    assert solution_function(0.0) == 0.0

def test_truncate_number_large_numbers(solution_function):
    # Test large numbers
    assert solution_function(1000.25) == 0.25
    assert solution_function(999999.123) == 0.123

def test_truncate_number_very_small_decimals(solution_function):
    # Test very small decimal parts
    result = solution_function(5.000001)
    assert abs(result - 0.000001) < 1e-10

def test_truncate_number_precision(solution_function):
    # Test floating point precision edge cases
    assert abs(solution_function(2.7) - 0.7) < 1e-10
    assert abs(solution_function(1.3) - 0.3) < 1e-10

def test_truncate_number_negative_float(solution_function):
    # Test negative numbers (though docstring says positive)
    assert solution_function(-3.5) == 0.5
    assert solution_function(-1.7) == 0.3

def test_truncate_number_negative_whole(solution_function):
    # Test negative whole numbers
    assert solution_function(-5.0) == 0.0
    assert solution_function(-10.0) == 0.0

def test_truncate_number_none_input(solution_function):
    # Test None input - should raise TypeError
    with pytest.raises(TypeError):
        solution_function(None)

def test_truncate_number_string_input(solution_function):
    # Test string input - should raise TypeError
    with pytest.raises(TypeError):
        solution_function("3.5")

def test_truncate_number_list_input(solution_function):
    # Test list input - should raise TypeError
    with pytest.raises(TypeError):
        solution_function([3.5])

def test_truncate_number_infinity(solution_function):
    # Test infinity input
    with pytest.raises((OverflowError, ValueError)):
        solution_function(float('inf'))

def test_truncate_number_negative_infinity(solution_function):
    # Test negative infinity input
    with pytest.raises((OverflowError, ValueError)):
        solution_function(float('-inf'))

def test_truncate_number_nan(solution_function):
    # Test NaN input
    result = solution_function(float('nan'))
    assert math.isnan(result)

def test_truncate_number_boolean_input(solution_function):
    # Test boolean input (should work as bool converts to int)
    assert solution_function(True) == 0.0
    assert solution_function(False) == 0.0

def test_truncate_number_complex_input(solution_function):
    # Test complex number input - should raise TypeError
    with pytest.raises(TypeError):
        solution_function(3+4j)
