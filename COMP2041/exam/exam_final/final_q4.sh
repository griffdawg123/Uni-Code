#!/bin/dash
file=$1
n=$(head -n1 "$file")
m=$(head -n1 "$file")
while read line; do
    if [ $line -lt $n ]; then
        n=$line
    elif [ $line -gt $m ]; then
        m=$line
    fi
done < $file
i=$n
found=0
while [ $i -le $m ]; do
    while read line; do
        if [ $line = $i ]; then
            found=1
            break
        fi
    done < $file
    if [ $found = 0 ]; then
        echo $i
    fi
    found=0
    i=$((i+1))
done