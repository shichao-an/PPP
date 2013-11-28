# Import core submodules
from . import serial, mt, mp  # NOQA
try:
    from . import omp  # NOQA
except ImportError:
    print "Please build extensions first with command:"
    print "python setup.py build_ext"
