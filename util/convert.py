from typing import List


def dec_to_base(dec_int: int, base: int, lowest_first: bool = False, pad_to_length: int = 0) -> List[int]:
    """Converts a single decimal value to its' equivalent in any other base. Returns a list of integers with the value
    for each order of magnitude, highest value first. Conversion of these values to single-character representations is
    up to the user.

    A base 'n' means the following:

    m * n**0, m * n**1, m * n**2, m * n**3, etc. with 0 <= m < n.

    The exponent is your 'order of magnitude', n is the base we're working in an 'm' is the range of possible values in
    this magnitude.

    Base 2:  m* 2**0, m* 2**1, m* 2**2, m* 2**3, etc. with m == 0 or 1
    Base 23: m*23**0, m*23**1, m*23**2, m*23**3, etc. with m == range(0,23)
    """
    if dec_int == 0:
        return [0]

    if base == 0 or base == 1:
        raise ValueError(f"You cannot express a number in base {base}.")

    digits = []
    while dec_int:
        digits.append(int(dec_int % base))
        dec_int //= base

    while len(digits) < pad_to_length:
        digits.append(0)

    return digits[::1 if lowest_first else -1]
