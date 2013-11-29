from ppp import cpu_bound, io_bound, memory_bound, overhead  # NOQA


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
    io_bound.mt.main()


if __name__ == "__main__":
    main()
