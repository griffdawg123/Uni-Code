#!/bin/dash

# === Test file inputs === 
PATH="$PATH:$(pwd)"

test_dir="$(mktemp -d)"
cd "$test_dir" || exit 1

expected_output="$(mktemp)"
actual_output="$(mktemp)"

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT 

cat > "$expected_output" <<EOF
100
foo
102
103
104
105
106
107
108
109
110
foo
112
EOF

seq 100 112 > hundred.txt
slippy 's/1.1/foo/g' hundred.txt > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

cat > "$expected_output" <<EOF
100
foo
102
103
104
105
106
107
108
109
110
foo
112
EOF

echo 's/1.1/foo/g' > commands.slippy
seq 100 112 | slippy -f commands.slippy > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

cat > "$expected_output" <<EOF
100
foo
102
103
104
105
106
107
108
109
110
foo
112
EOF

slippy -f commands.slippy hundred.txt > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi