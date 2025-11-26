from pathlib import Path
import pytest
import importlib.util

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

def test_spec_guided_find_closest_elements_basic_float_case(solution_function):
    """
    Validates Specs 1–5 on standard float list with a clear closest pair.
    """
    numbers = [1.2, 3.5, 2.8, 5.0, 3.6]
    res = solution_function(numbers)
    assert res[0] in numbers and res[1] in numbers and res[0] != res[1]      # Spec 1
    assert res[0] < res[1]                                                   # Spec 2
    assert all(abs(res[1] - res[0]) <= abs(x - y) 
               for x in numbers for y in numbers if x != y)                  # Spec 3
    assert len(numbers) >= 2                                                 # Spec 4
    assert isinstance(res[0], (int, float)) and isinstance(res[1], (int, float))  # Spec 5

def test_spec_guided_find_closest_elements_two_elements(solution_function):
    """
    Validates Specs 1–5 for minimum valid input length (2 elements).
    """
    numbers = [10.0, 10.1]
    res = solution_function(numbers)
    assert res[0] in numbers and res[1] in numbers and res[0] != res[1]      # Spec 1
    assert res[0] < res[1]                                                   # Spec 2
    assert all(abs(res[1] - res[0]) <= abs(x - y) 
               for x in numbers for y in numbers if x != y)                  # Spec 3
    assert len(numbers) >= 2                                                 # Spec 4
    assert isinstance(res[0], (int, float)) and isinstance(res[1], (int, float))  # Spec 5

def test_spec_guided_find_closest_elements_negative_and_positive(solution_function):
    """
    Validates Specs 1–5 when input includes negative & positive values.
    """
    numbers = [-2.5, 0.0, 3.2, -2.4, 7.1]
    res = solution_function(numbers)
    assert res[0] in numbers and res[1] in numbers and res[0] != res[1]      # Spec 1
    assert res[0] < res[1]                                                   # Spec 2
    assert all(abs(res[1] - res[0]) <= abs(x - y) 
               for x in numbers for y in numbers if x != y)                  # Spec 3
    assert len(numbers) >= 2                                                 # Spec 4
    assert isinstance(res[0], (int, float)) and isinstance(res[1], (int, float))  # Spec 5

def test_spec_guided_find_closest_elements_multiple_close_pairs(solution_function):
    """
    Validates Spec 3 when multiple close pairs exist; must pick any closest one.
    """
    numbers = [1.0, 2.0, 3.0, 4.0, 5.01, 5.0]  # 5.0 & 5.01 are closest
    res = solution_function(numbers)
    assert abs(res[1] - res[0]) == 0.01                                        # Spec 3

def test_spec_guided_find_closest_elements_duplicate_values(solution_function):
    """
    Validates Spec 1 and 3: input includes identical values but must return different ones.
    """
    numbers = [7.0, 7.0, 8.0, 10.0]
    res = solution_function(numbers)
    assert res[0] != res[1]                                                   # Spec 1
    assert all(abs(res[1] - res[0]) <= abs(x - y) 
               for x in numbers for y in numbers if x != y)                  # Spec 3

def test_spec_guided_find_closest_elements_integer_and_float_mix(solution_function):
    """
    Validates Spec 5: types of result elements are int or float (mixed input).
    """
    numbers = [1, 2.5, 3, 4.5]
    res = solution_function(numbers)
    assert isinstance(res[0], (int, float)) and isinstance(res[1], (int, float))  # Spec 5

def test_spec_guided_find_closest_elements_unsorted_list(solution_function):
    """
    Validates all Specs for an unsorted list with a known closest pair.
    """
    numbers = [100, 3.00001, 2.99999, 50, 0]
    res = solution_function(numbers)
    assert res[0] in numbers and res[1] in numbers and res[0] != res[1]      # Spec 1
    assert res[0] < res[1]                                                   # Spec 2
    assert all(abs(res[1] - res[0]) <= abs(x - y) 
               for x in numbers for y in numbers if x != y)                  # Spec 3
    assert isinstance(res[0], (int, float)) and isinstance(res[1], (int, float))  # Spec 5
