def truncate_number(number: float) -> float:
    """ Given a positive floating point number, it can be decomposed into
    an integer part (largest integer smaller than given number) and decimals
    (leftover part always smaller than 1).

    Return the decimal part of the number.
    """
    return number - int(number)

# Test cases
print(truncate_number(3.5))  # Expected: 0.5
print(truncate_number(0.0))  # Expected: 0.0
print(truncate_number(5.999))  # Expected: 0.999
print(truncate_number(10.0))  # Expected: 0.0