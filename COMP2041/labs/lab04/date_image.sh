#!/bin/dash
for file in "$@"
do
    ls -l "$file"
    date="$(echo $(ls -l "$file") | cut -d' ' -f6,7,8)"
    # echo "$date"
    convert -gravity south -pointsize 36 -draw "text 0,10 '$date'" $file $file
done