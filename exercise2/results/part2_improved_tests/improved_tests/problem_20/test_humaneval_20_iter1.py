"""
Test suite for HumanEval/20 - find_closest_elements
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
    assert candidate([1.0, 2.0, 3.9, 4.0, 5.0, 2.2]) == (3.9, 4.0)
    assert candidate([1.0, 2.0, 5.9, 4.0, 5.0]) == (5.0, 5.9)
    assert candidate([1.0, 2.0, 3.0, 4.0, 5.0, 2.2]) == (2.0, 2.2)
    assert candidate([1.0, 2.0, 3.0, 4.0, 5.0, 2.0]) == (2.0, 2.0)
    assert candidate([1.1, 2.2, 3.1, 4.1, 5.1]) == (2.2, 3.1)



@pytest.fixture
def solution_function(request):
    model = request.config.getoption("--model", default="gpt4o")
    strategy = request.config.getoption("--strategy", default="cot")
    module = get_solution_module(model, strategy, "20")
    return getattr(module, "find_closest_elements")

def test_find_closest_elements_humaneval(solution_function):
    check(solution_function)


# LLM-Generated Tests (Accumulated)


# --- Iteration 1 Tests ---

import pytest
from typing import List, Tuple


def find_closest_elements(numbers: List[float]) -> Tuple[float, float]:
    if len(numbers) < 2:
        raise ValueError("The list must contain at least two numbers.")
    
    numbers.sort()
    min_diff = float('inf')
    closest_pair = (numbers[0], numbers[1])
    
    for i in range(len(numbers) - 1):
        diff = numbers[i + 1] - numbers[i]
        if diff < min_diff:
            min_diff = diff
            closest_pair = (numbers[i], numbers[i + 1])
    
    return closest_pair


def test_empty_list(solution_function):
    # Test edge case: empty list should raise ValueError
    with pytest.raises(ValueError, match="The list must contain at least two numbers."):
        solution_function([])


def test_single_element(solution_function):
    # Test edge case: single element list should raise ValueError
    with pytest.raises(ValueError, match="The list must contain at least two numbers."):
        solution_function([5.0])


def test_two_elements_ordered(solution_function):
    # Test basic case: exactly two elements in ascending order
    result = solution_function([1.0, 3.0])
    assert result == (1.0, 3.0)


def test_two_elements_reverse_order(solution_function):
    # Test basic case: exactly two elements in descending order
    result = solution_function([5.0, 2.0])
    assert result == (2.0, 5.0)


def test_two_identical_elements(solution_function):
    # Test edge case: two identical elements (minimum possible difference of 0)
    result = solution_function([3.5, 3.5])
    assert result == (3.5, 3.5)


def test_multiple_identical_elements(solution_function):
    # Test case: multiple identical elements should return first pair
    result = solution_function([7.0, 7.0, 7.0, 7.0])
    assert result == (7.0, 7.0)


def test_closest_elements_example_1(solution_function):
    # Test docstring example 1: mixed numbers with decimal values
    result = solution_function([1.0, 2.0, 3.0, 4.0, 5.0, 2.2])
    assert result == (2.0, 2.2)


def test_closest_elements_example_2(solution_function):
    # Test docstring example 2: duplicate values
    result = solution_function([1.0, 2.0, 3.0, 4.0, 5.0, 2.0])
    assert result == (2.0, 2.0)


def test_unsorted_input(solution_function):
    # Test that function works with unsorted input
    result = solution_function([10.0, 1.0, 5.0, 3.0, 2.8])
    assert result == (2.8, 3.0)


def test_negative_numbers(solution_function):
    # Test with negative numbers
    result = solution_function([-5.0, -2.0, -1.0, 0.0, 3.0])
    assert result == (-1.0, 0.0)


def test_all_negative_numbers(solution_function):
    # Test with all negative numbers
    result = solution_function([-10.0, -8.5, -7.0, -3.0])
    assert result == (-8.5, -7.0)


def test_large_numbers(solution_function):
    # Test with large floating point numbers
    result = solution_function([1000000.0, 1000001.5, 2000000.0])
    assert result == (1000000.0, 1000001.5)


def test_very_small_differences(solution_function):
    # Test with very small differences between numbers
    result = solution_function([1.0, 1.00001, 1.1, 2.0])
    assert result == (1.0, 1.00001)


def test_mixed_integers_and_floats(solution_function):
    # Test with mix of integers and floats (treated as floats)
    result = solution_function([1, 2.1, 3, 4.5, 2.05])
    assert result == (2.05, 2.1)


def test_zero_difference_in_middle(solution_function):
    # Test case where closest pair (identical) is not at the beginning after sorting
    result = solution_function([1.0, 5.0, 5.0, 10.0])
    assert result == (5.0, 5.0)


def test_long_list_with_closest_at_end(solution_function):
    # Test longer list where closest pair appears at the end after sorting
    result = solution_function([1.0, 3.0, 5.0, 7.0, 9.0, 11.0, 11.1])
    assert result == (11.0, 11.1)
