#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char *argv[]) {
    struct stat path_stat;
    stat(argv[1], &path_stat);
    printf("%d\n", !S_ISREG(path_stat.st_mode));
    return 0;
}