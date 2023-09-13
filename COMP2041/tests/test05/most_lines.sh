#!/bin/dash
biggestlines=0
biggestfile=$0
for ~file in $@
do
    numlines=$(wc -l $file | cut -d" " -f1)
    if [ $numlines -gt $biggestlines ]; then
        biggestfile=$file
        biggestlines=$numlines
    fi
done
echo $biggestfile