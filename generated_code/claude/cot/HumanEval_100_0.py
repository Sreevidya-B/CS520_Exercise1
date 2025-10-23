def make_a_pile(n):
    """
    Given a positive integer n, you have to make a pile of n levels of stones.
    The first level has n stones.
    The number of stones in the next level is:
        - the next odd number if n is odd.
        - the next even number if n is even.
    Return the number of stones in each level in a list, where element at index
    i represents the number of stones in the level (i+1).

    Examples:
    >>> make_a_pile(3)
    [3, 5, 7]
    """
    result = [n]
    
    # Determine if n is odd or even
    is_odd = n % 2 == 1
    
    for i in range(1, n):
        if is_odd:
            # If n is odd, add the next odd number
            result.append(result[-1] + 2)
        else:
            # If n is even, add the next even number
            result.append(result[-1] + 2)
    
    return result