import ctypes
import multiprocessing
import numpy as np
import warnings

# Suppress "PEP 3118" warning
warnings.simplefilter("ignore", RuntimeWarning)


# Creating NumPy arrays for serial and multithreading programs
def init_matrix(matrix_size, random_size):
    return np.random.randint(random_size, size=(matrix_size, matrix_size))


def zero_matrix(matrix_size):
    return np.zeros((matrix_size, matrix_size), dtype=np.int64)


# Creating shared NumPy arrays for multiprocessing program
def mp_init_matrix(matrix_size, random_size):
    random = np.random.randint(random_size, size=matrix_size * matrix_size)
    shared_array_base = multiprocessing.Array(ctypes.c_int64, random)
    shared_array = np.ctypeslib.as_array(shared_array_base.get_obj())
    shared_array = shared_array.reshape(matrix_size, matrix_size)
    return shared_array


def mp_zero_matrix(matrix_size):
    zeros = np.zeros(matrix_size * matrix_size, dtype=np.int64)
    shared_array_base = multiprocessing.Array(ctypes.c_int64, zeros)
    shared_array = np.ctypeslib.as_array(shared_array_base.get_obj())
    shared_array = shared_array.reshape(matrix_size, matrix_size)
    return shared_array
