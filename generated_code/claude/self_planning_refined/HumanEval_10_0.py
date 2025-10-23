def is_palindrome(string: str) -> bool:
    """ Test if given string is a palindrome """
    return string == string[::-1]


def make_palindrome(string: str) -> str:
    """ Find the shortest palindrome that begins with a supplied string.
    Algorithm idea is simple:
    - Find the longest postfix of supplied string that is a palindrome.
    - Append to the end of the string reverse of a string prefix that comes before the palindromic suffix.
    >>> make_palindrome('')
    ''
    >>> make_palindrome('cat')
    'catac'
    >>> make_palindrome('cata')
    'catac'
    """
    # Edge case: empty string or already a palindrome
    if not string or is_palindrome(string):
        return string
    
    # Find the longest palindromic suffix
    for i in range(len(string), 0, -1):
        if is_palindrome(string[:i]):
            # Found the longest palindromic suffix
            # Append the reverse of the remaining prefix
            return string + string[i:][::-1]
    
    # If no palindromic suffix found (should never reach here as single characters are palindromes)
    return string + string[1:][::-1]