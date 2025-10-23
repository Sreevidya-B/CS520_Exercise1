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
    closest_pair = (sorted_numbers[0], sorted_numbers[1])
    min_diff = abs(sorted_numbers[1] - sorted_numbers[0])
    
    # Check each adjacent pair in the sorted list
    for i in range(1, len(sorted_numbers) - 1):
        current_diff = abs(sorted_numbers[i+1] - sorted_numbers[i])
        if current_diff < min_diff:
            min_diff = current_diff
            closest_pair = (sorted_numbers[i], sorted_numbers[i+1])
    
    return closest_pair