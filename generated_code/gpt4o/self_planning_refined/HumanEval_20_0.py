from typing import List, Tuple

def find_closest_elements(numbers: List[float]) -> Tuple[float, float]:
    # Sort the numbers to make it easier to find the closest pair
    sorted_numbers = sorted(numbers)
    
    # Initialize variables to store the minimum difference and the closest pair
    min_diff = float('inf')
    closest_pair = (0.0, 0.0)
    
    # Iterate through the sorted list and find the pair with the smallest difference
    for i in range(len(sorted_numbers) - 1):
        diff = sorted_numbers[i + 1] - sorted_numbers[i]
        if diff < min_diff:
            min_diff = diff
            closest_pair = (sorted_numbers[i], sorted_numbers[i + 1])
    
    return closest_pair