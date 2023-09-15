#include <stdio.h>
#include <stdint.h>
#include <assert.h>

#include "add.h"

// return the MIPS opcode for add $d, $s, $t
uint32_t add(uint32_t d, uint32_t s, uint32_t t) {

    uint32_t instruction = 0;
    instruction = instruction | ((s & 0b11111) << 21);
    instruction = instruction | ((t & 0b11111) << 16);
    instruction = instruction | ((d & 0b11111) << 11);
    instruction = instruction | 0b00000100000;
    return instruction;
}
