#!/bin/dash
# === test whitespace and comments ===

PATH="$PATH:$(pwd)"

test_dir="$(mktemp -d)"
cd "$test_dir" || exit 1

expected_output="$(mktemp)"
actual_output="$(mktemp)"

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT 

cat > "$expected_output" <<EOF
1
2
three
4
6
7
8
9
10
10
11
12
1three
14
15
16
17
EOF

seq 1 20 | slippy '10 p;5d   ;/.?3/  s/3/three/;  17   q;' > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

cat > "$expected_output" <<EOF
90
91
92
93
94
95
96
97
98
99
100+
100+
100+
100+
100+
100+
100+
100+
100+
100+
100+
EOF

seq 90  110 | slippy 's/[0-9]{3}/100+/ # over hundreds changed' > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

cat > "$expected_output" <<EOF
!
!O
!OO
!OOO
EOF

echo 's/1/!/g # turn 1 to exclamations' > commands.slippy
echo 's/0/O/g # turn 0 to O' >> commands.slippy
echo '/^!O*$/p # print powers of 10' >> commands.slippy

seq 1 1000 | slippy -n -f commands.slippy > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi