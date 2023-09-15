// A program that prints a hollow triangle
// Griffin Doyle (z5311098)
// 12/03

#include <stdio.h>

int main (void) {
    
    int size = 0;
    int row = 0; int col = 0;
    printf("Enter size: ");
    scanf("%d", &size);
    
    while (row < size) {
        col = 0;
        while (col < row+1) {
            if ((col != 0) && (col != row) && (row != size-1)){
                printf(" ");
            } else {
                printf("*");
            }
            col++;
        }
        printf("\n");
        row++;
    }
        
    return 0;
}
