def truncate_number(number: float) -> float:
    """
    Given a positive floating point number, it can be decomposed into
    an integer part (largest integer smaller than given number) and decimals
    (leftover part always smaller than 1).

    Return the decimal part of the number.
    
    >>> truncate_number(3.5)
    0.5
    """
    # Get the integer part by using int() which truncates toward zero
    integer_part = int(number)
    
    # Return the decimal part by subtracting the integer part
    return number - integer_part