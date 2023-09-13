#!/bin/dash
dir1=$1
dir2=$2
same=0
diff=0
one=0
two=0
for file1 in $(find $dir1/*); do
    if [ ! -d $file1 ]; then
        file2=$(echo $file1 | sed "s/"^$dir1"/"$dir2"/")
        if [ -f $file2 ]; then
            size1=$(wc -c $file1 | cut -d" " -f1)
            size2=$(wc -c $file2 | cut -d" " -f1)
            if [ $size1 = $size2 ]; then
                same=$((same+1))
            else
                diff=$((diff+1))
            fi
        else
            one=$((one+1))
        fi
    fi
done
for file2 in $(find $dir2/*); do
    if [ ! -d $file2 ]; then
        file1=$(echo $file2 | sed "s/"$dir2"/"$dir1"/")
        if [ ! -f $file1 ]; then
            two=$((two+=1))
        fi
    fi
done
echo "$same $diff $one $two"