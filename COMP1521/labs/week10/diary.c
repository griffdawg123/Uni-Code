#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    char *value = getenv("HOME");
    char *diary = "/.diary";
    int length = strlen(value) + 1 + strlen(diary) + 1;
	char diary_path[length];
	snprintf(diary_path, length, "%s/%s", value, diary);
    FILE *diary_file = fopen(diary_path, "a");
    for (int i = 1; i < argc; i++) {
        fprintf(diary_file, "%s", argv[i]);
        fprintf(diary_file, " ");
    }

    fprintf(diary_file, "\n");
    return 0;
}