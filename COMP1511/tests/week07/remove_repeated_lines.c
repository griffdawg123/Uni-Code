//A program that prints lines but not ones that it has seen before
//Griffin Doyle (z5311098)
//02/04

#include <stdio.h>
#include <string.h>

int main (void) {
    char strs[256][256];
    int i = 0;
    while (fgets(strs[i], 256, stdin)) {
        int j = 0;
        while (j < i) {
            if (!strcmp(strs[i], strs[j])) {
                j = i;
            }
            j++;
        }
        if (j == i) {
            fputs(strs[i], stdout);
        }
        i++;
    }

    return 0;
}
