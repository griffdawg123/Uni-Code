// a program that prints all integers up to a max divisible by 3 or 5
// Griffin Doyle (z5311098), 02/03/20

#include <stdio.h>

int main (void) {
    int max = 0;
    int counter = 1;
    printf("Enter number: ");
    scanf("%d", &max);
    while (counter < max) {
        if (counter % 3 == 0 || counter % 5 == 0) {
            printf("%d\n", counter);
        }
        counter++;
    }
    
    return 0;
}
