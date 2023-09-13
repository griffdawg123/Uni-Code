
#include <stdlib.h>

#include "tree.h"

int TreeSumOdds(Tree t) {
	if (t == NULL) {
		return 0;
	}
	if (t->value % 2) {
		return t->value + TreeSumOdds(t->left) + TreeSumOdds(t->right);
	}
	return TreeSumOdds(t->left) + TreeSumOdds(t->right);
}

