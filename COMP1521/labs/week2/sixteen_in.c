//
// Sample solution for COMP1521 lab exercises
//
// Convert string of binary digits to 16-bit signed integer

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <assert.h>
#include <math.h>

#define N_BITS 16

int16_t sixteen_in(char *bits);

int main(int argc, char *argv[]) {

    for (int arg = 1; arg < argc; arg++) {
        printf("%d\n", sixteen_in(argv[arg]));
    }

    return 0;
}

//
// given a string of binary digits ('1' and '0')
// return the corresponding signed 16 bit integer
//
int16_t sixteen_in(char *bits) {

    int16_t number = 0;
    int i = 0;
    while (i < N_BITS) {
        int16_t inputVal = bits[i]-'0';
        number = number | (inputVal << (N_BITS - i - 1));
        
        //for each bit in the input, add it at the right position
        i++;
    }

    return number;
}

