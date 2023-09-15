// draws an x the size that the user inputs
// Griffin Doyle (z5311098), 02/03/20

#include <stdio.h>

int main (void) {
    int size;
    int row = 1;
    int col;
    printf("Enter size: ");
    scanf("%d", &size);
    while (row <= size) {
        col = 1;
        while (col <= size) {
            if ((col == row) || ((size - col + 1) == row)) {
                printf("*");
            } else {
                printf("_");
            }
            col++;
        }
        printf("\n");
        row++;
    }
    return 0;
} 
