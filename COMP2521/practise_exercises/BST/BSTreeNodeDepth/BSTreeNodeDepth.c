
#include <stdlib.h>

#include "BSTree.h"

int BSTreeNodeDepth(BSTree t, int key) {
	if (t == NULL) {
		return -1;
	} else if (t->value == key) {
		return 0;
	} else {
		int depth;
		if (t->value > key) {
			depth = BSTreeNodeDepth(t->left, key);
		} else {
			depth = BSTreeNodeDepth(t->right, key);
		}
		return (depth == -1) ? depth : depth + 1;
	}
}

