Python and Parallel Programming
===============================
Final project for Multicore Processors: Architecture & Programming, Fall 2013 (CSCI-GA.3033-010)

Description
-----------

This project studies how to utilize parallelism in Python applications by comparing three different parallel programming methods. CPython's multithreading interface ``threading`` and process-based "threading" interface ``multiprocessing`` are discussed in terms of employing built-in functionalities, and OpenMP through ``cython.parallel`` in Cython are introduced in terms of thread-based native parallelism.

CPU-bound and I/O-bound programs are parallelized using these methods to demonstrate features and to compare performances. As an essential supplement, parallelized matrix programs are evaluated with ``multiprocessing`` and OpenMP approaches to study the memory aspect.

Usage
-----

Build Cython extensions::

  $ python setup.py build_ext


Make data for dependent programs::

  $ python run.py cpu_bound.makedata
  $ python run.py memory_bound.makedata


Run the project::

  $ python run.py cpu_bound.serial


Ensure output correctness::

  $ ./correctness.sh io_bound

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

