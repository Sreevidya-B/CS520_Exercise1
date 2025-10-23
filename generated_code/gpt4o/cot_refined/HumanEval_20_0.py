from typing import List, Tuple

def find_closest_elements(numbers: List[float]) -> Tuple[float, float]:
    """ From a supplied list of numbers (of length at least two) select and return two that are the closest to each
    other and return them in order (smaller number, larger number).
    """
    if len(numbers) < 2:
        raise ValueError("The list must contain at least two numbers.")
    
    # Sort the numbers to make it easier to find the closest pair
    sorted_numbers = sorted(numbers)
    min_diff = float('inf')
    closest_pair = (sorted_numbers[0], sorted_numbers[1])
    
    # Iterate through the sorted list and find the smallest difference
    for i in range(len(sorted_numbers) - 1):
        diff = sorted_numbers[i + 1] - sorted_numbers[i]
        if diff < min_diff:
            min_diff = diff
            closest_pair = (sorted_numbers[i], sorted_numbers[i + 1])
    
    return closest_pair