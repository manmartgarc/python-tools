"""
@author: Manuel Martinez
@email: manmartgarc@gmail.com

This script defines two formulas used to calculate great-circle distances
using a haversine formula.

Taken from https://en.wikipedia.org/wiki/Haversine_formula
"""

import numpy as np


def haversine(coord1, coord2, enum=False):
    """
    Returns the great-circle distance in miles between two points on a
    sphere given their coordinates as a pair of tuples or lists.

    Parameters
    ----------
    coord1: list or tuple
        First coordinate pair
    coord2: list or tuple
        Second coordinate pair
    enum: boolean
        Establishes whether coordinates are enumerated or indexed.

    Returns
    -------
    >>> haversine_coord([3,5], [4,7])
    154.27478490048566

    >>> haversine_coord((41.325, -72.325), (41.327, -72.327))
    0.17282397386672291
    """

    # assert length of coordinates
    assert len(coord1) + len(coord2) == 4, 'Coordinates exceed object length'

    r = 3959  # radius of the earth

    if enum is False:
        r_lat = np.radians(coord1[0])
        r_lat2 = np.radians(coord2[0])
        delta_r_lat = np.radians(coord2[0] - coord1[0])
        delta_r_lon = np.radians(coord2[1] - coord1[1])

        a = (np.sin(delta_r_lat / 2) * np.sin(delta_r_lat / 2) +
             np.cos(r_lat) * np.cos(r_lat2) *
             np.sin(delta_r_lon / 2) * np.sin(delta_r_lon / 2))
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        d = r * c

        return d

    else:
        r_lat = np.radians(coord1[1][0])
        r_lat2 = np.radians(coord2[1][0])
        delta_r_lat = np.radians(coord2[1][0] - coord1[1][0])
        delta_r_lon = np.radians(coord2[1][1] - coord1[1][1])

        a = (np.sin(delta_r_lat / 2) * np.sin(delta_r_lat / 2) +
             np.cos(r_lat) * np.cos(r_lat2) *
             np.sin(delta_r_lon / 2) * np.sin(delta_r_lon / 2))
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        d = r * c

        return d


def total_distance(points):
    """
    Calculates the sum of haversine distances within an array of
    coordinates.

    Parameters:
    ----------
    points: list or array-like
        array of coordinate pairs

    Returns
    -------
    Returns the length of a path passing throughout all the points
    in a given order

    >>> total_distance([[1,2], [4,6]])
    5.0
    >>> total_distance([[3,6], [7,6], [12,6]])
    9.0
    """

    # convert to numpy array
    if type(points) != 'numpy.ndarray':
        points = np.array(points)

    dists = np.empty(len(points) - 1)

    for i in range(len(points) - 1):
        dists[i] = haversine(points[i], points[i + 1])

    total = np.sum(dists)

    return total
