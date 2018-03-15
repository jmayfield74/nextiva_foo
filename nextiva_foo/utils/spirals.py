"""
Spiral sort functions
"""


# API =========================================================================

def sort(matrix=[]):
    """
    Return spiral sorted items from a matrix.

    >>> sort([
    ...     ["a", "b", "c", "d", "e"],
    ...     ["f", "g", "h", "i", "j"],
    ...     ["k", "l", "m", "n", "o"],
    ...     ["p", "q", "r", "s", "t"],
    ...     ["u", "y", "w", "x", "y"]
    ... ])
    ['a', 'b', 'c', 'd', 'e', 'j', 'o', 't', 'y', 'x', 'w', 'y', 'u', 'p', 'k', 'f', 'g', 'h', 'i', 'n', 's', 'r', 'q', 'l', 'm']


    :param matrix: a 2d matrix (square)
    :type matrix: [list]
    :return: sorted items
    :rtype: list
    """
    accumulator = []
    edge_funs = [top_edge, right_edge, bottom_edge, left_edge]
    while matrix:
        [
            accumulator.extend(edge_fun(matrix))
            for edge_fun in edge_funs
            if matrix
        ]
    return accumulator


# HELPERS =====================================================================

def top_edge(matrix):
    if not matrix:
        return []
    return matrix.pop(0)


def right_edge(matrix):
    return edge_pop(matrix, -1)


def bottom_edge(matrix):
    if not matrix:
        return []
    bottom = matrix.pop(-1)
    bottom.reverse()
    return bottom


def left_edge(matrix):
    left = edge_pop(matrix, 0)
    left.reverse()
    return left


def edge_pop(matrix, index):
    if not matrix:
        return []
    return [i.pop(index) for i in matrix]
