import numpy as np
from ppp.utils import db
from .settings import (RANDOM_SIZE, MATRIX_SIZE, MATRIX_A_DATA_FILENAME,
                       MATRIX_B_DATA_FILENAME)



def rand_matrix(matrix_size, random_size):
    return np.random.randint(random_size, size=(matrix_size, matrix_size))


def make():
    matrix_a_data = rand_matrix(MATRIX_SIZE, RANDOM_SIZE)
    matrix_b_data = rand_matrix(MATRIX_SIZE, RANDOM_SIZE)
    db.write_data(MATRIX_A_DATA_FILENAME, list(matrix_a_data))
    db.write_data(MATRIX_B_DATA_FILENAME, list(matrix_b_data))
