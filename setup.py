from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import os

os.environ['CC'] = 'gcc'

extensions = [
    Extension(
        name="ppp.cpu_bound.omp",
        sources=["ppp/cpu_bound/omp.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp']),
    #Extension(
        #name="ppp.overhead.omp",
        #sources=["ppp/overhead/omp.pyx"],
        #language="c++",
        #extra_compile_args=['-fopenmp'],
        #extra_link_args=['-fopenmp']),
]

setup(
    name='ppp',
    ext_modules=cythonize(extensions),
)
