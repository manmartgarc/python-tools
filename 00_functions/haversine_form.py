"""
@author: Manuel Martinez
@email: manmartgarc@gmail.com

This script defines two formulas used to calculate great-circle distances
using a haversine formula.

Taken from https://en.wikipedia.org/wiki/Haversine_formula
"""

import numpy as np

def haversine_coord(coord1, coord2):
    """
    Returns the great-circle distance between two points on a sphere given
    their longitudes and latitudes in miles as a tuple.

    >>> haversine_coord([3,5], [4,7])
    154.27478490048566

    >>> haversine_coord((41.325, -72.325), (41.327, -72.327))
    0.17282397386672291
    """
    r = 3959 #radius of the earth
    r_lat = np.radians(coord1[0])
    r_lat2 = np.radians(coord2[0])
    delta_r_lat = np.radians(coord2[0]-coord1[0])
    delta_r_lon = np.radians(coord2[1]-coord1[1])

    a = (np.sin(delta_r_lat / 2) * np.sin(delta_r_lat / 2) +
        np.cos(r_lat) * np.cos(r_lat2) *
        np.sin(delta_r_lon / 2) * np.sin(delta_r_lon / 2))
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

    d = r * c
    return d

def haversine_enum(item1, item2):
    """
    Returns the great-circle distance between two enumearted points
    on a sphere given their indexes, longitudes, and latitudes in miles
    as a tuple.

    >>> haversine_enum((0, (3,5)), (1, (4,7)))
    154.27478490048566

    >>> haversine_enum((0, (41.325, -72.325)), (1, (41.327, -72.327)))
    0.17282397386672291
    """
    r = 3959 #radius of the earth
    r_lat = np.radians(item1[1][0])
    r_lat2 = np.radians(item2[1][0])
    delta_r_lat = np.radians(item2[1][0]-item1[1][0])
    delta_r_lon = np.radians(item2[1][1]-item1[1][1])

    a = (np.sin(delta_r_lat / 2) * np.sin(delta_r_lat / 2) +
        np.cos(r_lat) * np.cos(r_lat2) *
        np.sin(delta_r_lon / 2) * np.sin(delta_r_lon / 2))
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

    d = r * c
    return d
