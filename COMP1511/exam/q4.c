#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

struct node {
    struct node *next;
    int          data;
};

int exclusive(struct node *head1, struct node *head2);
struct node *strings_to_list(int len, char *strings[]);

// DO NOT CHANGE THIS MAIN FUNCTION
int main(int argc, char *argv[]) {
    // create two linked lists from command line arguments
    int dash_arg = argc - 1;
    while (dash_arg > 0 && strcmp(argv[dash_arg], "-") != 0) {
        dash_arg = dash_arg - 1;
    }
    struct node *head1 = strings_to_list(dash_arg - 1, &argv[1]);
    struct node *head2 = strings_to_list(argc - dash_arg - 1, &argv[dash_arg + 1]);

    int result = exclusive(head1, head2);
    printf("%d\n", result);

    return 0;
}

// exclusive should return 1 if no value occurs in both lists
// exclusive should return 0 otherwise
int exclusive(struct node *head1, struct node *head2) {
    // iterate through list one and test if that value occurs in list 2
    struct node *current1 = head1;
    struct node *current2 = head2;
    while (current1 != NULL) {
        current2 = head2;
        while (current2 != NULL) {
            if (current1->data == current2->data) {
                return 0;
            }
            current2 = current2->next;
        }
        current1 = current1->next;
    }
    return 1;
}


// DO NOT CHANGE THIS FUNCTION
// create linked list from array of strings
struct node *strings_to_list(int len, char *strings[]) {
    struct node *head = NULL;
    for (int i = len - 1; i >= 0; i = i - 1) {
        struct node *n = malloc(sizeof (struct node));
        assert(n != NULL);
        n->next = head;
        n->data = atoi(strings[i]);
        head = n;
    }
    return head;
}
