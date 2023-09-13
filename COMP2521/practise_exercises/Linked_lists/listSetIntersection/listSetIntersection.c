
#include "list.h"

List listSetIntersection(List s1, List s2) {
	List intersection = newList();
	for (Node curr1 = s1->head; curr1 != NULL; curr1 = curr1->next) {
		for (Node curr2 = s2->head; curr2 != NULL; curr2 = curr2->next) {
			if (curr1->value == curr2->value) {
				Node new = newNode(curr1->value);
				new->next = intersection->head;
				intersection->head = new;
			}
		}
	}
	return intersection;
}

