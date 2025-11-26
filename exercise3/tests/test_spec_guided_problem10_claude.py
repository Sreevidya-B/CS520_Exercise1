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
    strategy = request.config.getoption("--strategy", default="cot")
    module = get_solution_module(model, strategy, "10")
    return getattr(module, "make_palindrome")

def test_spec_guided_make_palindrome_is_palindrome(solution_function):
    """
    Validates Specification 1: Result must be a palindrome
    Tests with a non-palindrome input string
    """
    result = solution_function("cat")
    assert all(result[i] == result[len(result)-1-i] for i in range(len(result)//2))

def test_spec_guided_make_palindrome_preserves_input(solution_function):
    """
    Validates Specification 2: Result must start with input string
    Tests with various input strings
    """
    test_cases = ["hello", "python", "test"]
    for input_str in test_cases:
        result = solution_function(input_str)
        assert result.startswith(input_str)

def test_spec_guided_make_palindrome_length_bounds(solution_function):
    """
    Validates Specifications 3 and 4: Result length must be between input length and 2*input length
    """
    input_str = "programming"
    result = solution_function(input_str)
    assert len(result) >= len(input_str)
    assert len(result) <= len(input_str) * 2

def test_spec_guided_make_palindrome_empty_string(solution_function):
    """
    Validates Specification 5: Empty string handling
    Tests that empty string returns empty string
    """
    result = solution_function("")
    assert result == ""
    
def test_spec_guided_make_palindrome_single_char(solution_function):
    """
    Validates Specification 5: Single character handling
    Tests that single character returns itself
    """
    result = solution_function("x")
    assert result == "x"

def test_spec_guided_make_palindrome_already_palindrome(solution_function):
    """
    Validates multiple specifications (1, 2, 3, 4)
    Tests with input that is already a palindrome
    """
    input_str = "radar"
    result = solution_function(input_str)
    assert result == input_str
    assert len(result) == len(input_str)

def test_spec_guided_make_palindrome_special_chars(solution_function):
    """
    Validates multiple specifications (1, 2, 3, 4)
    Tests with special characters and spaces
    """
    input_str = "a!b c"
    result = solution_function(input_str)
    assert result.startswith(input_str)
    assert all(result[i] == result[len(result)-1-i] for i in range(len(result)//2))
    assert len(result) <= len(input_str) * 2

def test_spec_guided_make_palindrome_complex_case(solution_function):
    """
    Validates all specifications together
    Tests with a complex input requiring significant transformation
    """
    input_str = "abcdef"
    result = solution_function(input_str)
    # Spec 1: Is palindrome
    assert all(result[i] == result[len(result)-1-i] for i in range(len(result)//2))
    # Spec 2: Starts with input
    assert result.startswith(input_str)
    # Spec 3 & 4: Length bounds
    assert len(input_str) <= len(result) <= len(input_str) * 2