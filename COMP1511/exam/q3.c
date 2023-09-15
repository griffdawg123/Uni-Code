// reads input until 0 and outputs the positive and negative numbers seperately
// Griffin Doyle (z5311098)
// 5/05

#include <stdio.h>

#define MAX 1000

int main (void) {
    int positives[MAX];
    int negatives[MAX];
    int posIndex = 0;
    int negIndex = 0;
    int input = 0;
    // read input until 0
    scanf("%d", &input);
    while (input != 0) {
        if (input > 0) {
            positives[posIndex] = input;
            posIndex++;
        } else if (input < 0) {
            negatives[negIndex] = input;
            negIndex++;
        }
        scanf("%d", &input);
    }
    // print out arrays;
    int i = 0;
    printf("Positive numbers were: ");
    while (i < posIndex) {
        printf("%d ", positives[i]);
        i++;
    }
    printf("\n");
    i = 0;
    printf("Negative numbers were: ");
    while (i < negIndex) {
        printf("%d ", negatives[i]);
        i++;
    }
    printf("\n");
}
