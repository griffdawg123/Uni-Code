#!/bin/dash
start=$1
set -- a b c d e f g h
echo $start
start_letter=$1
i=1
for letter in $@; do
    if [ $(echo $start | cut -b1) = $letter ]; then
        start_letter=$i
    fi
    i=$((i+1))
done
start_number=$(echo $start | cut -b2)
echo $@{$start_letter} $start_number
