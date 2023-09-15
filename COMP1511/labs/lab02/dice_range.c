//calculates the max and min values of a set of dice and the average values of them
//Griffin Doyle (z5311098), February 2020

#include <stdio.h>

int main (void) {
    int sides, dice;
    int max, min;
    float avg;
    
    printf("Enter the number of sides on your dice: ");
    scanf("%d", &sides);
    printf("Enter the number of dice being rolled: ");
    scanf("%d", &dice);
    
    if (sides <= 0 || dice <= 0) {
        printf("These dice will not produce a range.\n");
    } else {
        max = sides * dice;
        min = dice;
        avg = ((max+min)*1.0)/2;
        
        printf("Your dice range is %d to %d.\n", min, max);
        printf("The average value is %f\n", avg);
    } 
    return 0;
} 

