from typing import List, Tuple

def find_closest_elements(numbers: List[float]) -> Tuple[float, float]:
    # Sort the numbers to make it easier to find the closest pair
    numbers.sort()
    
    # Initialize variables to store the minimum difference and the closest pair
    min_diff = float('inf')
    closest_pair = (0.0, 0.0)
    
    # Iterate through the sorted list and find the pair with the smallest difference
    for i in range(len(numbers) - 1):
        diff = numbers[i + 1] - numbers[i]
        if diff < min_diff:
            min_diff = diff
            closest_pair = (numbers[i], numbers[i + 1])
    
    return closest_pair