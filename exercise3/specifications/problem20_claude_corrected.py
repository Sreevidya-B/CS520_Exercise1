# Corrected specifications for Problem 20 (claude)

assert isinstance(res, tuple) and len(res) == 2
assert res[0] <= res[1]
assert res[0] in numbers and res[1] in numbers
assert all(abs(res[1] - res[0]) <= abs(b - a) for a in numbers for b in numbers if b > a)
assert len(numbers) >= 2
