from typing import List, Tuple

def find_closest_elements(numbers: List[float]) -> Tuple[float, float]:
    """ From a supplied list of numbers (of length at least two) select and return two that are the closest to each
    other and return them in order (smaller number, larger number).
    >>> find_closest_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.2])
    (2.0, 2.2)
    >>> find_closest_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.0])
    (2.0, 2.0)
    """
    if len(numbers) < 2:
        raise ValueError("List must contain at least two numbers")
    
    # Sort the list to make finding closest pairs easier
    sorted_numbers = sorted(numbers)
    
    # Initialize with the first two elements
    min_diff = float('inf')
    closest_pair = (sorted_numbers[0], sorted_numbers[1])
    
    # Compare adjacent elements in the sorted list
    for i in range(len(sorted_numbers) - 1):
        current = sorted_numbers[i]
        next_num = sorted_numbers[i + 1]
        diff = abs(next_num - current)
        
        if diff < min_diff:
            min_diff = diff
            closest_pair = (current, next_num)
    
    return closest_pair