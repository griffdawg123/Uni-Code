//A program that takes a cipher and a jumbled sentence and unscrambles it
//Griffin Doyle (z5311098)
//31/03

#include <stdio.h>

int inAlphabet(int c);

int main(void) {
    int upper = 'A'-'a';
    int lower = 'a'-'A';

    char cipher[27];
    char alphabet[] = "abcdefghijklmnopqrstuvwxyz";
    fgets(cipher, 27, stdin);
    int character = 0;
    character = getchar();
    character = getchar();
    int i = 0;
    while (character != EOF) {
        while (i < 26) {
            //printf("%d %d %d %d\n", character, i, alphabet[i], cipher[i]);
            if (character == cipher[i]) {
                putchar(alphabet[i]);
                i = 26;
            } else if (character + lower == cipher[i]) {
                putchar(alphabet[i] + upper);
                i = 26; 
            } else if (inAlphabet(character)) {
                i++;
            } else {
                
                putchar(character);
                
                i = 26;
            }
            
        }
        character = getchar();
        i=0;
    }
}

int inAlphabet(int c) {
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z');
}
