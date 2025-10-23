from typing import List, Set

def is_multiply_prime(a: int) -> bool:
    """
    Returns true if the given number is the multiplication of exactly 3 prime numbers
    and false otherwise.
    
    Args:
        a: An integer less than 100
        
    Returns:
        bool: True if a is a product of exactly 3 prime numbers, False otherwise
    
    Example:
        is_multiply_prime(30) == True  # 30 = 2 * 3 * 5
    """
    if a <= 1:
        return False
    
    # Get prime factors
    prime_factors = []
    
    # Check if 2 is a factor
    while a % 2 == 0:
        prime_factors.append(2)
        a //= 2
    
    # Check for other prime factors
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