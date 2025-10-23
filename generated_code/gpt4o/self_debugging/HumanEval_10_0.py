def make_palindrome(string: str) -> str:
    """ Find the shortest palindrome that begins with a supplied string. """
    if not string:
        return string
    
    # Check each suffix of the string to find the longest palindromic suffix
    for i in range(len(string)):
        if is_palindrome(string[i:]):
            # Append the reverse of the prefix before the palindromic suffix
            return string + string[:i][::-1]
    return string

# Test cases
print(make_palindrome(''))       # ''
print(make_palindrome('cat'))    # 'catac'
print(make_palindrome('cata'))   # 'catac'