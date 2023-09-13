#!/bin/dash
# == Check that adding file to index does not alter the repo ==

# === Test different substitution delimeters===
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
113
114
115
116
117
118
119
120
EOF

seq 100 120 | slippy 'sW1.1WfooWg' > "$actual_output" 2>&1

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
113
114
115
116
117
118
119
120
EOF

seq 100 120 | slippy 's%1.1%foo%g' > "$actual_output" 2>&1

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
113
114
115
116
117
118
119
120
EOF

seq 100 120 | slippy 's~1.1~foo~g' > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi