//ciphers a string using a user entered cipher
//Griffin Doyle (z5311098)
//30/03

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
            if (character == alphabet[i]) {
                putchar(cipher[i]);
                i = 26;
            } else if (character + lower == alphabet[i]) { 
                putchar(cipher[i] + upper);
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
