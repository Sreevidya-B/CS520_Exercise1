def make_a_pile(n):
    stones = []
    current_stones = n
    for _ in range(n):
        stones.append(current_stones)
        if current_stones % 2 == 0:
            current_stones += 2
        else:
            current_stones += 2
    return stones

# Example usage
print(make_a_pile(3))  # Output: [3, 5, 7]