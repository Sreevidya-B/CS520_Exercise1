from typing import List

def separate_paren_groups(paren_string: str) -> List[str]:
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
            current_group = []  # Reset for the next group
    
    return result