// A program which reads integers line by line, and when it reaches the end of 
// input, prints those integers in reverse order, line by line. 
// Griffin Doyle (z5311098)
// 09/03/20

#include <stdio.h>

#define MAX_SIZE 100

int main(void) {
    // creates an array of numbers
    int numbers[MAX_SIZE];
    printf("Enter numbers forwards: \n");    

    int i = 0;
    while (scanf("%d", &numbers[i]) == 1) {
        // iterates through the arrays numbers and allows the user to
        // input numbers until they press "Control + D"
        i++;
    }
    printf("Reversed: \n");
    while (i > 0) {
        i--;
        printf("%d\n", numbers[i]);
    }
    
    return 0;
}
