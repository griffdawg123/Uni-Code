#include <stdio.h>
#include <ctype.h>

int main(int argc, char *argv[]) {

    FILE *file = fopen(argv[1], "r");
    int ascii = 0;

    while(!feof(file)) {
        int c = fgetc(file);
        if ((c >= 0) && (c <= 127)) {
            ascii++;
        }
    }
    printf("%s contains %d ASCII bytes\n", argv[1], ascii);
    return 0;
}