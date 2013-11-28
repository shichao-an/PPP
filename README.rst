Python and Parallel Programming
===============================
Final project for Multicore Processors: Architecture & Programming, Fall 2013

DESCRIPTION
-----------

This project studies how to utilize parallelism in Python applications by comparing three different parallel programming methods. CPython's multithreading interface ``threading`` and process-based "threading" interface ``multiprocessing`` are discussed in terms of employing built-in functionalities, and OpenMP through ``cython.parallel`` in Cython are introduced in terms of thread-based native parallelism.

CPU-bound and I/O-bound programs are parallelized using these methods to demonstrate features and to compare performances. As an essential supplement, parallelized matrix programs are evaluated with ``multiprocessing`` and OpenMP approaches to study the memory aspect.

USAGE
-----
1. Build Cython extensions::

  $ python setup.py build_ext

2. Make data:
	

3. Run the project::

  $ python run.py

4. Ensure correctness::

  $ ./correctness all
