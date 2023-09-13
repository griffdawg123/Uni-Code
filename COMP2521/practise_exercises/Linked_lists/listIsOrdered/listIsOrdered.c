
#include "list.h"

bool listIsOrdered(List l) {
	Node curr = l->head;
	// skips for 0 or 1 length lists
	while (curr != NULL && curr->next != NULL) {
		// +ve for inc., -ve for dec.
		int order = l->head->next->value - l->head->value;
		if ((curr->next->value - curr->value)*order < 0) { // signs must match, ie >= 0
			return false;
		}
		curr = curr->next;
	}
	return true;
}

