#!/bin/bash

usage="./benchmark.sh cpu_bound|io_bound|memory_bound|overhead|auto"
#programs=("mt" "mp" "omp")
programs=("omp")
#args=("cpu_bound" "io_bound" "memory_bound" "overhead")
args=("memory_bound")
num_threads=(1 2 4 8 16 32 64 128)
sed="/usr/local/bin/gsed"

if [ "$#" -ne 1 ]
then
    echo "$usage" 1>&2
    exit 1
fi

if [ "$1" = "auto" ]
then
    for arg in "${args[@]}"
    do
        echo "Benchmarking $arg programs..."
        for num_thread in "${num_threads[@]}"
        do
            echo "  Setting number of threads/processes to $num_thread..."
            $sed -i "s/ = \([0-9]\{1,\}\)  ;global/ = $num_thread  ;global/g" ppp.cfg
            #echo "    ${arg}.serial"
            #./run.py "${arg}.serial"
            #echo
            #sleep 5
            for program in "${programs[@]}"
            do
                echo "    $arg.$program (t/p: $num_thread)"
                ./run.py "${arg}.$program"
                echo
                sleep 5
            done
        done
    done
else
    exit_code=0
    for program in "${programs[@]}"
    do
        ./run.py "${1}.$program"
        if [ "$?" -ne "0" ]
        then
            exit_code=1
            break
        fi
    done
    if [ "$exit_code" -eq "1" ]
    then
        exit 1
    fi
fi
