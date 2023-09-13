#!/bin/dash
file=$1
backupno=0
while [ -f ".$file.$backupno" ]
do
    backupno=$((backupno+1))
done
backupname=".$file.$backupno"
cp "$file" "$backupname"
echo "Backup of '$file' saved as '$backupname'"