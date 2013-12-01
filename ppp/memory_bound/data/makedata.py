import numpy as np
from ppp.utils import db
from .settings import RANDOM_SIZE, MATRIX_SIZE, DATA_FILENAME


def init_matrix(matrix_size, random_size):
    return np.random.randint(random_size, size=(matrix_size, matrix_size))


def make():
    raw_array = init_matrix(MATRIX_SIZE, RANDOM_SIZE)
    db.write_data(DATA_FILENAME, list(raw_array))
