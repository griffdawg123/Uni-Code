// copy all of the values in source1 which are also found in source2 into destination
// return the number of elements copied into destination

#include <stdio.h>

#define SIZE 10

int common_elements(int length, int source1[length], int source2[length], int destination[length]) {
    int index = 0;
    int i = 0;
    while (i < length) {
        int j = 0;
        while (j < length) {
            if (source1[i] == source2[j]) {
                destination[index] = source1[i];
                index++;
                j = length;
            } else {
                j++;
            }
        }
        i++;
    }
    return index;
}

// You may optionally add a main function to test your common_elements function.
// It will not be marked.
// Only your common_elements function will be marked.

int main (void) {
    int source1[SIZE] = {3,1,4,1,5,9,2,6,5,3};
    int source2[SIZE] = {9,2,3,4,5,6,7,8,1,9};
    int destination[SIZE] = {0};
    int i = 0;
    printf("%d\n", common_elements(SIZE, source1, source2, destination));
    while (i < SIZE) {
        printf("%d\n", destination[i]);
        i++;
    }

    return 0;
}
