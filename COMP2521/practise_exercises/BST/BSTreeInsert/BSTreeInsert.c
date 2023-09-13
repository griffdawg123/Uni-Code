
#include <stdio.h>
#include <stdlib.h>

#include "BSTree.h"

BSTree BSTreeInsert(BSTree t, int val) {
	if (t == NULL) {
		BSTree new = malloc(sizeof(*new));
		new->left = NULL;
		new->right = NULL;
		new->value = val;
		return new;
	}
	if (val > t->value) {
		t->right = BSTreeInsert(t->right, val);
	} else if (val < t->value) {
		t->left = BSTreeInsert(t->left, val);
	} 
	return t;
}

