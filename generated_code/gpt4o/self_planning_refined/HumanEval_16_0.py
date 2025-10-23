def count_distinct_characters(string: str) -> int:
    """ Given a string, find out how many distinct characters (regardless of case) does it consist of """
    # Convert the string to lowercase to ensure case insensitivity
    lower_string = string.lower()
    
    # Use a set to store distinct characters
    distinct_characters = set(lower_string)
    
    # Return the number of distinct characters
    return len(distinct_characters)

# Example usage:
# print(count_distinct_characters('xyzXYZ'))  # Output: 3
# print(count_distinct_characters('Jerry'))   # Output: 4