// A program that removes duplicate values from an array
// Griffin Dolye (z5311098)
// 16/03

#include <stdio.h>

int remove_duplicates(int length, int source[length], int destination[length]); 

int main (void) {
    

    return 0;
}

int remove_duplicates(int length, int source[length], int destination[length]) {
    int index = 0;
    int i = 0;
    while (i < length) {
        int j = 0;
        int unique = 1;
        while (j < length) {
            //If value is the same but the index is different then skip this 
            //number if already in destination
            if (source[i] == source[j] && i != j) {
                int k = 0;
                int alreadyFound = 0;
                while (k < length) {
                    if (source[i] == destination[k]) {
                        alreadyFound++;
                        unique--;
                        k = length;
                        j = length;
                    }
                }
                if(!alreadyFound) {
                    destination[index] = source[i];
                    index++;
                }
            }
        }
        if(unique) {
            destination[index] = source[i];
            index++;
        }
        i++;
    }
    return index;
} 


/*
3, 1, 4, 1, 5, 9


*/
