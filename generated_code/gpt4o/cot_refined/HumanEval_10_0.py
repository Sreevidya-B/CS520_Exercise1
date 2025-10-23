from typing import List, Tuple, Dict, Optional

def is_palindrome(string: str) -> bool:
    """ Test if given string is a palindrome """
    return string == string[::-1]

def make_palindrome(string: str) -> str:
    """ Find the shortest palindrome that begins with a supplied string.
    Algorithm idea is simple:
    - Find the longest postfix of supplied string that is a palindrome.
    - Append to the end of the string reverse of a string prefix that comes before the palindromic suffix.
    """
    if not string:
        return string
    
    for i in range(len(string)):
        if is_palindrome(string[i:]):
            return string + string[:i][::-1]
    
    return string

# Example usage
if __name__ == "__main__":
    print(make_palindrome(''))        # Output: ''
    print(make_palindrome('cat'))     # Output: 'catac'
    print(make_palindrome('cata'))    # Output: 'catac'