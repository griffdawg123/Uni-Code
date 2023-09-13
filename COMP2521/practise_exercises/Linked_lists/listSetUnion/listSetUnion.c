
#include "list.h"

List listSetUnion(List s1, List s2) {
	List u = newList();
	Node curr = s1->head;
	while (curr != NULL) {
		Node new = newNode(curr->value);
		new->next = u->head;
		u->head = new;
		curr = curr->next;
	}
	curr = s2->head;
	while (curr != NULL) {
		Node checker = u->head;
		if (checker == NULL) {
			u->head = newNode(curr->value);
			curr = curr->next;
			continue;
		}
		while (checker->next != NULL) {
			if (checker->value == curr->value) {
				break;
			}
			checker = checker->next;
		}
		if (checker->next == NULL) {
			checker->next = newNode(curr->value);
		}
		curr = curr->next;
	}
	return u;
}

