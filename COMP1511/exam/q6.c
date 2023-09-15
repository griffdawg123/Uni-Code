#include <stdio.h>
#include <stdlib.h>

struct node {
    struct node *next;
    char        type;
};

struct node *append(struct node *head, char type);
int checkLast(struct node *head, char type);
struct node *deleteLast(struct node *head);

int main(void) {
    struct node *head = malloc(sizeof(struct node));
    head->next = NULL;
    head->type = ' ';
    int input = getchar();
    while (input != EOF) {
        if (input == '{') {
            head = append(head, '{');
        } else if (input == '}') {
            if (checkLast(head, '{')) {
                head = deleteLast(head);
            } else {
                head = append(head, ' ');
            }
        } else if (input == '<') {
            head = append(head, '<');
        } else if (input == '>') {
            if (checkLast(head, '<')) {
                head = deleteLast(head);
            } else {
                head = append(head, ' ');
            }
        } else if (input == '[') {
            head = append(head, '[');
        } else if (input == ']') {
            if (checkLast(head, '[')) {
                head = deleteLast(head);
            } else {
                head = append(head, ' ');
            }
        } else if (input == '(') {
            head = append(head, '(');
        } else if (input == ')') {
            if (checkLast(head, '(')) {
                head = deleteLast(head);
            } else {
                head = append(head, ' ');
            }
        }
        input = getchar();
    }
    if (head->next == NULL) {
        printf("Valid Sequence!\n");
    } else {
        printf("Invalid Sequence, the correct closing sequence is:\n");
        while (head->next != NULL) {
            struct node *current = head;
            while (current->next != NULL) {
                current = current->next;
            }
            if (current->type == '<') {
                printf(">\n");
            } else if (current->type == '(') {
                printf(")\n");
            } else if (current->type == '{') {
                printf("}\n");
            } else if (current->type == '[') {
                printf("]\n");
            } else if (current->type == ' ') {
                printf(" \n");
            }
            head = deleteLast(head);
        }
    }
    free(head);
}

struct node *append(struct node *head, char type) {
    struct node *current = head;
    while (current->next != NULL) {
        current = current->next;
    }
    current->next = malloc(sizeof(struct node));
    current->next->next = NULL;
    current->next->type = type;
    return head;
}

int checkLast(struct node *head, char type) {
    struct node *current = head;
    while (current->next != NULL) {
        current = current->next;
    }
    if (current->type == type) {
        return 1;
    }
    return 0;
}

struct node *deleteLast(struct node *head) {
    struct node *current = head;
    struct node *prev = NULL;
    
    while (current->next != NULL) {
        prev = current;
        current = current->next;
    }
    
    prev->next = current->next;
    free(current);
    return head;
}
