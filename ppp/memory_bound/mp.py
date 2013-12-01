import math
import multiprocessing
from ppp.utils.decorators import timing
from .data.utils import mp_init_matrix, mp_zero_matrix
from .data.settings import MATRIX_SIZE, RANDOM_SIZE


NUM_PROCESSES = 8

# Input matrices with random integers
matrix_a = mp_init_matrix(MATRIX_SIZE, RANDOM_SIZE)
matrix_b = mp_init_matrix(MATRIX_SIZE, RANDOM_SIZE)

# Output matrices with zeros
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

    #print chunksize
    for i in range(NUM_PROCESSES):
        start = chunksize * i
        end = chunksize * (i + 1)
        if i == NUM_PROCESSES - 1:
            end = MATRIX_SIZE
        #print start, end
        p = multiprocessing.Process(
            target=worker,
            args=(start, end)
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


def main():
    proc()
