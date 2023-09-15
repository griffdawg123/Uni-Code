#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    FILE *my_file = fopen(argv[1], "r+");
    if (my_file == NULL) {
        ferror(my_file);
    }

    int ch = fgetc(my_file);
    while(!feof(my_file)) {
        if (ch >= 128 && ch <= 255) {
            break;
        }
        ch = fgetc(my_file);
    }
    return 0;
}