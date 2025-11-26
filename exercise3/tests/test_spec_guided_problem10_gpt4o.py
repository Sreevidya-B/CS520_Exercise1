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

def test_spec_guided_make_palindrome_basic_case(solution_function):
    """
    Validates Specs 1–5 for a standard input 'race':
    - Palindromic result
    - Starts with input
    - Length checks
    - Proper prefix suffix handling
    """
    s = "race"
    res = solution_function(s)
    assert res == res[::-1]                                # Spec 1
    assert res.startswith(s)                               # Spec 2
    assert len(res) >= len(s)                              # Spec 3
    assert s.startswith(res[len(s):][::-1])                # Spec 4
    assert len(res) <= len(s) * 2                          # Spec 5

def test_spec_guided_make_palindrome_already_palindrome(solution_function):
    """
    Validates Specs 1–5 where input is already a palindrome.
    Output should match input exactly.
    """
    s = "level"
    res = solution_function(s)
    assert res == res[::-1]                                # Spec 1
    assert res.startswith(s)                               # Spec 2
    assert len(res) == len(s)                              # Specs 3 & 5
    assert s.startswith(res[len(s):][::-1])                # Spec 4

def test_spec_guided_make_palindrome_single_char(solution_function):
    """
    Validates Specs 1–5 for a one-character input (edge case).
    """
    s = "z"
    res = solution_function(s)
    assert res == res[::-1]                                # Spec 1
    assert res.startswith(s)                               # Spec 2
    assert len(res) == 1                                   # Spec 3 & 5
    assert s.startswith(res[len(s):][::-1])                # Spec 4

def test_spec_guided_make_palindrome_empty_input(solution_function):
    """
    Validates Specs 1–5 for empty string input (edge case).
    Output should also be empty (a valid palindrome).
    """
    s = ""
    res = solution_function(s)
    assert res == res[::-1]                                # Spec 1
    assert res.startswith(s)                               # Spec 2
    assert len(res) == 0                                   # Spec 3 & 5
    assert s.startswith(res[len(s):][::-1])                # Spec 4

def test_spec_guided_make_palindrome_with_digits(solution_function):
    """
    Validates Specs 1–5 for alphanumeric input.
    Ensures correctness even with numbers.
    """
    s = "ab123"
    res = solution_function(s)
    assert res == res[::-1]                                # Spec 1
    assert res.startswith(s)                               # Spec 2
    assert len(res) >= len(s)                              # Spec 3
    assert s.startswith(res[len(s):][::-1])                # Spec 4
    assert len(res) <= len(s) * 2                          # Spec 5

def test_spec_guided_make_palindrome_partial_suffix_palindrome(solution_function):
    """
    Validates Specs 1–5 when only a partial suffix is already a palindrome.
    For example: 'abac' → 'abacaba'
    """
    s = "abac"
    res = solution_function(s)
    assert res == res[::-1]                                # Spec 1
    assert res.startswith(s)                               # Spec 2
    assert len(res) >= len(s)                              # Spec 3
    assert s.startswith(res[len(s):][::-1])                # Spec 4
    assert len(res) <= len(s) * 2                          # Spec 5

def test_spec_guided_make_palindrome_uppercase_mixed(solution_function):
    """
    Validates Specs 1–5 for case-sensitive strings.
    'AaB' is not a palindrome, so reversed prefix must be added.
    """
    s = "AaB"
    res = solution_function(s)
    assert res == res[::-1]                                # Spec 1
    assert res.startswith(s)                               # Spec 2
    assert len(res) >= len(s)                              # Spec 3
    assert s.startswith(res[len(s):][::-1])                # Spec 4
    assert len(res) <= len(s) * 2                          # Spec 5
