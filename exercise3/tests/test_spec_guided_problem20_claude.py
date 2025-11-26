from pathlib import Path
import pytest
import importlib.util
from typing import List, Tuple

def get_solution_module(model, strategy, problem_num):
    """Dynamically load the solution module."""
    workspace_root = Path(__file__).parent.parent.parent
    solution_path = workspace_root / 'generated_code' / model / strategy / f'HumanEval_{problem_num}_0.py'
    
    if not solution_path.exists():
        raise FileNotFoundError(f"Solution not found: {solution_path}")
    
    spec = importlib.util.spec_from_file_location(
        f"solution_{model}_{strategy}_{problem_num}", 
        solution_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

@pytest.fixture
def solution_function(request):
    """Fixture to provide the solution function."""
    model = request.config.getoption("--model", default="gpt4o")
    strategy = request.config.getoption("--strategy", default="self_debugging")
    module = get_solution_module(model, strategy, "20")
    return getattr(module, "find_closest_elements")

def test_spec_guided_find_closest_elements_return_type(solution_function):
    """
    Validates Specification 1:
    - Result must be a tuple of length 2
    """
    result = solution_function([1.0, 2.0, 3.0, 4.0])
    assert isinstance(result, tuple)
    assert len(result) == 2

def test_spec_guided_find_closest_elements_ordering(solution_function):
    """
    Validates Specification 2:
    - First element must be less than or equal to second element
    """
    test_cases = [
        [1.0, 2.0, 3.0, 4.0],
        [4.0, 3.0, 2.0, 1.0],
        [1.0, 1.0, 2.0, 2.0]
    ]
    for numbers in test_cases:
        result = solution_function(numbers)
        assert result[0] <= result[1]

def test_spec_guided_find_closest_elements_membership(solution_function):
    """
    Validates Specification 3:
    - Both returned elements must be from the input list
    """
    numbers = [1.5, 2.5, 3.5, 4.5]
    result = solution_function(numbers)
    assert result[0] in numbers
    assert result[1] in numbers

def test_spec_guided_find_closest_elements_closest_pair(solution_function):
    """
    Validates Specification 4:
    - Returned pair must have the smallest absolute difference among all possible pairs
    """
    numbers = [1.0, 4.0, 2.0, 3.0]  # Closest pair should be (2.0, 3.0)
    result = solution_function(numbers)
    
    # Check if the difference between result pair is smallest among all pairs
    result_diff = abs(result[1] - result[0])
    for i in numbers:
        for j in numbers:
            if j > i:  # Only check pairs where second number is larger
                assert result_diff <= abs(j - i)

def test_spec_guided_find_closest_elements_min_length(solution_function):
    """
    Validates Specification 5:
    - Input list must have at least 2 elements
    """
    with pytest.raises(Exception):  # Should raise some kind of exception
        solution_function([1.0])
    
    with pytest.raises(Exception):
        solution_function([])

def test_spec_guided_find_closest_elements_duplicate_values(solution_function):
    """
    Edge case testing:
    - Validates specifications 1-4 with duplicate values
    """
    numbers = [1.0, 2.0, 2.0, 3.0]
    result = solution_function(numbers)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] <= result[1]
    assert result == (2.0, 2.0)

def test_spec_guided_find_closest_elements_floating_point(solution_function):
    """
    Edge case testing:
    - Validates specifications 1-4 with floating point numbers
    """
    numbers = [1.1, 1.12, 1.15, 1.20]
    result = solution_function(numbers)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] <= result[1]
    assert result[0] in numbers and result[1] in numbers
    assert abs(result[1] - result[0]) == pytest.approx(0.02)  # Should return (1.1, 1.12)