#!/bin/dash
# == Check usage of infiles and replaceing ==

PATH="$PATH:$(pwd)"

test_dir="$(mktemp -d)"
cd "$test_dir" || exit 1

expected_output="$(mktemp)"
actual_output="$(mktemp)"

seq 1 2 > two.txt
seq 1 5 > five.txt
touch empty.txt

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT 

cat > "$expected_output" <<EOF
1
2
3
3
5
EOF

slippy '3p;4d' five.txt > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

cat > "$expected_output" <<EOF
1
1
3
4
5
EOF

slippy '/2/d;4q' two.txt five.txt > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

cat > "$expected_output" <<EOF
1
1
3
4
5
EOF

slippy '/2/d;4q' two.txt empty.txt five.txt > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi
