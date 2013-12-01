import math
import threading
from ppp.utils.decorators import timing
from .data.utils import init_matrix, zero_matrix
from .data.settings import MATRIX_SIZE, RANDOM_SIZE


NUM_THREADS = 8

# Input matrices with random integers
matrix_a = init_matrix(MATRIX_SIZE, RANDOM_SIZE)
matrix_b = init_matrix(MATRIX_SIZE, RANDOM_SIZE)

# Output matrices with zeros
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


def main():
    proc()

