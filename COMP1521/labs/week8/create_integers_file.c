#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc < 4) {
        fprintf(stderr, "Wrong number of arguments");
        return 1;
    }

    FILE *my_file = fopen(argv[1], "a");

    if (my_file == NULL) {
        perror(argv[1]);
        return 1;
    }

    int start = atoi(argv[2]);
    int end = atoi(argv[3]);

    while (start <= end) {
        // TODO change any int to 
        fprintf(my_file, "%d", start);
        fprintf(my_file, "\n");
        start++;
    }

    return 0;

}