#!/usr/bin/env bash

rng1=$(( 1 + RANDOM % 10))
rng2=$(( 1 + RANDOM % 10))
rng3=$(( 1 + RANDOM % 10))

sleep $rng1
echo "was sleeping $rng1 sec"
sleep $rng2 
echo "was sleeping $rng2 sec"
sleep $rng3
echo "was sleeping $rng3 sec"

exec bash


# Я использовал CTRL + Z и jobs чтобы увидеть остановленные програамы, видел ост. s5.sh, fg- foreground - исполнение в терменале, bg- background - исп. вне терминала