import math
import threading
from ppp.utils import db
from ppp.utils.decorators import timing
from .data.settings import DATA_FILENAME

NUM_THREADS = 8

target_list = db.read_data(DATA_FILENAME)
points = {}
distances = {}
lock = threading.Lock()
max_distance = -1
min_distance = -1


def worker(target_slice):
    global max_distance, min_distance
    for row in target_list:
        # row[0]: origin; row[1]: destination; row[2]: distance
        lock.acquire()
        if int(row[2]) > max_distance:
            max_distance = int(row[2])
        if int(row[2]) < min_distance or min_distance == -1:
            min_distance = int(row[2])
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
    threads = []
    chunksize = int(math.ceil(len(target_list) / float(NUM_THREADS)))
    #print chunksize
    for i in range(NUM_THREADS):
        start = chunksize * i
        end = chunksize * (i + 1)
        if i == NUM_THREADS - 1:
            end = len(target_list)
        #print start, end
        t = threading.Thread(
            target=worker,
            args=(target_list[start:end],)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def main():
    proc()
    res = []
    for point in points:
        res.append([point, points[point], distances[point]])
    print max_distance, min_distance
    db.write_data('overhead-output_mt.txt', res)
