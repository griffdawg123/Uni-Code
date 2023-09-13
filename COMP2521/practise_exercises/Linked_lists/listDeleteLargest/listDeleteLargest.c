
#include "list.h"

int listDeleteLargest(List l) {
	int largest = -1;
	Node curr = l->head;
	while (curr != NULL) {
		if (curr->value > largest) {
			largest = curr->value;
		}
		curr = curr->next;
	}
	Node prev = NULL;
	curr = l->head;
	while (curr->value != largest) {
		prev = curr;
		curr = curr->next;
	}
	if (prev != NULL) {
		prev->next = curr->next;
	} else {
		l->head = curr->next;
	}
	free(curr);
	return largest;
}

