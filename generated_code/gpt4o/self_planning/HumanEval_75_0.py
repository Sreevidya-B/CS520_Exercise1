def is_multiply_prime(a):
    """Returns true if the given number is the multiplication of 3 prime numbers and false otherwise."""
    
    # List of prime numbers less than 100
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    
    # Check all combinations of three different primes
    for i in range(len(primes)):
        for j in range(i + 1, len(primes)):
            for k in range(j + 1, len(primes)):
                if primes[i] * primes[j] * primes[k] == a:
                    return True
    return False

# Example usage:
# print(is_multiply_prime(30))  # Should return True
# print(is_multiply_prime(60))  # Should return False