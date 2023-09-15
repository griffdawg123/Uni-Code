#include <stdio.h>
#include <stdlib.h>


# define TEST_ARRAY_SIZE 6

int positive_sum(int length, int array[]);

// This is a simple main function which could be used
// to test your positive_sum function.
// It will not be marked.
// Only your positive_sum function will be marked.


int main(void) {
    int test_array[TEST_ARRAY_SIZE] = {16, -12, 8, -3, 6, 12};

    int result = positive_sum(TEST_ARRAY_SIZE, test_array);
    printf("%d\n", result);

    return 0;
}


// positive_sum should return the sum of
// all the positive elements in array
int positive_sum(int length, int array[]) {
    int sum = 0;
    int i = 0;
    while (i < length) {
        if (array[i] > 0) {
            sum += array[i];
        }
        i++;
    }
    return sum;
}
