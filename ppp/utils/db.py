# I/O operations for locally stored data
import csv
import os
from ppp.utils import get_data_path


def write_data(filename, rows):
    filename = os.path.join(get_data_path(), filename)
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def read_data(filename):
    filename = os.path.join(get_data_path(), filename)
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        return list(reader)
