// Swap bytes of a short

#include <stdint.h>
#include <stdlib.h>
#include <assert.h>

// given uint16_t value return the value with its bytes swapped
uint16_t short_swap(uint16_t value) {
    // get value of first and second byte seperately
    // add them together but shifted accordingly
    uint16_t bit1 = value & 0xFF00;
    uint16_t bit2 = value & 0x00FF;
    uint16_t result = (bit1 >> 8) + (bit2 << 8);
    return result;
}
