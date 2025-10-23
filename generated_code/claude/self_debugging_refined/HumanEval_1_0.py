from typing import List


def separate_paren_groups(paren_string: str) -> List[str]:
    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    """
    result = []
    current_string = []
    paren_level = 0
    
    # Remove spaces
    paren_string = paren_string.replace(" ", "")
    
    for char in paren_string:
        if char == '(':
            current_string.append(char)
            paren_level += 1
        elif char == ')':
            current_string.append(char)
            paren_level -= 1
            
            # If we've closed a group, add it to the result
            if paren_level == 0:
                result.append(''.join(current_string))
                current_string = []
    
    return result