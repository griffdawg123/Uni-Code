#!/bin/dash
n=1
while [ $n -le "$1" ]
do
    echo "hello $2" > "hello$n.txt"
    n=$((n+1))
done
