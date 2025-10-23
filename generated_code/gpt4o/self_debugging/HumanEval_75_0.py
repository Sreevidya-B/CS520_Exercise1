def is_multiply_prime(a):
    def is_prime(n):
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

    if a < 2:
        return False

    primes = [i for i in range(2, a) if is_prime(i)]

    for i in range(len(primes)):
        for j in range(i, len(primes)):
            for k in range(j, len(primes)):
                if primes[i] * primes[j] * primes[k] == a:
                    return True
    return False

# 1. Potential bugs or edge cases:
#    - The function should handle numbers less than 2, which cannot be a product of three primes.
#    - The function should correctly identify when a number is not a product of three primes.
#    - The function should handle the upper limit of 100 correctly.

# 2. Explanation:
#    - The function first checks if the number is less than 2, returning False immediately.
#    - It generates a list of prime numbers less than the given number.
#    - It then checks all combinations of three primes to see if their product equals the given number.
#    - If a valid combination is found, it returns True; otherwise, it returns False.

# 3. The implementation is correct and handles the specified edge cases.