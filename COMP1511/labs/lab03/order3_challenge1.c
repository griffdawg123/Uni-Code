// takes three integers and prints them in ascending takes
// Griffin Doyle (z5311098), 02/03/20

#include <stdio.h>

int main (void) {
    int num1, num2, num3, temp = 0;
    printf("Enter integer: ");
    scanf("%d", &num1);
    printf("Enter integer: ");
    scanf("%d", &num2);
    printf("Enter integer: ");
    scanf("%d", &num3);
    
    temp = (num1 >= num2) * num1 + (num2 > num1) * num2;
    num1 = (num1 >= num2) * num2 + (num2 > num1) * num1;
    num2 = temp;
    
    temp = (num1 >= num3) * num1 + (num3 > num1) * num3;
    num1 = (num1 >= num3) * num3 + (num3 > num1) * num1;
    num3 = temp;
    
    temp = (num2 >= num3) * num2 + (num3 > num2) * num3;
    num2 = (num2 >= num3) * num3 + (num3 > num2) * num2;
    num3 = temp;
    
    printf("The integers in order are: %d %d %d\n", num1, num2, num3);
    return 0;
}
