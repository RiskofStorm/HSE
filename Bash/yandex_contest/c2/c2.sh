#!/usr/bin/env bash

sort_m=($(tail -n 1 input.txt))
num=($(head -n 1 input.txt | grep -o '[0-9]'))




if [ $sort_m = 'date' ];
    then cat input.txt | tail -n +2 | head -n -1 | LC_ALL=C sort  -k5,5g -k4,4g -k3,3g | awk  'BEGIN {FS=" ";} {print $1" "$2" "$3"."$4"."$5}'  | sed 's/\.\.//g'  > output.txt
elif [ $sort_m = 'name' ];
    then cat input.txt | tail -n +2 | head -n -1 | awk  'BEGIN {FS=" ";} {print $1" "$2" "$3"."$4"."$5}'  | sed 's/\.\.//g' | LC_ALL=C sort -k2 -k1  > output.txt
fi

exec bash
