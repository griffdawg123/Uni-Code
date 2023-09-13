#!/bin/dash
# == Test that no commands can be used without a valid tigger repository ==

PATH="$PATH:$(pwd)"

test_dir="$(mktemp -d)"
cd "$test_dir" || exit 1

expected_output="$(mktemp)"
actual_output="$(mktemp)"

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT 

# create a file
echo 1>a

# try tigger add
cat > "$expected_output" <<EOF
tigger-add: error: tigger repository directory .tigger not found
EOF

tigger-add > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# try tigger commit
cat > "$expected_output" <<EOF
tigger-commit: error: tigger repository directory .tigger not found
EOF

tigger-commit -m "first commit" > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# try tigger log
cat > "$expected_output" <<EOF
tigger-log: error: tigger repository directory .tigger not found
EOF

tigger-log > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# try tigger status
cat > "$expected_output" <<EOF
tigger-status: error: tigger repository directory .tigger not found
EOF

tigger-status > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# try tigger rm
cat > "$expected_output" <<EOF
tigger-rm: error: tigger repository directory .tigger not found
EOF

tigger-rm a> "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# try tigger branch
cat > "$expected_output" <<EOF
tigger-branch: error: tigger repository directory .tigger not found
EOF

tigger-branch new> "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# try tigger checkout
cat > "$expected_output" <<EOF
tigger-checkout: error: tigger repository directory .tigger not found
EOF

tigger-checkout new> "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# try tigger merge
cat > "$expected_output" <<EOF
tigger-merge: error: tigger repository directory .tigger not found
EOF

tigger-merge new -m new > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# try tigger show
cat > "$expected_output" <<EOF
tigger-show: error: tigger repository directory .tigger not found
EOF

tigger-show :a> "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi