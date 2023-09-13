#!/bin/dash
first=$(echo $1 | sed 's/\([a-zA-Z]*\)[0-9]*\([a-zA-Z]*\)$/\1/g')
second=$(echo $1 | sed 's/\([a-zA-Z]*\)[0-9]*\([a-zA-Z]*\)$/\2/g')
first_number=$(echo $1 | sed 's/\([a-zA-Z]*\)\([0-9]*\)\([a-zA-Z]*\)$/\2/g')
second_number=$(echo $2 | sed 's/\([a-zA-Z]*\)\([0-9]*\)\([a-zA-Z]*\)$/\2/g')
i=$first_number
while [ $i -le $second_number ]; do
    echo "$first$i$second"
    i=$((i+1))
done