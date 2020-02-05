from numpy import isclose


def to_float(number) -> float:
    """
    Cast numeric type to reals
    """

    if hasattr(number, "imag"):
        if isclose(number.imag, 0.0):
            return float(number.real)
        else:
            raise TypeError("imaginary part detected {number}".format(number=number))
    elif hasattr(number, "evalf"):
        tmp = complex(number.evalf())
        if hasattr(tmp, "imag") and isclose(tmp.imag, 0.0):
            return float(tmp.real)
        else:
            raise TypeError("casting number {number} of type {type} fo float failed".format(number=number, type=type(number)))
    else:
        try:
            return float(number)
        except TypeError:
            raise TypeError("casting number {number} of type {type} fo float failed".format(number=number, type=type(number)))