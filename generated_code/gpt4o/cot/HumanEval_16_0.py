def count_distinct_characters(string: str) -> int:
    """ Given a string, find out how many distinct characters (regardless of case) does it consist of """
    return len(set(string.lower()))

# Example usage:
# print(count_distinct_characters('xyzXYZ'))  # Output: 3
# print(count_distinct_characters('Jerry'))   # Output: 4