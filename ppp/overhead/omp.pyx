#cython: boundscheck=False
import math
import numpy as np
from cython.parallel import parallel, prange
from cython.operator cimport dereference as deref, preincrement as inc
cimport openmp  # NOQA
from libcpp.map cimport map
from libc.stdio cimport printf
from ppp.utils import db
from ppp.utils.decorators import timing
from ppp.settings import OVERHEAD
from .data.settings import DATA_FILENAME


NUM_THREADS = OVERHEAD.OMP_NUM_THREADS

target_list = []
points = {}
distances = {}
max_distance = -1
min_distance = -1


@timing
def proc():

    global target_list
    global points, distances
    global max_distance, min_distance
    cdef int n, num_threads, i
    num_threads = NUM_THREADS

    # Cython cannot modify shared variable in prange block
    # https://github.com/cython/cython/wiki/enhancements-prange
    #cdef unsigned int c_max_distance, c_min_distance
    #c_max_distance = -1
    #c_min_distance = -1

    # Declare local points and distance on the stack
    cdef map[int, int] c_points
    cdef map[int, int] c_distances

    # Initialize OpenMP lock
    cdef openmp.omp_lock_t lock
    openmp.omp_init_lock(&lock)

    # Convert `target_list` from list into NumPy array `ntg`
    ntg = np.array(target_list, dtype=np.int32)
    n = len(target_list)

    # Use a NumPy array to store max_distance and min_distance so that
    # they can be read and modified within the prange block
    # `ntmp` = [<max_distance>, <min_distance>]
    ntmp = np.array([max_distance, min_distance], dtype=np.int32)

    # Define memoryview `tg` on NumPy array `ntg`
    cdef int [:, :] tg = ntg  # NOQA

    # Define memoryview `tmp` on NumPy array `ntmp`
    cdef int [:] tmp = ntmp  # NOQA

    for i in prange(n, nogil=True, schedule="static", num_threads=num_threads):
        openmp.omp_set_lock(&lock)
        if tg[i][2] > tmp[0]:
            tmp[0] = tg[i][2]
        if tg[i][2] < tmp[1] or tmp[1] == -1:
            tmp[1] = tg[i][2]
        openmp.omp_unset_lock(&lock)

        openmp.omp_set_lock(&lock)
        if c_distances.find(tg[i][0]) == c_distances.end() \
        or tg[i][2] < c_distances[tg[i][0]]:
            c_points[tg[i][0]] = tg[i][1]
            c_distances[tg[i][0]] = tg[i][2]
        openmp.omp_unset_lock(&lock)

        openmp.omp_set_lock(&lock)
        if c_distances.find(tg[i][1]) == c_distances.end() \
        or tg[i][2] < c_distances[tg[i][1]]:
            c_points[tg[i][1]] = tg[i][0]
            c_distances[tg[i][1]] = tg[i][2]
        openmp.omp_unset_lock(&lock)

    # Assign global values
    #max_distance = c_max_distance
    #min_distance = c_min_distance

    # Iterate over the map `c_points` and `c_distances`, and convert it back to 
    # Python dictionary `points`
    cdef map[int, int].iterator c_points_it = c_points.begin()
    while c_points_it != c_points.end():
        points[deref(c_points_it).first] = deref(c_points_it).second
        inc(c_points_it)

    cdef map[int, int].iterator c_distances_it = c_distances.begin()
    while c_distances_it != c_distances.end():
        distances[deref(c_distances_it).first] = deref(c_distances_it).second
        inc(c_distances_it)

    max_distance = tmp[0]
    min_distance = tmp[1]


def main():
    global target_list
    starget_list = db.read_data(DATA_FILENAME)

    # Convert all strings into integers beforehand
    for t in starget_list:
        nt = [int(s) for s in t]
        target_list.append(nt)

    proc()
    res = []
    for point in points:
        res.append([point, points[point], distances[point]])
    print max_distance, min_distance
    db.write_data('overhead-output_omp.txt', res)
