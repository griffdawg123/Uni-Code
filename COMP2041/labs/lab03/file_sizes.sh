#!/bin/bash
files=$(ls)
small=()
medium=()
large=()
for file in $files; do
    linecount=$(echo $(wc $file) | sed 's/^ *//g' | cut -d' ' -f1)
    if [ $linecount -lt 10 ]
    then
        small+=($file)
    elif [ $linecount -lt 100 ]
    then
        medium+=($file)
    else
        large+=($file)
    fi

done

printf "Small files: "
for name in ${small[@]}; do
    printf "$name "
done
echo
printf 'Medium-sized files: '
for name in ${medium[@]}; do
    printf "$name "
done
echo
printf "Large files: "
for name in ${large[@]}; do
    printf "$name "
done
echo