// swaps upper case to lower case and vice versa
// Griffin Doyle (z5311098)
// 30/03

#include <stdio.h>

int swap(int c);

int main(void) {
    int character = getchar();
    while (character != EOF) {
        putchar(swap(character));
        character = getchar();
    }
}

int swap(int c) {
    if (c >= 'a' && c <= 'z') {
        int alphabetPosition = c - 'a';
        return 'A' + alphabetPosition;
    } else if (c >= 'A' && c <= 'Z') {
        int alphabetPosition = c - 'A';
        return 'a' + alphabetPosition;
    } else {
        return c;
    }
}
