// A program that sums user input until they cancel
// Griffin Doyle (z5311098)
// 12/03

#include <stdio.h>

int main (void) {

    int sum = 0;
    int temp = 0;
    int numbers = 0;
    
    printf("How many numbers: ");
    scanf("%d", &numbers);
    while (numbers > 0) {
        scanf("%d", &temp);
        sum += temp;
        numbers--;
    }
    printf("The sum is: %d\n", sum);
    
    
    return 0;
}
