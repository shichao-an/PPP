# I/O operations for locally stored data
import csv
import os


PROJECT_PATH = \
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
REPO_PATH = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir))


def get_data_path():
    data_path = os.path.join(REPO_PATH, 'data')
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    return data_path


def get_output_path(data_filename, suffix):
    base, ext = os.path.splitext(data_filename)
    dash = '-'
    return base + dash + suffix + ext


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
