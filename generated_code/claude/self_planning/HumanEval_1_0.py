def separate_paren_groups(paren_string: str) -> List[str]:
    """
    Separates groups of nested parentheses into separate strings.
    
    Args:
        paren_string: A string containing multiple groups of nested parentheses.
        
    Returns:
        A list of strings, each containing a balanced group of parentheses.
    """
    # Remove all spaces from the input string
    paren_string = paren_string.replace(" ", "")
    
    result = []
    stack = []
    current_group = ""
    
    for char in paren_string:
        current_group += char
        
        if char == '(':
            stack.append(char)
        elif char == ')':
            stack.pop()
            
            # If stack is empty, we've completed a balanced group
            if not stack:
                result.append(current_group)
                current_group = ""
    
    return result