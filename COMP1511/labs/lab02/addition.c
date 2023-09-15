//adds two numbers together entered by the user
//Griffin Doyle (z5311098, February 2020

#include <stdio.h>

int main(void) {
    int num1, num2;
    int sum;
    
    printf("Please enter two integers: ");
    scanf("%d %d", &num1, &num2);
    sum = num1 + num2;
    printf("%d + %d = %d\n", num1, num2, sum);
    return 0;
}
