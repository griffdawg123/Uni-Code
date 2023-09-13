#! /bin/dash
if [ ! -d "archive" ]; then
    mkdir "archive"
fi
i=6
while [ $i -gt 0 ]; do
    # echo $i
    
    if [ -f "log.$i" ]; then
        if [ $i = 6 ]; then
            gzip -c "log.6" > "archive/log.2021_05_06.gz"
            # gzip -c "log.6" > "archive/log.$(date +'%Y_%m_%d').gz"
        else
            mv "log.$i" "log.$((i+1))"
        fi
    fi
    i=$((i-1))
done
if [ -f "log" ]; then
    mv "log" "log.1"
fi