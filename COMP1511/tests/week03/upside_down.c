// A Program that prints the direction of the order of numbers
// Griffin Doyle (z5311098)
// 10/03/20

#include <stdio.h>

int main(void) {
    
    double num1, num2, num3;
    
    printf("Please enter three numbers: ");
    scanf("%lf %lf %lf", &num1, &num2, &num3);
    if ((num1 > num2) && (num2 > num3)) {
        printf("down\n");
    } else if ((num1 < num2) && (num2 < num3)) {
        printf("up\n");
    } else {
        printf("neither\n");
    }
    return 0;
}
