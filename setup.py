#!/usr/bin/env python
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import os

os.environ['CC'] = 'gcc-4.2'
os.environ['CXX'] = 'g++-apple-4.2'

extensions = [

    Extension(
        name="ppp.cpu_bound.omp",
        sources=["ppp/cpu_bound/omp.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp']),
    Extension(
        name="ppp.overhead.omp",
        sources=["ppp/overhead/omp.pyx"],
        language="c++",
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp']),
    Extension(
        name="ppp.io_bound.omp",
        sources=["ppp/io_bound/omp.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp']),
    Extension(
        name="ppp.memory_bound.omp",
        sources=["ppp/memory_bound/omp.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp']),
]

setup(
    name='ppp',
    ext_modules=cythonize(extensions),
)
