// takes three integers and prints them in ascending takes
// Griffin Doyle (z5311098), 02/03/20

#include <stdio.h>

int main (void) {
    int num1, num2, num3;
    printf("Enter integer: ");
    scanf("%d", &num1);
    printf("Enter integer: ");
    scanf("%d", &num2);
    printf("Enter integer: ");
    scanf("%d", &num3);
   /*
    If two numbers are equal for first number, first number will be smaller than one number and equal to the other
    ie ((num1 < num2) && (num1 == num3)) || ((num1 < num3) && (num1 == num2))
   
   */
   /*
    printf("%d\n", ((num1 > num2) && (num1 > num3)) * num1);
    printf("%d\n", ((num2 > num1) && (num2 > num3)) * num2);
    printf("%d\n", ((num3 > num2) && (num3 > num1)) * num3);
    */
    printf("The integers in order are: %d %d %d\n",
    
	((num1 < num2) && (num1 < num3)) * num1 +
	((num2 < num1) && (num2 < num3)) * num2 +
	((num3 < num2) && (num3 < num1)) * num3 +
 
	((((num1 < num2) && (num1 == num3)) || ((num1 < num3) && (num1 == num2))) && 
	    (((num2 < num1) && (num2 == num3)) || ((num2 < num3) && (num2 == num1)))) * num1 +
	((((num2 < num1) && (num2 == num3)) || ((num2 < num3) && (num2 == num1))) && 
	    (((num3 < num2) && (num3 == num1)) || ((num3 < num1) && (num3 == num2)))) * num2 +
	((((num3 < num2) && (num3 == num1)) || ((num3 < num1) && (num3 == num2))) &&
	    (((num1 < num2) && (num1 == num3)) || ((num1 < num3) && (num1 == num2)))) * num3 +

	((num1 == num2) && (num2 == num3) && (num3 == num1)) * num1,


	(((num1 < num2) && (num1 > num3)) || ((num1 < num3) && (num1 > num2))) * num1 +
	(((num2 < num1) && (num2 > num3)) || ((num2 < num3) && (num2 > num1))) * num2 +
	(((num3 < num2) && (num3 > num1)) || ((num3 < num1) && (num3 > num2))) * num3 +

	((((num1 == num2) || (num1 == num3)) && (num2 != num3)) && (((num2 == num1) || (num2 == num3)) && (num1 != num3))) * num1 +
	((((num2 == num1) || (num2 == num3)) && (num1 != num3)) && (((num3 == num2) || (num3 == num1)) && (num1 != num2))) * num2 +
	((((num3 == num2) || (num3 == num1)) && (num1 != num2)) && (((num1 == num2) || (num1 == num3)) && (num2 != num3))) * num3 +

	((num1 == num2) && (num2 == num3) && (num3 == num1)) * num1,


	((num1 > num2) && (num1 > num3)) * num1 +
	((num2 > num1) && (num2 > num3)) * num2 +
	((num3 > num2) && (num3 > num1)) * num3 +

	((((num1 > num2) && (num1 == num3)) || ((num1 > num3) && (num1 == num2))) && 
	    (((num2 > num1) && (num2 == num3)) || ((num2 > num3) && (num2 == num1)))) * num1 + 
	((((num2 > num1) && (num2 == num3)) || ((num2 > num3) && (num2 == num1))) && 
	    (((num3 > num2) && (num3 == num1)) || ((num3 > num1) && (num3 == num2)))) * num2 + 
	((((num3 > num2) && (num3 == num1)) || ((num3 > num1) && (num3 == num2))) && 
	    (((num1 > num2) && (num1 == num3)) || ((num1 > num3) && (num1 == num2)))) * num3 +

	((num1 == num2) && (num2 == num3) && (num3 == num1)) * num1);
	
		
    
    
    
    return 0;
}
