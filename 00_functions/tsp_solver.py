"""
@author:    Manuel Martinez
@email:     manmartgarc@gmail.com

TSP heuristic taken from:
        https://codereview.stackexchange.com/questions/81865/
        travelling-salesman-using-brute-force-and-heuristics
"""
from haversine_dist import haversine


def opt_tsp(points, start=None, enum=False):
    """
    As solving the problem in the brute force way is too slow,
    this function implements a simple heuristic: always
    go to the nearest city.

    Even if this algoritmh is extremely simple, it works pretty well
    giving a solution only about 25% longer than the optimal one
    (cit. Wikipedia), and runs very fast in O(N^2) time complexity.

    Parameters
    ----------
    points: list of list, or list of tuples
         Array of coordinate pairs.
    start: coordinate pair
         Explicitely use a start point, otherwise uses the first object
         of the points array.
    enum: boolean
         Option for using an indexed array of points, i.e.
         enumerate(points)

    Returns
    -------
    >>> opt_tsp([[i,j] for i in range(5) for j in range(5)])
    [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 4], [1, 3], [1, 2], [1, 1],
     [1, 0], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [3, 4], [3, 3], [3, 2],
     [3, 1], [3, 0], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4]]

    >>> optimized_travelling_salesman([[0,0],[10,0],[6,0]])
    [[0, 0], [6, 0], [10, 0]]
    """
    if enum is False:
        points = list(points)
    elif enum is True:
        points = list(enumerate(points))

    if start is None:
        start = points[0]
    else:
        start = points[start]

    must_visit = points
    path = [start]
    must_visit.remove(start)

    while must_visit:
        nearest = min(must_visit,
                      key=lambda x: haversine(path[-1], x, enum=enum))
        path.append(nearest)
        must_visit.remove(nearest)

    return path
