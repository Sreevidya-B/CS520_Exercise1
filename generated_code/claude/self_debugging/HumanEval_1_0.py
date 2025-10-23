def separate_paren_groups(paren_string: str) -> List[str]:
    """
    Separates groups of nested parentheses into separate strings.
    
    Args:
        paren_string: A string containing multiple groups of nested parentheses.
        
    Returns:
        A list of strings, each containing a balanced group of parentheses.
    """
    # Remove spaces from the input string
    paren_string = paren_string.replace(" ", "")
    
    result = []
    current_group = ""
    depth = 0
    
    for char in paren_string:
        if char == '(':
            depth += 1
            current_group += char
        elif char == ')':
            depth -= 1
            current_group += char
            
            # If we've returned to depth 0, we've completed a group
            if depth == 0:
                result.append(current_group)
                current_group = ""
    
    return result