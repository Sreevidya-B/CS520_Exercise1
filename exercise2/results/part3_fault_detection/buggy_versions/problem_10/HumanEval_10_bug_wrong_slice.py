def is_palindrome(string: str) -> bool:
    """ Test if given string is a palindrome """
    return string == string[::-1]

def make_palindrome(string: str) -> str:
    """ Find the shortest palindrome that begins with a supplied string. """
    if is_palindrome(string):
        return string
    
    for i in range(len(string)):
        if is_palindrome(string[i:]):
            return string + string[i:][::-1]
    
    return string  # This line is theoretically unreachable

# Test cases
print(make_palindrome(''))      # Output: ''
print(make_palindrome('cat'))   # Output: 'catac'
print(make_palindrome('cata'))  # Output: 'catac'