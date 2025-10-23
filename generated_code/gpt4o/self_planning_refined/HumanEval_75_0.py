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

def is_multiply_prime(a: int) -> bool:
    """Check if the number is the multiplication of 3 prime numbers."""
    if a < 2:
        return False
    
    primes = [i for i in range(2, a) if is_prime(i)]
    
    for i in range(len(primes)):
        for j in range(i, len(primes)):
            for k in range(j, len(primes)):
                if primes[i] * primes[j] * primes[k] == a:
                    return True
    return False