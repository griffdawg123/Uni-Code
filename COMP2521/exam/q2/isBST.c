// isBST.c ... implementation of isBST function

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "Tree.h"

/*
    You will submit only this one file.

    Implement the function "isBST" below. Read the exam paper for a
    detailed specification and description of your task.

    - DO NOT modify the code in any other files except for debugging
      purposes.
    - If you wish, you can add static variables and/or helper functions
      to this file.
    - DO NOT add a "main" function to this file.
*/

static bool doIsBST(Tree t, Node root);

int isBST(Tree t) {
  return doIsBST(t, t->root);
}

static bool doIsBST(Tree t, Node n) {
  // base case
  if (n == NULL) {
      return true;
    }
    // compare ordering on left and right side if needed
    bool l = true;
    bool r = true;
    if (n->left != NULL) {
      l = t->compare(n->rec, n->left->rec) > 0;
    }
    if (n->right != NULL) {
      r = t->compare(n->rec, n->right->rec) < 0;
    }
    bool bst = l && r;
    // recurse through the rest of the tree
    return (doIsBST(t, n->left) && doIsBST(t, n->right) && bst);
}