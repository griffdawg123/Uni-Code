#!/bin/dash
for file in $@; do
    if echo "$file" | grep -Eq "\..*$"; then
        echo "# $file already has an extension"
    fi 
    if head -n1 "$file" | grep -vEq "^#!.*"; then
        echo "# $file does not have a #! line"
    elif head -n1 "$file" | grep -vEq "(perl|python|sh)"; then
        echo "# $file no extension for #! line"
    else
        if head -n1 "$file" | grep -Eq "perl"; then
            if [ -f "$file.pl" ]; then
                echo "# $file.pl already exists"
            else
                echo "mv $file $file.pl"
                # mv "$file" "$file".pl
            fi
        elif head -n1 "$file" | grep -Eq "python"; then
            if [ -f "$file.py" ]; then
                echo "# $file.py already exists"
            else
                echo "mv $file $file.py"
                # mv "$file" "$file".py
            fi
        elif head -n1 "$file" | grep -Eq "sh"; then
            if [ -f "$file.sh" ]; then
                echo "# $file.sh already exists"
            else
                echo "mv $file $file.sh"
                # mv "$file" "$file".sh
            fi
        fi
    fi
done