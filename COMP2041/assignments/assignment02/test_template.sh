#!/bin/dash
# == Check that adding file to index does not alter the repo ==

PATH="$PATH:$(pwd)"

test_dir="$(mktemp -d)"
cd "$test_dir" || exit 1

expected_output="$(mktemp)"
actual_output="$(mktemp)"

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT 

# Test quit for line num

cat > "$expected_output" <<EOF
1
2
3
4
5
6
7
8
9
10
11
12
EOF

seq 1 20 | slippy 12q > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi
