from distutils.core import setup
from distutils.extension import Extension
#from Cython.Distutils import build_ext
from Cython.Build import cythonize
import os

os.environ['CC'] = 'gcc'

extensions = [
    Extension(
        "ppp.cpu_bound.omp",
        ["ppp/cpu_bound/omp.pyx"],
        #include_dirs = ['ppp/cpu_bound'],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp']),
]

setup(
    name='ppp',
    ext_modules=cythonize(extensions),
)
