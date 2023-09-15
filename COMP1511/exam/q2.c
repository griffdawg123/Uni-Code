#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

struct node {
    struct node *next;
    int          data;
};

int compare(struct node *head1, struct node *head2);
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

    int result = compare(head1, head2);
    printf("%d\n", result);

    return 0;
}

// compare should return -1 if head1 sums to less than head2.
// compare should return  0 if head1 and head2 sum to the same number.
// compare should return  1 if head1 sums to more than head2.
int compare(struct node *head1, struct node *head2) {
    //find sum of head 1 and head 2
    int sum1 = 0;
    int sum2 = 0;
    struct node *current = head1;
    while (current != NULL) {
        sum1 += current->data;
        current = current->next;
    }
    current = head2;
    while (current != NULL) {
        sum2 += current->data;
        current = current->next;
    }
    // compare sums
    if (sum1 > sum2) {
        return 1;
    } else if (sum2 > sum1) {
        return -1;
    } else {
        return 0;
    }
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
