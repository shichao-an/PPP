# cython: boundscheck=False
# cython: profile=True
import numpy as np
import os
from cython.parallel import parallel, prange
cimport openmp  # NOQA
from ppp.utils.decorators import timing
from ppp.utils import db
from ppp.settings import MEMORY_BOUND
from .data.utils import init_matrix, zero_matrix
from .data.settings import (MATRIX_SIZE, MATRIX_A_DATA_FILENAME,
                            MATRIX_B_DATA_FILENAME)


OMP_NUM_THREADS = MEMORY_BOUND.OMP_NUM_THREADS

matrix_a_data = []
matrix_b_data = []

# Input matrices
matrix_a = []
matrix_b = []

# Output matrix with zeros
matrix_c = zero_matrix(MATRIX_SIZE)


@timing
def proc():
    cdef int matrix_size, num_threads, row, col, i
    num_threads = OMP_NUM_THREADS
    matrix_size = MATRIX_SIZE
    #cdef int chunksize = 5 #matrix_size / num_threads
    # Define memoryviews on NumPy arrays
    cdef long [:, :] c_matrix_a = matrix_a  # NOQA
    cdef long [:, :] c_matrix_b = matrix_b  # NOQA
    cdef long [:, :] c_matrix_c = matrix_c  # NOQA

    # Dynamically typed alternative
    #c_matrix_a = matrix_a
    #c_matrix_b = matrix_b
    #c_matrix_c = matrix_c

    # Dynamically typed alternative
    #for row in xrange(matrix_size):
    for row in prange(matrix_size, nogil=True, schedule="static",
                      num_threads=num_threads):
        for col in xrange(matrix_size):
            for i in xrange(matrix_size):
                c_matrix_c[row][col] += c_matrix_a[row][i] * c_matrix_b[i][col]



def set_globals():
    global matrix_a_data, matrix_b_data
    global matrix_a, matrix_b
    matrix_a_data = db.read_data(MATRIX_A_DATA_FILENAME)
    matrix_b_data = db.read_data(MATRIX_B_DATA_FILENAME)
    matrix_a = init_matrix(MATRIX_SIZE, matrix_a_data)
    matrix_b = init_matrix(MATRIX_SIZE, matrix_b_data)


def main():
    set_globals()
    proc()
    #print matrix_c
    db.write_data('memory_bound-output_omp.txt', list(matrix_c))
