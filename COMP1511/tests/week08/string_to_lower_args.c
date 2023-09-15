//Changes the inputted string to all lower case
//Griffin Doyle (z5311098)
//09/04

#include <stdio.h>
#include <string.h>

int isUpper(int c); 

int main(int argc, char *argv[]) {
    int lower = 'a'-'A';
    int i = 1;
    while (i < argc) {
        int j = 0;
        while(j < strlen(argv[i])) {
            if (isUpper(argv[i][j])) {
                putchar(argv[i][j]+lower);
            } else {
                putchar(argv[i][j]);
            }
            j++;
        }
        printf(" ");
        i++;
    }
    printf("\n");
}

int isUpper(int c) {
    return (c >= 'A' && c <= 'Z');
}


