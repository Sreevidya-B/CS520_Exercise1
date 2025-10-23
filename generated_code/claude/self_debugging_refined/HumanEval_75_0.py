def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_multiply_prime(a):
    """Write a function that returns true if the given number is the multiplication of 3 prime numbers
    and false otherwise.
    Knowing that (a) is less then 100. 
    Example:
    is_multiply_prime(30) == True
    30 = 2 * 3 * 5
    """
    # Handle edge cases
    if a < 8:  # Smallest product of 3 primes is 2*2*2=8
        return False
    
    # Find all prime factors
    prime_factors = []
    n = a
    for i in range(2, int(a**0.5) + 1):
        while n % i == 0 and is_prime(i):
            prime_factors.append(i)
            n //= i
    
    if n > 1 and is_prime(n):
        prime_factors.append(n)
    
    # Check if we have exactly 3 prime factors (can include duplicates)
    return len(prime_factors) == 3