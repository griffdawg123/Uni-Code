
#include "list.h"

List listSetUnion(List s1, List s2) {
	List newL = newList();
	Node currRead, currWrite;
	if (s1->head != NULL) {
		newL->head = newNode(s1->head->value);
		currRead = s1->head->next;
		currWrite = newL->head;
	} else if(s2->head != NULL)  {
		newL->head = newNode(s2->head->value);
		currRead = s2->head->next;
		currWrite = newL->head;
	} else {
		return newL;
	}
	while (currRead != NULL) {
		currWrite->next = newNode(currRead->value);
		currRead = currRead->next;
		currWrite = currWrite->next;
	}
	currRead = s2->head;
	while (currRead != NULL) {
		bool found = false;
		Node checker = newL->head;
		while (!found && checker != NULL) {
			if (checker->value == currRead->value) {
				found = true;
			}
			checker = checker->next;
		}
		if (!found) {
			currWrite->next = newNode(currRead->value);
			found = false;
			currWrite = currWrite->next;
		}
		currRead = currRead->next;
	}
	return newL;
}

