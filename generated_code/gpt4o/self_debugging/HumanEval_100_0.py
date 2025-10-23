def make_a_pile(n):
    pile = []
    current_stones = n
    for _ in range(n):
        pile.append(current_stones)
        if n % 2 == 0:
            current_stones += 2
        else:
            current_stones += 2
    return pile

# Test cases
print(make_a_pile(3))  # [3, 5, 7]
print(make_a_pile(4))  # [4, 6, 8, 10]