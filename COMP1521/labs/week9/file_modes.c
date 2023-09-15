#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>

void print_perms(char *filename);

int main(int argc, char *argv[]) {
    for (int arg = 1; arg < argc; arg++) {
        print_perms(argv[arg]);
    }
    return 0;
}

void print_perms(char *filename) {
    struct stat s;
    if (stat(filename, &s) != 0) {
        perror(filename);
        exit(1);
    }

    printf( (S_ISDIR(s.st_mode)) ? "d" : "-");
    printf( (s.st_mode & S_IRUSR) ? "r" : "-");
    printf( (s.st_mode & S_IWUSR) ? "w" : "-");
    printf( (s.st_mode & S_IXUSR) ? "x" : "-");
    printf( (s.st_mode & S_IRGRP) ? "r" : "-");
    printf( (s.st_mode & S_IWGRP) ? "w" : "-");
    printf( (s.st_mode & S_IXGRP) ? "x" : "-");
    printf( (s.st_mode & S_IROTH) ? "r" : "-");
    printf( (s.st_mode & S_IWOTH) ? "w" : "-");
    printf( (s.st_mode & S_IXOTH) ? "x" : "-");
    printf(" %s\n", filename);
}