// A program that prins a number of boxes given by the user
// Griffin Doyle (z5311098)
// 16/03

#include <stdio.h>

#define SIZE 199

void assignVals(int grid[SIZE][SIZE], int buffer, int size) {
    int i = buffer;
    while (i < size-buffer) {
        int j = buffer;
        while (j < size-buffer) {
            if (buffer%2 == 0) {
                grid[i][j] = 1;
            } else {
                grid[i][j] = 0;
            }
            j++;
        }
        i++;
    }
}

void printGrid(int grid[SIZE][SIZE], int size) {
    int i = 0;
    while (i < size) {
        int j = 0;
        while (j < size) {
            printf("%d", grid[i][j]);
            j++;
        }
        printf("\n");
        i++;
    }
}

int main (void) {
    int size;
    int grid[SIZE][SIZE] = {0};
    int buffer = 0;
    
    printf("How many boxes: ");
    scanf("%d", &size);
    while (buffer < size*2) {
        assignVals(grid, buffer, 4 * size - 1);
        buffer++;
    }
    printGrid(grid, 4 * size - 1);
    return 0;
}


