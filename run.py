#!/usr/bin/env python
from ppp import cpu_bound, io_bound, memory_bound, overhead  # NOQA
#from ppp import io_bound


def main():
    #cpu_bound.makedata.make()
    #cpu_bound.serial.main()
    #cpu_bound.mt.main()
    #cpu_bound.mp.main()
    #cpu_bound.omp.main()
    #overhead.serial.main()
    #overhead.mt.main()
    #overhead.mp.main()
    #overhead.omp.main()
    #io_bound.serial.main()
    #io_bound.mt.main()
    #io_bound.mp.main()
    #io_bound.omp.main()
    #import ppp.memory_bound.data.makedata
    #ppp.memory_bound.data.makedata.make()
    #memory_bound.serial.main()
    #memory_bound.mt.main()
    memory_bound.mp.main()
    #memory_bound.omp.main()


if __name__ == "__main__":
    main()
