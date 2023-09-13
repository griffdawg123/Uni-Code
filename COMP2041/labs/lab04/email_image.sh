#!/bin/dash

for file in "$@"
do
    echo -e "$file displayed to the screen if possible"
    display "$file" 2> /dev/null
    read -p "Address to e-mail this image to? " email
    read -p "Message to accompany image? " message
    echo "$message" | mutt -s "Image!" -e 'set copy=0' -a "$file" -- "$email" 2> /dev/null
done