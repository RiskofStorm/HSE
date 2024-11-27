#!/usr/bin/env bash
myarr=($(ls -la | awk '{print $1, $9}'))
unset myarr[0]
pattern="\<${1}\>"
(for row in "${myarr[@]}"
do
    echo $row
done) | paste - -


if [[ $# -eq 0 ]]
    then exit 0
fi

echo ""
if [[ ${myarr[@]} =~ $pattern ]]
    then echo "file ${1} is found"
    else echo "file ${1} is not found"
fi

exec bash



