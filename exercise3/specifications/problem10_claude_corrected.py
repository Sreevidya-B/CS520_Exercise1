# Corrected specifications for Problem 10 (claude)

assert all(res[i] == res[len(res)-1-i] for i in range(len(res)//2))
assert res.startswith(string)
assert len(res) >= len(string)
assert len(res) <= len(string) * 2
assert (len(string) <= 1) <= (res == string)
