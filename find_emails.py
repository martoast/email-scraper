import re

def find_emails(text: str) -> set:
    """Find all email addresses in a given string.

    Args:
        text (str): The string to search for email addresses.

    Returns:
        set: A set of email addresses found in the string.
    """
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    return set(re.findall(email_pattern, text))
