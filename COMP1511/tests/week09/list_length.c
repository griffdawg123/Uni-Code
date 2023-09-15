// counts the number of elements in the lists
// Griffin Doyle <z5311098>
// 19/04

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

struct node {
    struct node *next;
    int          data;
};

int length(struct node *head);
struct node *strings_to_list(int len, char *strings[]);

// DO NOT CHANGE THIS MAIN FUNCTION

int main(int argc, char *argv[]) {
    // create linked list from command line arguments
    struct node *head = strings_to_list(argc - 1, &argv[1]);

    int result = length(head);
    printf("%d\n", result);

    return 0;
}


// Return the length of the linked list pointed by head
int length(struct node *head) {
    // initiate counter and current node pointing to head
    int counter = 0;
    struct node *current = head;
    // loop through list until current is null
    while (current != NULL) {
        // increment counter for every element in list
        counter++;
        current = current->next;
    }
    // return counter
    return counter;
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
