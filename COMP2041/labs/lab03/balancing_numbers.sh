#!/bin/bash
while IFS='$\n' read -r input
do
    for ((i=0; i<${#input}; i++)); do
        char="${input:$i:1}"
        if [[ "$char" == '\n' ]]
        then
            echo newline
        fi
        if [[ "$char" =~ ^[0-9]$ ]]
        then
            if [ $char -lt 5 ]
            then
                input=$(echo $input | tr "$char" "<")
            elif [ $char -gt 5 ]
            then
                input=$(echo $input | tr "$char" ">")
            fi
        fi
    done
    echo -e "$input"
done