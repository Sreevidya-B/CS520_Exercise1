from typing import List

def is_prime(n: int) -> bool:
    """Check if a number is a prime number."""
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

def generate_primes(upper_limit: int) -> List[int]:
    """Generate a list of prime numbers up to a given upper limit."""
    primes = []
    for num in range(2, upper_limit + 1):
        if is_prime(num):
            primes.append(num)
    return primes

def is_multiply_prime(a: int) -> bool:
    """Check if the given number is the multiplication of 3 prime numbers."""
    if a < 2:
        return False
    
    primes = generate_primes(100)
    n = len(primes)
    
    for i in range(n):
        for j in range(i, n):
            for k in range(j, n):
                if primes[i] * primes[j] * primes[k] == a:
                    return True
    return False