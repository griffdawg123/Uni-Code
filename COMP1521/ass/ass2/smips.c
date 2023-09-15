#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

// Instruction constants

#define ADD 1
#define SUB 2
#define AND 3
#define OR 4
#define SLT 5
#define MUL 6
#define BEQ 7
#define BNE 8
#define ADDI 9
#define SLTI 10
#define ANDI 11
#define ORI 12
#define LUI 13
#define SYS 14

// instruction method 
void add(int instruction, int registers[31], int process);
void sub(int instruction, int registers[31], int process);
void and_(int instruction, int registers[31], int process);
void or_(int instruction, int registers[31], int process);
void slt(int instruction, int registers[31], int process);
void mul(int instruction, int registers[31], int process);
int beq(int instruction, int registers[31], int process);
int bne(int instruction, int registers[31], int process);
void addi(int instruction, int registers[31], int process);
void slti(int instruction, int registers[31], int process);
void andi(int instruction, int registers[31], int process);
void ori(int instruction, int registers[31], int process);
void lui(int instruction, int registers[31], int process);
int sys(int instruction, int registers[31], int process);

// decode instruction
int getInstruction(int instruction);

int main(int argc, char *argv[]) {

    // error check arguments
    if (argc < 2) {
        fprintf(stderr, "Incorrect no. args");
        return 1;
    }
    
    // error check file opening
    FILE *my_file = fopen(argv[1], "r");
    if (my_file == NULL) {
        ferror(my_file);
    }

    // initialise variables and arrays 
    int registers[32] = {0}; // holds register values to be used in the processes
    int instructionsSet[1000] = {0}; // holds each line of input from the file as they are read
    int PC = 0; // the line number of the program, used later to point at which instruction is to be performed
    int printed = 0; // 0 when the program hasn't been printed, becomes 1 when it has


    printf("Program\n");
    int i = 0; // holds the value of the defined constants for each instruction, -1 if invalid instruction
    char line[17] = {0}; // input string
    int lineBin = 0; // used to hold instruction as a integer
    // loop until the whole file has been read
    while (!feof(my_file)) {
        fgets(line, 16, my_file); // get line from input
        lineBin = strtol(line, NULL, 16); // turn line into an integer
        instructionsSet[PC] = lineBin; // put input into instructionsSet
        // can only print if instruction is valid
        if (i != -1 && !feof(my_file)) {
            if (PC < 10) {
                printf(" ");
            }
            printf(" %d: ", PC);
        }
        //finish looping when we get to the end of the file
        if (feof(my_file)) {
            break;
        }
        // get instruciton, if valid, increment PC counter, else tell user
        i = getInstruction(lineBin);
        if (i != -1) {
            PC++;
        } else {
            printf("%s:%d: invalid instruction code: %08x", argv[1], PC, lineBin);
        }
        // check whidh instruction has been called and call that function
        // since printed is 0 at this point, only the program is printed and 
        // no instructions are performed
        if (i == ADD) {add(lineBin, registers, printed);} else 
        if (i == SUB) {sub(lineBin, registers, printed);} else 
        if (i == AND) {and_(lineBin, registers, printed);} else 
        if (i == OR) {or_(lineBin, registers, printed);} else
        if (i == SLT) {slt(lineBin, registers, printed);} else 
        if (i == SYS) {sys(lineBin, registers, printed);} else
        if (i == LUI) {lui(lineBin, registers, printed);} else 
        if (i == ORI) {ori(lineBin, registers, printed);} else 
        if (i == ANDI) {andi(lineBin, registers, printed);} else 
        if (i == SLTI) {slti(lineBin, registers, printed);} else 
        if (i == ADDI) {addi(lineBin, registers, printed);} else 
        if (i == BNE) {bne(lineBin, registers, printed);} else 
        if (i == BEQ) {beq(lineBin, registers, printed);} else 
        if (i == MUL) {mul(lineBin, registers, printed);}
    }
    printed++; // now program has been printed, begin perfoming instructions
    printf("Output\n");
    // the current value of PC is the end of the program but PC is then used to be an index for running the program
    int pcMax = PC;
    PC = 0;
    while (PC < pcMax) {
        // check what the instruction is
        int instruction = getInstruction(instructionsSet[PC]);
        if (instruction == ADD) {
            add(instructionsSet[PC], registers, printed);
            PC++;
        } else if (instruction == SUB) {
            sub(instructionsSet[PC], registers, printed);
            PC++;
        } else if (instruction == AND) {
            and_(instructionsSet[PC], registers, printed);
            PC++;
        } else if (instruction == OR) {
            or_(instructionsSet[PC], registers, printed);
            PC++;
        } else if (instruction == SLT) {
            slt(instructionsSet[PC], registers, printed);
            PC++;
        } else if (instruction == SYS) {
            int error = sys(instructionsSet[PC], registers, printed);
            // sys returns 1 if $v0 register code is invalid
            if (error == 1) {
                printf("Unknown system call: %d\n", registers[2]);
                break;
            // sys returns -1 if $v0 register code is 10 --> exit
            } else if (error == -1) {
                break;
            }
            PC++;
        } else if (instruction == LUI) {
            lui(instructionsSet[PC], registers, printed);
            PC++;
        } else if (instruction == ORI) {
            ori(instructionsSet[PC], registers, printed);
            PC++;
        } else if (instruction == ANDI) {
            andi(instructionsSet[PC], registers, printed);
            PC++;
        } else if (instruction == SLTI) {
            slti(instructionsSet[PC], registers, printed);
            PC++;
        } else if (instruction == ADDI) {
            addi(instructionsSet[PC], registers, printed);
            PC++;
        } else if (instruction == BNE) {
            int offset = bne(instructionsSet[PC], registers, printed);
            PC += offset;
        } else if (instruction == BEQ) {
            int offset = beq(instructionsSet[PC], registers, printed);
            PC += offset;
        } else if (instruction == MUL) {
            mul(instructionsSet[PC], registers, printed);
            PC++;
        }
        
    }
    printf("Registers After Execution\n");
    // print all of the registers that arent 0
    for (int j = 0; j < 32; j++) {
        if (registers[j] != 0) {
            printf("$%d", j);
            if (j < 10) {
                printf(" ");
            }
            printf(" = %d\n", registers[j]);
        }
    }
    return 0;
}

