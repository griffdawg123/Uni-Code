#!/bin/bash
if [ $# -lt 2 ] || [ $# -gt 2 ]
then
    echo "Usage: ./echon.sh <number of lines> <string>"
    exit 1
elif ! [[ $1 =~ ^[0-9]+$ ]]
then
    echo "./echon.sh: argument 1 must be a non-negative integer"
    exit 1
fi

n=$1
text=$2
for ((i=0; i<n; i++)); do
    echo $text
done
exit 0