//prints the range between two numbers 
//Griffin Doyle (z5311098), 01/03/20

#include <stdio.h>

int main(void) {
    int min = -1, max = -1;
    printf("Enter start: ");
    scanf("%d", &min);
    printf("Enter finish: ");
    scanf("%d", &max);
    while (min <= max) {
        printf("%d\n", min);
        min++;
    }
    return 0;
}
