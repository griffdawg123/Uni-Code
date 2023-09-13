
#include "list.h"

void listReverse(List l) {
	Node newHead = NULL;
	Node curr = l->head;
	while (curr != NULL) {
		Node next = curr->next;
		curr->next = newHead;
		newHead = curr;
		curr = next;
	}
	l->head = newHead;
}

