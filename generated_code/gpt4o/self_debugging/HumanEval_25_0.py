def factorize(n: int) -> List[int]:
    """ Return list of prime factors of given integer in the order from smallest to largest.
    Each of the factors should be listed number of times corresponding to how many times it appears in factorization.
    Input number should be equal to the product of all factors.
    """
    factors = []
    # Check for number of 2s that divide n
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    # n must be odd at this point, so a skip of 2 (i.e., i = i + 2) can be used
    for i in range(3, int(n**0.5) + 1, 2):
        # While i divides n, append i and divide n
        while n % i == 0:
            factors.append(i)
            n //= i
    # If n is a prime number greater than 2, then append it
    if n > 2:
        factors.append(n)
    return factors

# 1. Potential bugs or edge cases:
#    - Input is 1: The function should return an empty list since 1 has no prime factors.
#    - Input is a prime number: The function should return a list containing the number itself.
#    - Input is 0 or negative: The function should handle these gracefully, though typically factorization is defined for positive integers.

# 2. Handling:
#    - The function correctly handles the case where n is 1 by returning an empty list.
#    - For prime numbers, the function will return the number itself as a factor.
#    - The function does not explicitly handle 0 or negative numbers, as these are not typical inputs for factorization.

# 3. The implementation is correct for the intended use cases (positive integers).