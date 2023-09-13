#!/bin/dash
# == test branching functionality ==

PATH="$PATH:$(pwd)"

test_dir="$(mktemp -d)"
cd "$test_dir" || exit 1

expected_output="$(mktemp)"
actual_output="$(mktemp)"

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT 

cat > "$expected_output" <<EOF
!aaaaaa!
!!aaaaa!!
!!!aaaa!!!
!!!!aaa!!!!
!!!!!aa!!!!!
!!!!!!a!!!!!!
!!!!!!!!!!!!!!
!!!!!!!!!!!!!!
EOF

echo s/([^!]*)[^!]/!\1!/ > commands.slippy
echo t skip >> commands.slippy
echo : begin >> commands.slippy
echo q >> commands.slippy
echo : skip >> commands.slippy
echo p >> commands.slippy
echo b begin >> commands.slippy
echo aaaaaaa | slippy -f commands.slippy  > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

cat > "$expected_output" <<EOF
>234567890123456789
>>34567890123456789
>>>4567890123456789
>>>>567890123456789
>>>><67890123456789
>>>><<7890123456789
>>>><<<890123456789
>>>><<<<90123456789
>>>><<<<<0123456789
>>>><<<<<>123456789
>>>><<<<<>>23456789
>>>><<<<<>>>3456789
>>>><<<<<>>>>456789
>>>><<<<<>>>>>56789
>>>><<<<<>>>>><6789
>>>><<<<<>>>>><<789
>>>><<<<<>>>>><<<89
>>>><<<<<>>>>><<<<9
>>>><<<<<>>>>><<<<<
>>>><<<<<>>>>><<<<<
EOF

echo : right > commands.slippy
echo s/[^<>]/>/ >> commands.slippy
echo t skip1 >> commands.slippy
echo q >> commands.slippy
echo : skip1 >> commands.slippy
echo p >> commands.slippy
echo /[<>]+5/b left >> commands.slippy
echo b right >> commands.slippy
echo : left >> commands.slippy
echo s/[^<>]/</ >> commands.slippy
echo t skip2 >> commands.slippy
echo q >> commands.slippy
echo : skip2 >> commands.slippy
echo p >> commands.slippy
echo /[<>]+0/b right >> commands.slippy
echo b left >> commands.slippy
echo 1234567890123456789 | 2041 slippy -f commands.slippy   > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi
