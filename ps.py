#!/usr/bin/env python
import math
import psutil
import subprocess
import sys
import time
from run import entries


def main():
    usage = "python profile.py <package>.<module>\n"

    if len(sys.argv) != 2:
        sys.stderr.write(usage)
        sys.exit(1)

    arg = sys.argv[1]
    if arg in entries:
        popen = subprocess.Popen(['./run.py', arg], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        p = psutil.Process(popen.pid)
        stat = {
            'cpu_percent': [],
            'cpu_times': [],
            'memory': [],
            'connections': [],
            'file_descriptors': [],
            'threads': [],
            'subprocesses': [],
            'sub_times': {},
        }
        m = math.pow(2, 20)
        try:
            while p.is_running():
                stat['cpu_percent'].append(p.get_cpu_percent())
                stat['cpu_times'].append(p.get_cpu_times())
                stat['memory'].append(float(p.get_memory_info().rss / m))
                stat['connections'].append(len(p.get_connections()))
                stat['file_descriptors'].append(p.get_num_fds())
                stat['threads'].append(p.get_num_threads())
                children = p.get_children()
                stat['subprocesses'].append(len(children))
                for child in children:
                    if child.pid in stat['sub_times']:
                        cpu_times = child.get_cpu_times()
                        stat['sub_times'][child.pid].append(cpu_times)
                    else:
                        stat['sub_times'][child.pid] = []
                time.sleep(0.05)
        except:
            stdout, stderr = popen.communicate()
            if stderr:
                sys.stderr.write(stderr)
                sys.exit(1)

            print stdout

            print 'CPU Percent (%%) - Max: %.2f, Min: %.2f, Avg: %.2f' % \
                (max(stat['cpu_percent']), min(stat['cpu_percent']),
                 sum(stat['cpu_percent']) / len(stat['cpu_percent']))
            print 'CPU Times (sec) - User: %.4f, System: %.4f' % \
                (stat['cpu_times'][-1][0], stat['cpu_times'][-1][1])
            print 'Memory (MB) - Max: %.2f, Min: %.2f, Avg: %.2f' % \
                (max(stat['memory']), min(stat['memory']),
                 sum(stat['memory']) / len(stat['memory']))
            print 'Connections - Max: %d, Min: %d, Avg: %d' % \
                (max(stat['connections']), min(stat['connections']),
                 sum(stat['connections']) / len(stat['connections']))
            print 'File Descriptors - Max: %d, Min: %d, Avg: %d' % \
                (max(stat['file_descriptors']), min(stat['file_descriptors']),
                 sum(stat['file_descriptors']) / len(stat['file_descriptors']))
            print 'Threads - Max: %d, Min: %d, Avg: %d' % \
                (max(stat['threads']), min(stat['threads']),
                 sum(stat['threads']) / len(stat['threads']))
            print 'Subprocesses - Max: %d, Min: %d, Avg: %d' % \
                (max(stat['subprocesses']), min(stat['subprocesses']),
                 sum(stat['subprocesses']) / len(stat['subprocesses']))
            sub_user_time = 0.0
            sub_sys_time = 0.0
            for p in stat['sub_times']:
                sub_user_time += stat['sub_times'][p][-1][0]
                sub_sys_time += stat['sub_times'][p][-1][1]
            print 'Subprocesses times - User: %.4f. System %.4f' % \
                (sub_user_time, sub_sys_time)

    else:
        sys.stderr.write("Invalid module `%s'.\n" % arg)
        sys.exit(1)


if __name__ == "__main__":
    main()
