# Specification 1: The result must be a palindrome
assert res == res[::-1]

# Specification 2: The result must start with the original input string
assert res.startswith(string)

# Specification 3: The length of the result must be at least as long as the input string
assert len(res) >= len(string)

# Specification 4: The suffix added to form the palindrome is the reverse of a prefix of the input string
added_suffix = res[len(string):]
assert string.startswith(added_suffix[::-1])

# Specification 5: The result is the shortest possible palindrome starting with the input string
# There should be no shorter string starting with `string` that is also a palindrome
assert all((string + string[:i][::-1] != res) for i in range(len(string)))
