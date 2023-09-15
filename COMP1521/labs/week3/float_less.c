// Compare 2 floats using bit operations only

#include <stdint.h>
#include <stdlib.h>
#include <assert.h>

#include "floats.h"


float_components_t float_bits(uint32_t f);
int is_nan(float_components_t f);
int is_positive_infinity(float_components_t f);
int is_negative_infinity(float_components_t f);
int is_zero(float_components_t f);

// float_less is given the bits of 2 floats bits1, bits2 as a uint32_t
// and returns 1 if bits1 < bits2, 0 otherwise
// 0 is return if bits1 or bits2 is Nan
// only bit operations and integer comparisons are used
uint32_t float_less(uint32_t bits1, uint32_t bits2) {
    // PUT YOUR CODE HERE
    float_components_t one = float_bits(bits1);
    float_components_t two = float_bits(bits2);
    if ((bits1 ^ bits2) == 0) {
        return 0;
    }
    if(is_nan(one) || is_nan(two)) {
        return 0;
    }
    if (is_negative_infinity(one)) {
        return 1;
    } else if(is_positive_infinity(one)) {
        return 0;
    }
    if (is_negative_infinity(two)){
        return 0;
    } else if(is_positive_infinity(two)) {
        return 1;
    }

    if (is_zero(one)) {
        if (two.sign == 1) {
            return 0;
        } else {
            return 1;
        }
    } else if (is_zero(two)) {
        if (one.sign == 1) {
            return 1;
        } else {
            return 0;
        }
    }

    if ((one.sign == 1) && (two.sign == 0)) {
        return 1;
    } else if ((one.sign == 0) && (two.sign == 1)) {
        return 0;
    }

    if (one.exponent-127 < two.exponent-127) {
        return 1;
    } else if(one.exponent-127 > two.exponent-127) {
        return 0;
    }

    if (one.sign == 0) {
        if (one.fraction < two.fraction) {
            return 1;
        } else if (one.fraction > two.fraction) {
            return 0;
        }
    } else if (one.sign == 1) {
        if (one.fraction < two.fraction) {
            return 0;
        } else if (one.fraction > two.fraction) {
            return 1;
        }
    }
    return 0;
}

#define SIGN 0b1
#define EXP 0b11111111
#define FRAC 0b11111111111111111111111

// separate out the 3 components of a float
float_components_t float_bits(uint32_t f) {
    struct float_components *float_components = malloc(sizeof(struct float_components));
    float_components->sign = (f >> 31) & SIGN;
    float_components->exponent = (f >> 23) & EXP;
    float_components->fraction = f & FRAC;
    return *float_components;
}

// given the 3 components of a float
// return 1 if it is NaN, 0 otherwise
// NaN --> 01111111111111111111111111111111
// exponents ^ EXP should be 0
// fraction ^ FRAC should be 0
int is_nan(float_components_t f) {
    return (((f.exponent & EXP) == EXP) && ((f.fraction & FRAC) != 0));
}

// given the 3 components of a float
// return 1 if it is inf, 0 otherwise
// inf --> 01111111100000000000000000000000
// sign ^ SIGN should be 1
// exponent ^ EXP should be 0
int is_positive_infinity(float_components_t f) {
    return (((f.sign & SIGN) == 0) && ((f.exponent & EXP) == EXP) && ((f.fraction & FRAC) == 0));
}

// given the 3 components of a float
// return 1 if it is -inf, 0 otherwise
// -inf --> 11111111100000000000000000000000
int is_negative_infinity(float_components_t f) {
    return (((f.sign & SIGN) == SIGN) && ((f.exponent & EXP) == EXP));
}

// given the 3 components of a float
// return 1 if it is 0 or -0, 0 otherwise
// 0 --> 0/1 0000000000000000000000000000000
// exponent ^ EXP should be 1
// fraction ^ FRAC should be 1
int is_zero(float_components_t f) {
    return (((f.exponent & EXP) == 0) && ((f.fraction & FRAC) == 0));
}