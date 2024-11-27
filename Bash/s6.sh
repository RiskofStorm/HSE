#!/usr/bin/env bash

cat ${1} | wc -l > output.txt

ls ${1}  2>> error.log

exec bash