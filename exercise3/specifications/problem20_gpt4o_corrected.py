# Corrected specifications for Problem 20 (gpt4o)

assert res[0] in numbers and res[1] in numbers and res[0] != res[1]
assert res[0] < res[1]
assert all(abs(res[1] - res[0]) <= abs(x - y) for x in numbers for y in numbers if x != y)
assert len(numbers) >= 2
assert isinstance(res[0], (int, float)) and isinstance(res[1], (int, float))
