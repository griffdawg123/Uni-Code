//A program that prints out a string in reverse
//Griffin Doyle (z5311098)
// 02/04

#include <stdio.h>

int main(void) {
    char str[256]={' '};
    while(fgets(str, 256, stdin)) {
        int i = 0;
        while (str[i] != '\0') {
            i++;
        }
        int nl = 0;
        while (i >= 0) {
            if(str[i] != '\0') {
                if (nl) {
                    printf("%c", str[i]);
                } else {
                    nl++;
                }
            }
            i--;
        }
        printf("\n");
    }
}
