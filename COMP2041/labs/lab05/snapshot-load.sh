#!/bin/dash
backupdir=0
while [ -d ".snapshot.$backupdir" ]
do
    backupdir=$((backupdir+1))
done
dirname=".snapshot.$backupdir"
echo "Creating snapshot $backupdir"
# echo "$dirname"
mkdir "$dirname"
for file in *
do
    if [ ! "$file" = "snapshot-save.sh" ] && [ ! "$file" = "snapshot-load.sh" ]
    then
        cp "$file" "$dirname/$file"
    fi
done
snapshotno=$1
dirname=".snapshot.$snapshotno"
echo "Restoring snapshot $1"
for file in "$dirname"/*
do
    cp "$file" "$(echo "$file" | sed 's/.*\/\(.*\..*\)$/\1/g')"
done