#!/bin/dash
for dir in ./*
do
    if [ -d $dir ]; then
        directory_name=${dir##*/}
        num_items=$(ls $dir | wc -l)
        if [ $num_items -ge 2 ]; then
            echo $directory_name
        fi
    fi
done