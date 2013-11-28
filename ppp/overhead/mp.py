import math
import multiprocessing
from ppp.utils import db
from ppp.utils.decorators import timing
from .data.settings import DATA_FILENAME


NUM_PROCESSES = 8

_target_list = db.read_data(DATA_FILENAME)
manager = multiprocessing.Manager()
target_list = manager.list(_target_list)
points = manager.dict()
distances = manager.dict()
lock = manager.Lock()
lock = multiprocessing.Lock()  # Better alternative
max_distance = manager.Value('i', -1)
max_distance = multiprocessing.Value('i', -1)  # Better alternative
min_distance = manager.Value('i', -1)
min_distance = multiprocessing.Value('i', -1)  # Better alternative


def worker(target_slice):
    for row in target_slice:
        # row[0]: origin; row[1]: destination; row[2]: distance
        lock.acquire()
        if int(row[2]) > max_distance.value:
            max_distance.value = int(row[2])
        if int(row[2]) < min_distance.value or min_distance.value == -1:
            min_distance.value = int(row[2])
        lock.release()

    for row in target_slice:
        lock.acquire()
        if row[0] not in distances or int(row[2]) < distances[row[0]]:
            points[row[0]] = row[1]
            distances[row[0]] = int(row[2])
        lock.release()

    for row in target_slice:
        lock.acquire()
        if row[1] not in distances or int(row[2]) < distances[row[1]]:
            points[row[1]] = row[0]
            distances[row[1]] = int(row[2])
        lock.release()


@timing
def proc():
    processes = []
    chunksize = int(math.ceil(len(target_list) / float(NUM_PROCESSES)))
    #print chunksize
    for i in range(NUM_PROCESSES):
        start = chunksize * i
        end = chunksize * (i + 1)
        if i == NUM_PROCESSES - 1:
            end = len(target_list)
        #print start, end
        p = multiprocessing.Process(
            target=worker,
            args=(target_list[start:end],))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


def main():
    proc()
    res = []
    for point in dict(points):
        res.append([point, points[point], distances[point]])
    print max_distance.value, min_distance.value
    db.write_data('overhead-output_mp.txt', res)
