from typing import List

def separate_paren_groups(paren_string: str) -> List[str]:
    """
    Input to this function is a string containing multiple groups of nested parentheses. 
    Your goal is to separate those groups into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other.
    Ignore any spaces in the input string.
    """
    # Remove spaces from the input string
    paren_string = paren_string.replace(" ", "")
    
    # Initialize variables
    result = []
    current_group = []
    balance = 0
    
    # Iterate over each character in the string
    for char in paren_string:
        # Add character to the current group
        current_group.append(char)
        
        # Update balance
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
        
        # If balance is zero, we have a complete group
        if balance == 0:
            result.append(''.join(current_group))
            current_group = []  # Reset current group for the next set of parentheses
    
    return result

# Example usage
# print(separate_paren_groups('( ) (( )) (( )( ))'))  # Output: ['()', '(())', '(()())']