#!/bin/dash
# == Test that a rm --cached can be re added to the repo ==
# create a file
# try tigger add
# try tigger commit
# try tigger status
# try tigger log
# try tigger show
# try tigger rm

PATH="$PATH:$(pwd)"

test_dir="$(mktemp -d)"
cd "$test_dir" || exit 1

expected_output="$(mktemp)"
actual_output="$(mktemp)"

trap 'rm "$expected_output" "$actual_output" -rf "$test_dir"' INT HUP QUIT TERM EXIT 

# create new repository

cat > "$expected_output" <<EOF
Initialized empty tigger repository in .tigger
EOF

tigger-init > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# create new file
echo 1>a

# add file to repo
cat > "$expected_output" <<EOF
EOF

tigger-add a > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# commit file to repo
cat > "$expected_output" <<EOF
Committed as commit 0
EOF

tigger-commit -m "first commit" > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# check file status
cat > "$expected_output" <<EOF
a - same as repo
EOF

tigger-status > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# remove file
cat > "$expected_output" <<EOF
EOF

tigger-rm --cached a > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# check status again
cat > "$expected_output" <<EOF
a - untracked
EOF

tigger-status > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# add file back to index
cat > "$expected_output" <<EOF
EOF

tigger-add a> "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# Commit file again
cat > "$expected_output" <<EOF
nothing to commit
EOF

tigger-commit -m "second commit"> "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# check status again
cat > "$expected_output" <<EOF
a - same as repo
EOF

tigger-status> "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi