import ConfigParser
import os


PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
REPO_PATH = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir))

user_home = os.path.expanduser('~')
config_file = os.path.join(REPO_PATH, 'ppp.cfg')
config = ConfigParser.ConfigParser()
config.read(config_file)


class Struct(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)


# Global config
num_threads = config.getint('global', 'num_threads')
num_processes = config.getint('global', 'num_processes')
omp_num_threads = config.getint('global', 'omp_num_threads')
assert num_threads >= 0
assert num_processes >= 0
assert omp_num_threads >= 0

# Specific configs
sections = {
    'cpu-bound': 'CPU_BOUND',
    'io-bound': 'IO_BOUND',
    'memory-bound': 'MEMORY_BOUND',
    'overhead': 'OVERHEAD'
}

for section_name in sections:
    section_config = {
        'NUM_THREADS': config.getint(section_name, 'num_threads')
        if num_threads == 0 else num_threads,
        'NUM_PROCESSES': config.getint(section_name, 'num_processes')
        if num_processes == 0 else num_processes,
        'OMP_NUM_THREADS': config.getint(section_name, 'omp_num_threads')
        if omp_num_threads == 0 else omp_num_threads,
    }
    vars()[sections[section_name]] = Struct(**section_config)
