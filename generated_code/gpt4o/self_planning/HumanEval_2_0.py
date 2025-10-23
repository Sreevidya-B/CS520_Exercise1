def truncate_number(number: float) -> float:
    """ Given a positive floating point number, it can be decomposed into
    an integer part (largest integer smaller than given number) and decimals
    (leftover part always smaller than 1).

    Return the decimal part of the number.
    """
    # Subtract the integer part from the number to get the decimal part
    integer_part = int(number)
    decimal_part = number - integer_part
    return decimal_part

# Edge cases:
# - If the number is an integer, the decimal part should be 0.0
# - If the number is very close to an integer, ensure precision is handled correctly