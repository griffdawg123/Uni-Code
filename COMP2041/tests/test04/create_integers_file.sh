#!/bin/dash
first=$1
second=$2
file=$3
i=$first
if test ! -f "$file"
then
    touch "$file"
fi
while [ "$i" -lt $((second+1)) ]
do
    echo "$i" >> "$file"
    i=$((i+1))
done
