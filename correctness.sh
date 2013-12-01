#!/bin/bash

repo_path=$(dirname $BASH_SOURCE)
data_path="$repo_path/data"
usage="./correctness.sh cpu_bound|io_bound|memory_bound|overhead"
cpu_bound_prefix="cpu_bound-output"
overhead_prefix="overhead-output"
io_bound_prefix="io_bound-output"
memory_bound_prefix="memory_bound-output"


if [ -n "$1" ]
then
    if [ "$1" = "cpu_bound" ]
    then
        echo

    elif [ "$1" = "overhead" ]
    then
        echo "Checking overhead..."
        diff <(sort "$data_path/${overhead_prefix}_serial.txt") \
             <(sort "$data_path/${overhead_prefix}_mt.txt")
        diff <(sort "$data_path/${overhead_prefix}_serial.txt") \
             <(sort "$data_path/${overhead_prefix}_mp.txt")
        diff <(sort "$data_path/${overhead_prefix}_serial.txt") \
             <(sort "$data_path/${overhead_prefix}_omp.txt")

    elif [ "$1" = "io_bound" ]
    then
        echo "Checking io_bound..."
        diff <(sort "$data_path/${io_bound_prefix}_serial.txt") \
             <(sort "$data_path/${io_bound_prefix}_mt.txt")
        diff <(sort "$data_path/${io_bound_prefix}_serial.txt") \
             <(sort "$data_path/${io_bound_prefix}_mp.txt")
        diff <(sort "$data_path/${io_bound_prefix}_serial.txt") \
             <(sort "$data_path/${io_bound_prefix}_omp.txt")

    elif [ "$1" = "memory_bound" ]
    then
        diff "$data_path/${memory_bound_prefix}_serial.txt" \
             "$data_path/${memory_bound_prefix}_mt.txt"
        diff "$data_path/${memory_bound_prefix}_serial.txt" \
             "$data_path/${memory_bound_prefix}_mp.txt"
        diff "$data_path/${memory_bound_prefix}_serial.txt" \
             "$data_path/${memory_bound_prefix}_omp.txt"

    else
        echo "Invalid argument $1." 1>&2
        exit 1
    fi
else
    echo "$usage" 1>&2
    exit 1
fi
