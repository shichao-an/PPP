import random
from ppp.utils import db
from .settings import LIST_LEN, RANDOM_START, RANDOM_END, DATA_FILENAME


target_list = []
remove_indexes = []


def make():
    for i in range(LIST_LEN):
        a = random.randint(RANDOM_START, RANDOM_END)
        b = random.randint(RANDOM_START, RANDOM_END)
        if a == b:
            continue
        distance = random.randint(RANDOM_START, RANDOM_END)
        t = [a, b, distance]
        target_list.append(t)

    db.write_data(DATA_FILENAME, target_list)
