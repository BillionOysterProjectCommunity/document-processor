from typing import List

import numpy as np


def check_digit(v: str):

    n = []
    s = ""

    for char in v:
        if char.isdigit():
            n.append(char)
        else:
            pass

    i = s.join(n)

    return i


def filter_nums(x):
    try:
        x = int(x)
    except ValueError:
        return np.nan
    # Prevent outliers from misread data points.
    if x >= 15 and x <= 200:
        return x
    else:
        return np.nan


def filter_strings(x):
    if str(x) == "L":  # Live Oyster Classifier
        return x
    if str(x) == "D":  # Dead Oyster Classifier
        return x
    else:
        return np.nan


def truncate(v: np.array) -> List:
    """
    Returns an array of 1 dimensional elements
    """
    return [x[0] for x in v]
