#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>

long get_size(char *filename);

int main(int argc, char *argv[]) {
    long total_size = 0;
    for (int arg = 1; arg < argc; arg++) {
        total_size += get_size(argv[arg]);
    }
    printf("Total: %ld bytes\n", total_size);
    return 0;
}

long get_size(char *filename) {

    struct stat s;
    if (stat(filename, &s) != 0) {
        perror(filename);
        exit(1);
    }
    long size = (long)s.st_size;
    printf("%s: %ld bytes\n", filename, size);
    return size;
}
