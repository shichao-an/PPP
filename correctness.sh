#!/bin/bash

repo_path=$(dirname $BASH_SOURCE)
data_path="$repo_path/data"
usage="./correctness.sh cpu_bound|io_bound|memory_bound|overhead"

if [ -n "$1" ]
then
    if [ "$1" = "cpu_bound" ]
    then
        echo
    elif [ "$1" = "overhead" ]
    then
        echo "Checking overhead..."
        diff <(sort "$data_path/overhead-output_serial.txt") \
             <(sort "$data_path/overhead-output_mt.txt")
        diff <(sort "$data_path/overhead-output_serial.txt") \
             <(sort "$data_path/overhead-output_mp.txt")
        diff <(sort "$data_path/overhead-output_serial.txt") \
             <(sort "$data_path/overhead-output_omp.txt")
    else
        echo "Invalid argument $1." 1>&2
        exit 1
    fi
else
    echo "$usage" 1>&2
    exit 1
fi
