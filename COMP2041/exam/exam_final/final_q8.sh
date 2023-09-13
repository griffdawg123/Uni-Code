#!/bin/dash
array_remove() {
    index="$
    shift
    i=1
    while [ "$i" -lt "$index" ]; do
        $((i+=1))
        echo "$1"
        shift
    done
    shift
    echo "$@"
    "
}
i=0
for file1 in $@; do
    j=0
    for file2 in $@; do
        if diff -q $file1 $file2> /dev/null; then
            if [ $j -le $i ]; then
                continue
            else
                # set -- "$(array_remove $j $@)"
                echo "ln -s $file1 $file2"
            fi
        fi 
        j=$((j+1))
    done
    i=$((i+1))
done