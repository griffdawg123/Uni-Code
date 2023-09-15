#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv){
    if (argc < 2) {
        fprintf(stderr, "Incorrect no. args");
        return 1;
    }

    FILE *my_file = fopen(argv[1], "a");
    if (my_file == NULL) {
        ferror(my_file);
    }
    for (int i = 2; i < argc; i++) {
        fputc(atoi(argv[i]), my_file);
    }
    return 0;
}