"""
@author: Manuel Martinez
@email: manmartgarc@gmail.com

This script defines two formulas used to calculate great-circle distances
using a haversine formula.
"""
from typing import List, Union
import numpy as np


def haversine(coords: np.array) -> np.array:
    """
    Returns the grea -circle distance in miles between two coordinates,
    or two pairs of coordinate arrays on a sphere
    (specified in decimal degrees)

    Taken from https://en.wikipedia.org/wiki/Haversine_formula

    Parameters
    ----------
    coord0:     First coordinate pair(s)
    coord1:     Second coordinate pair(s)

    Returns
    -------
    >>> haversine([3,5], [4,7])
    154.27478490048566

    >>> haversine((41.325, -72.325), (41.327, -72.327))
    0.17282397386672291
    """
    r = 3959  # radius of the earth

    coords = np.array(coords)
    # assert length of coordinates pairs to be compared
    if coords.shape[1] != 4:
        raise ValueError('Coords matrix must only have 4 dimensions')
    coords = np.radians(coords)

    # add dimension if only one dimensional vector
    if len(coords.shape) == 1:
        coords = coords.reshape(1, -1)

    # difference in phis
    a = np.square((coords[:, 2] - coords[:, 0]) / 2)
    # difference in lambdas
    b = np.square((coords[:, 3] - coords[:, 1]) / 2)
    # cosines of phis0
    phicos0 = np.cos(coords[:, 0])
    # cosine of phis1
    phicos1 = np.cos(coords[:, 2])

    # calculate distance
    d = 2 * r * np.arcsin(np.sqrt(a + phicos0 * phicos1 * b))
    # ( ͡° ͜ʖ ͡°)
    return d


def total_distance(coords: List[float]) -> float:
    """
    Calculates the sum of haversine distances within an array of
    coordinates.

    Parameters:
    ----------
    points: array of coordinate pairs

    Returns
    -------
    Returns the length of a path passing throughout all the points
    in a given order

    >>> total_distance([[1,2], [4,6]])
    5.0
    >>> total_distance([[3,6], [7,6], [12,6]])
    9.0
    """
    # restructure coordinates coordinate array in the following fashion
    # [[3, 5], [4, 6], [5, 7]] -> [[3, 5, 4, 6], [4, 6, 5, 7], [4, 6, 4, 6]]
    coords = np.hstack([coords, np.roll(coords, shift=-1, axis=0)])

    # replace last distance calculation to be 0
    coords[-1, -2:] = coords[-1, :-2]

    # calculate total distance
    totald = np.sum(haversine(coords[:, :2], coords[:, 2:]))

    return totald
