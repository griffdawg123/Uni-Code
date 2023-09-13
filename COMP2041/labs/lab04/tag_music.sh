#!/bin/dash

for directory in "$@"
do
    for file in "$directory"/*.mp3
    do
        file=$(echo "$file" | sed "s|//|/|g")
        albumyear="$(echo "$file" | rev | cut -d'/' -f2 | rev)"
        album="$(echo "$albumyear" | cut -d',' -f1)"
        year="$(echo "$albumyear" | rev | cut -d',' -f1 | rev | sed -e 's/^[[:space:]]*//')"
        filename="$(echo "$file" | rev | cut -d'/' -f1 | rev)"
        track="$(echo "$filename" | cut -d'-' -f1 | sed -e 's/^[[:space:]]*//' | sed -e 's/[[:space:]]*$//')"
        title="$(echo "$filename" | cut -d'-' -f2 | sed -e 's/^[[:space:]]*//' | sed -e 's/[[:space:]]*$//')"
        artist="$(echo "$filename" | cut -d'-' -f3 | sed -e 's/^[[:space:]]*//'| sed 's/.mp3//g')"
        # echo "$file"
        # echo
        # echo "$year"
        id3 -t"$title" -T"$track" -a"$artist" -A"$albumyear" -y"$year" "$file" > /dev/null  
        # echo $title $track $artist $album $year $file
    done
done
