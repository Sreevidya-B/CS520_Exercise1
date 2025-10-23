def count_distinct_characters(string: str) -> int:
    """
    Given a string, find out how many distinct characters (regardless of case) does it consist of
    
    >>> count_distinct_characters('xyzXYZ')
    3
    >>> count_distinct_characters('Jerry')
    4
    """
    # Convert string to lowercase to make it case-insensitive
    lowercase_string = string.lower()
    
    # Use a set to count unique characters
    unique_chars = set(lowercase_string)
    
    # Return the count of unique characters
    return len(unique_chars)