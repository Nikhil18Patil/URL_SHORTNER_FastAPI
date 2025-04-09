import string

BASE62 = string.digits + string.ascii_letters

def encode_base62(num: int) -> str:
    """Converts an integer to a base62 string."""
    if num == 0:
        return BASE62[0]
    result = ""
    base = len(BASE62)
    while num:
        num, rem = divmod(num, base)
        result = BASE62[rem] + result
    return result
