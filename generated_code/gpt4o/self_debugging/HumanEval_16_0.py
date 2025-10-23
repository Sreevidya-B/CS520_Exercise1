def count_distinct_characters(string: str) -> int:
    """ Given a string, find out how many distinct characters (regardless of case) does it consist of """
    return len(set(string.lower()))

# Edge cases and handling:
# 1. Empty string: The function will return 0 as there are no characters.
# 2. Case insensitivity: The function converts the string to lowercase, ensuring 'A' and 'a' are considered the same.
# 3. Non-alphabetic characters: The function will count distinct non-alphabetic characters as well.