import math
import threading
from ppp.utils.decorators import timing
from ppp.utils import db
from ppp.settings import MEMORY_BOUND
from .data.utils import init_matrix, zero_matrix
from .data.settings import (MATRIX_SIZE, MATRIX_A_DATA_FILENAME,
                            MATRIX_B_DATA_FILENAME)


NUM_THREADS = MEMORY_BOUND.NUM_THREADS


matrix_a_data = []
matrix_b_data = []

# Input matrices
matrix_a = []
matrix_b = []

# Output matrix with zeros
matrix_c = zero_matrix(MATRIX_SIZE)


def worker(start, end):
    for row in xrange(start, end):
        for col in xrange(MATRIX_SIZE):
            for i in xrange(MATRIX_SIZE):
                matrix_c[row][col] += matrix_a[row][i] * matrix_b[i][col]


@timing
def proc():
    threads = []
    chunksize = int(math.floor(MATRIX_SIZE / float(NUM_THREADS)))

    #print chunksize
    for i in range(NUM_THREADS):
        start = chunksize * i
        end = chunksize * (i + 1)
        if i == NUM_THREADS - 1:
            end = MATRIX_SIZE
        #print start, end
        t = threading.Thread(
            target=worker,
            args=(start, end)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


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
    db.write_data('memory_bound-output_mt.txt', list(matrix_c))
