// Multiply a float by 2048 using bit operations only

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <assert.h>

#include "floats.h"

#define SIGN 0b1
#define EXP 0b11111111
#define FRAC 0b11111111111111111111111

// float_2048 is given the bits of a float f as a uint32_t
// it uses bit operations and + to calculate f * 2048
// and returns the bits of this value as a uint32_t
//
// if the result is too large to be represented as a float +inf or -inf is returned
//
// if f is +0, -0, +inf or -int, or Nan it is returned unchanged
//
// float_2048 assumes f is not a denormal number
//
float_components_t float_bits(uint32_t f) {
    struct float_components *float_components = malloc(sizeof(struct float_components));
    float_components->sign = (f >> 31) & SIGN;
    float_components->exponent = (f >> 23) & EXP;
    float_components->fraction = f & FRAC;
    return *float_components;
}

uint32_t float_2048(uint32_t f) {
    //2048 is 2^11
    // 2^(138-127)
    // E = 2^7 + 2^3 + 2^1 = 10001010
    float_components_t a = float_bits(f);
    if (((a.exponent & EXP) == EXP) && ((a.fraction & FRAC) != 0)) {
        return f;
    } else if (((a.sign & SIGN) == 0) && ((a.exponent & EXP) == EXP) && ((a.fraction & FRAC) == 0)) {
        return f;
    } else if (((a.sign & SIGN) == SIGN) && ((a.exponent & EXP) == EXP)) {
        return f;
    } else if (((a.exponent & EXP) == 0) && ((a.fraction & FRAC) == 0)) {
        return f;
    }
    
    
    float_components_t b = float_bits(0x45000000);
    float_components_t *result = malloc(sizeof(float_components_t));
    result->sign = a.sign;
    result->exponent = ((a.exponent) + (b.exponent-127));

    if ((result->exponent - 127 > 127) && a.exponent > 127) {
        if (result->sign) {
            return 0xff800000;
        } else {
            return 0x7f800000;
        }
    
    }
    result->fraction = a.fraction;
    uint32_t newVal = (result->sign << 31) + (result->exponent << 23) + (result->fraction );

    return newVal;
}

//0 10000010(130 = 3 + 127)  00000000000000000000000 -a 
//0 10001010(138 = 11 + 127) 00000000000000000000000 - b (2048)
//0 10001101(141 = 14 + 127) 00000000000000000000000
