#!/bin/dash
for file in $@
do
    includes="$(cat $file | grep -E "^#include \".*\"" | cut -d" " -f2 | cut -c2- | rev | cut -c2- | rev)"
    for include in $includes
    do
        if [ ! -f $include ]
        then
            echo "$include included into $file does not exist"
        fi
    done
done