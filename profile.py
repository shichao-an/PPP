#!/usr/bin/env python
import cProfile
import pstats
import pyximport
import sys
from run import entries
import ppp



del entries['cpu_bound.makedata']
del entries['memory_bound.makedata']


def main():

    usage = "python profile.py <package>.<module>\n"

    if len(sys.argv) != 2:
        sys.stderr.write(usage)
        sys.exit(1)

    arg = sys.argv[1]
    if arg in entries:
        pyximport.install()
        command = entries[arg].__module__ + '.main()'
        cProfile.runctx(command, globals(), locals(), "Profile.prof")

        s = pstats.Stats("Profile.prof")
        s.strip_dirs().sort_stats("time").print_stats()


if __name__ == "__main__":
    main()
