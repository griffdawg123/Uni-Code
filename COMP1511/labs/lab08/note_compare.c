// Compare two Note structs
// list_compare.c
//
// This program was written by YOUR-NAME-HERE (z5311098)
// on 06/04


#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

// A struct note * IS a Note
typedef struct note *Note;

//There are 10 octaves (0 to 9) and 12 notes (0 to 11)
struct note {
    int octave;
    int key;
    struct note *next;
};

int note_compare(Note a, Note b);

//Returns 1 if a is higher than b
//       -1 if b is higher than a
//        0 if they are equal
int note_compare(Note a, Note b) {
    if(a->octave > b->octave) {
        return 1;
    } else if (a->octave < b->octave) {
        return -1;
    } else {
        if (a->key > b->key) {
            return 1;
        } else if (a->key < b->key) {
            return -1;
        } else {
            return 0;
        }
    }

}
int main(void) {

    int octave, key;
    scanf("%d %d", &octave, &key);
    // NOTE: the {octave, key, NULL} syntax is short for
    // a.octave = octave; a.key = key; a.next = NULL;
    struct note a = {octave, key, NULL};
    scanf("%d %d", &octave, &key);
    struct note b = {octave, key, NULL};
    int compared = note_compare(&a, &b);
    if (compared == 1) {
        printf("a is higher than b\n");
    } else if (compared == -1) {
        printf("b is higher than a\n");
    } else {
        printf("a and b are equal\n");
    }
    

    return 0;
}
