def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """
    Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    
    Args:
        numbers: List of float numbers to check
        threshold: The maximum allowed difference between any two numbers
        
    Returns:
        True if any two numbers are closer than threshold, False otherwise
    """
    n = len(numbers)
    
    # Compare each pair of numbers
    for i in range(n):
        for j in range(i + 1, n):
            if abs(numbers[i] - numbers[j]) < threshold:
                return True
    
    return False