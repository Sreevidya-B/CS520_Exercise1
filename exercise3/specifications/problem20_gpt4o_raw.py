# Specification 1: The result must be a tuple of two distinct elements from the input list
assert res[0] in numbers and res[1] in numbers and res[0] != res[1]

# Specification 2: The two elements must be in increasing order
assert res[0] < res[1]

# Specification 3: The difference between the two returned elements is minimal among all pairs in the list
assert all(abs(res[1] - res[0]) <= abs(x - y) for x in numbers for y in numbers if x != y)

# Specification 4: Input list must contain at least two elements
assert len(numbers) >= 2

# Specification 5: Returned values must preserve floating-point type (if inputs are float)
assert isinstance(res[0], float) and isinstance(res[1], float)
