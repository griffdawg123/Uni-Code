#include "list.h"

void reverseDLList(List l) {
	Node curr = l->first;
	while (curr != NULL) {
		Node next = curr->next;
		Node temp = curr->next;
		curr->next = curr->prev;
		curr->prev = temp;
		curr = next;
	}
	Node temp = l->last;
	l->last = l->first;
	l->first = temp;
}

