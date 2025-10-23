from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """
    Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    """
    # Sort the list to bring close elements next to each other
    numbers.sort()
    
    # Iterate through the sorted list and check the difference between consecutive elements
    for i in range(len(numbers) - 1):
        if numbers[i + 1] - numbers[i] < threshold:
            return True
    
    return False