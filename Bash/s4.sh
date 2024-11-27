#!/usr/bin/env bash

function greet(){
    echo "Hello, ${1}"
}

function concat(){
    sum=$(( $1 + $2 ))
    echo "$sum"
}

greet Danil
concat 2 2

exec bash