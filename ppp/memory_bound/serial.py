import numpy as np
import os
import psutil
from ppp.utils.decorators import timing
from ppp.utils import db
from .data.utils import init_matrix, zero_matrix
from .data.settings import (MATRIX_SIZE, MATRIX_A_DATA_FILENAME,
                            MATRIX_B_DATA_FILENAME)


matrix_a_data = []
matrix_b_data = []

# Input matrices
matrix_a = []
matrix_b = []

# Output matrix with zeros
matrix_c = zero_matrix(MATRIX_SIZE)


@timing
def proc():

    for row in xrange(MATRIX_SIZE):
        for col in xrange(MATRIX_SIZE):
            for i in xrange(MATRIX_SIZE):
                matrix_c[row][col] += matrix_a[row][i] * matrix_b[i][col]


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
    db.write_data('memory_bound-output_serial.txt', list(matrix_c))
