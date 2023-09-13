
#include "list.h"

int numDupesInOrderedList(List l) {
	Node curr = l->head;
	int dupes = 0;
	while (curr != NULL && curr->next != NULL){
		if (curr->value == curr->next->value) {
			dupes++;
		}
		curr = curr->next;
	}
	return dupes;
}

