# Corrected specifications for Problem 10 (gpt4o)

assert res == res[::-1]
assert res.startswith(string)
assert len(res) >= len(string)
assert string.startswith(res[len(string):][::-1])
assert len(res) <= len(string) * 2
