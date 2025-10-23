def is_multiply_prime(a):
    """
    Returns true if the given number is the multiplication of 3 prime numbers
    and false otherwise.
    Knowing that (a) is less than 100.
    """
    # Generate primes up to sqrt(100)
    def get_primes(n):
        primes = []
        sieve = [True] * (n + 1)
        for p in range(2, n + 1):
            if sieve[p]:
                primes.append(p)
                for i in range(p * p, n + 1, p):
                    sieve[i] = False
        return primes
    
    primes = get_primes(int(100 ** 0.5) + 1)
    
    # Check if a is a product of exactly 3 primes
    prime_factors = []
    
    # Edge case: if a is 1 or negative, return False
    if a <= 1:
        return False
    
    # Find prime factors
    for p in primes:
        while a % p == 0:
            prime_factors.append(p)
            a //= p
        if a == 1:
            break
    
    # If a is not 1 after division by all primes up to sqrt(100),
    # then a itself is a prime number
    if a > 1:
        prime_factors.append(a)
    
    # Return True if there are exactly 3 prime factors
    return len(prime_factors) == 3