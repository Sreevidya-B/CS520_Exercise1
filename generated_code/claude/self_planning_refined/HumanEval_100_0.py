from typing import List

def make_a_pile(n: int) -> List[int]:
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
    current = n
    
    for _ in range(n - 1):
        if current % 2 == 0:  # If current is even
            current += 2  # Next even number
        else:  # If current is odd
            current += 2  # Next odd number
        
        result.append(current)
    
    return result