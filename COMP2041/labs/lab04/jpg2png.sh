#!/bin/dash

for file in "."/*".jpg"
do
    # echo -e $("$file" | sed "s|^./||g")
    if test -e "$(echo "$file" | sed "s/.jpg/.png/g")"; then
        echo "$(echo "$file" | sed "s/.jpg/.png/g"  | sed "s|^./||g") already exists"
        exit 1
    else
        # echo "$(echo "$file" | sed "s/.jpg/.png/g") does not exist"
        convert "$file" "$(echo "$file" | sed "s/.jpg/.png/g")" 2> /dev/null
        rm "$file"
    fi
done