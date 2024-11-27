#!/usr/bin/env bash
inc=0
if [[ ${1} -lt 0 ]]
    then echo "number is negative"
elif [[ ${1} -gt 0 ]]
    then echo "nubmer is positive"
    while [[ $inc -le ${1} ]]
        do
            echo $inc
            inc=$(( inc + 1))
        done
else
    echo "number is zero"
fi





exec bash