#!/usr/bin/env python
import os
import sys
from ppp import cpu_bound, io_bound, memory_bound, overhead  # NOQA


entries = {
    'cpu_bound.makedata': cpu_bound.data.make,
    'memory_bound.makedata': memory_bound.data.make,
    'cpu_bound.serial': cpu_bound.serial.main,
    'cpu_bound.mt': cpu_bound.mt.main,
    'cpu_bound.mp': cpu_bound.mp.main,
    'cpu_bound.omp': cpu_bound.omp.main,
    'overhead.serial': overhead.serial.main,
    'overhead.mt': overhead.mt.main,
    'overhead.mp': overhead.mp.main,
    'overhead.omp': overhead.omp.main,
    'io_bound.serial': io_bound.serial.main,
    'io_bound.mt': io_bound.mt.main,
    'io_bound.mp': io_bound.mp.main,
    'io_bound.omp': io_bound.omp.main,
    'memory_bound.serial': memory_bound.serial.main,
    'memory_bound.mt': memory_bound.mt.main,
    'memory_bound.mp': memory_bound.mp.main,
    'memory_bound.omp': memory_bound.omp.main,
}


def main():
    usage = "python run.py <package>.<module>\n"

    if len(sys.argv) != 2:
        sys.stderr.write(usage)
        sys.exit(1)

    print "PID: %d" % os.getpid()
    arg = sys.argv[1]
    if arg in entries:
        entries[arg]()
    else:
        sys.stderr.write("Invalid module `%s'.\n" % arg)
        sys.exit(1)


if __name__ == "__main__":
    main()
