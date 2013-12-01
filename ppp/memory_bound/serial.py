from ppp.utils.decorators import timing
from .data.utils import init_matrix, zero_matrix
from .data.settings import MATRIX_SIZE, RANDOM_SIZE


# Input matrices with random integers
matrix_a = init_matrix(MATRIX_SIZE, RANDOM_SIZE)
matrix_b = init_matrix(MATRIX_SIZE, RANDOM_SIZE)

# Output matrices with zeros
matrix_c = zero_matrix(MATRIX_SIZE)


@timing
def proc():
    """
    int row, column;
    for(row = 0; row < MATRIX_ROWS; row++)
        for(column = 0; column < MATRIX_COLS; column++)
        {
            output[row][column] = 0;  // Initialize output matrix' element to 0
            int i;
            for(i = 0; i < MATRIX_COLS; i++)
                output[row][column] += input_a[row][i] * input_b[i][column];
        }
}
    """
    for row in xrange(MATRIX_SIZE):
        for col in xrange(MATRIX_SIZE):
            for i in xrange(MATRIX_SIZE):
                matrix_c[row][col] += matrix_a[row][i] * matrix_b[i][col]


def main():
    #print matrix_a
    #print
    #print matrix_b
    proc()
    #print
    #print matrix_c
