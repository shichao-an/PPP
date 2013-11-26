import os

PROJECT_PATH = \
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

REPO_PATH = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir))


def get_data_path():
    data_path = os.path.join(REPO_PATH, 'data')
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    return data_path
