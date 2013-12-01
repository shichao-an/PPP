import math
import multiprocessing
from ppp.utils.decorators import timing
from ppp.utils import db
from .data.utils import mp_init_matrix, mp_zero_matrix
from .data.settings import (MATRIX_SIZE, MATRIX_A_DATA_FILENAME,
                            MATRIX_B_DATA_FILENAME)


NUM_PROCESSES = 8

matrix_a_data = []
matrix_b_data = []

# Input matrices
matrix_a = []
matrix_b = []

# Output matrix with zeros
matrix_c = mp_zero_matrix(MATRIX_SIZE)


def worker(start, end):
    for row in xrange(start, end):
        for col in xrange(MATRIX_SIZE):
            for i in xrange(MATRIX_SIZE):
                matrix_c[row][col] += matrix_a[row][i] * matrix_b[i][col]


@timing
def proc():
    processes = []
    chunksize = int(math.floor(MATRIX_SIZE / float(NUM_PROCESSES)))
    print chunksize
    for i in range(NUM_PROCESSES):
        start = chunksize * i
        end = chunksize * (i + 1)
        if i == NUM_PROCESSES - 1:
            end = MATRIX_SIZE
        print start, end
        p = multiprocessing.Process(
            target=worker,
            args=(start, end)
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


def set_globals():
    global matrix_a_data, matrix_b_data
    global matrix_a, matrix_b
    matrix_a_data = db.read_data(MATRIX_A_DATA_FILENAME)
    matrix_b_data = db.read_data(MATRIX_B_DATA_FILENAME)
    matrix_a = mp_init_matrix(MATRIX_SIZE, matrix_a_data)
    matrix_b = mp_init_matrix(MATRIX_SIZE, matrix_b_data)


def main():
    set_globals()
    proc()
    db.write_data('memory_bound-output_mp.txt', list(matrix_c))
