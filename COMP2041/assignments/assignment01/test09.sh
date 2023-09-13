#!/bin/dash
# == Standard workflow of tigger displays standard behavious ==

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

# create README file
echo "Welcome to my tigger project!">README
touch main.py

# add initial files to the repo
cat > "$expected_output" <<EOF
EOF

tigger-add README main.py > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# add to the repo
cat > "$expected_output" <<EOF
Committed as commit 0
EOF

tigger-commit -m "first commit" > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# create a new branch
cat > "$expected_output" <<EOF
EOF

tigger-branch "hello world" > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# checkout new branch
cat > "$expected_output" <<EOF
Switched to branch 'hello world'
EOF

tigger-checkout first > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# make changes to working file
echo "print('Hello World!')">main.py

# add to the index
cat > "$expected_output" <<EOF
EOF

tigger-add a > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# add to the repo
cat > "$expected_output" <<EOF
Committed as commit 1
EOF

tigger-commit -m "hello world" > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# create new planning file
echo "TODO: add user input">todo.txt

# add to the index
cat > "$expected_output" <<EOF
EOF

tigger-add todo.txt > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# add to the repo
cat > "$expected_output" <<EOF
Committed as commit 2
EOF

tigger-commit -m "todo" > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# add stuff to main file
echo "input('Enter some text')">>main.py

# add to the repo
cat > "$expected_output" <<EOF
Committed as commit 3
EOF

tigger-commit -a -m "added input" > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# edit todo text
echo "N/A">todo.txt

# attempt to remove file
cat > "$expected_output" <<EOF
tigger-rm: error: 'todo.txt' in the repository is different to the working file
EOF

tigger-rm todo.txt > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# actually remove file
cat > "$expected_output" <<EOF
EOF

tigger-rm --force todo.txt > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# go back to master
cat > "$expected_output" <<EOF
Switched to branch 'master'
EOF

tigger-checkout master > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi

# merge in changes
cat > "$expected_output" <<EOF
Fast-forward: no commit created
EOF

tigger-merge "hello world" -m "hello world and input implemented" > "$actual_output" 2>&1

if ! diff "$expected_output" "$actual_output"; then
    echo "Failed test"
    exit 1
fi