#!/bin/dash
regex=$1
file=$2
# echo $(cat "$file" | grep -E "$regex" | head -n1 | cut -d"|" -f2)
first_year=$(cat "$file" | grep -E "$regex" | head -n1 | cut -d"|" -f2)
last_year=$(cat "$file" | grep -E "$regex" | head -n1 | cut -d"|" -f2)
while read line; do
    if echo "$line" | grep -Eq "$regex"; then
        year=$(echo "$line" | cut -d"|" -f2)
        if [ "$year" -gt "$last_year" ]; then
            last_year="$year"
        elif [ "$year" -lt "$first_year" ]; then
            first_year="$year"
        fi
    fi
done < "$file"
seq "$first_year" "$last_year" >tmp
# cat tmp
# cat "$file" | grep -E "^$regex|" | cut -d"|" -f2 | sort | uniq
cat "$file" | grep -E "$regex" | cut -d"|" -f2 | sort | uniq | grep -v -f - tmp
rm -f tmp