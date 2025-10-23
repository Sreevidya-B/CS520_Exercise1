def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def is_multiply_prime(a: int) -> bool:
    """
    Returns true if the given number is the multiplication of 3 prime numbers
    and false otherwise.
    
    Args:
        a: An integer less than 100
        
    Returns:
        bool: True if a is a product of exactly 3 prime numbers, False otherwise
    """
    # Handle edge cases
    if a <= 1:
        return False
    
    # Find all prime factors
    prime_factors = []
    factor = 2
    temp_a = a
    
    while factor * factor <= temp_a:
        while temp_a % factor == 0:
            prime_factors.append(factor)
            temp_a //= factor
        factor += 1
    
    if temp_a > 1:
        prime_factors.append(temp_a)
    
    # Check if there are exactly 3 prime factors
    if len(prime_factors) == 3:
        return True
    
    # Check if there are fewer than 3 prime factors but some are repeated
    # For example: 2*2*3 = 12, which has 3 prime factors but only 2 unique ones
    return False