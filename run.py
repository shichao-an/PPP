from ppp.cpu_bound.data import makedata
from ppp.cpu_bound import serial
from ppp.cpu_bound import mt
from ppp.cpu_bound import mp
from ppp.cpu_bound import omp


def main():
    #makedata.make()
    #serial.main()
    #mt.main()
    omp.main()

if __name__ == "__main__":
    main()
