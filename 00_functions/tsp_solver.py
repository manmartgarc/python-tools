"""
@author: Manuel Martinez
@email: manmartgarc@gmail.com


TSP heuristic taken from:
        https://codereview.stackexchange.com/questions/81865/
        travelling-salesman-using-brute-force-and-heuristics

"""
import numpy as np

from haversine_form import haversine_enum
from haversine_form import haversine_coord

def total_distance(points):
    """
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
    
    return sum([haversine_coord(point, points[index + 1])
                for index, point in enumerate(points[:-1])])

def total_distance_enum(points):
    """
    Returns the length of a path passing throughout all the points
    in a given order, if the input is an enumerated list of tuples.

    >>> total_distance_enum([(0, (1,3)), (1, (3, 7))])
    308.85055937873676
    >>> total_distance_enum([(0, (3,6)), (1, (7, 6)), (2, (12, 6))])
    621.8782657780996
    """
    return sum([haversine_enum(points[i], points[i + 1])
                for i in range(len(points) - 1)])

def optimized_travelling_salesman_coord(points, start=None):
    """
    As solving the problem in the brute force way is too slow,
    this function implements a simple heuristic: always
    go to the nearest city.

    Even if this algoritmh is extremely simple, it works pretty well
    giving a solution only about 25% longer than the optimal one (cit. Wikipedia),
    and runs very fast in O(N^2) time complexity.

    >>> optimized_travelling_salesman([[i,j] for i in range(5) for j in range(5)])
    [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 4], [1, 3], [1, 2], [1, 1],
     [1, 0], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [3, 4], [3, 3], [3, 2],
     [3, 1], [3, 0], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4]]
    >>> optimized_travelling_salesman([[0,0],[10,0],[6,0]])
    [[0, 0], [6, 0], [10, 0]]
    """
    points = list(points)
    if start is None:
        start = points[0]
    else:
        start = points[start]
    must_visit = points
    path = [start]
    must_visit.remove(start)
    while must_visit:
        nearest = min(must_visit,
                       key=lambda x: haversine_coord(path[-1], x))
        path.append(nearest)
        must_visit.remove(nearest)
    return path

def optimized_travelling_salesman_enum(points, start=None):
    """
    As solving the problem in the brute force way is too slow,
    this function implements a simple heuristic: always
    go to the nearest city.

    Even if this algoritmh is extremely simple, it works pretty well
    giving a solution only about 25% longer than the optimal one (cit. Wikipedia),
    and runs very fast in O(N^2) time complexity.

    >>> optimized_travelling_salesman([[i,j] for i in range(5) for j in range(5)])
    [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 4], [1, 3], [1, 2], [1, 1],
     [1, 0], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [3, 4], [3, 3], [3, 2],
     [3, 1], [3, 0], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4]]
    >>> optimized_travelling_salesman([[0,0],[10,0],[6,0]])
    [[0, 0], [6, 0], [10, 0]]
    """
    points = list(enumerate(points))
    if start is None:
        start = points[0]
    elif start is not None:
        start = points[start]
    must_visit = points
    path = [start]
    must_visit.remove(start)
    while must_visit:
        nearest = min(must_visit,
                       key=lambda x: haversine_enum(path[-1], x))
        path.append(nearest)
        must_visit.remove(nearest)
    return path
