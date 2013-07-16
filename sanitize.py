import string
valid_chars = frozenset(list("-_.() %s%s" % (string.ascii_letters, string.digits)))

def sanitize(s):
    return ''.join(c for c in s if c in valid_chars)
