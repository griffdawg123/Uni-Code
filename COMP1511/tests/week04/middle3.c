// A program that prints the middle of three integers
// Griffin Doyle (z5311098)
// 12/03/20

#include <stdio.h>

int main(void) {

    int num1, num2, num3;
    
    printf("Enter integer: ");
    scanf("%d", &num1);
    printf("Enter integer: ");
    scanf("%d", &num2);
    printf("Enter integer: ");
    scanf("%d", &num3);
    
    if (((num1 >= num2) && (num1 <= num3)) || ((num1 <= num2) && (num1 >= num3))) {
        printf("Middle: %d\n", num1);
    } else if (((num2 >= num1) && (num2 <= num3)) || ((num2 <= num1) && (num2 >= num3))) {
        printf("Middle: %d\n", num2);
    } else {
        printf("Middle: %d\n", num3);
    }
    
    return 0;
}
