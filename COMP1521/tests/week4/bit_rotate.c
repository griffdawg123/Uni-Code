#include "bit_rotate.h"

// return the value bits rotated left n_rotations
uint16_t bit_rotate(int n_rotations, uint16_t bits) {
    uint16_t overflow = 0;
    while(n_rotations <= 0) {
        n_rotations+=16;
    }
    n_rotations = n_rotations % 16;
    for (int i = 0; i < n_rotations; i++) {
        overflow += 1 << (15-i);
    }
    
    overflow = overflow & bits;
    
    overflow = overflow >> (16-n_rotations);
    return (bits << n_rotations) + overflow;
}

// 0b1010011111000101 << 12
// 0b110010011111000 x
// 0b101101001111100




//100111110001100
//100111110001011