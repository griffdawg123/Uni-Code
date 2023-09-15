// A program that counts down from 10 to 0
// Griffin Doyle, (z5311098) 02/03/20

#include <stdio.h>

int main (void) {
    int counter = 10;
    while (counter >= 0) {
        printf("%d\n", counter);
        counter--;
    }
    return 0;
}
