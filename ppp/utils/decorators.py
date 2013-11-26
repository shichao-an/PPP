from functools import wraps
import time


def timing(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        start = time.time()
        res = f(*args, **kwds)
        end = time.time()
        print "%s:%.6f" % (f.func_name, float(end - start))
        return res
    return wrapper
