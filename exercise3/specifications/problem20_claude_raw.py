# Specification 1: Result contains exactly two numbers
assert isinstance(res, tuple) and len(res) == 2

# Specification 2: First number in result is smaller than or equal to second
assert res[0] <= res[1]

# Specification 3: Both numbers in result must be from input list
assert res[0] in numbers and res[1] in numbers

# Specification 4: Distance between result numbers is minimal among all pairs
assert all(abs(res[1] - res[0]) <= abs(b - a) 
          for a in numbers for b in numbers if b > a)

# Specification 5: Input list must have at least two elements
assert len(numbers) >= 2