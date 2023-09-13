#!/bin/dash
for file in *.htm
do
    if [ -f "$(echo "$file" | sed "s/.htm$/.html/g")" ]
    then
        echo "$(echo "$file" | sed 's/.htm$/.html/g')" exists
        exit 1
    fi
    # echo $file
    mv "$file" "$(echo "$file" | sed 's/\(.*\.\)htm$/\1html/g')"
done
