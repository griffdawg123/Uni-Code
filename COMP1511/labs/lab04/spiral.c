// Prints out a spiral in a grid of nxn size
// Griffin Doyle (z53110980
// 09/03/20

#include <stdio.h>

int main(void) {

    int size = 0;
    printf("Enter size: ");
    scanf("%d", &size);
    
    
    int row = 0, col = 0;
    while (row < size) {
        col = 0;
        if ((row == 0) || (row == size-1)) {
            while (col < size) {
                printf("*");
                col++;
            }

        } else if ((row < (size+1)/2) && (row % 2 == 0)) {
            while (col < size) {
                if (col == (size - (row+1)/2)) {
                    printf("*");
                } else {
                    printf("-");
                }
                col++;
            }
        }
        printf("\n");
        row++;
    }
    
    return 0;
}




/*

row = 0 and row= n-1 are full lines of stars
every second line:
    for row <= (n+1)/2, stars from the right is (row+1)/2, stars from the left is (row-1)/22
    for row > (n+1)/2,  
    
*/

