#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
int main(int argc, char **argv) {
    
    FILE *file1 = fopen(argv[1], "r+");
    
    int ch = fgetc(file1);
    while(!feof(file1)) {
        if (ch >= 128 && ch <= 255) {
            fseek(file1, -1, SEEK_CUR);
            fputc('*', file1);            
        }
        ch = fgetc(file1);
    }
    rewind(file1);
    while((ch = fgetc(file1)) != EOF ){
        if(ch != '*'){
            fseek(file1, -1, SEEK_CUR);
            fputc(ch, file1);
        }
    }
    return 0;
}