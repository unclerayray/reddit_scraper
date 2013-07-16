__doc__ = """Method for sanitizing strings to get safe filenames."""

import string
valid_chars = frozenset(''.join(("-_.() ", string.ascii_letters, string.digits)))

def sanitize(s):
    return ''.join(c for c in s if c in valid_chars)
