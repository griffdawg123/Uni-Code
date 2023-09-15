//Returns and prints the difference between the two notes
//Griffin Doyle (z5311098)
// 06/04


#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

// A struct note * IS a Note
typedef struct note *Note;

//There are 10 octaves (0 to 9) and 12 notes (0 to 11)
struct note {
    int octave;
    int key;
    Note next;
};

Note note_subtract(Note higher, Note lower);
void print_note(Note n);

int main(void) {
    int octave, key;
    scanf("%d %d", &octave, &key);
    // NOTE: the {octave, key, NULL} syntax is short for
    // a.octave = octave; a.key = key; a.next = NULL;
    struct note a = {octave, key, NULL};
    scanf("%d %d", &octave, &key);
    struct note b = {octave, key, NULL};
    Note diff = note_subtract(&a, &b);
    print_note(diff);
    free(diff);
    return 0;
}

// For a note with octave 0, and note 9,
// `print_note` should print:
// "0 09\n"
void print_note(Note n) {
    if (n->key >= 10) {
        printf("%d %d\n", n->octave, n->key);
    } else {
        printf("%d 0%d\n", n->octave, n->key);
    }
}



//Returns a pointer to a malloced struct containing the difference between a 
//higher and a lower note
Note note_subtract(Note higher, Note lower) {
    struct note *diff = malloc(sizeof(struct note));
    diff->octave = higher->octave - lower->octave;
    diff->key = higher->key - lower->key;
    if (diff->key < 0) {
        diff->key += 12;
        diff->octave -= 1;
    }
    return diff;

}
