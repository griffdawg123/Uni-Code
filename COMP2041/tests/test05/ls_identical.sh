#!/bin/dash
touch tmp
# for file1 in $1/*
# do
#     if [ -f "$file1" ]; then
#         for file2 in $2/*
#         do
#             if [ -f "$file2" ]; then
#                     if diff "$file1" "$file2" >/dev/null; then
#                         echo ${file1##*/} >> tmp
#                     fi
#             fi
#         done
#     fi
# done
for file in "$1"/*
do
    file_name=${file##*/}
    # ! diff -q "$file" "$2/$file_name">/dev/null
    # echo $?
    if [ -f "$2/$file_name" ] && diff -q "$file" "$2/$file_name">/dev/null; then
        echo "$file_name" >> tmp
    fi
done
cat tmp | uniq | sort
rm tmp