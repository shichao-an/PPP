#cython: boundscheck=False
# cython: profile=True
import numpy as np
from cython.parallel import parallel, prange
cimport openmp  # NOQA
from libc.stdio cimport printf
from ppp.utils import db
from ppp.utils.decorators import timing
from ppp.settings import CPU_BOUND
from .data.settings import DATA_FILENAME


target_list = []
OMP_NUM_THREADS = CPU_BOUND.OMP_NUM_THREADS


@timing
def proc():

    global target_list
    cdef int n, num_threads, i, j
    num_threads = OMP_NUM_THREADS

    # Convert `target_list` from list into NumPy array `ntg`
    ntg = np.array(target_list, dtype=np.int32)
    n = len(target_list)

    # Define memoryview `tg` on NumPy array `ntg`
    cdef int [:, :] tg = ntg  # NOQA

    # Define memoryview `remove_indexes` on NumPy array initialized with zeros
    n_remove_indexes = np.zeros((n,), dtype=np.int32)
    cdef int [:] remove_indexes = n_remove_indexes  # NOQA

    #cdef double start, end
    for i in prange(n, nogil=True, schedule="static", num_threads=num_threads):
        #num_threads = openmp.omp_get_num_threads()
        #printf("wtime: %d\n", openmp.omp_get_wtime())
        if remove_indexes[i] == 1:
            continue

        for j in xrange(i + 1, n):
            # Record duplicates to be removed
            if tg[i][0] == tg[j][0] and tg[i][1] == tg[j][1]:
                #printf("%d\n", j)
                remove_indexes[j] = 1

            # Fix reverse distance
            elif tg[i][0] == tg[j][1] and tg[i][1] == tg[j][0]:
                tg[j][2] == tg[i][2]
        #printf("wtime: %d\n", num_threads)

    # Reinitialize `target_list` and append non-duplicates from `tg`
    target_list = []
    for i in range(n):
        if remove_indexes[i] == 0:
            target_list.append(tg[i])


def main():
    global target_list
    starget_list = db.read_data(DATA_FILENAME)

    # Convert all strings into integers beforehand
    for t in starget_list:
        nt = [int(s) for s in t]
        target_list.append(nt)

    proc()

    output_filename = db.get_output_path(DATA_FILENAME, 'output_omp')
    db.write_data(output_filename, target_list)

if __name__ == "__main__":
    main()
