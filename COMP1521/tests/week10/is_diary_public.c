#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    char *value = getenv("HOME");
    char *diary = "/.diary";
    int length = strlen(value) + 1 + strlen(diary) + 1;
	char diary_path[length];
	snprintf(diary_path, length, "%s/%s", value, diary);
    if (access(diary_path, R_OK) != -1) {
        printf("1\n");
    } else {
        printf("0\n");
    }

    return 0;
}