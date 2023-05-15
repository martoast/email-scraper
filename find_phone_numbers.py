import re

def find_phone_numbers(text: str) -> set:
    """Find all phone numbers in a given string.

    Args:
        text (str): The string to search for phone numbers.

    Returns:
        set: A set of phone numbers found in the string.
    """
    phone_pattern = re.compile(r'\+\d{1,3}\s\d{1,3}\s\d{1,3}\s\d{4}')
    return set(re.findall(phone_pattern, text))
