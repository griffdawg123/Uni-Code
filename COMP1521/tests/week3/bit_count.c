// count bits in a uint64_t

#include <assert.h>
#include <stdint.h>
#include <stdlib.h>



// return how many 1 bits value contains
int bit_count(uint64_t value) {
    //for i in each bit (left shift 1 by i)
    //check if result is not 0, hence add 1
    uint64_t one = 0x0000000000000001;
    int count = 0;
    for (int i = 0; i < 64; i++) {
        if ((one << i) & value) {
            count++;
        }
    }

    return count;
}
