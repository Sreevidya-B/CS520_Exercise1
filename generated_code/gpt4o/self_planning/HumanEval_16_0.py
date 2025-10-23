def count_distinct_characters(string: str) -> int:
    # Convert the string to lowercase to ensure case insensitivity
    string = string.lower()
    # Use a set to store distinct characters
    distinct_characters = set(string)
    # Return the number of distinct characters
    return len(distinct_characters)

# Test cases
print(count_distinct_characters('xyzXYZ'))  # Output: 3
print(count_distinct_characters('Jerry'))   # Output: 4