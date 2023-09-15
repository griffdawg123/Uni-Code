// Sample solution for COMP1521 lab exercises
//
// generate the opcode for an addi instruction

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <assert.h>

#include "addi.h"

// return the MIPS opcode for addi $t,$s, i
uint32_t addi(int t, int s, int i) {

    uint32_t result = 0b00100000000000000000000000000000;
    result = result | (s << 21);
    result = result | (t << 16);
    result = result | (i & 0xFFFF);
    

    return result; // REPLACE WITH YOUR CODE

}
