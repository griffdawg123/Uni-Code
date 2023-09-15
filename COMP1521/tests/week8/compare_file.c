#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
int main(int argc, char **argv) {
    
    FILE *file1 = fopen(argv[1], "r");
    FILE *file2 = fopen(argv[2], "r");
    
    int b1 = fgetc(file1);
    int b2 = fgetc(file2);
    int byte = 0;
    while((!feof(file1)) && (!feof(file2))) {
        if (b1 != b2) {
            break;
        }
        byte++;
        b1 = fgetc(file1);
        b2 = fgetc(file2);
    }

    if (feof(file1) && !feof(file2)) {
        printf("EOF on %s\n", argv[1]);
    } else if (feof(file2) && !feof(file1)) {
        printf("EOF on %s\n", argv[2]);
    } else if (!feof(file1) && !feof(file2)) {
        printf("Files differ at byte %d\n", byte);
    } else {
        printf("Files are identical\n");
    }
    return 0;
}