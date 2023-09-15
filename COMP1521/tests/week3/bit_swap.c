// swap pairs of bits of a 64-bit value, using bitwise operators

#include <assert.h>
#include <stdint.h>
#include <stdlib.h>

// return value with pairs of bits swapped
uint64_t bit_swap(uint64_t value) {
    //get value of each bit then add to new value
    uint64_t one = 1;
    uint64_t two = 2;
    uint64_t result = 0;

    for (int i = 0; i < 64; i+=2) {
        uint64_t bit1 = value & (one << i);
        uint64_t bit2 = value & (two << i);
        result += bit1 << 1;
        result += bit2 >> 1;
    }
    return result;
}
