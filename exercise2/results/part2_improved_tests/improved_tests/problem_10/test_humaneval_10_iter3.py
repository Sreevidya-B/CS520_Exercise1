"""
Test suite for HumanEval/10 - make_palindrome
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
    assert candidate('') == ''
    assert candidate('x') == 'x'
    assert candidate('xyz') == 'xyzyx'
    assert candidate('xyx') == 'xyx'
    assert candidate('jerry') == 'jerryrrej'


@pytest.fixture
def solution_function(request):
    model = request.config.getoption("--model", default="gpt4o")
    strategy = request.config.getoption("--strategy", default="cot")
    module = get_solution_module(model, strategy, "10")
    return getattr(module, "make_palindrome")

def test_make_palindrome_humaneval(solution_function):
    check(solution_function)


# LLM-Generated Tests (Accumulated)


# --- Iteration 1 Tests ---

import pytest

def test_is_palindrome_empty_string(solution_function):
    # Test empty string - should be palindrome
    assert is_palindrome('') == True

def test_is_palindrome_single_character(solution_function):
    # Test single character - should be palindrome
    assert is_palindrome('a') == True

def test_is_palindrome_valid_palindromes(solution_function):
    # Test various valid palindromes
    assert is_palindrome('aba') == True
    assert is_palindrome('racecar') == True
    assert is_palindrome('madam') == True
    assert is_palindrome('level') == True

def test_is_palindrome_non_palindromes(solution_function):
    # Test strings that are not palindromes
    assert is_palindrome('cat') == False
    assert is_palindrome('hello') == False
    assert is_palindrome('python') == False

def test_is_palindrome_case_sensitive(solution_function):
    # Test case sensitivity - should not be palindrome due to case
    assert is_palindrome('Aba') == False
    assert is_palindrome('Level') == False

def test_is_palindrome_with_spaces_and_special_chars(solution_function):
    # Test palindromes with spaces and special characters
    assert is_palindrome('a a') == True
    assert is_palindrome('!@!') == True
    assert is_palindrome('a b a') == True
    assert is_palindrome('a b c') == False

def test_make_palindrome_empty_string(solution_function):
    # Test empty string - should return empty string
    assert solution_function('') == ''

def test_make_palindrome_already_palindrome(solution_function):
    # Test strings that are already palindromes
    assert solution_function('a') == 'a'
    assert solution_function('aba') == 'aba'
    assert solution_function('racecar') == 'racecar'
    assert solution_function('madam') == 'madam'

def test_make_palindrome_single_character(solution_function):
    # Test single character - should return same character
    assert solution_function('x') == 'x'
    assert solution_function('z') == 'z'

def test_make_palindrome_two_characters(solution_function):
    # Test two character strings
    assert solution_function('ab') == 'aba'
    assert solution_function('xy') == 'xyx'
    assert solution_function('aa') == 'aa'

def test_make_palindrome_examples_from_docstring(solution_function):
    # Test examples provided in docstring
    assert solution_function('cat') == 'catac'
    assert solution_function('cata') == 'catac'

def test_make_palindrome_longer_strings(solution_function):
    # Test longer strings that need palindrome creation
    assert solution_function('abcd') == 'abcdcba'
    assert solution_function('hello') == 'helloolleh'
    assert solution_function('test') == 'testset'

def test_make_palindrome_partial_palindrome_suffix(solution_function):
    # Test strings where suffix is already palindromic
    assert solution_function('abcdc') == 'abcdcba'
    assert solution_function('xyzy') == 'xyzyx'

def test_make_palindrome_with_repeated_characters(solution_function):
    # Test strings with repeated characters
    assert solution_function('aab') == 'aabaa'
    assert solution_function('aaab') == 'aaabaaaa'
    assert solution_function('abbb') == 'abbbba'

def test_make_palindrome_special_characters(solution_function):
    # Test strings with special characters and numbers
    assert solution_function('a1') == 'a1a'
    assert solution_function('!@') == '!@!'
    assert solution_function('123') == '123321'

def test_make_palindrome_mixed_case(solution_function):
    # Test strings with mixed case
    assert solution_function('Ab') == 'AbA'
    assert solution_function('Hello') == 'HellolleH'

def test_make_palindrome_numeric_strings(solution_function):
    # Test numeric strings
    assert solution_function('12') == '121'
    assert solution_function('123') == '123321'
    assert solution_function('1221') == '1221'

# --- Iteration 2 Tests ---

import pytest

def test_make_palindrome_two_identical_characters(solution_function):
    assert solution_function('aa') == 'aa'

def test_make_palindrome_already_palindrome_odd_length(solution_function):
    assert solution_function('racecar') == 'racecar'

def test_make_palindrome_already_palindrome_even_length(solution_function):
    assert solution_function('abba') == 'abba'

def test_make_palindrome_long_string_needs_prefix(solution_function):
    assert solution_function('abcde') == 'abcdedcba'

# --- Iteration 3 Tests ---

import pytest

def test_make_palindrome_already_palindrome_multiple_chars(solution_function):
    """Test with strings that are already palindromes"""
    assert solution_function('aba') == 'aba'
    assert solution_function('racecar') == 'racecar'
    assert solution_function('madam') == 'madam'
    assert solution_function('aa') == 'aa'

def test_make_palindrome_symmetric_patterns(solution_function):
    """Test with strings that have symmetric patterns"""
    assert solution_function('abcba') == 'abcba'
    assert solution_function('12321') == '12321'
    assert solution_function('abccba') == 'abccba'

