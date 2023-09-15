// Determines the most frequent input in the command line args

#include <stdio.h>
#include <string.h>

int main (int argc, char *argv[]) {
    int currIndex = 1;
    int maxIndex = 0;
    int maxAmount = 0;
    
    
    while (currIndex < argc) {
        int i = 1;
        int amount = 0;
        // how many of current one is in argv
        while (i < argc) {
            if (strcmp(argv[i], argv[currIndex]) == 0) {
                amount++;
            }
            i++;
        }
        // re assign max
        if (amount > maxAmount) {
            maxIndex = currIndex;
            maxAmount = amount;
        }
        
        currIndex++;
    }
    printf("%s", argv[maxIndex]);
    
}
