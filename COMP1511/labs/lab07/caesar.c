// Ciphers a sentence uising the caesar cipher
// Griffin Doyle (z5311098)
// 30/03

#include <stdio.h>

int cipher(int key, int c);
int type(int c);

int main(void) {
    int key = 0;
    scanf("%d", &key);
    int character = getchar();
    while (character != EOF) {
        putchar(cipher(key, character));
        character = getchar();
    }
}

int cipher(int key, int c) {
    int newChar = 0;
    if (type(c) == 0) {
        newChar = c + key % 26;
        if (newChar >= 'a' && newChar <= 'z') {
            return newChar;
        } else {
            if (newChar < 'a') {
                newChar += 26;
                return newChar;
            } else {
                newChar -= 26;
                return newChar;
            }
        }
    } else if (type(c) == 1) {
        newChar = c + key % 26;
        if (newChar >= 'A' && newChar <= 'Z') {
            return newChar;
        } else {
            if (newChar < 'A') {
                newChar += 26;
                return newChar;
            } else {
                newChar -= 26;
                return newChar;
            }
        }
    } else {
        return c;
    }
}

// 0 - lower
// 1 - upper
// 2 - not letter

int type(int c) {
    if (c >= 'a' && c <= 'z') {
        return 0;
    } else if (c >= 'A' && c <= 'Z') {
        return 1;
    } else {
        return 2;
    }
}
