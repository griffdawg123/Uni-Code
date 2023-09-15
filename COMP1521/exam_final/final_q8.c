#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    FILE *file = fopen(argv[1], "r");

    int charbuffer[4];
    int valid = 0;
    while (!feof(file)) {
        charbuffer[0] = fgetc(file);
        if((charbuffer[0] & 0b10000000) == 0) {
            valid++;
        } else {
            charbuffer[1] = fgetc(file);
            if (((charbuffer[0] & 0b11100000) == 0b11000000) 
                        && ((charbuffer[1] & 0b11000000) == 0b10000000)) {
                valid++;
            } else {
                charbuffer[2] = fgetc(file);
                if (((charbuffer[0] & 0b11110000) == 0b11100000) 
                        && ((charbuffer[1] & 0b11000000) == 0b10000000) 
                        && ((charbuffer[2] & 0b11000000) == 0b10000000)) {
                    valid++;
                } else {
                    charbuffer[3] = fgetc(file);
                    if (((charbuffer[0] & 0b11111000) == 0b11110000) 
                        && ((charbuffer[1] & 0b11000000) == 0b10000000)
                        && ((charbuffer[2] & 0b11000000) == 0b10000000)
                        && ((charbuffer[3] & 0b11000000) == 0b10000000)) {
                        valid++;
                    } else {
                        break;
                    }
                }
            }   
        }
    }

    if (feof(file)) {
        printf("%s: %d UTF-8 characters\n", argv[1], valid);
    } else {
        printf("%s: invalid UTF-8 after %d valid UTF-8 characters\n", argv[1], valid);
    }

    return 0;
}