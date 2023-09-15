//ouputs whether or not a year is a leap year
//Griffin Doyle (z5311098), February 2020

#include <stdio.h>

int main(void) { 
    int year;
    printf("Enter year: ");
    scanf("%d", &year);
    if (year % 400 == 0) {
        printf("%d is a leap year.\n", year);
    } else {
        if (year % 100 == 0) {
            printf("%d is not a leap year.\n", year);
        } else {
            if (year % 4 == 0) {
                printf("%d is a leap year.\n", year);
            } else {
                printf("%d is not a leap year.\n", year);
            }
        }
    }
    return 0;
}