// uses bit mask to work out which instruction is input and returns that defined code
// returns -1 if invalid
int getInstruction(int instruction) {
    if ((instruction & 	0b11111100000000000000011111111111) == 0x20) {
        return ADD;
    } else if ((instruction & 	0b11111100000000000000011111111111) == 0x22) {
        return SUB;
    } else if ((instruction & 	0b11111100000000000000011111111111) == 0x24) {
        return AND;
    } else if ((instruction & 	0b11111100000000000000011111111111) == 0x25) {
        return OR;
    } else if ((instruction & 	0b11111100000000000000011111111111) == 0x2A) {
        return SLT;
    } else if ((instruction &   0b11111111111111111111111111111111) == 0xC) {
        return SYS;
    } else if ((instruction & 	0b11111100000000000000011111111111) == 0x70000002) {
        return MUL;
    } else if ((instruction & 	0b11111100000000000000000000000000) == 0x34000000) {
        return ORI;
    } else if ((instruction & 	0b11111111111000000000000000000000) == 0x3C000000) {
        return LUI;
    } else if ((instruction & 	0b11111100000000000000000000000000) == 0x30000000) {
        return ANDI;
    } else if ((instruction & 	0b11111100000000000000000000000000) == 0x28000000) {
        return SLTI;
    } else if ((instruction & 	0b11111100000000000000000000000000) == 0x20000000) {
        return ADDI;
    } else if ((instruction & 	0b11111100000000000000000000000000) == 0x14000000) {
        return BNE;
    } else if ((instruction & 	0b11111100000000000000000000000000) == 0x10000000) {
        return BEQ;
    } else {
        return -1; 
    }   
}


