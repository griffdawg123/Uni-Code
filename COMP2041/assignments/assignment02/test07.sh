#!/bin/dash
# == Test append, change and insert ==

PATH="$PATH:$(pwd)"

test_dir="$(mktemp -d)"
cd "$test_dir" || exit 1

expected_output="$(mktemp)"
actual_output="$(mktemp)"

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT 

cat > "$expected_output" <<EOF
1
2
insert
change
append
4
5
EOF

echo 3i insert > commands.slippy
echo 3a append >> commands.slippy
echo 3c change >> commands.slippy
seq 1 5 | slippy -f commands.slippy  > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

cat > "$expected_output" <<EOF
even
even
five
even
even
even
five
even
even
five
even
even
even
five
finished
EOF

echo /[02468]\$/a even > commands.slippy
echo /[05]$/a five >> commands.slippy
echo \$a finished >> commands.slippy
seq 1 20 | slippy -n -f commands.slippy  > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi