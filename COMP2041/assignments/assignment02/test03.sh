#!/bin/dash
# === Test multiple functions ===

PATH="$PATH:$(pwd)"

test_dir="$(mktemp -d)"
cd "$test_dir" || exit 1

expected_output="$(mktemp)"
actual_output="$(mktemp)"

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT 

cat > "$expected_output" <<EOF
10
11
12
13
14
16
17
18
19
20
EOF

seq 1 20 | 2041 slippy -n '15d;/../p' > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

cat > "$expected_output" <<EOF
1
2
3
4
6
7
8
9
10
EOF

seq 1 20 | 2041 slippy '/.?5/d;10q' > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

cat > "$expected_output" <<EOF
10
11
12
1!
14
15
16
17
18
19
20
21
22
2!
24
25
26
27
28
29
!0
EOF

seq 1 30 | slippy -n 's/3/!/g;/../p' > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi
