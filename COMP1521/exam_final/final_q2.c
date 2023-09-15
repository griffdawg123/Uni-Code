#include <assert.h>
#include <stdint.h>
#include <stdlib.h>

// given a uint32_t value,
// return 1 iff the least significant (bottom) byte
// is equal to the 2nd least significant byte; and
// return 0 otherwise
int final_q2(uint32_t value) {

    int first = value & 0xFF;
    int second = (value & 0xFF00) >> 8;

    if (first == second) {
        return 1;
    } 
    
    return 0;
}
