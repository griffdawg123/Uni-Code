#!/bin/bash

if [ $# -lt 2 ] || [ $# -gt 2 ]
then
    echo "Usage: scraping_courses.sh <year> <course-prefix>"
    exit 1
elif ! [[ $1 =~ ^[0-9]+$ ]] || [ $1 -lt 2019 ] || [ $1 -gt 2022 ] 
then
    echo "./scraping_courses.sh: argument 1 must be an integer between 2019 and 2022"
    exit 1
else
    year=$1
    code=$2
    undergrad=$(echo -e $(curl -sl https://www.handbook.unsw.edu.au/api/content/render/false/query/+unsw_psubject.implementationYear:$year%20+unsw_psubject.studyLevel:undergraduate%20+unsw_psubject.educationalArea:$code*%20+unsw_psubject.active:1%20+unsw_psubject.studyLevelValue:ugrd%20+deleted:false%20+working:true%20+live:true/orderby/unsw_psubject.code%20asc/limit/10000/offset/0 | 2041 jq -r '[.contentlets[] | "\(.code) \(.title)"]'))
    postgrad=$(echo -e $(curl -sl https://www.handbook.unsw.edu.au/api/content/render/false/query/+unsw_psubject.implementationYear:$year%20+unsw_psubject.studyLevel:postgraduate%20+unsw_psubject.educationalArea:$code*%20+unsw_psubject.active:1%20+unsw_psubject.studyLevelValue:pgrd%20+deleted:false%20+working:true%20+live:true/orderby/unsw_psubject.code%20asc/limit/10000/offset/0 | 2041 jq -r '[.contentlets[] | "\(.code) \(.title)"]'))
    # https://stackoverflow.com/questions/71053907/how-to-parse-and-convert-string-list-to-json-string-array-in-shell-command
    mapfile -d '' arrayU < <(2041 jq -j '.[] + "\u0000"' <<< "$undergrad")
    mapfile -d '' arrayP < <(2041 jq -j '.[] + "\u0000"' <<< "$postgrad")

    array+=("${arrayU[@]}" "${arrayP[@]}")
    #https://stackoverflow.com/questions/7442417/how-to-sort-an-array-in-bash
    IFS=$'\n' sorted=($(sort <<<"${array[*]}"))
    unset IFS
    if [ ${#sorted[@]} -gt 0 ]
    then
        printf '%s\n' "${sorted[@]}" | uniq 
    fi
    # printf '%s\n' "${arrayP[@]}"
fi