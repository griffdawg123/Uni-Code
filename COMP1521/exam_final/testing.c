#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    FILE *file = fopen(argv[1], "r");

    printf("%c\n", fgetc(file));
    printf("%c\n", fgetc(file));
    printf("%c\n", fgetc(file));
    printf("%c\n", fgetc(file));

    fseek(file, -3, SEEK_CUR);
    printf("%c\n", fgetc(file));

    return 0;
}