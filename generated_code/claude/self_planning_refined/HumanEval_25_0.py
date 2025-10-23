from typing import List

def factorize(n: int) -> List[int]:
    """ Return list of prime factors of given integer in the order from smallest to largest.
    Each of the factors should be listed number of times corresponding to how many times it appeares in factorization.
    Input number should be equal to the product of all factors
    >>> factorize(8)
    [2, 2, 2]
    >>> factorize(25)
    [5, 5]
    >>> factorize(70)
    [2, 5, 7]
    """
    factors = []
    
    # Handle edge case
    if n <= 1:
        return factors
    
    # Check for factor 2 first (optimization)
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    
    # Check for odd factors
    factor = 3
    while factor * factor <= n:
        while n % factor == 0:
            factors.append(factor)
            n //= factor
        factor += 2  # Only check odd numbers
    
    # If n is a prime number greater than 2
    if n > 1:
        factors.append(n)
    
    return factors