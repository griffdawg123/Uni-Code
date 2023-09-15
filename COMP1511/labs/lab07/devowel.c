// removes vowels from a string
// Griffin Doyle (z5311098)
// 30/03

#include <stdio.h>

int isVowel(int character);

int main (void) {

    int character = getchar();
    while (character != EOF) {
        if (!isVowel(character)) {
            putchar(character);
        }
        character = getchar();
    }
} 

int isVowel(int c) {
    return (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u');
}
