# Specification 1: Result must be a palindrome (reads the same forward and backward)
assert all(res[i] == res[len(res)-1-i] for i in range(len(res)//2))

# Specification 2: Result must start with the input string
assert res.startswith(string)

# Specification 3: Result must be at least as long as input string
assert len(res) >= len(string)

# Specification 4: Result must be the shortest possible palindrome starting with input string
assert not any(p.startswith(string) and all(p[i] == p[len(p)-1-i] for i in range(len(p)//2)) 
               for p in [res[:i] for i in range(len(string), len(res))])

# Specification 5: For empty or single char input, result equals input
assert (len(string) <= 1) <= (res == string)