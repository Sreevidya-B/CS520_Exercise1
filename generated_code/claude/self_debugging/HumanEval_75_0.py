def is_multiply_prime(a):
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
    
    # Check for factor 2
    while a % 2 == 0:
        prime_factors.append(2)
        a //= 2
    
    # Check for odd factors
    factor = 3
    while factor * factor <= a:
        while a % factor == 0:
            prime_factors.append(factor)
            a //= factor
        factor += 2
    
    # If a is a prime number greater than 2
    if a > 2:
        prime_factors.append(a)
    
    # Check if there are exactly 3 prime factors
    return len(prime_factors) == 3