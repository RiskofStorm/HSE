#!/usr/bin/env bash

file=($(wc input.txt))
lines=${file[0]}
words=${file[1]}
chars=$(grep -o '[A-Za-z]' input.txt | wc -l)

echo "Input file contains:
$chars letters
$words words
$lines lines" > output.txt

exec bash

# bash c1.sh input.txt
# cat output.txt

 