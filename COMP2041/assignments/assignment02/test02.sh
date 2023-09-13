#!/bin/dash
# === Test Functions for regex ===

PATH="$PATH:$(pwd)"

test_dir="$(mktemp -d)"
cd "$test_dir" || exit 1

expected_output="$(mktemp)"
actual_output="$(mktemp)"

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT 

cat > "$expected_output" <<EOF
1
2
3
4
5
EOF

seq 1 20 | slippy /^5/q > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

cat > "$expected_output" <<EOF
17
27
EOF

seq 15 30 | slippy -n /7/p > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

cat > "$expected_output" <<EOF
3
4
5
6
7
8
9
EOF

seq 1 30 | slippy '/[0-2]+/d' > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

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
13
14
1:)
EOF

seq 1 15 | slippy '/[0-2]/s/5$/:\)/g' > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi
