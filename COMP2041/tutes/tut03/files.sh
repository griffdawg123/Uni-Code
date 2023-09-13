#!/bin/bash
for f in "$@"
do
    filename="echo $f | sed 's/".gz"//g'"
    echo $filename
    if test -f "$filename"; then 
        zcat $filename
    else
        echo "No such file: $filename.gz"
    fi
done
