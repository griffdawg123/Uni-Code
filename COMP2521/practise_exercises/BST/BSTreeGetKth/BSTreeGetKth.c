
#include <stdlib.h>

#include "BSTree.h"

BSTree doBSTreeGetKth(BSTree t, int *k);

int BSTreeGetKth(BSTree t, int k) {
	BSTree kth = doBSTreeGetKth(t, &k);
	if (kth == NULL) {
		return -1;
	}
	return kth->value;
}

BSTree doBSTreeGetKth(BSTree t, int *k) {
	if (t == NULL) {
		return NULL;
	}
	BSTree left = doBSTreeGetKth(t->left, k);
	if (left != NULL) {
		return left;
	}
	int i = *k;
	i--;
	*k = i;
	if (*k == -1) {
		return t;
	}
	return doBSTreeGetKth(t->right, k);
}
