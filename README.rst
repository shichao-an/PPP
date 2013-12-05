Python and Parallel Programming
===============================
Final project for Multicore Processors: Architecture & Programming, Fall 2013 (CSCI-GA.3033-010)

Description
-----------

This project studies how to utilize parallelism in Python applications by comparing three different parallel programming methods. CPython's multithreading interface ``threading`` and process-based "threading" interface ``multiprocessing`` are discussed in terms of employing built-in functionalities, and OpenMP through ``cython.parallel`` in Cython are introduced in terms of thread-based native parallelism.

CPU-bound and I/O-bound programs are parallelized using these methods to demonstrate features and to compare performances. As essential supplements, a derivative CPU-bound application and a matrix multiplication program are parallelized to study the overhead and memory aspect.

Usage
-----
Install requirements::

  $ pip install -r requirements.txt


Build Cython extensions::

  $ python setup.py build_ext


Make data for dependent programs::

  $ python run.py cpu_bound.makedata
  $ python run.py memory_bound.makedata


Specify number of thread/process in ppp.cfg (when global value is greater than zero, it overrides all other sections)::

  [cpu-bound]
  num_threads = 8
  num_processes = 8
  omp_num_threads = 8


Run the project by specifying package and module::

  $ python run.py <package>.<module>


Automatic benchmarking::

  $ ./benchmark.sh auto


Ensure output correctness::

  $ ./correctness.sh io_bound


Profile a program::

  $ python profile.py <package>.<module>


Show process status of a program::

  $ python ps.py <package>.<module>


Command-line arguments
----------------------

The arguments to run.py are listed as follows:

- cpu_bound.makedata
- memory_bound.makedata
- cpu_bound.serial
- cpu_bound.mt
- cpu_bound.mp
- cpu_bound.omp
- overhead.serial
- overhead.mt
- overhead.mp
- overhead.omp
- io_bound.serial
- io_bound.mt
- io_bound.mp
- io_bound.omp
- memory_bound.serial
- memory_bound.mt
- memory_bound.mp
- memory_bound.omp

