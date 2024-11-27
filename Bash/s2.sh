#!/usr/bin/env bash

echo $PATH

PATH=${1}:$PATH
# temporal because missing exec bash, but I'm using it

echo "export PATH=${1}:$PATH" >> $HOME/.bashrc
exec bash