import random

def generate_cookie_value():
    """
    >>> len(generate_cookie_value())
    128

    """

    return str("".join(random.choice("0123456789ABCEDFabcdef@&!") for i in range(128)))

def addition(a,b):
    """
    >>> addition(2,4)
    {'result': 6}
    """
    y = int(a)+int(b)
    return {'result': y }