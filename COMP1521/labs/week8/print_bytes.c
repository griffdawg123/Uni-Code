#include <stdio.h>
#include <ctype.h>

int main(int argc, char **argv) {
    
    FILE *my_file = fopen(argv[1], "r");
    if (my_file == NULL) {
        perror("hello.txt");
        return 1;
    }

    int ch;
    int i = 0;
    fseek(my_file, 0, SEEK_SET);
    while ((ch = fgetc(my_file)) != EOF) {
        if (isprint(ch)){
            printf("byte %4d: %3d 0x%02x '%c'\n", i, ch, ch, ch);
        } else {
            printf("byte %4d: %3d 0x%02x  \n", i, ch, ch);
        }
        i++;
    }
    return 0;
}