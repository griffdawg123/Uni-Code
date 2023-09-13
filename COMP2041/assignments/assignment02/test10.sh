#!/bin/dash
# == replacement in file testing ==

PATH="$PATH:$(pwd)"

test_dir="$(mktemp -d)"
cd "$test_dir" || exit 1

expected_output="$(mktemp)"
actual_output="$(mktemp)"

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT \

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
=1=0
11
12
13
14
15
16
17
18
19
=2=0
EOF

seq 1 20 | twenty.txt
2041 slippy -i '/0$/s/^(.)/=\1=/' twenty.txt 
cat twenty.txt > "$actual_output" 2>&1

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
15
16
17
18
19
20
EOF

seq 1 20 | twenty.txt
2041 slippy -i -n 'p' twenty.txt 
cat twenty.txt > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi