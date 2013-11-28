from functools import wraps
import time


def timing(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        start = time.time()
        res = f(*args, **kwds)
        end = time.time()
        try:
            func_name = f.func_name
        except AttributeError:
            func_name = f.__name__
        print "%s:%s:%.6f" % (f.__module__, func_name, float(end - start))
        return res
    return wrapper