void add(int instruction, int registers[31], int process) {
    // use bit mask to get 5 bit register number
    int s = ((0b11111 << 21) & instruction) >> 21;
    int t = ((0b11111 << 16) & instruction) >> 16;
    int d = ((0b11111 << 11) & instruction) >> 11;
    // if the program has been printed, perform instruction, else just print
    if (process) {
    // program is not allowed to change $0
        if (d != 0) {
            registers[d] = registers[s] + registers[t];
        }
    } else {
        printf("add  $%d, $%d, $%d\n", d, s, t);
    }
}
void sub(int instruction, int registers[31], int process) {
    int s = ((0b11111 << 21) & instruction) >> 21;
    int t = ((0b11111 << 16) & instruction) >> 16;
    int d = ((0b11111 << 11) & instruction) >> 11;
    
    if (process) {
        if (d != 0) {
            registers[d] = registers[s] - registers[t];
        }
    } else {
        printf("sub  $%d, $%d, $%d\n", d, s, t);
    }
}
void and_(int instruction, int registers[31], int process) {
    int s = ((0b11111 << 21) & instruction) >> 21;
    int t = ((0b11111 << 16) & instruction) >> 16;
    int d = ((0b11111 << 11) & instruction) >> 11;
    
    if (process) {
        if (d != 0) {
            registers[d] = registers[s] & registers[t];
        }
    } else {
        printf("and  $%d, $%d, $%d\n", d, s, t);
    }
}
void or_(int instruction, int registers[31], int process) {
    int s = ((0b11111 << 21) & instruction) >> 21;
    int t = ((0b11111 << 16) & instruction) >> 16;
    int d = ((0b11111 << 11) & instruction) >> 11;
    
    if (process) {
        if (d != 0) {
            registers[d] = registers[s] | registers[t];
        }
    } else {
        printf("or  $%d, $%d, $%d\n", d, s, t);
    }
}
void slt(int instruction, int registers[31], int process) {
    int s = ((0b11111 << 21) & instruction) >> 21;
    int t = ((0b11111 << 16) & instruction) >> 16;
    int d = ((0b11111 << 11) & instruction) >> 11;
    
    if (process) {
        if (d != 0) {
            if (registers[s] < registers[t]) {
                registers[d] = 1;
            } else {
                registers[d] = 0;
            }
        }
    } else {
        printf("slt  $%d, $%d, $%d\n", d, s, t);
    }
}
void mul(int instruction, int registers[31], int process) {
    int s = ((0b11111 << 21) & instruction) >> 21;
    int t = ((0b11111 << 16) & instruction) >> 16;
    int d = ((0b11111 << 11) & instruction) >> 11;
    
    if (process) {
        if (d != 0) {
            registers[d] = registers[s] * registers[t];
        }
    } else {
        printf("mul  $%d, $%d, $%d\n", d, s, t);
    }
}
int beq(int instruction, int registers[31], int process) {
    int s = ((0b11111 << 21) & instruction) >> 21;
    int t = ((0b11111 << 16) & instruction) >> 16;
    int I = (0b1111111111111111 & instruction);
    if ((I & 0b1000000000000000) == 0b1000000000000000) {
        I = -((I ^ 0b1111111111111111) + 0b1);
    }
    if (process) {
        if (registers[s] == registers[t]) {
            return I;
        } else {
            return 1;
        }
    } else {
        printf("beq  $%d, $%d, %d\n", s, t, I);
        return 1;
    }

}
int bne(int instruction, int registers[31], int process) {
    int s = ((0b11111 << 21) & instruction) >> 21;
    int t = ((0b11111 << 16) & instruction) >> 16;
    int I = (0b1111111111111111 & instruction);
    if ((I & 0b1000000000000000) == 0b1000000000000000) { 
        I = -((I ^ 0b1111111111111111) + 0b1);
    }
    if (process) {
        if (registers[s] != registers[t]) {
            return I;
        } else {
            return 1;
        }
    } else {
        printf("bne  $%d, $%d, %d\n", s, t, I);
        return 1;
    }
}
void addi(int instruction, int registers[31], int process) {
    int s = ((0b11111 << 21) & instruction) >> 21;
    int t = ((0b11111 << 16) & instruction) >> 16;
    int I = (0b1111111111111111 & instruction);
    if ((I & 0b1000000000000000) == 0b1000000000000000) {
        I = -((I ^ 0b1111111111111111) + 0b1);
    }
    if (process) {
        if (t != 0) {
            registers[t] = registers[s] + I;
        }
    } else {
        printf("addi $%d, $%d, %d\n", t, s, I);
    }
}
void slti(int instruction, int registers[31], int process) {
    int s = ((0b11111 << 21) & instruction) >> 21;
    int t = ((0b11111 << 16) & instruction) >> 16;
    int I = (0b1111111111111111 & instruction);
    if ((I & 0b1000000000000000) == 0b1000000000000000) {
        I = -((I ^ 0b1111111111111111) + 0b1);
    }
    if (process) {
        if (t != 0) {
            if (registers[s] < I) {
                registers[t] = 1;
            } else {
                registers[t] = 0;
            }
        }
    } else {
        printf("slti  $%d, $%d, %d\n", t, s, I);
    }
    
}
void andi(int instruction, int registers[31], int process) {
    int s = ((0b11111 << 21) & instruction) >> 21;
    int t = ((0b11111 << 16) & instruction) >> 16;
    int I = (0b1111111111111111 & instruction);
    if ((I & 0b1000000000000000) == 0b1000000000000000) {
        I = -((I ^ 0b1111111111111111) + 0b1);
    }
    if (process) {
        if (t != 0) {
            registers[t] = registers[s] & I;
        }
    } else {
        printf("andi  $%d, $%d, %d\n", t, s, I);
    }
}
void ori(int instruction, int registers[31], int process) {
    int s = ((0b11111 << 21) & instruction) >> 21;
    int t = ((0b11111 << 16) & instruction) >> 16;
    int I = (0b1111111111111111 & instruction);
    if ((I & 0b1000000000000000) == 0b1000000000000000) {
        I = (~I) | 0b1;
    }
    //printf("%d\n%d\n%d\n", t, s, I);
    if (process) {
        if (t != 0) {
            registers[t] = registers[s] | I;
        }
    } else {
        printf("ori  $%d, $%d, %d\n", t, s, I);
    }
}
void lui(int instruction, int registers[31], int process) {
    int t = ((0b11111 << 16) & instruction) >> 16;
    int I = (0b1111111111111111 & instruction);
    if ((I & 0b1000000000000000) == 0b1000000000000000) {
        I = ((~I) | 0b1);
    }
    if (process) {
        if (t != 0) {
            registers[t] = I << 16;
        }
    } else {
        printf("lui  $%d, %d\n", t, I);
    }
}
int sys(int instruction, int registers[31], int process) {
    if (process) {
        if (registers[2] == 1) {
            printf("%d", registers[4]);
            return 0;
        } else if (registers[2] == 10) {
            return -1;
        } else if (registers[2] == 11) {
            printf("%c", registers[4]);
            return 0;
        } 
    } else {
        printf("syscall\n");
        return 0;
    }
    return 1;
}