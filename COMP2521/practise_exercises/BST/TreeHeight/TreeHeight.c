
#include <stdlib.h>

#include "tree.h"

int max(int a, int b) {
    return a > b ? a : b;
}

int TreeHeight(Tree t) {
    if (t == NULL) {
        return -1;
    }
    return 1 + max(TreeHeight(t->left), TreeHeight(t->right));
}

