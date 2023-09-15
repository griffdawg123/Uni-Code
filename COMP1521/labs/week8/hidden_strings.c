#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
int main(int argc, char **argv) {
    
    if (argc < 2) {
        fprintf(stderr, "Incorrect no. args");
        return 1;
    }
    
    FILE *my_file = fopen(argv[1], "r");
    if (my_file == NULL) {
        ferror(my_file);
    }
    
    //printf("debugger\n");
    int ch = 0;
    while (!feof(my_file)) {
        int chars[3];
        for (int i = 0; i < 3; i ++) {
            chars[i] = fgetc(my_file);
        }
        ch = fgetc(my_file);
        if (isprint(chars[0]) && isprint(chars[1]) && isprint(chars[2]) && isprint(ch)) {
            for (int j=0; j < 3; j++) {
                printf("%c",chars[j]);
            }
            while(isprint(ch)) {
                printf("%c",ch);
                ch = fgetc(my_file);
            }
            printf("\n");
        } else {
            if(isprint(ch)) {
                fseek(my_file, -1, SEEK_CUR);
                if (isprint(chars[2])) {
                    fseek(my_file, -1, SEEK_CUR);
                    if (isprint(chars[1])) {
                        fseek(my_file, -1, SEEK_CUR);
                    }
                } 
            }
        }
        
    }
    return 0;
}