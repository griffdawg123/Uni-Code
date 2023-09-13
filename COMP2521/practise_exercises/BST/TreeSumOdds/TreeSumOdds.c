
#include <stdlib.h>

#include "tree.h"

int TreeSumOdds(Tree t) {
	if (t == NULL) {
		return 0;
	}
	return TreeSumOdds(t->left) + TreeSumOdds(t->right) + ((abs(t->value % 2) == 1) ? t->value : 0);
}

