// Print a 2D array
// Griffin Doyle (z5311098)
// 09/03/20

#include <stdio.h>

#define SIZE 4

void print_2D_array(int array[SIZE][SIZE]);


int main(void) {
    int array[SIZE][SIZE] = {
        {0, 1, 2, 3}, 
        {4, 5, 6, 7}, 
        {8, 9, 10, 11}, 
        {12, 13, 14, 15}
    };
    print_2D_array(array);
    return 0;
}

void print_2D_array(int array[SIZE][SIZE]) {

    int rows = 0;
    int cols;
    
    
    while (rows < SIZE) {
        //column number is reset to 0 at the start of each row
        cols = 0;
        while (cols < SIZE) {
            if (array[rows][cols] < 10) {
                printf("0");
            }
            // print value at location (rows, cols)
            printf("%d ", array[rows][cols]);
            cols++;
        }
        // new line at the end of each row
        printf("\n");
        rows++;
    }
    
}
