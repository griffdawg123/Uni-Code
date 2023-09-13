#!/bin/dash
# === Test Functions for line num ===

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

cat > "$expected_output" <<EOF
1
2
3
4
5
5
6
7
8
9
10
EOF

seq 1 10 | slippy 5p > "$actual_output" 2>&1

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
8
9
10
EOF

seq 1 10 | slippy 7d > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

cat > "$expected_output" <<EOF
10
11
12
13
~~~
15
16
17
18
19
20
EOF

seq 10 20 | 2041 slippy '5s|1.?|~~~|g' > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi
