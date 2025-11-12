"""
Test suite for HumanEval/16 - count_distinct_characters
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
    assert candidate('') == 0
    assert candidate('abcde') == 5
    assert candidate('abcde' + 'cade' + 'CADE') == 5
    assert candidate('aaaaAAAAaaaa') == 1
    assert candidate('Jerry jERRY JeRRRY') == 5


@pytest.fixture
def solution_function(request):
    model = request.config.getoption("--model", default="gpt4o")
    strategy = request.config.getoption("--strategy", default="cot")
    module = get_solution_module(model, strategy, "16")
    return getattr(module, "count_distinct_characters")

def test_count_distinct_characters_humaneval(solution_function):
    check(solution_function)


# LLM-Generated Tests (Accumulated)


# --- Iteration 1 Tests ---

import pytest
from typing import Any

def count_distinct_characters(string: str) -> int:
    """ Given a string, find out how many distinct characters (regardless of case) does it consist of """
    return len(set(string.lower()))

class TestCountDistinctCharacters:
    
    def test_empty_string(self):
        # Test with empty string - should return 0
        assert solution_function("") == 0
    
    def test_single_character(self):
        # Test with single character - should return 1
        assert solution_function("a") == 1
        assert solution_function("A") == 1
    
    def test_same_character_repeated(self):
        # Test with same character repeated - should return 1
        assert solution_function("aaaa") == 1
        assert solution_function("AAAA") == 1
        assert solution_function("aAaA") == 1
    
    def test_mixed_case_characters(self):
        # Test with mixed case - should be case insensitive
        assert solution_function("xyzXYZ") == 3
        assert solution_function("aAbBcC") == 3
        assert solution_function("Hello") == 4
    
    def test_all_distinct_characters(self):
        # Test with all unique characters
        assert solution_function("abcdef") == 6
        assert solution_function("Jerry") == 4
        assert solution_function("python") == 6
    
    def test_special_characters_and_numbers(self):
        # Test with special characters and numbers
        assert solution_function("123") == 3
        assert solution_function("!@#$") == 4
        assert solution_function("a1b2c3") == 6
        assert solution_function("Hello, World!") == 10
    
    def test_whitespace_characters(self):
        # Test with whitespace characters
        assert solution_function("a b c") == 4  # includes space
        assert solution_function("   ") == 1    # only spaces
        assert solution_function("\t\n\r") == 3 # different whitespace chars
    
    def test_unicode_characters(self):
        # Test with unicode characters
        assert solution_function("café") == 4
        assert solution_function("naïve") == 5
        assert solution_function("résumé") == 6
    
    def test_very_long_string(self):
        # Test with very long string
        long_string = "a" * 1000 + "b" * 1000
        assert solution_function(long_string) == 2
    
    def test_all_ascii_printable(self):
        # Test with various ASCII characters
        ascii_string = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        assert solution_function(ascii_string) == 36  # 10 digits + 26 letters
    
    def test_none_input_raises_exception(self):
        # Test that None input raises AttributeError
        with pytest.raises(AttributeError):
            solution_function(None)
    
    def test_non_string_input_raises_exception(self):
        # Test that non-string inputs raise AttributeError
        with pytest.raises(AttributeError):
            solution_function(123)
        
        with pytest.raises(AttributeError):
            solution_function(['a', 'b', 'c'])
        
        with pytest.raises(AttributeError):
            solution_function({'a': 1, 'b': 2})
    
    def test_string_with_newlines_and_tabs(self):
        # Test with strings containing newlines and tabs
        assert solution_function("hello\nworld") == 9
        assert solution_function("a\tb\tc") == 4
    
    def test_palindrome_strings(self):
        # Test with palindrome strings
        assert solution_function("racecar") == 4
        assert solution_function("madam") == 3
        assert solution_function("A man a plan a canal Panama") == 9

# --- Iteration 2 Tests ---

import pytest

def test_count_distinct_characters_empty_string(solution_function):
    assert solution_function('') == 0

def test_count_distinct_characters_single_character(solution_function):
    assert solution_function('a') == 1

def test_count_distinct_characters_all_same_character(solution_function):
    assert solution_function('aaaa') == 1

def test_count_distinct_characters_mixed_case_repeated(solution_function):
    assert solution_function('AaAaAa') == 1

def test_count_distinct_characters_special_characters(solution_function):
    assert solution_function('!@#$%') == 5

# --- Iteration 3 Tests ---

import pytest

def test_count_distinct_characters_with_spaces(solution_function):
    assert solution_function('a b c') == 4

def test_count_distinct_characters_with_numbers(solution_function):
    assert solution_function('abc123') == 6

def test_count_distinct_characters_with_special_chars(solution_function):
    assert solution_function('a!@#a') == 4

def test_count_distinct_characters_mixed_case_numbers(solution_function):
    assert solution_function('AaA111') == 2

def test_count_distinct_characters_whitespace_only(solution_function):
    assert solution_function('   ') == 1
