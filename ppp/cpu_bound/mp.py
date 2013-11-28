import multiprocessing
import math
from ppp.utils import db
from ppp.utils.decorators import timing
from ppp.settings import CPU_BOUND
from .data.settings import DATA_FILENAME


NUM_PROCESSES = CPU_BOUND.NUM_PROCESSES
manager = multiprocessing.Manager()
target_list = manager.list()
remove_indexes = manager.list()


def worker(target_slice, start):
    #proc_info = "Process ID: %d" % os.getpid()
    #print proc_info
    for i, t in enumerate(target_slice, start):
        if i in remove_indexes:
            continue
        for j in range(i + 1, len(target_list)):
            # Record duplicates to be removed
            if t[0] == target_list[j][0] and t[1] == target_list[j][1]:
                remove_indexes.append(j)
            # Fix reverse distance
            elif t[0] == target_list[j][1] and t[1] == target_list[j][0]:
                target_list[j][2] == t[2]


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
            args=(target_list[start:end], start)
        )
        processes.append(p)
        p.start()

    #print "Number of processes: ", len(processes)
    for p in processes:
        p.join()

    # Remove duplicates by popping
    remove_indexes.sort()
    count = 0
    for i in remove_indexes:
        index = i - count
        target_list.pop(index)
        count += 1


def main():
    global target_list
    target_list = db.read_data(DATA_FILENAME)
    proc()
    output_filename = db.get_output_path(DATA_FILENAME, 'output_mp')
    db.write_data(output_filename, target_list)


if __name__ == "__main__":
    main()
